# 2021-3-4  
FROM python:3.8-slim

RUN pip install fire pika requests redis pymysql \
    && pip install spacy==2.2.4 \
    && pip install http://ftp.werror.com:8021/tmp/spacy/en_core_web_sm-2.2.5.tar.gz 
#    && pip install textacy 

COPY mqrun.py /mqrun.py
WORKDIR /
ENTRYPOINT python /mqrun.py 
#CMD python /mqrun.py 