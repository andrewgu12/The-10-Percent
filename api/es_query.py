from elasticsearch import Elasticsearch
from collections import defaultdict
import re
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client = Elasticsearch()


def build_sub_category_query(phrase):
    body = {
        "size":500,
        "query": {
            "multi_match": {
                "query": phrase,
                "type":  "phrase",
                "fields": ["bill_text"]
            }
        },
        "_source": {
            "include": ["doc_id", "bill_text", "year"]
        }
    }
    return body


def get_title(text):
    title = ""
    text = text[:500]
    text = text.replace("\n", " ")
    chunks = re.split('; |\*', text)
    for ch in chunks:
        ch = ch.upper()
        if 'COUNCIL' in ch or 'COMMISSION' in ch:
            title = ch
            title = ' '.join(w for w in title.split(' ') if w.isalpha())
            return title.title()
    return title


def get_bill_object(bill):
    json_bill = dict()
    json_bill["doc_id"] = bill["doc_id"]
    json_bill["link"] = "http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:"+ bill["doc_id"]
    json_bill["title"] = get_title(bill['bill_text'])
    json_bill["year"] = bill["year"]
    return json_bill


def search_es(q, topn=10):

    response = client.search(
        index="eu",
        body=build_sub_category_query(q),
        request_timeout=50
    )

    results_set = dict()

    year_bill_count_dict = defaultdict(int)
    cnt = 0
    all_bills = []
    for hit in response['hits']['hits']:
        bill = hit['_source']
        year = bill['year']
        if cnt< topn:
            bill_json = get_bill_object(bill)
            if len(bill_json['title'])>5:
                all_bills.append(bill_json)
                cnt+=1
        if year:
            year_bill_count_dict[year]+=1

    if len(year_bill_count_dict)>0:
        logger.info("Keyphrase : %s, doc_count %i", q, sum(year_bill_count_dict.values()))
    else:
        logger.info("Failed to get bills for %s", q)
    #sort bills
    results_set["bills"] = sorted(all_bills, key = lambda x:x["year"], reverse=True)
    results_set["year_counts"] = year_bill_count_dict
    return results_set


if __name__ == '__main__':
    print search_es("oil")



