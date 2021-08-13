# 2021-2-13  | docker build -t wrask/uvirun . | docker run --rm -it -e pyfile=http://cikuu.werror.com/app/nldp/nldp.py -p 8889:80 wrask/uvirun  | 102M
FROM python:3.8-alpine3.10

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install requests requests_async asyncio \
    && pip install redis \
    && apk del .build-deps gcc libc-dev make

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /
EXPOSE 80
CMD python /main.py 