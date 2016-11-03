from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import glob 
import json

es = Elasticsearch()

INDEX_NAME = "eu"
TYPE_NAME = "bill"
if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))

print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME)
print(" response: '%s'" % (res))

class Doc(object):
    
    def __init__(self, doc_id, year, sector, doc_type, bill_text):
        self.doc_id = doc_id
        self.year = year
        self.sector = sector 
        self.doc_type = doc_type
        self.bill_text = bill_text
    
    def get(self):
        doc_json = {}
        doc_json['doc_id'] = self.doc_id
        doc_json['year'] = self.year
        doc_json['sector'] = self.sector
        doc_json['doc_type'] = self.doc_type
        doc_json['bill_text'] = self.bill_text
        return json.dumps(doc_json, ensure_ascii=False)

def doc_iter():
    """
    Dump all bills from "eu_html_data" folder to elasticsearch. 
    "eu_html_data" folder contains html documents. Generated using 
    https://github.com/andrewgu12/The-10-Percent/blob/master/scraper.py
    
    """
    for d in glob.glob('eu_html_data/*'):
        doc_id = d.split('/')[-1]
        sector = int(doc_id[0])
        year = int(doc_id[1:5])
        doc_type = doc_id[5:].replace(doc_id[-4:], '')
        html_doc = open(d, 'r').read()
        soup = BeautifulSoup(html_doc, "lxml")
        bill_text = soup.text
        doc = Doc(doc_id=doc_id, sector=sector, year=year, doc_type=doc_type, bill_text=bill_text)
        yield doc
        
if __name__ == '__main__':
    bulk_data = [] 
    doc_count = 0
    for doc in doc_iter():
        op_dict = {
            "index": {
                "_index": INDEX_NAME, 
                "_type": TYPE_NAME, 
                "_id": doc.doc_id
            }
        }
        bulk_data.append(op_dict)
        bulk_data.append(doc.get())
        doc_count+=1
        if doc_count % 1000 ==0:
            res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)
            print ('Indexing.. %i', doc_count)
            bulk_data = []

    res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)  
