from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from multiprocessing import Manager

app = Flask(__name__)
api = Api(app)

manager = Manager()
data_storage = manager.dict()


class UsersOnlineResource(Resource):
    @staticmethod
    def get():
        req_date = request.args.get('date')

        if not req_date:
            return {"error": "date parameter is required."}, 400

        users_online = data_storage.get(req_date, None)
        return {"usersOnline": users_online}, 200


api.add_resource(UsersOnlineResource, "/api/stats/users")

if __name__ == '__main__':
    app.run(debug=True)
