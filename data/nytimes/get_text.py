import sys
import os
import numpy as np
import pandas
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import cPickle as pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

stop = stopwords.words('english')

positive_file = open('/Users/bauer/insight/teleborder/data/nlp/opinion-lexicon-English/positive-words.txt')
negative_file = open('/Users/bauer/insight/teleborder/data/nlp/opinion-lexicon-English/negative-words.txt')
positive_words = []
for line in positive_file:
    sline = line.split()
    if len(sline) and sline[0][0] != ';':
        positive_words.append(sline[0].decode('utf-8'))
negative_words = []
for line in negative_file:
    sline = line.split()
    if len(sline) and sline[0][0] != ';':
        try:
            negative_words.append(sline[0].decode('utf-8'))
        except:
            print 'Ignoring the word {0}.'.format(sline[0])
stemmer = SnowballStemmer("english")
positive_stemmed = []
for word in positive_words:
    positive_stemmed.append(stemmer.stem(word))
negative_stemmed = []
for word in negative_words:
    negative_stemmed.append(stemmer.stem(word))


filenames = []
dirs = os.listdir('/Users/bauer/insight/teleborder/data/nytimes')
for dir in dirs:
    if re.match('^20', dir):
        dir2 = os.path.join('/Users/bauer/insight/teleborder/data/nytimes',dir)
        files = os.listdir(dir2)
        for fn in files:
            if re.match('^log_api', fn):
                filename = os.path.join(dir2,fn)
                filenames.append(filename)
print 'Parsed {0} filenames'.format(len(filenames))
acount = 1

article_sents = []
article_dates = []
article_tosave = []
for filename in filenames:
    print filename
    json_file = open(filename)
    try:
        json_data = json.load(json_file)
    except:
        continue
    for article in json_data['response']['docs']:
        pubdate = pandas.to_datetime(article['pub_date']).date()
        url = article['web_url']
        p = None
        try:
            p=requests.get(url).content
        except:
            print 'Skipping url {0}: bad request'.format(url)
            continue
        soup=BeautifulSoup(p)
        paragraphs=soup.select("p.story-body-text")
        if paragraphs:
            text=""
            for paragraph in paragraphs:
                text+=paragraph.text
            text=text.encode('ascii', 'ignore')
        else:
            paragraphs = soup.find(id='articleBody')
            if not paragraphs:
                paragraphs = soup.find('div', attrs={'class': 'articleBody'})
                if not paragraphs:
                    print 'Text not found in {0}'.format(url)
                    continue
            paragraphs = paragraphs.get_text(strip=True)
            text = paragraphs.encode('ascii', 'ignore')
        text = re.sub(r'\W+', ' ', text)
        article_data = {'body':text, 'pubdate':pubdate}
        # pickle.dump(article_data, open('/Users/bauer/insight/teleborder/data/nytimes/article_text/article{0}.txt'.format(acount), 'w'))
        article_tosave.append(article_data)
        acount += 1

        tokens = nltk.word_tokenize(text)
        words = [w.lower().decode('utf-8') for w in tokens]
        words = [i for i in words if i not in stop]

        stemmer = SnowballStemmer("english")
        stemmed = []
        for word in words:
            stemmed.append(stemmer.stem(word))

        score = 0
        count = 0
        for word in stemmed:
            if word in positive_stemmed:
                score += 1
                count += 1
            if word in negative_stemmed:
                score -= 1
                count += 1

        #print 'Score = {0}, Count = {1} pubdate = {2}'.format(score, count, pubdate)
        article_sents.append(score)
        article_dates.append(pubdate)
        
    json_file.close()

# print article_dates
# print article_sents
pickle.dump((article_dates,article_sents), open('/Users/bauer/insight/teleborder/data/nytimes/sentiment_data1.txt', 'w'))
pickle.dump(article_tosave, open('/Users/bauer/insight/teleborder/data/nytimes/article_data1.txt', 'w'))

