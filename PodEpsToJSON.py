import json
import sqlite3
import urllib
from bs4 import BeautifulSoup
from datetime import datetime

conn = sqlite3.connect('pftcrawlerdb.sqlite')
cur = conn.cursor()

cur.execute('''
    SELECT  Podcasts.name, Appearances.episode, Appearances.title, Appearances.date, Appearances.link 
    FROM    Appearances 
    JOIN    Podcasts on Appearances.podcast_id = Podcasts.id''')
    
rows = cur.fetchall()

# name, ep#, title, date, link
# content = name + '-' + epidsode + '-' + title
# print rows

eps = []
data = {'episodes': eps}

# i = 1
for row in rows:
    content = str(row[0]) + '-' + str(row[1]) + '-' + (str(row[2])).strip()
    dateobj = datetime.strptime(str(row[3])[:10], '%Y-%m-%d')

#     start: new Date(2010, 7, 15),
#    datestr = 'new Date(%s, %s, %s)' % (str(dateobj.year), str(dateobj.month), str(dateobj.day))
    datestr = str(row[3])[:10]
    
    epdict = {}
    epdict = {'start': datestr, 'content' : content}
    eps.append(epdict)
#     i +=1

data = {'episodes': eps}


# write to json file
outfile = open('podeps.json', 'w')
outfile.truncate()
json.dump(eps, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
outfile.close()