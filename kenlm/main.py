# 2020-2-21 | docker run -it -e VIRTUAL_HOST=cclm.werror.com --rm --name cclm -p 8889:80 -v /home/cikuu/model/cclm:/model wrask/kenlm
import kenlm,math,os,uvicorn,json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app	 = FastAPI()

c = kenlm.Config() 
c.load_method = kenlm.LoadMethod.LAZY
files = [file for file in os.listdir(f"/model") if file.endswith(".trie") or file.endswith(".klm") or file.endswith(".bin") or file.endswith(".kenlm")]
model = kenlm.Model( f"/model/{files[0]}", c)

mapf = {
'score':	lambda snt : model.score(snt),
'scores':	lambda snt : model.full_scores(snt),
'ppl':		lambda snt : model.perplexity(snt), 
'flue':		lambda snt : 1.0/(1.0+ math.log10(model.perplexity(snt))), #getao
}

class ItemSnts(BaseModel):
	snts: list

@app.post('/kenlm/snts/{func}')
async def kenlm_post_by_func(snts: list = ["I go home.", "I go to home."], func:str="ppl"):	
	''' func: score/scores/ppl/flue '''
	return {snt : mapf[func](snt) for snt in snts} # [(snt, mapf[func](snt)) for snt in snts]

#class ItemSnt(BaseModel):
#	snt: str

@app.post('/kenlm/snt/{func}')
async def kenlm_sntfunc(snt: str="I love you.", func:str="flue"):	# called by sntf
	''' func: score/scores/ppl/flue '''
	return {func: round(mapf[func](snt), 4)}

kenlm_score	= lambda snt : model.score(snt)
full_scores	= lambda snt : model.full_scores(snt)
kenlm_ppl	= lambda snt : model.perplexity(snt)
kenlm_flue	= lambda snt : 1.0/(1.0+ math.log10(model.perplexity(snt))) #getao

sntadd		= lambda snt,idx,w : " ".join([lex if i != idx else f"{w} {lex}" for lex, i in zip(snt.split(), range( snt.count(' ') + 1))])
sntrep		= lambda snt,idx,w : " ".join([lex if i != idx else w for lex, i in zip(snt.split(), range( snt.count(' ') + 1))])
sntdel		= lambda snt,idx : " ".join([lex for lex, i in zip(snt.split(), range( snt.count(' ') + 1)) if i != idx])

flue_add	= lambda snt,widx,w : round(kenlm_flue(sntadd(snt,widx, w)) / kenlm_flue(snt), 4)
flue_rep	= lambda snt,widx,w : round(kenlm_flue(sntrep(snt,widx, w)) / kenlm_flue(snt), 4)
flue_del	= lambda snt,widx : round(kenlm_flue(sntdel(snt,widx)) / kenlm_flue(snt), 4)

@app.get('/')
def home(): return HTMLResponse(content='''<h2>kenlm API:7098</h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-2-11''')

@app.get('/kenlm/score')
def kenlm_snt_score(snt:str="I love you|I like you"): 
	return [ (s, round(model.score(s), 4)) for s in snt.strip().split("|")]

@app.get('/kenlm/fullscores')
def kenlm_fullscores(snt:str="I love you|I like you"): 
	return [ (s, full_scores(s,midx)) for s in snt.strip().split("|")]

@app.get('/kenlm/ppl')
def get_kenlm_ppl(snt:str="I love you|I like you"): 
	return [ (s,round(kenlm_ppl(s,midx), 4)) for s in snt.strip().split("|")]

@app.get('/kenlm/flue')
def get_kenlm_flue(snt:str="I love you|I like you"): 
	return [ (s, round(kenlm_flue(s,midx), 4)) for s in snt.strip().split("|")]

@app.get('/kenlm/flueadd') 
def flueadd(snt:str="I love you", wordidx:int=0, word:str=''): 
	return flue_add(snt, wordidx, word, midx) 

@app.get('/kenlm/fluerep')
def fluerep(snt:str="I love you", wordidx:int=0, word:str=''):
	return flue_rep(snt, wordidx, word, midx) 

@app.get('/kenlm/fluedel')
def fluedel(snt:str="I love you", wordidx:int=0): 
	return flue_del(snt, wordidx, midx)

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=80)