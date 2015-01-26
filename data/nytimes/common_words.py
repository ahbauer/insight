import sys
import cPickle as pickle
import datetime
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

article_data = pickle.load(open('/Users/bauer/insight/teleborder/data/nytimes/article_data1.txt','r'))
print '{0} articles read in from file'.format(len(article_data))

stop = stopwords.words('english')
all_words = {}
stemmed_words = []
for article in article_data:
    text = article['body']
    pubdate = datetime.datetime.combine(article['pubdate'], datetime.datetime.min.time())
    mindate = datetime.datetime.strptime('2013-01', "%Y-%m")
    maxdate = datetime.datetime.strptime('2015-01', "%Y-%m")
    
    if (pubdate > mindate) and (pubdate < maxdate):
        
        tokens = nltk.word_tokenize(text)
        article_words = [w.lower().decode('utf-8') for w in tokens]
        article_words = [i for i in article_words if i not in stop]
        
        bigram_measures = nltk.collocations.BigramAssocMeasures()

        stemmer = SnowballStemmer("english")
        for article_word in article_words:
            stemmed = stemmer.stem(article_word)
            stemmed_words.append(stemmed)
            if stemmed not in all_words:
                all_words[stemmed] = 1
            else:
                all_words[stemmed] += 1


finder = nltk.collocations.BigramCollocationFinder.from_words(stemmed_words)
finder.apply_freq_filter(10)
print finder.nbest(bigram_measures.pmi, 100)  
exit(0)


for word in sorted(all_words, key=all_words.get, reverse=True):
    if all_words[word]>1:
        print '{0} {1}'.format(word,all_words[word])

