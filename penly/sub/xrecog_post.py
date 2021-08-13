# redis stream consumer, 2021-6-18 | python xrecog.py en_US recog --http_port 8461
import fire, json, redis, socket, os, time, requests
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

r = None
logger = None

now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
recog = lambda listkey,port=8460: requests.get(f"http://172.17.0.1:{port}/",params={"listkey":listkey}).json()

xyt = lambda tups: { "x": [int(tup[0]) for tup in tups] ,  "y": [int(tup[1]) for tup in tups],  "t": [int(tup[-1]) for tup in tups]}
stroke_xyt = lambda stroke: xyt([ s.split(',')  for s in stroke.split(' ')])
events = lambda listkey: {"events": [stroke_xyt(s) for s in r.lrange(listkey, 0,-1)] }
recog_post2 = lambda listkey,port=8460: requests.post(f"http://172.17.0.1:{port}/",data=json.dumps(events(listkey)), timeout=10).json()

MAX_RETRY = 4
def recog_post(listkey, port=8460):
    strokes = [stroke_xyt(s) for s in r.lrange(listkey, 0,-1)]
    events = json.dumps({"events": strokes })
    logger.debug(events)
    retry = MAX_RETRY
    while retry > 0:
        reply = None
        try:
            reply = requests.post(f"http://172.17.0.1:{port}/",data=events, timeout=10)
            ret = reply.json()
            return ret
        except Exception as e:
            if (reply != None):
                logger.debug(f"retry-{retry}:{reply.text}")
            else:
                logger.debug(f"retry-{retry}: None")
        retry -= 1

    return None

def process(id,params, r, http_port, pid):  #{ap}:{page}:{pen}:{item}
	try:
		key = params['key']
		llen = r.llen(key) 
		#bbox = recog(key, http_port)
		bbox = recog_post(key, http_port)
		if bbox is None:
			print(f"recog {key} failed")
			return
		label = bbox['label']
		logger.debug(f"{key} -->{label}")
		r.zadd( f"{key}:label", {label:llen})
		if len(bbox['words']) > 0:  
			candidates = bbox['words'][0].get('candidates', [])
			r.hset( f"{key}:cands", llen, json.dumps(candidates) )
		r.publish("pen_label", json.dumps({'key':key, 'label': label , 'llen': llen}) )
		r.publish(f"log_xrecog_{pid}",f"{id},{key}/{llen},{now()} -> {label}")
	except Exception as ex:
		logger.exception(ex)

def consume(stream, group, http_port=8461, host='localhost', port=6379, db=0, waitms=3600000, oper='1'):
	global r
	global logger

	# logging
	logging.getLogger("requests").setLevel(logging.WARNING)
	logger = logging.getLogger("xrecog")
	logger.setLevel(level=logging.DEBUG)
	formatter = "%(asctime)s %(filename)s %(levelname)s %(name)s:%(lineno)s %(message)s"
	console_handler = logging.StreamHandler()
	console_handler.setLevel(level=logging.DEBUG)
	console_handler.setFormatter(logging.Formatter(formatter))
	logfile = "logs/xrecog-" + stream + '-' + str(oper)
	time_rotate_file = TimedRotatingFileHandler(filename=logfile, when='midnight', interval=1, atTime=datetime.time(0, 0, 0), backupCount=10)
	time_rotate_file.setFormatter(logging.Formatter(formatter))
	time_rotate_file.setLevel(logging.DEBUG)
	logger.addHandler(time_rotate_file)

	r = redis.Redis(host=host, port=port, db=db, decode_responses=True) 
	try:
		r.xgroup_create(stream, group,  mkstream=True)
	except Exception as e:
		logger.exception(e)

	pid = os.getpid()
	consumer_name = f'consumer_{socket.gethostname()}_{pid}'
	logger.info(f"Started: {consumer_name}|{stream}|{group}\t{now()}" + str(r))
	while True:
		item = r.xreadgroup(group, consumer_name, {stream: '>'}, count=1, noack=True, block= waitms )
		try:
			if not item: break
			logger.debug(item)
			id,params = item[0][1][0]  #[['_new_snt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
			process(id,params, r, http_port, pid)
		except Exception as e:
			logger.exception(e)

	r.xgroup_delconsumer(stream, group, consumer_name)
	r.close()
	print ("Quitted:", consumer_name, "\t",now())

if __name__ == '__main__': 
	fire.Fire(consume) 
