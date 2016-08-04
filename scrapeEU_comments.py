import lxml.html
import requests
import json
import time
import sys


from PyPDF2 import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import PyPDF2

import docx

from urllib2 import Request, urlopen

from bs4 import BeautifulSoup

import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 

import wget

class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit() 


start = time.time()

filename = "eu_comment_data.json" 


base_url = "http://ec.europa.eu/europe2020/public-consultation/contributions/index_en.htm#top"
r = Render(base_url)  

result = r.frame.toHtml()
formatted_result = str(result.toAscii())

soup = BeautifulSoup(formatted_result, 'lxml')

table = soup.find('table', id ="rec-2012")

print(table)


start1 = time.time()

response = requests.get(base_url)

tree = html.fromstring(response.text)



end1 = time.time()



print('Got page: ' + str(end1 - start1))



print(filename)


all_publications = []

count = 0

full_pub_url = 'http://ec.europa.eu/'


for row in table.find_all('tr'):
    count += 1
    if count == 1:
        continue


    col = row.find_all('td')
    # print(col)
    name = col[0].string
    lang = col[1].string
    country = col[2].string
    typeOrg = col[3].string
    mainAreas = col[4].string
    fullContribLink = full_pub_url + col[5].find('a').get('href')


    print(fullContribLink)

    try:
        remoteFile = urlopen(Request(fullContribLink)).read()

    except:
        continue
    memoryFile = StringIO(remoteFile)

    try: #PDF DOC
        pdfReader = PdfFileReader(memoryFile)
        pdfAsString = ' '.join([pdfReader.getPage(pageNumber).extractText().replace('\n', ' ') for pageNumber in range(pdfReader.numPages)])

    except:
        continue
        # filename = wget.download(url)
        # doc = docx.Document(filename)
        # pdfAsString = ' '.join([paragraph.text for paragraph in doc.paragraphs])



    dictForThisComment = {'name' : name,
                        'lang' : lang,
                        'county' : country,
                        'typeOrg' : typeOrg,
                        'mainAreas' : mainAreas,
                        'full_publication_url' : fullContribLink,
                        'full_pdf' : pdfAsString}


    all_publications.append(dictForThisComment)
    # print(name)
    # print(lang)
    # print(country)
    # print(typeOrg)
    # print(mainAreas)
    # print(fullContribLink)

    # print(dictForThisComment)
    print(count)

print('THIS MANY DOCS: ' + str(len(all_publications)))
with open(filename, u'wb') as fp:
    fp.write(json.dumps(all_publications, indent=4, separators=(u', ', u':')))

