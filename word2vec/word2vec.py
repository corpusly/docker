# 2021-2-10 docker run -it --rm -p 8889:80 192.168.1.24:5000/word2vec 
import uvicorn, gensim 
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

import gensim.downloader as api
model = api.load("word2vec-google-news-300") #"glove-wiki-gigaword-300") #glove-twitter-25")  # download the model and return as object ready for use
#model.most_similar("cat")

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> word2vec/gensim http api </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-2-10")

@app.get('/word2vec/similar')
def wv_similar(key: str ='overcome', topn:int=10):  return model.most_similar(key, topn=topn)

class Item(BaseModel): 
	positive: list
	negative: list
	topn: Optional[int] = 10
	
@app.post('/word2vec/most_similar')
def wv_most_similar(item: Item):
	''' #model.most_similar(positive=['woman', 'king'], negative=['man'])   '''
	return model.most_similar(positive=item.positive, negative=item.negative, topn=item.topn)

@app.get('/word2vec/get_vector')
def get_vector(key: str='consider'):  
	try:
		return list(model.get_vector(key))
	except Exception as e:
		print (e)
	return []

@app.get('/word2vec/get/{w}')
def wv_get(w: str='consider'):  return list(model[w])

@app.get('/word2vec/getcosine/{w1}/{w2}')
def cosine(w1:str='woman', w2:str='man'): return float(model.similarity(w1,w2))   # output: 0.73723527 

@app.get('/word2vec/cosine')
def words_cosine(words1:str='woman,man,lady', words2:str='man,lady', sepa:str=','): 
	arr1 = words1.split(sepa)
	arr2 = words2.split(sepa)
	return [ (w1, w2, float(model.similarity(w1,w2)))  for w1 in arr1 for w2 in arr2 if w1 != w2 ]

@app.get('/word2vec/notmatch')
def wv_get(words: str="breakfast cereal dinner lunch"): return model.doesnt_match(words.strip().split()) 

if __name__ == '__main__':
	print ("hello word2vec", flush=True)
	uvicorn.run(app, host='0.0.0.0', port=80)