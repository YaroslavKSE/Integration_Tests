from flask import request
from flask_restful import Resource
from sql_db_models.setup_database import DB_NAME

import sqlite3


class UsersTotalResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get("userId")
        average_required = request.args.get("averageRequired")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if not user_id:
            return {"error": "userId parameter is required"}, 404

        if user_id and average_required != 'true':
            cursor.execute(
                "SELECT SUM(strftime('%s', COALESCE(end_time, datetime('now'))) - strftime('%s', start_time)) "
                "FROM individual_user_online_spans WHERE userId = ?", (user_id,))

            result = cursor.fetchone()
            total_time_in_seconds = result[0] if result else None
            return {"totalTime": total_time_in_seconds}

        if user_id and average_required == 'true':
            cursor.execute('''SELECT SUM(strftime('%s', COALESCE(end_time, datetime('now'))) - strftime('%s', start_time)) 
                                  FROM individual_user_online_spans 
                                  WHERE userId = ?''', (user_id,))
            total_seconds = cursor.fetchone()[0] or 0

            # Total unique days online
            cursor.execute('''SELECT COUNT(DISTINCT date(start_time)) 
                                  FROM individual_user_online_spans 
                                  WHERE userId = ?''', (user_id,))
            total_days = cursor.fetchone()[0] or 0

            # Total unique weeks online
            cursor.execute('''SELECT COUNT(DISTINCT strftime('%Y', start_time) || strftime('%W', start_time)) 
                                  FROM individual_user_online_spans 
                                  WHERE userId = ?''', (user_id,))

            total_weeks = cursor.fetchone()[0] or 0

            day_average = total_seconds / total_days if total_days != 0 else None
            week_average = total_seconds / total_weeks if total_weeks != 0 else None

            return {
                "dayAverage": day_average,
                "weekAverage": week_average
            }
