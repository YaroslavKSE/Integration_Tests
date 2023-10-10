from flask import request
from flask_restful import Resource
from setup_database import DB_NAME

import sqlite3


class UsersTotalResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get("userId")

        if not user_id:
            return {"error": "userId parameter is required"}, 404

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(strftime('%s', COALESCE(end_time, datetime('now'))) - strftime('%s', start_time)) "
                       "FROM individual_user_online_spans WHERE userId = ?", (user_id,))

        result = cursor.fetchone()
        conn.close()

        total_time_in_seconds = result[0] if result else None
        return {"totalTime": total_time_in_seconds}
