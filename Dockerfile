# 2021-1-29, base image
FROM python:3.8-alpine3.10

LABEL maintainer="zy <zy@cikuu.com>"

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && apk del .build-deps gcc libc-dev make

COPY ./gunicorn_conf.py /gunicorn_conf.py
COPY ./main.py /main.py
WORKDIR /

EXPOSE 8000

CMD uvicorn main:app --port 8000 --host 0.0.0.0
