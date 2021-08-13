# 2021-2-10
FROM python:3.8-slim

LABEL maintainer="zy <zy@cikuu.com>"

RUN pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install gensim \
    && pip install requests \
    && apt-get update \
    && apt-get install wget -y
    
WORKDIR /root
#RUN wget http://ftp.werror.com:8021/tmp/gensim-data-glove300.tar.gz && tar zxvf gensim-data-glove300.tar.gz && rm gensim-data-glove300.tar.gz
RUN wget http://ftp.werror.com:8021/tmp/gensim-data-word2vec-google-news-300.tar.gz && tar zxvf gensim-data-word2vec-google-news-300.tar.gz && rm gensim-data-word2vec-google-news-300.tar.gz

COPY ./word2vec.py /word2vec.py

EXPOSE 80
CMD python /word2vec.py