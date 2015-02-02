import os
import re
import time
import numpy as np

results_files = []

do_immigration = True
current_dir = '/Users/bauer/insight/teleborder/data/nytimes/immigration'

# begindate = '20050801'
# enddate = '20051231'

years = ['2001','2002','2003','2004','2005']
m1s = ['01','03','05','07','10']
m2s = ['02','04','07','09','12']
d1s = ['01','01','01','01','01']
d2s = ['28','30','31','30','31']

for year in years:
    for m1,m2,d1,d2 in zip(m1s,m2s,d1s,d2s):
        directory = year + m1
        begindate = year + m1 + d1
        enddate = year + m2 + d2
        
        os.mkdir(os.path.join(current_dir,directory))
        os.chdir(os.path.join(current_dir,directory))
        
        npages = -1
        done = False
        page = 0
        while not done:
        #    call = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=%22United+States+Economy%22&fq=source%3A%22The+New+York+Times%22+and+news_desk%3A%22Business%22+and+document_type%3D%22article%22&begin_date=20070101&end_date=20141231&page={0}&api-key=8cbd506758608f03f71e955c07315a98%3A4%3A69419709'.format(page)
            call = None
            if do_immigration:
                call = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=%22Immigration%22&fq=source%3A%22The+New+York+Times%22+and+news_desk%3A%22National%22+and+document_type%3A%22article%22&begin_date={0}&end_date={1}&page={2}&api-key=8cbd506758608f03f71e955c07315a98%3A4%3A69419709'.format(begindate, enddate, page)        
            else:
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
                        break
            
            if npages < 0:
                print 'Can\'t determine number of pages...'
                exit(1)
    
            time.sleep(0.2)
            page += 1
            if page > npages:
                done = True

