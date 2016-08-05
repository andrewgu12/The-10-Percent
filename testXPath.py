import lxml.html
import requests
import json
import time
import sys


from PyPDF2 import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import PyPDF2
from urllib2 import Request, urlopen



start = time.time()


base_url = "http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52016PC0482&rid=1"


start1 = time.time()

response = requests.get(base_url)




page = lxml.html.fromstring(response.text)

list_items = page.xpath("//p[@class='Statut']")

statute = list_items[0].text

list_items = page.xpath("//p[@class='Typedudocument_cp']")
typeDoc = list_items[0].text


list_items = page.xpath("//p[@class='Titreobjet_cp']")

title = list_items[0].text

fullTitle = statute +' ' + typeDoc + ' ' + title
print(statute)
print(fullTitle)


