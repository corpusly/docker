
3.5  https://github.com/chssch/textacy-docker/blob/master/Dockerfile

FROM python:latest
RUN apt-get -qy update --fix-missing
RUN pip install --upgrade pip
RUN pip install -U spacy ipython
RUN pip install git+https://github.com/chartbeat-labs/textacy.git
RUN python -m spacy.en.download --force all

21.2.14: 
- move word_idf.py to pypi: pigai.word_idf , push online 

docker run --rm -it python:3.8-alpine3.10 /bin/sh

ps@gpu24:~/cikuu/docker/uvirun$ docker run --rm -it -e pyfile=http://cikuu.werror.com/app/nldp/nldp.py -p 8889:80 uvirun 
Connecting to cikuu.werror.com (153.36.240.24:80)
main.py              100% |********************************|  1307  0:00:00 ETA
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)


>>> ruler = nlp.add_pipe("attribute_ruler")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/cikuu/miniconda3/envs/spacy/lib/python3.8/site-packages/spacy/language.py", line 751, in add_pipe
    raise ValueError(Errors.E007.format(name=name, opts=self.component_names))
ValueError: [E007] 'attribute_ruler' already exists in pipeline. Existing names: ['tok2vec', 'tagger', 'parser', 'senter', 'ner', 'attribute_ruler', 'lemmatizer']

https://spacy.io/api/attributeruler   ===> repos 

https://spacy.io/usage/linguistic-features/#mappings-exceptions


https://spacy.io/models/zh#zh_core_news_trf


# Download best-matching version of specific model for your spaCy installation
python -m spacy download en_core_web_sm

# pip install .tar.gz archive from path or URL
pip install /Users/you/en_core_web_sm-2.2.0.tar.gz
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz

pip install http://ftp.werror.com:8021/tmp/en_core_web_sm-3.0.0.tar.gz 
pip install http://ftp.werror.com:8021/tmp/en_core_web_md-3.0.0.tar.gz 


https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-3.0.0
https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz
https://github.com/explosion/spacy-models/releases/download/zh_core_web_sm-3.0.0/zh_core_web_sm-3.0.0.tar.gz
https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.0.0/en_core_web_trf-3.0.0.tar.gz

pip install torch==1.2.0 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

=== https://spacy.io/usage/saving-loading
import spacy
from spacy.tokens import DocBin

doc_bin = DocBin(attrs=["LEMMA", "ENT_IOB", "ENT_TYPE"], store_user_data=True)
texts = ["Some text", "Lots of texts...", "..."]
nlp = spacy.load("en_core_web_sm")
for doc in nlp.pipe(texts):
    doc_bin.add(doc)
bytes_data = doc_bin.to_bytes()

# Deserialize later, e.g. in a new process
nlp = spacy.blank("en")
doc_bin = DocBin().from_bytes(bytes_data)
docs = list(doc_bin.get_docs(nlp.vocab))


https://spacy.io/usage/projects#fastapi   || to make docker images  spacy:3.0.1,  with fastapi, and cmd tools 
cosine = lexeme.similarity  ===> insim 

lookup? add ectans ? is it open? 

https://spacy.io/api/vectors#most_similar
queries = numpy.asarray([numpy.random.uniform(-1, 1, (300,))])
most_similar = nlp.vocab.vectors.most_similar(queries, n=10)

===
apple = nlp.vocab["apple"]
orange = nlp.vocab["orange"]
apple_orange = apple.similarity(orange)
orange_apple = orange.similarity(apple)
assert apple_orange == orange_apple

>>> nlp.vocab['football'].similarity(nlp.vocab['orange'])
0.21652275
>>> nlp.vocab['football'].similarity(nlp.vocab['ball'])
0.49674925
>>> nlp.vocab['football'].similarity(nlp.vocab['niche'])
0.17494923
>>> nlp.vocab['football'].similarity(nlp.vocab['consider'])
0.23825042


# https://github.com/explosion/sense2vec

tandalone usage
from sense2vec import Sense2Vec

s2v = Sense2Vec().from_disk("/path/to/s2v_reddit_2015_md")
query = "natural_language_processing|NOUN"
assert query in s2v
vector = s2v[query]
freq = s2v.get_freq(query)
most_similar = s2v.most_similar(query, n=3)
# [('machine_learning|NOUN', 0.8986967),
#  ('computer_vision|NOUN', 0.8636297),
#  ('deep_learning|NOUN', 0.8573361)]
Usage as a spaCy pipeline component
warning Note that this example describes usage with spaCy v3. For usage with spaCy v2, download sense2vec==1.0.3 and check out the v1.x branch of this repo.

import spacy

nlp = spacy.load("en_core_web_sm")
s2v = nlp.add_pipe("sense2vec")
s2v.from_disk("/path/to/s2v_reddit_2015_md")

doc = nlp("A sentence about natural language processing.")
assert doc[3:6].text == "natural language processing"
freq = doc[3:6]._.s2v_freq
vector = doc[3:6]._.s2v_vec
most_similar = doc[3:6]._.s2v_most_similar(3)
# [(('machine learning', 'NOUN'), 0.8986967),
#  (('computer vision', 'NOUN'), 0.8636297),
#  (('deep learning', 'NOUN'), 0.8573361)]


Tok2Vec.__call__ METHOD
Apply the pipe to one document and add context-sensitive embeddings to the Doc.tensor attribute, allowing them to be used as features by downstream components. The document is modified in place, and returned. This usually happens under the hood when the nlp object is called on a text and all pipeline components are applied to the Doc in order. Both __call__ and pipe delegate to the predict and set_annotations methods.

https://github.com/explosion/spacy-transformers

# docker-compose.yml 

version: '2'

services:
  spacyapi:
    image: jgontrum/spacyapi:en_v2
    ports:
      - "0.0.0.0:4327:80"
    restart: always

# dockerfile 

 # 2021-2-9
FROM python:3.8-slim

LABEL maintainer="zy <zy@cikuu.com>"

RUN pip install spacy==2.2.4 && pip install http://ftp.werror.com:8021/tmp/en_core_web_sm-2.2.5.tar.gz 

EXPOSE 80
CMD ls -l /

=======

Collecting textacy
  Downloading textacy-0.10.1-py3-none-any.whl (183 kB)
Collecting jellyfish>=0.7.0
  Downloading jellyfish-0.8.2.tar.gz (134 kB)
Collecting cachetools>=2.0.1
  Downloading cachetools-4.2.1-py3-none-any.whl (12 kB)
Requirement already satisfied: srsly>=0.0.5 in /usr/local/lib/python3.8/site-packages (from textacy) (2.4.0)
Collecting joblib>=0.13.0
  Downloading joblib-1.0.1-py3-none-any.whl (303 kB)
Collecting spacy<3.0.0,>=2.2.0
  Downloading spacy-2.3.5.tar.gz (5.8 MB)
  Installing build dependencies: started


pip install spacy==3.0.1 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

import unittest
class Test(unittest.TestCase):
	@classmethod
	def setUpClass(cls): init_args()
	def test_debug(self):
		res = dsk(["I have a knowledge.","I love you."], {'id':0, 'timeout':1.5})
		pprint (res) #pprint( [v for k,v in res['snt'].items()] )


===
import uvicorn, fastapi 
from fastapi import FastAPI, routing
router = [
	routing.APIRoute("/nlp/info", endpoint= lambda: "spacy 3.0.1", methods=['get',]),
	routing.APIRoute("/nlp/tojson", endpoint= tojson, methods=['get',]),
]
app = FastAPI(routers=router)

