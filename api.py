from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
import datetime

app = Flask(__name__)
api = Api(app)

data_storage = None

DB_NAME = 'online_users.db'


def str_to_datetime(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')


# Calculate the difference in seconds between two datetimes
def time_difference(date1, date2):
    return abs((date1 - date2).total_seconds())


class UsersOnlineResource(Resource):
    @staticmethod
    def get():
        req_date = request.args.get('date')
        user_id = request.args.get('userId')

        if not req_date:
            return {"error": "date parameter is required."}, 400

        if req_date and not user_id:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT online_count FROM user_stats WHERE date=?", (req_date,))
            result = cursor.fetchone()
            conn.close()

            users_online = result[0] if result else None
            return {"usersOnline": users_online}, 200

        if req_date and user_id:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT isOnline, currentOnlineTime, lastSeenDate FROM individual_user_stats WHERE userId=?",
                           (user_id,))
            result = cursor.fetchone()
            conn.close()

            if not result:
                return {"error": "User not found."}, 404

            is_online, current_online_time, last_seen_date = result

            if is_online and current_online_time == req_date:
                return {"wasUserOnline": True, "nearestOnlineTime": None}, 200

            if not is_online and last_seen_date != "":
                return {"wasUserOnline": False, "nearestOnlineTime": last_seen_date}, 200

            else:
                return {"wasUserOnline": False, "nearestOnlineTime": None}, 200


api.add_resource(UsersOnlineResource, "/api/stats/users")


class UserPredictionResource(Resource):
    @staticmethod
    def get():
        req_date = request.args.get('date')
        if not req_date:
            return {"error": "Date parameter is required."}, 400

        req_datetime = datetime.datetime.strptime(req_date, '%Y-%m-%dT%H:%M:%S')
        day_of_week = req_datetime.day
        hour = req_datetime.hour

        # Query the database for historical data for the given day and hour
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        day_str = req_datetime.strftime('%d')
        hour_str = req_datetime.strftime('%H')

        # Construct and execute the SQL query
        cursor.execute('''SELECT online_count FROM user_stats
                          WHERE strftime('%d', date) = ? AND strftime('%H', date) = ?''',
                       (day_str, hour_str))

        online_counts = [row[0] for row in cursor.fetchall()]

        # Calculate the average
        if not online_counts:
            return {"onlineUsers": 0}, 200

        avg_online_users = sum(online_counts) / len(online_counts)

        return {"onlineUsers": round(avg_online_users)}, 200


api.add_resource(UserPredictionResource, "/api/predictions/users")

if __name__ == '__main__':
    app.run(debug=True)
