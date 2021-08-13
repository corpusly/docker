#2021-1-14
from collections import	namedtuple
from fairseq import	checkpoint_utils, options, tasks, utils
from fairseq.data import encoders
import fileinput,torch, json
import logging
from logging.handlers import TimedRotatingFileHandler

import uvicorn, random, os, socket,redis
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

class ItemSnts(BaseModel):
	snts: list
	topn: Optional[int] = 1
	merge: Optional[bool] = True
	tokenize: Optional[bool] = True

class ItemDoc(BaseModel):
	doc: str
	topn: Optional[int] = 1
	merge: Optional[bool] = True
	tokenize: Optional[bool] = True

app = FastAPI()

@app.get('/')
def home(): return HTMLResponse(content='''<h2>gec trans, GPU-enabled </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-1-14''')

@app.get('/cuda')
def cuda_info(): 
	return {'torch.cuda.device_count()':torch.cuda.device_count(), 'torch.version.cuda':torch.version.cuda, 
	'torch.cuda.is_available()': torch.cuda.is_available(),
	'CUDA_VISIBLE_DEVICES': os.environ["CUDA_VISIBLE_DEVICES"],	
	'ip': socket.gethostbyname(socket.gethostname()), 
	'args': uvicorn.args, }	

# logging
logger = logging.getLogger("translater")
logger.setLevel(level=logging.DEBUG)
formatter = "%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s"
console_handler = logging.StreamHandler()
console_handler.setLevel(level=logging.DEBUG)
console_handler.setFormatter(logging.Formatter(formatter))
logger.addHandler(console_handler)


def	buffered_read(snts,	buffer_size):
	buffer = []
	for	src_str	in snts:
		buffer.append(src_str.strip())
		if len(buffer) >= buffer_size:
			yield buffer
			buffer = []
	if len(buffer) > 0:
		yield buffer

Batch =	namedtuple('Batch',	'ids src_tokens	src_lengths')

def	make_batches(lines,	args, task,	max_positions, encode_fn):
	tokens = [
		task.source_dictionary.encode_line(
			encode_fn(src_str),	add_if_not_exist=False
		).long()
		for	src_str	in lines
	]
	lengths	= torch.LongTensor([t.numel() for t	in tokens])
	itr	= task.get_batch_iterator(
		dataset=task.build_dataset_for_inference(tokens, lengths),
		max_tokens=args.max_tokens,
		max_sentences=args.max_sentences,
		max_positions=max_positions,
	).next_epoch_itr(shuffle=False)
	for	batch in itr:
		yield Batch(
			ids=batch['id'],
			src_tokens=batch['net_input']['src_tokens'], src_lengths=batch['net_input']['src_lengths'],
		)


