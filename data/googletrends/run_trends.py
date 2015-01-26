import sys
import os

infile = open('../nytimes/common_bad', 'r')
for line in infile:
    word = line.split()
    command = 'python /Users/bauer/software/python/google-trends-csv-downloader-master/test.py {0}'.format(word)
    os.system(command)
infile.close()
infile = open('../nytimes/common_good', 'r')
for line in infile:
    word = line.split()
    command = 'python /Users/bauer/software/python/google-trends-csv-downloader-master/test.py {0}'.format(word)
    os.system(command)
infile.close()
