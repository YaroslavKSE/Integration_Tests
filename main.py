from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import unittest

app = Flask(__name__)
api = Api(app)

# Sample data
users_data = {
    "total": 217,
    "data": [
        {
            "userId": "8b0b5db6-19d6-d777-575e-915c2a77959a",
            "nickname": "Nathaniel6",
            "firstName": "Nathaniel",
            "lastName": "Murphy",
            "registrationDate": "2023-09-19T08:48:06.5731641+00:00",
            "lastSeenDate": "null",
            "isOnline": True
        },
        {
            "userId": "e13412b2-fe46-7149-6593-e47043f39c91",
            "nickname": "Terry_Weber",
            "firstName": "Terry",
            "lastName": "Weber",
            "registrationDate": "2022-10-24T17:46:53.1388008+00:00",
            "lastSeenDate": "2023-09-30T13:12:08.9408478+00:00",
            "isOnline": False
        },
        {
            "userId": "cbf0d80b-8532-070b-0df6-a0279e65d0b2",
            "nickname": "Willard66",
            "firstName": "Willard",
            "lastName": "Treutel",
            "registrationDate": "2023-05-04T23:29:34.6069562+00:00",
            "lastSeenDate": "2023-09-30T13:09:48.9229466+00:00",
            "isOnline": False
        },
        {
            "userId": "de5b8815-1689-7c78-44e1-33375e7e2931",
            "nickname": "Nick37",
            "firstName": "Nick",
            "lastName": "Boyle",
            "registrationDate": "2023-08-08T07:18:54.3367009+00:00",
            "lastSeenDate": "null",
            "isOnline": True
        },
        {
            "userId": "e31e41f4-4992-cd5d-def4-4c79f86bb0e1",
            "nickname": "Jerry_Adams6",
            "firstName": "Jerry",
            "lastName": "Adams",
            "registrationDate": "2022-09-24T15:33:18.0113307+00:00",
            "lastSeenDate": "2023-09-30T12:51:48.7659228+00:00",
            "isOnline": "null"
        },
        {
            "userId": "908dcb71-beeb-57c4-72f6-50451a6c3d12",
            "nickname": "Leticia.Pagac",
            "firstName": "Leticia",
            "lastName": "Pagac",
            "registrationDate": "2022-09-29T23:41:42.1597638+00:00",
            "lastSeenDate": "null",
            "isOnline": True
        },
        {
            "userId": "5ed4eae5-d93c-6b18-be47-93a787c73bcb",
            "nickname": "Myrtle27",
            "firstName": "Myrtle",
            "lastName": "Ernser",
            "registrationDate": "2022-11-19T06:54:20.5472617+00:00",
            "lastSeenDate": "2023-09-30T12:54:48.7930216+00:00",
            "isOnline": False
        },
        {
            "userId": "3f9747d7-d084-7db4-5226-220085e07b54",
            "nickname": "Erik_Abshire",
            "firstName": "Erik",
            "lastName": "Abshire",
            "registrationDate": "2023-03-20T00:31:49.2624028+00:00",
            "lastSeenDate": "2023-09-30T13:09:28.9201821+00:00",
            "isOnline": False
        },
        {
            "userId": "05227367-07f0-b3a5-8345-2513e0c45cca",
            "nickname": "Robin.Herman70",
            "firstName": "Robin",
            "lastName": "Herman",
            "registrationDate": "2023-02-04T07:08:53.4751734+00:00",
            "lastSeenDate": "2023-09-30T13:13:28.9495739+00:00",
            "isOnline": False
        },
        {
            "userId": "938a6656-0b54-6a9c-76a2-bbfac8f3de81",
            "nickname": "Karl94",
            "firstName": "Karl",
            "lastName": "Emard",
            "registrationDate": "2023-02-09T03:38:52.5794963+00:00",
            "lastSeenDate": "null",
            "isOnline": False
        }
    ]
}


class UsersOnlineResource(Resource):
    @staticmethod
    def get():
        # Parse the 'date' query parameter
        req_date = request.args.get('date')

        if not req_date:
            return {"error": "date parameter is required."}, 400

        # Count users that were online at the given date
        users_online = 0
        for user in users_data["data"]:
            if user["isOnline"]:
                users_online += 1

        if users_online == 0:
            return {"usersOnline": None}, 200

        return {"usersOnline": users_online}, 200


class TestUsersOnlineResource(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_valid_request(self):
        pass

    def test_missing_date(self):
        pass


# Add the resource to the API
api.add_resource(UsersOnlineResource, "/api/stats/users")

if __name__ == '__main__':
    app.run(debug=True)
