# 2021-2-11 | docker run -it --rm -p 8889:80 trs_sentiment
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from transformers import pipeline

app = FastAPI()
classifier = pipeline('sentiment-analysis')

@app.get('/')
def home(): return HTMLResponse(content=f"<h2> sentiment-analysis </h2> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a> <br>2021-2-11")

@app.get('/sentiment/get')
def sentiment_analysis_get(snt: str = 'We are very happy to include pipeline into the transformers repository.'):  
	return classifier(snt)

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=80)
