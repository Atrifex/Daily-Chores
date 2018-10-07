from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

class UserAPI(Resource):
    def get(self, id):
        pass

    def post(self, id):
        pass

api.add_resource(UserAPI, '/chores/<int:id>', endpoint = 'user')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
