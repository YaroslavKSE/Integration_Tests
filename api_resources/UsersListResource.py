from flask_restful import Resource
from flask import jsonify

from models import get_all_users
from sql_db_models.sql_user_statistics_models import get_users_list


class UsersListResource(Resource):
    @staticmethod
    def get():
        # Get the users list with first seen dates
        users_list = get_users_list()

        # Get the complete list of all users with nicknames
        all_users = get_all_users()

        # Convert all_users to a dictionary for faster access
        users_dict = {user['userId']: user for user in all_users}

        # Now match the userId and enrich the users_list with nicknames
        for user in users_list:
            user_id = user['userId']
            # Find the nickname using the userId and add it to the user data
            user['nickname'] = users_dict.get(user_id, {}).get('nickname', 'Unknown')

        # Return the enriched list of users as JSON
        return jsonify(users_list)
