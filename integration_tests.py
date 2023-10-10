from api import app
from setup_database import setup_db
from database_populator import populate_data

import unittest
import time


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        # Set up the testing client
        self.app = app.test_client()

        # Pre-populate the database with known data
        self.populate_test_data()

    def populate_test_data(self):
        setup_db()

        current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        user_id = "e51c2535-test-test-test-aa7af408e927"
        is_online = True
        last_seen = "2023-10-02T08:28:29.0102812+00:00"
        start_online_time = "2023-10-05T17:01:17"
        end_online_time = "2023-10-05T17:05:32"

        populate_data(current_time, user_id, is_online, last_seen, start_online_time, end_online_time)

        self.current_time = current_time
        self.user_id = user_id
        self.is_online = is_online
        self.last_seen = last_seen
        self.start_online_time = start_online_time
        self.end_online_time = end_online_time

    def test_api_response_data_exists_about_all_users_online(self):
        response = self.app.get(f'/api/stats/users?date={self.current_time}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"usersOnline": 5})

    def test_api_response_data_not_exists_about_all_users_online(self):
        # Query a date for which we haven't populated data
        wrong_time = '2077-01-01T00:00:00'
        response = self.app.get(f'/api/stats/users?date={wrong_time}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"usersOnline": None})

    def test_api_response_data_for_a_concrete_user_which_is_online_at_correct_time(self):
        response = self.app.get(f'/api/stats/users?date={self.start_online_time}&userId={self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "wasUserOnline": True,
            "nearestOnlineTime": None
        })

    def test_api_response_data_for_a_concrete_user_which_is_online_at_incorrect_time(self):
        wrong_time = '2077-01-01T00:00:00'
        response = self.app.get(f'/api/stats/users?date={wrong_time}&userId={self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "wasUserOnline": False,
            "nearestOnlineTime": self.end_online_time
        })

    def test_api_response_data_for_a_concrete_user_which_is_online_invalid_user_id(self):
        invalid_user_id = 'user_no_info_12312312'
        response = self.app.get(f'/api/stats/users?date={self.current_time}&userId={invalid_user_id}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'User not found.'})

    def test_api_response_data_for_a_concrete_user_which_is_online_no_nearest_online_time_found(self):
        wrong_time = '2077-01-01T00:00:00'
        user_with_no_timespan = "e51c2535-test-test-test-no_time_span"
        response = self.app.get(f'/api/stats/users?date={wrong_time}&userId={user_with_no_timespan}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "wasUserOnline": False,
            "nearestOnlineTime": None
        })

    def test_successful_api_response_for_predicting_online_user_count(self):
        base_time_for_prediction = "2023-12-01T22:08:45"
        mean_number_of_online_users = 59
        response = self.app.get(f'/api/predictions/users?date={base_time_for_prediction}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"onlineUsers": mean_number_of_online_users})

    def test_unsuccessful_api_response_for_predicting_online_user_count(self):
        base_time_for_prediction = "2023-12-01T12:08:45"
        response = self.app.get(f'/api/predictions/users?date={base_time_for_prediction}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"onlineUsers": None})

    def test_successful_api_response_for_predicting_the_chance_of_being_user_online(self):
        response = self.app.get(f'/api/predictions/users?date={self.start_online_time}&tolerance={0.75}&'
                                f'userId={self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "willBeOnline": True,
            "onlineChance": 1.0
        })

    def test_unsuccessful_api_response_for_predicting_the_chance_of_being_user_online(self):
        response = self.app.get(f'/api/predictions/users?date={self.current_time}&tolerance={0.75}&'
                                f'userId={self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "willBeOnline": False,
            "onlineChance": 0
        })

    def test_successful_api_response_for_calculating_total_seconds_user_was_online(self):
        response = self.app.get(f'/api/stats/user/total?userId={self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "totalTime": 255
        })

    def test_api_for_calculating_total_seconds_user_was_online_if_system_has_no_info_about_user(self):
        invalid_user_id = 'user_no_info_12312312'
        response = self.app.get(f'/api/stats/user/total?userId={invalid_user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "totalTime": None
        })


if __name__ == '__main__':
    unittest.main()
