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

        if len(user_id) != 36:
            return {"error": "User not found."}, 404

        if req_date and user_id:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''SELECT start_time, end_time FROM individual_user_online_spans 
                                      WHERE userId = ? 
                                      ORDER BY ABS(julianday(start_time) - julianday(?))''',
                           (user_id, req_date))
            nearest_time = cursor.fetchone()
            conn.close()

            if nearest_time:
                start_time, end_time = nearest_time
                # Check which one is closer: start_time or end_time
                nearest_online_time = min([time for time in [start_time, end_time] if time],
                                          key=lambda d: abs(str_to_datetime(d) - str_to_datetime(req_date)))
                if end_time is not None:
                    if start_time <= req_date <= end_time:
                        return {"wasUserOnline": True, "nearestOnlineTime": None}, 200
                    if req_date > end_time:
                        return {"wasUserOnline": False, "nearestOnlineTime": nearest_online_time}, 200
                elif end_time is None and start_time <= req_date:
                    return {"wasUserOnline": True, "nearestOnlineTime": None}, 200
                else:
                    return {"wasUserOnline": False, "nearestOnlineTime": None}, 200
            else:
                nearest_online_time = None
                return {"wasUserOnline": False, "nearestOnlineTime": nearest_online_time}, 200


api.add_resource(UsersOnlineResource, "/api/stats/users")


class UserPredictionResource(Resource):
    @staticmethod
    def get():
        req_date = request.args.get('date')
        if not req_date:
            return {"error": "Date parameter is required."}, 400

        req_datetime = datetime.datetime.strptime(req_date, '%Y-%m-%dT%H:%M:%S')

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
