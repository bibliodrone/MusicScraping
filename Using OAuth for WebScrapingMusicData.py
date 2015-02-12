
# coding: utf-8

# In[ ]:

#!/usr/bin/env python
#
# WebScrapingMusicData--Using OAuth
# Gerald Walden
# Harvard University Library, Information and Technical Services
# 
# (planned)  Expects a pre-created .csv file created from Aleph stub records
# (planned)  Parses .csv data fields to form queries to pass to the Discogs API, to be searched against the Discogs database.
# (underway) Completes an OAuth request against the discogs.com API. 
# 
#
import json
import sys
import urlparse

import oauth2 as oauth

# See http://www.discogs.com/settings/developers . Consumer key and consumer secret credentials
# are assigned to each unique application and remain static for its lifetime.
# the consumer details below were generated for the 'WebScrapingMusicData' application.
consumer_key = 'rkxdPYDwoSWoNlsIKTPw'
consumer_secret = 'ENaFePmBDFFOULwdcBIEZlSwboJptbSY'

# oauth end-points are defined by discogs.com staff. These static endpoints
# are called at various stages of oauth handshaking.
request_token_url = 'https://api.discogs.com/oauth/request_token'
authorize_url = 'https://www.discogs.com/oauth/authorize'
access_token_url = 'https://api.discogs.com/oauth/access_token'

# A unique user-agent is required with Discogs API requests
user_agent = 'M3taData'


# In[ ]:

# create oauth Consumer and Client objects using
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

# pass in your consumer key and secret to the token request URL. Discogs returns
# an ouath_request_token as well as an oauth request_token secret.
resp, content = client.request(request_token_url, 'POST', headers={'User-Agent': user_agent})

# Discogs api should return HTTP 200 OK. If not, there was an error and the program terminates.
if resp['status'] != '200':
    sys.exit('Invalid response {0}.'.format(resp['status']))

request_token = dict(urlparse.parse_qsl(content))

print ' == Request Token == '
print '    * oauth_token        = {0}'.format(request_token['oauth_token'])
print '    * oauth_token_secret = {0}'.format(request_token['oauth_token_secret'])
print

# Authorize our newly received request_token against the discogs oauth endpoint.
# Program prompts the user to "accept" the terms of the application. They are asked to navigate 
# to a url formed from the oauth token.
# 
# If the user accepts, discogs displays a key to the user that is used for
# verification. The key is required in the 2nd phase of authentication. Phew! But, it is more secure...
print 'Please browse to the following URL {0}?oauth_token={1}'.format(
        authorize_url, request_token['oauth_token'])

# Waiting for user input
accepted = 'n'
while accepted.lower() == 'n':
    print
    accepted = raw_input('Have you received your Verification code from {0}?oauth_token={1} [y/n] :'.format(
        authorize_url, request_token['oauth_token']))

# request the verification token from the user.
oauth_verifier = raw_input('Verification code :')

# Generate objects that pass the verification key with the oauth token and oauth
# secret to the discogs access_token_url
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, 'POST', headers={'User-Agent': user_agent})


# In[ ]:

# if verification is successful, the discogs oauth API will return an access token
# and access token secret. The oauth_token_secret should be saved to disk, to a database or some
# other local store. All further requests to the discogs.com API that require authentication
# and must be made with these access_tokens.
access_token = dict(urlparse.parse_qsl(content))

print ' == Access Token =='
print '    * oauth_token        = {0}'.format(access_token['oauth_token'])
print '    * oauth_token_secret = {0}'.format(access_token['oauth_token_secret'])
print ' Authentication complete. Future requests must be signed with the above tokens.'
print


# In[ ]:

# Now try a request to verify that everything's working
token = oauth.Token(key=access_token['oauth_token'],
        secret=access_token['oauth_token_secret'])
client = oauth.Client(consumer, token)
resp, content = client.request('https://api.discogs.com', 
        headers={'User-Agent': user_agent})

print ' == Authenticated API request =='
print '    * response status      = {0}'.format(resp['status'])
#print '    * saving image to disk = R-40522-1098545214.jpg'
pageResponse = json.loads(content)
print pageResponse


# In[2]:

# With an active auth token, we're able to reuse the client object and request 
# additional discogs authenticated endpoints, such as database search.
resp, content = client.request('https://api.discogs.com/database/search?release_title=House+For+All&artist=Blunted+Dummies',
        headers={'User-Agent': user_agent})

if resp['status'] != '200':
    sys.exit('Invalid API response {0}.'.format(resp['status']))

releases = json.loads(content)
print '\n== Search results for release_title=House For All, Artist=Blunted Dummies =='
for release in releases['results']:
    print '\n\t== discogs-id {id} =='.format(id=release['id'])
    print u'\tTitle\t: {title}'.format(title=release.get('title', 'Unknown'))
    print u'\tYear\t: {year}'.format(year=release.get('year', 'Unknown'))
    print u'\tLabels\t: {label}'.format(label=', '.join(release.get('label',
                 ['Unknown'])))
    print u'\tCat No\t: {catno}'.format(catno=release.get('catno', 'Unknown'))
    print u'\tFormats\t: {fmt}'.format(fmt=', '.join(release.get('format',
                 ['Unknown']))) 


# In[ ]:



