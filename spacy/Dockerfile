# 2021-2-13
FROM wrask/uvirun

RUN apk add --no-cache --virtual .build-deps g++ libc-dev make \
    && pip install marisa_trie pygtrie numpy pandas \
    && pip install spacy==3.0.1 \
    && pip install http://ftp.werror.com:8021/tmp/en_core_web_sm-3.0.0.tar.gz \
    && pip install http://ftp.werror.com:8021/tmp/en_core_web_md-3.0.0.tar.gz 

WORKDIR /
EXPOSE 80
CMD python /main.py 