class generate_batch():

	def	__init__(self, args):
		#parser = options.get_generation_parser(interactive=True)
		#args = options.parse_args_and_arch(parser)
		utils.import_user_module(args)

		if args.buffer_size	< 1:
			args.buffer_size = 1
		if args.max_tokens is None and args.max_sentences is None:
			args.max_sentences = 1

		if args.beam is None:
			args.beam = 5
		if args.bpe is None:
			args.bpe = 'subword_nmt'
		if args.tokenizer is None:
			args.tokenizer = 'space'
		if args.remove_bpe is None:
			args.remove_bpe = '@@ '

		assert not args.sampling or	args.nbest == args.beam, \
			'--sampling	requires --nbest to	be equal to	--beam'
		assert not args.max_sentences or args.max_sentences	<= args.buffer_size, \
			'--max-sentences/--batch-size cannot be	larger than	--buffer-size'

		self.use_cuda =	torch.cuda.is_available() and not args.cpu

		# Setup	task, e.g.,	translation
		task = tasks.setup_task(args)

		# Load ensemble
		logger.info('loading model(s) from %s' % (args.path))
		models,	_model_args	= checkpoint_utils.load_model_ensemble(
			args.path.split(':'),
			arg_overrides=eval(args.model_overrides),
			task=task,
		)

		# Set dictionaries
		self.src_dict =	task.source_dictionary
		self.tgt_dict =	task.target_dictionary

		# Optimize ensemble	for	generation
		for	model in models:
			model.make_generation_fast_(
				beamable_mm_beam_size=None if args.no_beamable_mm else args.beam,
				need_attn=args.print_alignment,
			)
			if args.fp16:
				model.half()
			if self.use_cuda:
				model.cuda()

		# Initialize generator
		self.generator = task.build_generator(args)

		# Handle tokenization and BPE
		self.tokenizer = encoders.build_tokenizer(args)
		self.bpe = encoders.build_bpe(args)


		# Load alignment dictionary	for	unknown	word replacement
		# (None	if no unknown word replacement,	empty if no	path to	align dictionary)
		self.align_dict	= utils.load_align_dict(args.replace_unk)

		self.max_positions = utils.resolve_max_positions(
		task.max_positions(),
		*[model.max_positions()	for	model in models]
		)

		if args.buffer_size	> 1:
			logger.info('Sentence buffer size: %s' % args.buffer_size)
		self.args =	args
		self.task =	task
		self.models	= models
	def	encode_fn(self,x):
		if self.tokenizer is not None:
			x =	self.tokenizer.encode(x)
		if self.bpe	is not None:
			x =	self.bpe.encode(x)
		return x

	def	decode_fn(self,x):
		if self.bpe	is not None:
			x =	self.bpe.decode(x)
		if self.tokenizer is not None:
			x =	self.tokenizer.decode(x)
		return x
	
	def	translate(self,snts,verbose=False):
		output_snts	= []
		start_id = 0
		for	inputs in buffered_read(snts, self.args.buffer_size):
			results	= []
			for	batch in make_batches(inputs, self.args, self.task,	self.max_positions,	self.encode_fn):
				src_tokens = batch.src_tokens
				src_lengths	= batch.src_lengths
				#cudalock.acquire()
				if self.use_cuda:
					src_tokens = src_tokens.cuda()
					src_lengths = src_lengths.cuda()

				sample = {
					'net_input': {
						'src_tokens': src_tokens,
						'src_lengths': src_lengths,
					},
				}
				translations = self.task.inference_step(self.generator,	self.models, sample)
				#cudalock.release()
				for	i, (id,	hypos) in enumerate(zip(batch.ids.tolist(),	translations)):
					src_tokens_i = utils.strip_pad(src_tokens[i], self.tgt_dict.pad())
					results.append((start_id + id,src_tokens_i,	hypos))
			# sort output to mastch	input order
			if verbose == True:
				for	id,	src_tokens,	hypos in sorted(results, key=lambda	x: x[0]):
					if self.src_dict is	not	None:
						src_str	= self.src_dict.string(src_tokens, self.args.remove_bpe)
						logger.debug('S-{}\t{}\t{}'.format(id,	src_str, src_tokens))

					# Process top predictions
					self.args.nbest	= max(self.args.nbest,1)
						
					for	hypo in	hypos[:min(len(hypos), self.args.nbest)]:
						hypo_tokens, hypo_str, alignment = utils.post_process_prediction(
							hypo_tokens=hypo['tokens'].int().cpu(),
							src_str=src_str,
							alignment=hypo['alignment'],
							align_dict=self.align_dict,
							tgt_dict=self.tgt_dict,
							remove_bpe=self.args.remove_bpe,
						)
						hypo_str = self.decode_fn(hypo_str)
						logger.debug('H-{}\t{}\t{}'.format(id,	hypo['score'], hypo_str))
						logger.debug('P-{}\t{}'.format(
							id,
							' '.join(map(lambda	x: '{:.4f}'.format(x), hypo['positional_scores'].tolist()))
						))
						if self.args.print_alignment:
							alignment_str =	" ".join(["{}-{}".format(src, tgt) for src,	tgt	in alignment])
							logger.debug('A-{}\t{}'.format(
								id,
								alignment_str
						))
			elif verbose ==	False:
				for	id,	src_tokens,	hypos in sorted(results, key=lambda	x: x[0]):
					if self.src_dict is	not	None:
						src_str	= self.src_dict.string(src_tokens, self.args.remove_bpe)
					# Process top predictions
					output_snt = []
					for	hypo in	hypos[:min(len(hypos), self.args.nbest)]:
						hypo_tokens, hypo_str, alignment = utils.post_process_prediction(
							hypo_tokens=hypo['tokens'].int().cpu(),
							src_str=src_str,
							alignment=hypo['alignment'],
							align_dict=self.align_dict,
							tgt_dict=self.tgt_dict,
							remove_bpe=self.args.remove_bpe,
						)
						hypo_str = self.decode_fn(hypo_str)
						output_snt.append([hypo_str, hypo['score'], alignment])
					output_snts.append(output_snt)
			start_id +=	len(inputs)
		return output_snts


