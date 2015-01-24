import os
import re
import time
import numpy as np

npages = -1
done = False
page = 0
results_files = []

begindate = '20140702'
enddate = '20141231'

outfilename = 'query_results_files'
while not done:
#    call = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=%22United+States+Economy%22&fq=source%3A%22The+New+York+Times%22+and+news_desk%3A%22Business%22+and+document_type%3D%22article%22&begin_date=20070101&end_date=20141231&page={0}&api-key=8cbd506758608f03f71e955c07315a98%3A4%3A69419709'.format(page)
    call = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=%22United+States+Economy%22&fq=source%3A%22The+New+York+Times%22+and+news_desk%3A%22Business%22+and+document_type%3A%22article%22&begin_date={0}&end_date={1}&page={2}&api-key=8cbd506758608f03f71e955c07315a98%3A4%3A69419709'.format(begindate, enddate, page)
    command = 'wget -O log_api{0} \'{1}\''.format(page,call)
    # print command
    os.system(command)

    # find where the result was saved
    # log = open('log_api')
    # results_file = None
    # for line in log:
    #     matches = re.search('(\S+) saved', line)
    #     if matches:
    #         results_file = matches.group(1)
    #         results_file = results_file[1:-1]
    #         results_files.append(results_file)
    # log.close()
    # if results_file is None:
    #     print 'Can\'t find results filename'
    #     exit(1)
    results = open('log_api{0}'.format(page))
    for line in results:
        if npages < 0:
            matches = re.match('{"response":{"meta":{"hits":(\d+)', line)
            if matches:
                nhits = int(matches.group(1))
                npages = int(np.ceil(nhits/10.))
                print 'nhits: {0}, npages {1}'.format(nhits, npages)
                if npages > 100:
                    print 'Need to reduce the size of the query!'
                    exit(1)
            
    if npages < 0:
        print 'Can\'t determine number of pages...'
        exit(1)
    
    time.sleep(0.2)
    page += 1
    if page > npages:
        done = True

# log = open('log')
# for line in log:
#     matches = re.match('Saving to: `(\S+)\'', line)
#     if matches:
#         print 'found it! {0}'.format(matches.group(1))

# do something about the returned filename
# get number of articles
# loop over the rest of the pages
