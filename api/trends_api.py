from flask import Flask
from flask_restful import Resource, Api
from es_query import search_es

app = Flask(__name__)
api = Api(app)


class TrendsApi(Resource):
    def get(self, phrase):
        result = search_es(q=phrase)
        return result

api.add_resource(TrendsApi, '/search/<string:phrase>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)