# 2021-2-6, base + svnbase image |192.168.1.24:5000/cikuusvn  | docker run -itd -e VIRTUAL_HOST=sentord.werror.com --restart always --name sentord 192.168.1.24:5000/cikuusvn python uvirun.py /home/cikuu/uvirun/sentord.py --pip pygtrie | 21-2-6  
FROM python:3.8-alpine3.10

LABEL maintainer="zy <zy@cikuu.com>"

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install fire \
    && pip install requests \
    && pip install redis \
    && apk add subversion \
    && apk del .build-deps gcc libc-dev make

WORKDIR /home
RUN svn co http://117.79.131.116:6666/svn/yankc/cikuu/ --username zhangyue --password zhangy1235 --depth files  && svn up cikuu/app --username zhangyue --password zhangy1235

RUN ln -s /home/cikuu /usr/local/lib/python3.8/site-packages/cikuu && ln -s /home/cikuu /cikuu && ln -s /home/cikuu/uvirun /uvirun

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80
CMD ls -l /home/cikuu/app