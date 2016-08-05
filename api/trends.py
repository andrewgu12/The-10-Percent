from elasticsearch import Elasticsearch
from collections import defaultdict
from scipy.stats.mstats import zscore


client = Elasticsearch([
    'http://fn-elasticsearch:mAS0vE8fyZbiycZ84HsFccwiuvk31s8Of7uU24I2JuKrTFnC2OmjTVAzzKuFcwxG@52.2.157.128:8080'])


class Trends(object):

    @staticmethod
    def build_sub_category_query(phrase):
        body = {
            "size" :10000,
            "query": {
                "multi_match" : {
                    "query":      phrase,
                    "type":       "phrase",
                    "fields":     [ "title", "description", "extracted_text" ]
                }
            },
            "_source": {
                "include": ["_id", "bill_action_dates.introduced", "bill_action_dates.first_action"]
            }
        }
        return body

    def search_es(self, key_phrase):
        response = client.search(
            index="bills",
            body=self.build_sub_category_query(key_phrase),
            request_timeout=500
        )

        year_bill_count_dict = defaultdict(int)
        for hit in response['hits']['hits']:
            bill = hit['_source']
            year = None
            if bill['bill_action_dates']['introduced']:
                year = int(bill['bill_action_dates']['introduced'].split('-')[0])
            elif bill['bill_action_dates']['first_action']:
                year = int(bill['bill_action_dates']['first_action'].split('-')[0])
            #else:
            #    print("No date information.")
            if year:
                year_bill_count_dict[year]+=1

        print("Keyphrase : %s, doc_count %i", key_phrase, sum(year_bill_count_dict.values()))
        return year_bill_count_dict

    def query(self, q):
        count_dict = self.search_es(key_phrase=q)
        years = count_dict.keys()
        counts = count_dict.values()
        z_normalized_counts = zscore(counts)
        z_normalized_dict = dict(zip(years, z_normalized_counts))
        return z_normalized_dict



