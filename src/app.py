from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}

class UserAPI(Resource):
    def get(self, id):
        pass

    def post(self, id):
        pass

#To verify if server is running
api.add_resource(HelloWorld,'/')
api.add_resource(UserAPI, '/chores/<int:id>', endpoint = 'user')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
