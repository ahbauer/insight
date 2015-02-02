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
from nltk.corpus import wordnet

def words_afinn():
    words_file = open('/Users/bauer/insight/teleborder/data/nlp/AFINN/AFINN-111.txt')
    word_dict = {}
    for line in words_file:
        sline = line.split()
        # skip multiple-word entries
        if len(sline) != 2:
            continue
        word_dict[sline[0].decode('utf-8')] = int(sline[1])
    print 'Read in {0} single words from the AFINN file'.format(len(word_dict.keys()))
    return word_dict

def words_common():
    word_dict = {}
    words_file = open('/Users/bauer/insight/teleborder/data/nytimes/common_good')
    for line in words_file:
        sline = line.split()
        word_dict[sline[0].decode('utf-8')] = 1
    words_file.close()
    words_file = open('/Users/bauer/insight/teleborder/data/nytimes/common_bad')
    for line in words_file:
        sline = line.split()
        word_dict[sline[0].decode('utf-8')] = -1
    words_file.close()
    print 'Read in {0} words from the common words files'.format(len(word_dict.keys()))
    return word_dict
    
def words_grown():
    word_dict = {}
    words_file = open('/Users/bauer/insight/teleborder/data/nytimes/common_good')
    for line in words_file:
        sline = line.split()
        word = sline[0].decode('utf-8')
        word_dict[word] = 1
        synonyms = wordnet.synsets(word)
        for synonym in synonyms:
            matches = re.match('Synset\(\'(\w+).', str(synonym))
            if matches:
                word = matches.group(1)
                word_dict[word] = 0.5
    words_file.close()
    words_file = open('/Users/bauer/insight/teleborder/data/nytimes/common_bad')
    for line in words_file:
        sline = line.split()
        word = sline[0].decode('utf-8')
        word_dict[word] = -1
        synonyms = wordnet.synsets(word)
        for synonym in synonyms:
            matches = re.match('Synset\(\'(\w+).', str(synonym))
            if matches:
                word = matches.group(1)
                word_dict[word] = -0.5
    words_file.close()
    print 'Read in {0} words from the common words files'.format(len(word_dict.keys()))
    return word_dict


article_sents = []
article_dates = []

stop = stopwords.words('english')
word_dict = words_common()

stemmer = SnowballStemmer("english")
stems_p1 = []
stems_p05 = []
stems_n1 = []
stems_n05 = []
words_stemmed = {}
for word in word_dict.keys():
    words_stemmed[stemmer.stem(word)] = word_dict[word]
    if word_dict[word]>0.:
        stems_p1.append(stemmer.stem(word))
    else:
        stems_n1.append(stemmer.stem(word))
stems_p1 = set(stems_p1)
stems_n1 = set(stems_n1)

# syn_dict = {}
# for refword in word_dict:
#     refsyns = wordnet.synsets(refword)
#     for refsyn in refsyns:
#         syn_dict[refsyn] = word_dict[refword]

article_data = pickle.load(open('/Users/bauer/insight/teleborder/data/nytimes/article_data2.txt','r'))
print '{0} articles read in from file'.format(len(article_data))
for article in article_data:
    text = article['body']
    pubdate = article['pubdate']

    tokens = nltk.word_tokenize(text)
    article_words = [w.lower().decode('utf-8') for w in tokens]
    article_words = [i for i in article_words if i not in stop]
    
    # score = 0
    # for refsyn in syn_dict:
    #     for article_word in article_words:
    #         articlesyns = wordnet.synsets(article_word)
    #         for articlesyn in articlesyns:
    #             pathsim = refsyn.path_similarity(articlesyn)
    #             if pathsim is not None:
    #                 score += syn_dict[refsyn]*(pathsim-0.5)
    
    stemmer = SnowballStemmer("english")
    stemmed = []
    for article_word in article_words:
        stemmed.append(stemmer.stem(article_word))
    
    # score = 0
    # stemmed = set(stemmed)
    # score += 1.0*len(stemmed.intersection(stems_p1))
    # score += 0.5*len(stemmed.intersection(stems_p05))
    # score -= 1.0*len(stemmed.intersection(stems_n1))
    # score -= 0.5*len(stemmed.intersection(stems_n05))
    
    score = 0
    count = 0
    fdist = nltk.FreqDist(stemmed)
    for word_stemmed in stems_p1:
        score += 10.0*fdist.freq(word_stemmed)
    for word_stemmed in stems_n1:
        score -= 10.0*fdist.freq(word_stemmed)
    
    # for article_word in stemmed:
    #     if article_word in words_stemmed.keys():
    #         score += words_stemmed[article_word]
    #         count += 1

    article_sents.append(score)
    article_dates.append(pubdate)
    if score>2:
        print article_data

#pickle.dump((article_dates,article_sents), open('/Users/bauer/insight/teleborder/data/nytimes/immigration/sentiment_data_freq2.txt', 'w'))
