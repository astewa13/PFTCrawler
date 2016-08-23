import json
import sqlite3
import urllib
from bs4 import BeautifulSoup
from datetime import datetime

conn = sqlite3.connect('pftcrawlerdb.sqlite')
cur = conn.cursor()

cur.execute('''
    SELECT  Podcasts.name, Appearances.episode, Appearances.title, Appearances.date, Appearances.link, Podcasts.id 
    FROM    Appearances 
    JOIN    Podcasts on Appearances.podcast_id = Podcasts.id''')
    
rows = cur.fetchall()

# name, ep#, title, date, link
# content = name + '-' + epidsode + '-' + title
# print rows

eps = []

for row in rows:
    label = str(row[0]) + '-' + str(row[1]) + '-' + (str(row[2])).strip()
    link = str(row[4])
    content = '<a href="' + link + '" target="_blank">' + label + '</a>'
    dateobj = datetime.strptime(str(row[3])[:10], '%Y-%m-%d')
    datestr = str(row[3])[:10]
    id = row[5]
    
    epdict = {}
    epdict = {'group': id, 'start': datestr, 'content' : content}
    eps.append(epdict)



# write to json file
outfile = open('podeps_links.json', 'w')
outfile.truncate()
json.dump(eps, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
outfile.close()