#  docker build -t wrask/spacy224,   2021.8.7
FROM wrask/spacy:2.2.4
RUN pip install redis pymysql fire 
WORKDIR /
COPY sntbr.py ./
CMD python /sntbr.py 