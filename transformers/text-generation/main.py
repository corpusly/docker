# 2021-2-11 | docker run -it --rm -p 8889:80 trs_fillmask
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from transformers import pipeline

app = FastAPI()
f = pipeline("text-generation")

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> text-generation:4.3.2 </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-2-11")

@app.get('/fillmask/get')
def text_generation_get(snt: str = "As far as I am concerned, I will", max_length:int = 10, do_sample:bool=False):  
	return f(snt, max_length=max_length, do_sample=do_sample)

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=80)