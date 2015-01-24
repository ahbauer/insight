import sys
import os
import numpy as np
import pandas
import re
import time
import json
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import cPickle as pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

article_sents = []
article_dates = []

stop = stopwords.words('english')

words_file = open('/Users/bauer/insight/teleborder/data/nlp/AFINN/AFINN-111.txt')
word_dict = {}
for line in words_file:
    sline = line.split()
    # skip multiple-word entries
    if len(sline) != 2:
        continue
    word_dict[sline[0].decode('utf-8')] = int(sline[1])
print 'Read in {0} single words from the AFINN file'.format(len(word_dict.keys()))

stemmer = SnowballStemmer("english")
words_stemmed = {}
for word in word_dict.keys():
    words_stemmed[stemmer.stem(word)] = word_dict[word]

article_data = pickle.load(open('/Users/bauer/insight/teleborder/data/nytimes/article_data1.txt','r'))
print '{0} articles read in from file'.format(len(article_data))
for article in article_data:
    text = article['body']
    pubdate = article['pubdate']

    tokens = nltk.word_tokenize(text)
    article_words = [w.lower().decode('utf-8') for w in tokens]
    article_words = [i for i in article_words if i not in stop]

    stemmer = SnowballStemmer("english")
    stemmed = []
    for article_word in article_words:
        stemmed.append(stemmer.stem(article_word))

    score = 0
    count = 0
    for article_word in stemmed:
        if article_word in words_stemmed.keys():
            score += words_stemmed[article_word]
            count += 1

    article_sents.append(score)
    article_dates.append(pubdate)

pickle.dump((article_dates,article_sents), open('/Users/bauer/insight/teleborder/data/nytimes/sentiment_data_afinn.txt', 'w'))
