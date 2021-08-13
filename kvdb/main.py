# 2021-2-1, uvicorn app  | docker run -itd -p 7086:8000 --name kvdb wrask/kvdb
import uvicorn,os
import kvdb
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
map = {filename.lower().split(".")[0] : kvdb.Kvdb(f'/data/{filename}') for filename in os.listdir('/data') if filename.endswith(".kvdb") }
print ( map, flush=True) #map = {'gzjc': kvdb.Kvdb('/data/gzjc.kvdb'), 'clec': kvdb.Kvdb('/data/clec.kvdb'), }

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> kvdb http api </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-2-1")

@app.get('/corpus/{name}/{key}') #http://localhost:8000/corpus/clec/~dobj_VERB_NOUN:problem
def kv_get(name: str='gzjc', key: str = 'dobj_VERB_NOUN:door', defau:str=None):  
	return map[name].get(key, defau)

@app.get('/corpus/top/{name}/{key}') 
def kv_get(name: str='gzjc', key: str = 'open:dobj_VERB_NOUN', topn:int=10):  
	return map[name](key, topn)

@app.get('/corpus/mf/{name}/{key}')
def kv_mf(name: str='gzjc', key: str = 'learn', len:int = 2):  
	return round(1000000 * map[name][key] / float(map[name]['sum:LEX']), len)

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=8000)