import json
import sqlite3
import urllib
from bs4 import BeautifulSoup
from datetime import datetime

conn = sqlite3.connect('pftcrawlerdb.sqlite')
cur = conn.cursor()

cur.execute('''
    SELECT  Podcasts.id, Podcasts.name
    FROM    Podcasts
    ORDER BY Podcasts.name''')
    
rows = cur.fetchall()

shows = []

for row in rows:
    id = row[0]
    content = row[1]
    epdict = {}
    epdict = {'id': id, 'content' : content}
    shows.append(epdict)

# write to json file
outfile = open('groups.json', 'w')
outfile.truncate()
json.dump(shows, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
outfile.close()