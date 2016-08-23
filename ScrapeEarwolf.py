import sqlite3
import urllib
from bs4 import BeautifulSoup
from datetime import datetime

conn = sqlite3.connect('pftcrawlerdb.sqlite')
cur = conn.cursor()

# Setup database
cur.executescript('''
DROP TABLE IF EXISTS Podcasts;
DROP TABLE IF EXISTS Appearances;

CREATE TABLE Podcasts (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Appearances (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    podcast_id  INTEGER,
    episode     INTEGER,
    title       STRING,
    date        DATETIME,
    link        TEXT UNIQUE)
''')

url = raw_input('Enter - ')
if len(url) == 0 : url = 'http://www.earwolf.com/person/paul-f-tompkins/'
html = urllib.urlopen(url).read()

soup = BeautifulSoup(html, 'lxml')

divTags = soup("div", {"class":"ep-description"})

# comment out when not debugging
# i = int(raw_input('Enter iterations to run: '))

for dtag in divTags:
    
    # comment out when not debugging
    # if i == 0: break
    # i -= 1
    
    # clear title and link list vars
    eptitle = ''
    eplink = ''
    podcast = ''
    epnum = ''
    epdatestr = ''
    epdate = datetime
    
    # get ep title
    eptitle = (dtag.parent.h1.text).replace(':', ' - ')
    
    # get ep link
    eplink = dtag.a.get('href', None)
    
    # parse text in span texts to a list & convert to ascii
    spanTags = dtag.find_all('span')
    tagTexts = []
    for tag in spanTags : tagTexts.append((tag.text).encode('ascii', 'ignore'))
    
    # get podcast name
    podcast = tagTexts[0].split('#')[0].strip()
    
    # get episode number
    epnum = tagTexts[0].split('#')[1].strip()
    
    # get episode date or assign earliest date if date string not parsable
    epdatestr = tagTexts[1].strip()
    try:
        epdate = datetime.strptime(epdatestr, '%B %d, %Y')
    except:
        epdate = datetime.min
    
    # write values to database    
    cur.execute('''INSERT OR IGNORE INTO Podcasts (name) 
        VALUES ( ? )''', ( podcast, ) )
    
    cur.execute('SELECT id FROM Podcasts WHERE name = ? ', (podcast, ))
    pod_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Appearances
        (podcast_id, episode, title, date, link) VALUES ( ?, ?, ?, ?, ? )''', 
        ( pod_id, epnum, eptitle, epdate, eplink ) )

conn.commit()
    
    
    
#     print alleps
# 
#     
# if len(titleerror) != 0: print 'There were title errors: ', titleerror
#     
# if len(linkerror) != 0: print 'There were link errors: ', linkerror
# 
# 
# for key, value in alleps.items(): print value[0]

    
    

