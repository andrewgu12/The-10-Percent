from gensim.models import Word2Vec
from six import iterkeys
import json

class WordVectors(object):

    def __init__(self, w2v_model=None):
        self.w2v_model = w2v_model

    @classmethod
    def load_model(cls, model_name):
        result = cls()
        result.w2v_model = Word2Vec.load(fname=model_name)
        return result

    def get_bill_info(self, bill_id, topn=10):
        us_bills = []
        eu_bills = []
        phrases = []
        bill_id = 'eu_'+bill_id
        try:
            result_set = self.w2v_model.most_similar(positive=[bill_id], topn=topn+100)
            for key, score in result_set:
                if 'bill_id' in key:
                    key = key.replace('bill_id_', '')
                    url = "https://app.fiscalnote.com/bills/"+ key
                    us_bills.append({"doc_id":key, "url":url})
                elif 'eu_' in key:
                    key = key.replace('eu_', '')
                    url = "http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:"+ key
                    eu_bills.append({"doc_id":key, "url":url})
                else:
                    phrases.append(key)
        except:
            print ("Exception in %s", bill_id)

        result_json = dict()
        result_json["us_bills"] = us_bills[:5]
        result_json["eu_bills"] = eu_bills[:5]
        result_json["phrases"] = phrases[:5]
        return json.dumps(result_json)


if __name__ == '__main__':
    print ()
    #Load a pre-trained model
    #print (wv.get_similar_phrases('freight_rail', topn=1000))
    #print (wv.get_related_phrases_for_a_bill('USB00184467'))




