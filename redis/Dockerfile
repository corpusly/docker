# 2021-1-29, base + redis image | run -it -p 8889:8000 uviredis python main.py 192.168.1.100 --port 8008
FROM python:3.8-alpine3.10

LABEL maintainer="zy <zy@cikuu.com>"

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install redis \
    && apk del .build-deps gcc libc-dev make

COPY ./main.py /main.py
WORKDIR /

EXPOSE 8000

CMD python main.py 192.168.1.100 --port 8008 --db 0
