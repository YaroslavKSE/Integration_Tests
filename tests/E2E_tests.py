import subprocess
import sys
import time
import tracemalloc
import unittest

import requests

from sql_db_models.database_populator import *

API_BASE_URL = 'http://127.0.0.1:80/api'  # Replace with your API's base URL


class TestE2E(unittest.TestCase):

    def setUp(self):
        tracemalloc.start()

        current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        user_id = "e51c2535-test-test-test-aa7af408e927"
        is_online = True
        last_seen = "2023-10-02T08:28:29.0102812+00:00"
        start_online_time = "2023-10-05T17:01:17"
        end_online_time = "2023-10-05T17:05:32"

        populate_data(current_time, user_id, is_online, last_seen, start_online_time, end_online_time)

        # Start the API
        self.api_process = subprocess.Popen([sys.executable, 'api.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.worker_process = subprocess.Popen([sys.executable, 'worker.py'], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)

        # Give it a few seconds to ensure everything is up and running before the tests
        time.sleep(2)

    def tearDown(self):
        # Terminate the API and worker processes
        self.api_process.terminate()
        self.worker_process.terminate()

        # Close stdout and stderr streams
        self.api_process.stdout.close()
        self.api_process.stderr.close()
        self.worker_process.stdout.close()
        self.worker_process.stderr.close()

        # Optionally wait for them to fully terminate
        self.api_process.wait()
        self.worker_process.wait()

    def test_userOnlineResource_usersOnline_is_not_None(self):
        response = requests.get(f'{API_BASE_URL}/stats/users?date=2023-10-05T17:01:17')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('usersOnline', data)  # Check that 'usersOnline' is part of the response

    def test_userOnlineResource_usersOnline_is_None(self):
        response = requests.get(f'{API_BASE_URL}/stats/users?date=2023-15-05T17:01:17')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('usersOnline', data)  # Check that 'usersOnline' is part of the response

    def test_UsersOnlineResource_wasUserOnline_True(self):
        response = requests.get(f'{API_BASE_URL}/stats/users?date=2023-10-05T17:03:27&'
                                f'userId=e51c2535-test-test-test-aa7af408e927')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {
            "wasUserOnline": True,
            "nearestOnlineTime": None
        })

    def test_UsersOnlineResource_wasUserOnline_False(self):
        response = requests.get(f'{API_BASE_URL}/stats/users?date=2023-10-06T17:03:27&'
                                f'userId=e51c2535-test-test-test-aa7af408e927')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {
            "wasUserOnline": False,
            "nearestOnlineTime": "2023-10-05T17:05:32"
        })

    def test_UsersTotalResource_dayAverage_and_weekAverage_is_not_None(self):
        response = requests.get(f'{API_BASE_URL}/stats/user/total?userId=e51c2535-test-test-test-aa7af408e927'
                                f'&averageRequired=true')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {
            "dayAverage": data["dayAverage"],
            "weekAverage": data["weekAverage"]
        })

    def test_UserPredictionResource_online_user_count_is_not_None(self):
        response = requests.get(f'{API_BASE_URL}/predictions/users?date=2024-10-05T17:05:32')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {"onlineUsers": data["onlineUsers"]})

    def test_UsersForgetResource_data_about_user_was_forgotten_successfully(self):
        response = requests.get(f'{API_BASE_URL}/user/forget?userId=e51c2535-test-test-test-aa7af408e927')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {
            "userId": f"Data about e51c2535-test-test-test-aa7af408e927 was forgotten"
        })


if __name__ == '__main__':
    unittest.main()
