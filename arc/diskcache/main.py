# 2021-1-29, uvicorn app  | docker run -itd -p 7086:8000 --name dc wrask/diskcache
import uvicorn, zlib 
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from cikuu.mod.diskcache import Index
db= Index('/dcdata')
app = FastAPI()

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> diskcache(5.0.3) http api </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-1-29")

@app.get('/dc/get')
def dc_get(key: str, default:str=None, compress:bool=False):  return db.get(key, default) if not compress else zlib.decompress(db.get(key, default))

@app.get('/dc/set')
def dc_set(key: str, value:str, compress:bool=False):  
	db[key] = zlib.compress(value) if compress else value
	return db[key]

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=80)
