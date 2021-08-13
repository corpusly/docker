# 2021-1-29, uvicorn app   docker run -itd -p 7085:8000 --name nltk wrask/nltk
import argparse,uvicorn,nltk
from textblob import Word #http://www.nltk.org/howto/wordnet.html
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/nltk/synset')
def nltk_synset(w:str="consider"):
	synset = { lemma.name() for ws in Word(w).synsets for lemma in ws.lemmas() if not '_' in lemma.name()}
	synset.discard(w) #http://www.nltk.org/howto/wordnet.html  antoynms also exists path
	return synset

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> nltk http api </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-1-29")

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=80)
