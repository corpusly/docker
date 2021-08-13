# 2021-1-29, base + diskcache image | run -it -p 8889:8000 -v ~/dcdata:/dcdata diskcache python main.py
FROM python:3.8-alpine3.10

LABEL maintainer="zy <zy@cikuu.com>"

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install diskcache==5.0.3 \
    && apk del .build-deps gcc libc-dev make

COPY ./main.py /main.py
ADD ./dcdata.tar.gz /
WORKDIR /

EXPOSE 8000

CMD python main.py
