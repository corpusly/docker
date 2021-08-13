# 2021-1-29, uvicorn app 
import argparse,uvicorn,redis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

parser = argparse.ArgumentParser(description='args')
parser.add_argument('host', type=str, help='redis host name, ie: 127.0.0.1, 192.168.1.55')
parser.add_argument('--port', default=6379, type=int)
parser.add_argument('--db', default=0, type=int)
parser.add_argument('--decode_responses', default=True, type=bool)
args = parser.parse_args() #args, unknown = parser.parse_known_args()

r = redis.Redis(host=args.host, port=args.port, decode_responses=args.decode_responses)
print ( r, flush=True)

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> redis http api </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-1-29")

@app.get('/redis/get')
def redis_get(key: str):  return r.get(key)

@app.get('/redis/set')
def redis_set(key: str, value:str):  return r.set(key, value)

@app.get('/redis/hgetall')
def redis_hgetall(key: str):  return r.hgetall(key)

@app.get('/redis/hset')
def redis_hset(name: str, key:str, value:str):  return r.hset(name, key, value)

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=8000)
