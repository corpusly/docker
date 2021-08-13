https://radimrehurek.com/gensim/models/word2vec.html

1. subwords
2. use word2vec to filter, and ranking 
3. use pattern to bing the sentence including two words 


-- pika.werror.com: , with mother data inside , also with word2vec inside, kpf, kpstop 
-- new a dataset, ie:  kpstop= {}

# Show all available models in gensim-data
print(list(gensim.downloader.info()['models'].keys()))
['fasttext-wiki-news-subwords-300',
 'conceptnet-numberbatch-17-06-300',
 'word2vec-ruscorpora-300',
 'word2vec-google-news-300',
 'glove-wiki-gigaword-50',
 'glove-wiki-gigaword-100',
 'glove-wiki-gigaword-200',
 'glove-wiki-gigaword-300',
 'glove-twitter-25',
 'glove-twitter-50',
 'glove-twitter-100',
 'glove-twitter-200',
 '__testing_word2vec-matrix-synopsis']
>>>
# Download the "glove-twitter-25" embeddings
glove_vectors = gensim.downloader.load('word2vec-google-news-300')
>>>
# Use the downloaded vectors as usual:
glove_vectors.most_similar('twitter')
[('facebook', 0.948005199432373),
 ('tweet', 0.9403423070907593),
 ('fb', 0.9342358708381653),
 ('instagram', 0.9104824066162109),
 ('chat', 0.8964964747428894),
 ('hashtag', 0.8885937333106995),
 ('tweets', 0.8878158330917358),
 ('tl', 0.8778461217880249),
 ('link', 0.8778210878372192),
 ('internet', 0.8753897547721863)]


https://github.com/RaRe-Technologies/gensim-data

python -m gensim.downloader --info  # show info about available models/datasets
python -m gensim.downloader --download text8  # download text8 dataset to ~/gensim-data/text8
python -m gensim.downloader --download glove-twitter-25  # download model to ~/gensim-data/glove-twitter-50/

python -m gensim.downloader --download glove-wiki-gigaword-300


# Chinese word2vec
https://www.cnblogs.com/bincoding/p/8911943.html
https://github.com/Embedding/Chinese-Word-Vectors
https://github.com/ymcui/Chinese-BERT-wwm


https://www.cnblogs.com/Allen-rg/p/10589035.html

3、模型使用

model.most_similar(positive=['woman', 'king'], negative=['man'])  
#输出[('queen', 0.50882536), ...]  
   
model.doesnt_match("breakfast cereal dinner lunch".split())  
#输出'cereal'  
   
model.similarity('woman', 'man')  
#输出0.73723527  
   
model['computer']  # raw numpy vector of a word  
#输出array([-0.00449447, -0.00310097,  0.02421786, ...], dtype=float32)  
　　