# 2021-2-12 | docker build -t wrask/fts5 . | docker run -it --rm -p 8889:80 wrask/fts5
FROM python:3.8-alpine3.10

RUN pip install --no-cache-dir uvicorn fastapi 
WORKDIR /

RUN wget http://ftp.werror.com:8021/tmp/snt-fts5.tar.gz -O /snt-fts5.tar.gz \
    && tar zxvf /snt-fts5.tar.gz  \
    && rm /snt-fts5.tar.gz

COPY *.py /
EXPOSE 80
CMD python /main.py
