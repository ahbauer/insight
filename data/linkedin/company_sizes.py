import oauth2 as oauth
import httplib2
import time, os, simplejson, json
import re
import pymysql as mdb

##### set up linkedin api stuff

# Fill the keys and secrets you retrieved after registering your app
consumer_key      =   '77j34t97311rpq'
consumer_secret  =   'gIfJdqwggIXfO2aC'
user_token           =   '44d9230f-1322-4257-b957-2676632ac2bc'
user_secret          =   '24aa1638-3095-4522-bde5-4114e1753bcc'
 
# Use your API key and secret to instantiate consumer object
consumer = oauth.Consumer(consumer_key, consumer_secret)
 
# Use the consumer object to initialize the client object
client = oauth.Client(consumer)
 
# Use your developer token and secret to instantiate access token object
access_token = oauth.Token(
            key=user_token,
            secret=user_secret)
 
client = oauth.Client(consumer, access_token)

####### end linkedin setup

# read in the geographic codes
geography = {}
states = {}
glc_file = open('../glc/glc_codes.csv')
for line in glc_file:
    sline = line.split(',')
    if sline[0] == 'For Official Use Only':
        continue
    state_long = sline[1].lower()
    state_short = sline[2].lower()
    city = sline[4].lower()
    code = int(sline[6])
    if state_long not in geography:
        geography[state_long] = {}
    geography[state_long][city] = code
    if state_short not in geography:
        geography[state_short] = {}
    geography[state_short][city] = code
    states[state_long] = state_short

# get the companies from the DB
company_sizes = {}
size_codes = {'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8}
con = mdb.connect('localhost', 'anne', '', 'teleborder')
cur = con.cursor()
cur.execute('select lca_case_employer_name,lca_case_employer_city,lca_case_employer_state from H1B;')
cur_results = {}
nresults = 0
for result in cur:
    nresults += 1
    [lca_company_name,city,state] = result[0:3]
    name = lca_company_name.lower()
    city = city.lower()
    state = state.lower()
    cur_results[name] = {}
    cur_results[name]['city'] = city
    cur_results[name]['state'] = state
    nresults += 1
print '{0} unique company names out of {1} DB entries'.format(len(cur_results.keys()),nresults)
for name in cur_results.keys():
    city = cur_results[name]['city']
    state = cur_results[name]['state']
    if state in geography:
        #print 'Found the state {0}'.format(state)
        state_short = state
        if state in states:
            state_short = states[state]
        if city in geography[state]:
            #print 'Found the city {0}'.format(city)
            name = name.replace('&', ' and ')
            name = re.sub(r'\W +', ' ', name)
            #print 'Looking for company {0}'.format(name)
            # ask linkedin for the size
            #resp,content = client.request('https://api.linkedin.com/v1/company-search?format=json&facet=location,us:{0}&keywords={1}'.format(geography[state][city],name), "GET", "")
            resp,content = client.request('https://api.linkedin.com/v1/company-search:(companies:(id,name,universal-name,employee-count-range,locations))?format=json&country_code=us&state_code={0}&keywords={1}&sort=company-size'.format(state_short,name), "GET", "")
            time.sleep(0.2)
            # print 'resp:'
            # print resp
            # print '\ncontent:'
            content = json.loads(content)
            try:
                ncompanies = content["companies"]["_total"]
            except:
                print 'PROBLEM!'
                print content
                exit(1)
            if ncompanies == 0:
                print 'No matches for {0}'.format(name)
                continue
            #print content
            #print len(content["values"])
            for company in content["companies"]["values"]:
                score=0
                #print company['name']
                # parse the content to get the most character matches (ignore whitespace) in both name and universal name
                #name_parts = name.split()
                name_parts = re.compile(r'[^A-Z^a-z]+').split(name)
                for part in name_parts:
                    if not part:
                        continue
                    if re.search(part,company['name'].lower()):
                        score += 1
                    if re.search(part,company['universalName'].lower()):
                        score += 1
                company['score'] = score
            company = sorted(content["companies"]["values"], key=lambda k: k['score'], reverse=True)[0]
            if company['score'] == 0:
                print 'No good name matches for {0}'
                continue
            else:
                try:
                    print '{0} best match: {1}, size category: {2}'.format(name, company['name'],size_codes[company['employeeCountRange']['code']])
                    company_sizes[lca_company_name] = size_codes[company['employeeCountRange']['code']]
                except:
                    continue
                    #print 'Problem... no company size for best match {0}'.format(company['name'])

print 'Matched {0} out of {1} companies'.format(len(company_sizes.keys()),len(cur_results.keys()))
with open('company_sizes.txt', 'w') as outfile:
    json.dump(company_sizes, outfile)

