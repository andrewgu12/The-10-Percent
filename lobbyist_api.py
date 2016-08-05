from flask import Flask
from flask_restful import Resource, Api
from lobbyist_query import search_issues

app = Flask(__name__)
api = Api(app)


class LobbyistApi(Resource):
   def get(self, issue):
       result = search_issues(q = issue)
       return result

api.add_resource(LobbyistApi, '/<string:issue>')

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)