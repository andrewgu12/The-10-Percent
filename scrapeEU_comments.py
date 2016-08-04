import lxml.html
import requests
import json
import time
import sys


from PyPDF2 import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import PyPDF2
from urllib2 import Request, urlopen

from bs4 import BeautifulSoup


start = time.time()

base_url = "https://ec.europa.eu/transparency/regdoc/?fuseaction=list&n=10&adv=0&coteId=&year=&number=&version=F&dateFrom=&dateTo=&serviceId=&documentType=&title=&titleLanguage=&titleSearch=EXACT&sortBy=NUMBER&sortOrder=DESC&p=%s&"
# base_url = "https://www.cbo.gov/cost-estimates?search_api_views_fulltext=&field_congressionalsession=%s&page=%s"
publication_url = "https://www.cbo.gov"
# These are hard coded from looking at the website, change them for other sessions
start_page = 1
max_page = 63137

filename = "eu_data.json" 

print(filename)


all_publications = []

count = 0

for page_num in xrange(start_page, max_page):

    start1 = time.time()
    print "Scraping Index Page %s" % page_num

    page_url = base_url % (page_num)
    print(page_url)
    response = requests.get(page_url)
    if response.status_code != 200:
        print "Failed to get page %s -- status code %s" % (page_url, response.status_code)

    end1 = time.time()



    print('Got page: ' + str(end1 - start1))

    soup = BeautifulSoup(response.text, 'lxml')
    # table = soup.find(class_='tableFile2')



    page = lxml.html.fromstring(response.text)


    soup = BeautifulSoup(response.text, 'lxml')

    table = soup.find('table', id ='searchList')

    tableCount = 0

    for row in table.find_all('tr'):
        col = row.find_all('td')

        print(col)

        if col == []:
            continue


        if tableCount % 2 == 0: #FIRST ROW FOR THIS DOC

            doc_ref_number = col[0].b.string.strip()


            responsible_dg = col[1].string.strip()

            date = col[2].string.strip()

            print(doc_ref_number)
            print(responsible_dg)
            print(date)

        else:
            print(col)
            description = col[0].string.strip()
            print(col[1].find('a').get('href'))
            full_document_link = col[1].find('a').get('href')
            print(description)
            print('PDF:' + full_document_link)
            # sys.exit(0)


        if tableCount == 10:
            sys.exit(0)

        tableCount += 1



    list_items = page.xpath("//div[@class='item-list cost-estimates-search']/ol/li")
    for item in list_items:


        try:
            # copy the fields on the list pages
            # try:


            title = item.xpath("div[@class='views-field views-field-title']")[0].text_content()
            # except:
            #     title = ''
            # try:
            analysis_type = item.xpath("span[@class='views-field views-field-type']")[0].text_content()
            # except:
            #     analysis_type = ''
            # try:
            short_summary = item.xpath("div[@class='views-field views-field-search-api-excerpt']")[0].text_content()

            date = item.xpath("span[@class='views-field views-field-field-display-date']")[0].text_content()


            # except:
            #     short_summary = ''
            # try:
            full_publication_url =  publication_url + item.xpath("div[@class='views-field views-field-title']/h3/a")[0].attrib["href"]

            # print(full_publication_url)
            # sys.exit(0)
            # except:
            #     full_publication_url = ''

            # access the publication page
            publication_page_obj = lxml.html.fromstring(requests.get(full_publication_url).text)
            # grab the full summary
            # try:
            full_summary = publication_page_obj.xpath("//div[@class='field field-name-body field-type-text-with-summary field-label-hidden']")[0].text_content()
            # except:
            #     full_summary = ''
            # grab the url to the full page
            # print(publication_page_obj.xpath("//a[@class='read-complete-document']"))

        except:
            continue




        try:
            full_document_link = publication_page_obj.xpath("//a[@class='read-complete-document']")[0].attrib["href"]

            remoteFile = urlopen(Request(full_document_link)).read()
            memoryFile = StringIO(remoteFile)
            pdfReader = PdfFileReader(memoryFile)


            pdfAsString = ' '.join([pdfReader.getPage(pageNumber).extractText().replace('\n', ' ') for pageNumber in range(pdfReader.numPages)])
        
        except:
            continue

        publication = {
            "title": title,
            "analysis_type": analysis_type,
            "short_summary": short_summary,
            "publication_url": full_publication_url,
            "full_summary": full_summary,
            "full_document_link": full_document_link,
            "full_pdf": pdfAsString,
            "date" : date
        }
        all_publications.append(publication)
        count = count + 1

    end2 = time.time()

    print('Parsed page: ' + str(end2 - end1))

    print('Total : ' + str(end2 - start))
        # print(publication)
    #     # break


    with open(filename, u'wb') as fp:
        fp.write(json.dumps(all_publications, indent=4, separators=(u', ', u':')))


    # with open(filename, "w+") as fwriter:
    #     json.dump(all_publications, fwriter)

    print('GOT THIS MANY DOCUMENTS: ' + str(count))
    
