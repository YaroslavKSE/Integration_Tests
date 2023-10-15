from flask import request
from flask_restful import Resource
from sql_db_models.setup_database import DB_NAME

import datetime
import sqlite3


class UserPredictionResource(Resource):
    @staticmethod
    def get():
        req_date = request.args.get('date')
        tolerance = float(request.args.get('tolerance', '0'))  # Default to 0 if not provided
        user_id = request.args.get('userId')
        if not req_date:
            return {"error": "Date parameter is required."}, 400

        if req_date and not tolerance and not user_id:
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
            conn.close()
            # Calculate the average
            if not online_counts:
                return {"onlineUsers": None}, 200

            avg_online_users = sum(online_counts) / len(online_counts)

            return {"onlineUsers": round(avg_online_users)}, 200

        if req_date and tolerance and user_id:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            req_datetime = datetime.datetime.strptime(req_date, '%Y-%m-%dT%H:%M:%S')
            # This gives a string representation of the day of the week (0 for Sunday, 1 for Monday, etc.)
            day_of_week = req_datetime.strftime('%w')
            hour_minute = req_datetime.strftime('%H:%M')

            # Fetch number of times user was online at the same weekday and time
            cursor.execute('''SELECT COUNT(*) FROM individual_user_online_spans 
                              WHERE userId = ? AND 
                                    strftime('%w', start_time) = ? AND 
                                    strftime('%H:%M', start_time) = ?''',
                           (user_id, day_of_week, hour_minute))

            times_online_at_this_time = cursor.fetchone()[0]

            # Fetch total weeks of data for this user
            cursor.execute('''SELECT COUNT(DISTINCT strftime('%Y-%W', start_time)) 
                                      FROM individual_user_online_spans WHERE userId = ?''', (user_id,))

            total_weeks = cursor.fetchone()[0]
            conn.close()
            if total_weeks == 0:  # Avoid division by zero
                return {"error": "No historical data available for this user."}, 404

            online_chance = times_online_at_this_time / total_weeks

            return {
                       "willBeOnline": online_chance >= tolerance,
                       "onlineChance": online_chance
                   }, 200
