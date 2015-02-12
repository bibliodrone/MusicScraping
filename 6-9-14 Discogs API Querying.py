# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import sys
import csv
import requests
import time
import bs4
import re
from bs4 import BeautifulSoup
import discogs_client as discogs

# <codecell>

reload (sys)
sys.setdefaultencoding('utf-8')

# <codecell>

discogs.user_agent = 'bibliodrone/0.1 +http://harvard.edu'

# <codecell>

with open('brief_recs_sample.csv', 'Ur') as f:
    data = list(tuple(rec) for rec in csv.reader(f, delimiter=',')) #make sure 'brief_recs_sample.csv' is in the correct directory!
    
lengthOfList = len(data)

# <codecell>

for x in range(1, lengthOfList/10): ##Titles from the .csv file
    print data[x][4]
    

# <codecell>

#Search by title ie. release
for x in range(1, lengthOfList/10): #start range index at 1 instead of 0 to omit the TITLE_DISPLAY heading.
    #query = data[x][4].replace(' [sound recording]', '').replace(' [videorecording]', '') #can add the 'replace' function right on to the String variable declaration
    query = data[x][4]
    s = discogs.Search(query)
    time.sleep(1) ## API throttle = 1 second
    print
    print query + ' ...searching'
    try:
            data = s.results
            print data
            #print s.results()[0].data['year'] #could append all this data into another list?
            #print s.results()[0].data['id']
            #print s.results()[0].data['genres']

    except discogs.DiscogsAPIError:
        print '    *Search returned an error*'

# <codecell>


