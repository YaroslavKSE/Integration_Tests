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
        cursor.execute('''CREATE TABLE IF NOT EXISTS individual_user_online_spans
                            (userId text, 
                            start_time text, 
                            end_time text, 
                            PRIMARY KEY(userId, start_time))''')

        current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        user_id = "e51c2535-test-test-test-aa7af408e927"
        is_online = True
        last_seen = "2023-10-02T08:28:29.0102812+00:00"
        start_online_time = "2023-10-05T17:01:17"
        end_online_time = "2023-10-05T17:05:32"
        cursor.execute("INSERT OR REPLACE INTO user_stats VALUES (?, ?)",
                       (current_time, 5))

        cursor.execute('''INSERT OR REPLACE INTO individual_user_stats 
                       (userId, isOnline, currentOnlineTime, lastSeenDate) 
                       VALUES (?, ?, ?, ?)''',
                       (user_id, is_online, current_time if is_online else None, last_seen))

        cursor.execute("INSERT OR REPLACE INTO individual_user_online_spans (userId, start_time) VALUES (?, ?)",
                       (user_id, start_online_time))
        cursor.execute(
            "UPDATE individual_user_online_spans SET end_time = ? WHERE userId = ? AND end_time IS NULL",
            (end_online_time, user_id))

        conn.commit()
        conn.close()
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


if __name__ == '__main__':
    unittest.main()