def replace_unk(hypo_str, raw_snt):
	hypo_tokens = hypo_str.split()
	src_tokens = raw_snt.split()
	for i, ht in enumerate(hypo_tokens):
		if ht.find('<unk>') >= 0:
			if i == 0:
				logger.debug("replace unk in {} with {}".format(i, src_tokens[0]))
				hypo_tokens[i] = src_tokens[0]
				continue

			if i == len(hypo_tokens) - 1:
				logger.debug("replace unk in {} with {}".format(i, src_tokens[-1]))
				hypo_tokens[i] = src_tokens[-1]
				continue

			idx1 = -1
			idx2 = -1
			try:
				idx1 = src_tokens.index(hypo_tokens[i-1])
				idx2 = src_tokens.index(hypo_tokens[i+1], idx1)
			except :
				pass
			logger.debug('idx of {}={}, idx of {}={}'.format(hypo_tokens[i-1], idx1, hypo_tokens[i+1], idx2))
			# 'Grandma', '��s', 'photo' --> 'Grandma', '<unk>', 's', 'photo'
			if idx1 >= 0 and idx2 == -1 and i < len(hypo_tokens) - 2:
				idx2 = src_tokens.index(hypo_tokens[i+2], idx1)
				logger.debug('idx of {}={}, idx of {}={}'.format(hypo_tokens[i-1], idx1, hypo_tokens[i+2], idx2))
				if idx2 - idx1 == 2:
					logger.debug("replace unk in {} with {}".format(i, src_tokens[idx1+1]))
					hypo_tokens[i] = src_tokens[idx1+1]
					del hypo_tokens[i+1]
					continue

			if idx1 > 0 and idx2 - idx1 == 2:
				src_token = src_tokens[idx1+1]
			elif idx1>0 and idx1 < len(src_tokens)-2 and (src_tokens[idx1+2].startswith(hypo_tokens[i+1]) or hypo_tokens[i+1].startswith(src_tokens[idx1+2])):
				src_token = src_tokens[idx1+1]
			elif idx2>2 and (src_tokens[idx2-2].endswith(hypo_tokens[i-1]) or hypo_tokens[i-1].endswith(src_tokens[idx2-2])):
				src_token = src_tokens[idx2-1]
			else:
				idx1 = -1
				for j in range(max(0,i-3), min(len(src_tokens)-2, i+3)):
					if (src_tokens[j].endswith(hypo_tokens[i-1]) or hypo_tokens[i-1].endswith(src_tokens[j])) and (src_tokens[j+2].startswith(hypo_tokens[i+1]) or hypo_tokens[i+1].startswith(src_tokens[j+2])):
						idx1 = j+1
						break
				if idx1 >= 1:
					src_token = src_tokens[idx1]
				else:
					src_token = src_tokens[i]
			logger.debug("replace unk in {} with {}".format(i, src_token))
			hypo_tokens[i] = src_token
	return ' '.join(hypo_tokens)


detokenize_sent = lambda x: TreebankWordDetokenizer().detokenize(x.split(' '))

class gec_batch_server(object):
	def __init__(self,args):
		self.gec = generate_batch(args)

	def translate(self, snts):
		return self.gec.translate(snts)

	def trans_snts(self, snts):
		''' translate [snts] in a batch mode'''
		trans = self.gec.translate(snts)
		return [(snts[i],trans[i]) for i in range(len(snts))]

	def gec_diff(self, oris):
		''' [snts] -> (src, trg, trans_diff)'''
		logger.debug(" parse doc: %s" % (snts))
		try:
			res = self.trans_snts(snts)
			logger.debug(json.dumps(res))
			trans =  [(oris[i], replace_unk(res[i][1][0][0], snts[i])) for i in range(len(snts))]
		except BaseException as err:
			logger.exception(err)
			res = self.trans_snts([snt for snt in snts])
			trans =  [(oris[i], res[i][1][0][0]) for i in range(len(snts))]

			return trans

def _gec_snts(arr, topn: int=1, asdic:bool=False):
	trans = gb.translate(arr)
	res = []
	for i in range(len(trans)):
		re = []
		for j in range(min(int(topn), len(trans[i]))):
			re.append([replace_unk(trans[i][j][0], arr[i]), trans[i][j][1]])
		res.append(re)
	return {arr[i]:res[i] for i in range(len(arr))} if asdic else [ {'snt':arr[i], 'gec':res[i] }  for i in range(len(arr))]

@app.get('/gecsnts')
async def gecsnts(snts: str='["It are ok.","He has ready."]', topn: int=1):
	arr = json.loads(snts)
	return _gec_snts(arr, topn)

@app.get('/gecsnts_cached')
async def gecsnts_cached(snts: str='["It are ok.","He has ready."]', topn: int=1):
	arr = json.loads(snts)
	res = uvicorn.r.mget(arr)
	dic = _gec_snt([snt for snt, tgt in res if tgt is None], topn=1, asdic=True)
	for k,v in dic.items():  uvicorn.r.set(k, v[0][0])
	return [ {'snt':snt, 'gec':dic[snt] } if tgt is None else {'snt':snt, 'gec':[[tgt, 0]] } for snt, tgt in res]

