from flask import Flask
from flask_restful import Resource, Api, reqparse
from update_chores import DatabaseManager
from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)
api = Api(app)

class Chores(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('identifier')
        parser.add_argument('username')

        args = parser.parse_args()
        print(args)

        db = DatabaseManager()
        return db.update_chore(args["identifier"], args["username"])

api.add_resource(Chores, '/chores')

#Health checks
health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
