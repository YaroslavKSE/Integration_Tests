from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3


app = Flask(__name__)
api = Api(app)

data_storage = None

DB_NAME = 'online_users.db'


class UsersOnlineResource(Resource):
    @staticmethod
    def get():
        req_date = request.args.get('date')

        if not req_date:
            return {"error": "date parameter is required."}, 400

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT online_count FROM user_stats WHERE date=?", (req_date,))
        result = cursor.fetchone()
        conn.close()

        users_online = result[0] if result else None
        return {"usersOnline": users_online}, 200


api.add_resource(UsersOnlineResource, "/api/stats/users")

if __name__ == '__main__':
    app.run(debug=True)
