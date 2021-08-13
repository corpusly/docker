# 2021-8-6 | docker build -t wrask/mqeev .  |
FROM python:3.8-alpine
LABEL maintainer="zy <zy@cikuu.com>"

RUN apk add bash && pip install --no-cache-dir fire pymysql redis pika 

WORKDIR /
COPY ./*.py ./

CMD python mqeev.py
