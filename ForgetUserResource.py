from flask import request
from flask_restful import Resource
from setup_database import DB_NAME

import sqlite3


class ForgetUserResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get('userId')
        if not user_id:
            return {"error": "userId parameter is required"}, 400

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Check if user exists in the individual_user_stats
        cursor.execute("SELECT * FROM individual_user_stats WHERE userId = ?", (user_id,))
        if not cursor.fetchone():
            return {"error": "user not found"}, 404

        # Delete the user's data from individual_user_stats
        cursor.execute("DELETE FROM individual_user_stats WHERE userId = ?", (user_id,))

        # Delete the user's data from individual_user_online_spans
        cursor.execute("DELETE FROM individual_user_online_spans WHERE userId = ?", (user_id,))

        # Commit the changes
        conn.commit()
        conn.close()

        return {"userId": f"Data about {user_id} was forgotten"}, 200