@app.post('/gecsnts')
async def gec_snts(item: ItemSnts):
	''' translate the given sentences'''
	arr = item.snts
	trans = gb.translate(arr)
	res = []
	for i in range(len(trans)):
		re = []
		for j in range(min(item.topn, len(trans[i]))):
			re.append([replace_unk(trans[i][j][0], arr[i]), trans[i][j][1]])
		res.append(re)
	ret = [ {'snt':arr[i], 'gec':res[i] }  for i in range(len(arr))]
	return ret

import errant, spacy # 2020-9-10 #https://github.com/chrisjbryant/errant
errant.annotator = errant.load('en', nlp=spacy.load('en_core_web_sm'))
#align		= lambda doc, tdoc:  { f"e_{e.type}@{e.o_start}": f"_{e.o_start}_{e.o_end}_{e.o_str}_{e.c_start}_{e.c_end}_{e.c_str}_{e.type}" for e in errant.annotator.annotate(doc, tdoc) } #1 2 are 1 2 is R:VERB:SVA 
align		= lambda doc, tdoc:  { f"e_{e.type}@{e.o_start}/gec": (e.o_start,e.o_end,e.o_str,e.c_start,e.c_end,e.c_str,e.type) for e in errant.annotator.annotate(doc, tdoc) } #1 2 are 1 2 is R:VERB:SVA
nlp			= spacy.load("en_core_web_sm")  # change to read from cache later 

def _gec_errant(snt:str, gec:str, include_src:bool=False):
	try:
		doc, tdoc = nlp(snt), nlp(gec)   #change to : spacyr.parse(snt), spacyr.parse(trans) 
		dic = align(doc,tdoc)
		dic.update({'gec':gec})
		if include_src : dic.update({'snt':snt})
		return dic
	except Exception as e:
		print ("_gec_errant ex:", e, snt, gec)
		return {'snt': snt, 'gec': gec, 'err': str(e)}

class ItemSnt(BaseModel):
	snt: str
	cache: Optional[bool] = False

@app.post('/gec/snt')
async def gec_snt(item: ItemSnt):
	try:
		res = _gec_snts([item.snt])
		tgt = res[0]['gec'][0][0]
		return _gec_errant(item.snt, tgt)
	except Exception as e:
		print ("gec_snt", e, item.snt)
		return {'snt': item.snt, 'err': str(e)}

class ItemPair(BaseModel):
	snt: str
	gec: str
@app.post('/gec/errant')
async def gec_errant(item: ItemPair): return _gec_errant(item.snt, item.gec)

if __name__ == '__main__':
	parser = options.get_generation_parser(interactive=True)
	parser.add_argument('--port', default=80, type=int,  help='server port')
	parser.add_argument('--source_lang', default='er', type=str,  help='source language')
	parser.add_argument('--target_lang', default='co', type=str,  help='target language')
	parser.add_argument('--bpe_codes', default='./code', type=str,  help='bpe_codes')
	parser.add_argument('--buffer_size', default=10, type=int,  help='buffer size')
	parser.add_argument('--batch_size', default=10, type=int,  help='batch size')
	parser.add_argument('--num_workers', default=20, type=int,  help='num workers')
	parser.add_argument('--remove_bpe', default='@@ ', type=str,  help='reomve bpe')
	parser.add_argument('--gpus', default='0,1', type=str,  help='CUDA_VISIBLE_DEVICES')
	parser.add_argument('--cuda', default='-1', type=str,  help='selected cuda')
	parser.add_argument('--random', default='-1', type=int,  help='sum of the GPUs, random one')
	parser.add_argument('--id', default='1', help="log id")
	parser.add_argument('--redis_host', default='127.0.0.1', type=str)
	parser.add_argument('--redis_port', default=6379, type=int)
	parser.add_argument('--redis_db', default='-1', type=int)

	args = options.parse_args_and_arch(parser)
	os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda if args.cuda != '-1' else args.gpus  #'0,1,2,3'
	if args.random > 0 : os.environ["CUDA_VISIBLE_DEVICES"] = str(int(random.random() * (args.random-1) ))
	if args.redis_db > 0 : setattr(uvicorn, 'r', redis.Redis(host=args.redis_host, port=args.redis_port, db=args.redis_db, decode_responses=True))

	gb = gec_batch_server(args)
	setattr(uvicorn, 'args', args)
	uvicorn.run(app, host='0.0.0.0', port=args.port)

'''
wget -O test.html 'http://127.0.0.1:20001/gecsnts/json' --post-data '{"snts":["It is ok.","He has ready."],"topn":3}'
wget -O test.html 'http://127.0.0.1:20001/gecsnts?snts=["How older are you?","It am hard for you too do it ."]&topn=3'
'''