# 2021-1-29, base + nltk image | run -it -p 8889:8000 nltk python main.py | docker run -it -p 8889:8000 nltk
FROM python:3.8-alpine3.10

LABEL maintainer="zy <zy@cikuu.com>"

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install textblob \
    && pip install nltk \
    && apk del .build-deps gcc libc-dev make

#RUN [ "python", "-c", "import nltk; nltk.download('all')" ]

ADD ./nltk_data.tar.gz /root/
COPY ./main.py /main.py
WORKDIR /

EXPOSE 80

CMD python main.py
