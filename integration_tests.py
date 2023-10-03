import unittest
import sqlite3
import time
from api import app, DB_NAME


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        # Set up the testing client
        self.app = app.test_client()

        # Pre-populate the database with known data
        self.populate_test_data()

    def populate_test_data(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_stats 
                      (date text primary key, online_count integer)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS individual_user_stats
                              (userId text primary key, 
                               isOnline bool, 
                               currentOnlineTime text, 
                               lastSeenDate text)''')

        test_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        user_id = "test1234"
        is_online = True
        last_seen = "2023-10-02T08:28:29.0102812+00:00"

        cursor.execute("INSERT OR REPLACE INTO user_stats VALUES (?, ?)",
                       (test_time, 5))

        cursor.execute('''INSERT OR REPLACE INTO individual_user_stats 
                       (userId, isOnline, currentOnlineTime, lastSeenDate) 
                       VALUES (?, ?, ?, ?)''',
                       (user_id, is_online, test_time if is_online else None, last_seen))

        conn.commit()
        conn.close()
        self.test_time = test_time
        self.user_id = user_id
        self.is_online = is_online
        self.last_seen = last_seen

    def test_api_response_data_exists_about_all_users_online(self):
        response = self.app.get(f'/api/stats/users?date={self.test_time}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"usersOnline": 5})

    def test_api_response_data_not_exists_about_all_users_online(self):
        # Query a date for which we haven't populated data
        wrong_time = '2077-01-01T00:00:00'
        response = self.app.get(f'/api/stats/users?date={wrong_time}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"usersOnline": None})

    def test_api_response_data_for_a_concrete_user_which_is_online_at_correct_time(self):
        response = self.app.get(f'/api/stats/users?date={self.test_time}&userId={self.user_id}')
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
            "nearestOnlineTime": None
        })

    def test_api_response_data_for_a_concrete_user_which_is_online_invalid_user_id(self):
        invalid_user_id = 'user_no_info_12312312'
        response = self.app.get(f'/api/stats/users?date={self.test_time}&userId={invalid_user_id}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'User not found.'})

    def test_api_response_data_for_a_concrete_user_which_is_online_no_nearest_online_time_found(self):
        wrong_time = '2077-01-01T00:00:00'
        response = self.app.get(f'/api/stats/users?date={wrong_time}&userId={self.user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "wasUserOnline": False,
            "nearestOnlineTime": None
        })


if __name__ == '__main__':
    unittest.main()
