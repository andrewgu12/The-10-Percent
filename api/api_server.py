from flask import Flask, Response
from es_query import search_es
from lobbyist_query import search_issues
from comments_query import analyzeSentiment
from embedding import WordVectors
import json

app = Flask(__name__)

wv = WordVectors.load_model('/Users/varun.kumar/trunk/intern_day/w2v_eu/w2v_eu_model')

@app.route('/search_bills/<string:phrase>')
def api_es(phrase):
    bills_result = search_es(q=phrase)
    js = json.dumps(bills_result)
    return Response(js, status=200, mimetype='application/json')


@app.route('/search_issues/<string:issue>')
def api_lobbyiest(issue):
    issue_result = search_issues(q=issue)
    return Response(issue_result, status=200, mimetype='application/json')


@app.route('/bill_info/<string:bill_id>')
def api_bill_info(bill_id):
     bill_info = wv.get_bill_info(bill_id=bill_id)
     return Response(bill_info, status=200, mimetype='application/json')


@app.route('/comments/<string:celex>')
def api_comments(celex):
    bill_info = analyzeSentiment(celex=celex)
    return Response(bill_info, status=200, mimetype='application/json')

# class TrendsApi(Resource):
#     def get(self, phrase):
#         result = search_es(q=phrase)
#         return result
#
#
# class LobbyistApi(Resource):
#     def get(self, issue):
#         result = search_issues(q=issue)
#         return result

#api.add_resource(LobbyistApi, '/<string:issue>')
#api.add_resource(TrendsApi, '/search_bills/<string:phrase>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)