from flask import Flask
from flask_restful import Resource, Api
from lobbyist_query import search_issues

app = Flask(__name__)
api = Api(app)

#52010DC2020

class CommentApi(Resource):
   def get(self, celex):
       result = search_issues(celex = celex)
       return result

api.add_resource(LobbyistApi, '/<string:celex>')

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)