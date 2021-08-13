#2021-2-12 |  docker run -it --rm -p 8889:80 wrask/fts5
import os,uvicorn,json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from fts5 import Fts5

app		= FastAPI()
files	= [file for file in os.listdir(f"/model") if file.endswith(".fts5") ]
map		= { file.lower().split(".")[0]: Fts5(f"/model/{file}")  for file in files}

@app.get('/')
def home(): 
	''' corpus:  bnc,gzjc,sino,dic '''
	return HTMLResponse(content='''<h2>snt fts5,  bnc,sino,dic,gzjc</h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-2-12''')

@app.get('/fts5/{corpus}/gramcnt')
def fts_gramcnt(corpus:str='bnc', gram:str="overcome the|overcome this"): 
	return [ (s, map[corpus].gramcnt(s) ) for s in gram.strip().split("|")]

@app.get('/fts5/{corpus}/cooccur')
def fts_cooccur(corpus:str='bnc', words1:str="overcome,problem", words2:str="difficulty,open"): 
	return [ (w1, w2, map[corpus].cooccur(w1,w2) ) for w1 in words1.strip().split(",") for w2 in words2.strip().split(",")]

@app.get('/fts5/{corpus}/phraseso')
def fts_snt_phraseso(corpus:str='bnc', q:str="overcome the", topn:int=10): 
	return list(map[corpus].conn.execute(f"SELECT * FROM fts where fts match '\"{q}\"' limit {topn}"))

@app.get('/fts5/{corpus}/snt')
def fts_snt_so(corpus:str='bnc', q:str="overcome the", topn:int=10): 
	return list(map[corpus].conn.execute(f"SELECT * FROM fts where fts match '{q}' limit {topn}"))

@app.get('/fts5/{corpus}/count')
def fts_snt_count(corpus:str='bnc', q:str="overcome AND problem AND new"): 
	return list(map[corpus].conn.execute(f"SELECT count(*) FROM fts where fts match '{q}'"))[0][0]

@app.get('/fts5/{corpus}/dualword')
def fts_snt_dualword(corpus:str='bnc', w1:str="overcome", w2:str="problem", topn:int=10): 
	return list(map[corpus].conn.execute(f"SELECT * FROM fts where fts match '{w1} AND {w2}' limit {topn}"))

@app.get('/fts5/{corpus}/andwords')
def fts_snt_andwords(corpus:str='bnc', words:str="overcome,problem", topn:int=10): 
	query = words.replace(",", ' AND ')
	return list(map[corpus].conn.execute(f"SELECT * FROM fts where fts match '{query}' limit {topn}"))

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=80)