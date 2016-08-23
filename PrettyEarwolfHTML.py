import urllib
from bs4 import BeautifulSoup

url = 'http://www.earwolf.com/person/paul-f-tompkins/'
html = urllib.urlopen(url).read()

soup = BeautifulSoup(html, 'lxml')

f = open('PrettyEarwolfHTML.html', 'w')

f.write(soup.prettify('utf-8', 'minimal'))
   # for line in soup.prettify('utf-8', 'minimal'):
#       f.write(str(line))

f.close()