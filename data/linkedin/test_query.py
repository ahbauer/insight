import oauth2 as oauth
import httplib2
import time, os, simplejson
 
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
 
# Make call to LinkedIn to retrieve your own profile
# By default, the LinkedIn API responses are in XML format. If you prefer JSON, simply specify the format in your call
#resp,content = client.request("https://api.linkedin.com/v1/people/~?format=json", "GET", "")

company_name = "EYE SPECIALISTS OF INDIANA"
resp,content = client.request('https://api.linkedin.com/v1/company-search?format=json&country-code=us&keywords={0}'.format(company_name), "GET", "")
print 'resp:'
print resp

print '\ncontent:'
print content