#from bs4 import BeautifulSoup
import requests
import logging
import multiprocessing as mp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# class Legislation(object):
#
#     @staticmethod
def read_html(doc_code):
    print doc_code
    sector_id = '5'
    year = list(xrange(2015, 2017))
    for y in year:
        for doc_number in xrange(1000):
            doc_number = str(doc_number).zfill(4)
            doc_id = sector_id+str(y)+doc_code+ doc_number
            base_url = 'http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/'
            payload = {'uri': 'CELEX:'+doc_id}
            r = requests.get(base_url, params=payload)
            try:
                if r.status_code == 200:
                    with open('/Users/varun.kumar/trunk/intern_day/html_data/'+doc_id, 'w') as html_doc:
                        html_doc.write(r.text.encode('ascii', 'ignore'))
                else:
                    logger.info("Doc_id %s not found.", doc_id)
            except:
                logger.error("Exception in reading web page for %s", doc_id)


if __name__=='__main__':
    sector = [3, 4, 5]
    doc_type = {'3':['E', 'F', 'R', 'L', 'D', 'S', 'M', 'J', 'B', 'K', 'O', 'H', 'A', 'G', 'C', 'Q', 'X', 'Y'],
                '4' : ['A', 'D', 'X', 'Y'],
                '5' : ['AG', 'KG', 'IG', 'XG' 'PC', 'DC', 'JC', 'SC', 'EC', 'FC', 'GC', 'XC', 'AP', 'BP', 'IP',
                'DP', 'XP', 'AA', 'TA', 'SA', 'XA', 'AB', 'HB', 'XB', 'AE', 'IE', 'AC', 'XC', 'AR', 'IR', 'XR',
                'AK', 'XK', 'XX']}

    pool = mp.Pool(processes=6)
    pool.map(read_html, doc_type['5'])
    #Legislation.read_html(doc_id)


