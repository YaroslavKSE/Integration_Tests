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
        test_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        cursor.execute("INSERT OR REPLACE INTO user_stats VALUES (?, ?)",
                       (test_time, 5))
        conn.commit()
        conn.close()
        self.test_time = test_time

    def test_api_response(self):
        response = self.app.get(f'/api/stats/users?date={self.test_time}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"usersOnline": 5})

    def test_api_response_no_data(self):
        # Query a date for which we haven't populated data
        wrong_time = '2077-01-01T00:00:00'
        response = self.app.get(f'/api/stats/users?date={wrong_time}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"usersOnline": None})


if __name__ == '__main__':
    unittest.main()
