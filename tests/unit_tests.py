import unittest
import json
from unittest.mock import patch, MagicMock, Mock
from worker import setup_db, worker
from models import get_users_data


class TestUsersData(unittest.TestCase):

    @patch('requests.get')
    def test_successful_response(self, mock_get):
        # Mocking a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_data = {
            "total": 217,
            "data": [{"nickname": "Alice", "isOnline": True, "lastSeenDate": None},
                     {"nickname": "Bob", "isOnline": False, "lastSeenDate": "2023-09-25T10:30:00+00:00"},
                     {"nickname": "Snack", "isOnline": False, "lastSeenDate": "2023-09-24T10:30:00+00:00"},
                     {"nickname": "Nick", "isOnline": False, "lastSeenDate": "2023-09-26T12:00:00+00:00"}]
        }
        mock_response.json.return_value = mock_data
        mock_response.text = json.dumps(mock_data)
        mock_get.return_value = mock_response

        # Calling the function
        result = get_users_data({'offset': 0})

        # Asserting the result
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]['nickname'], "Alice")
        self.assertEqual(result[1]['nickname'], "Bob")
        self.assertEqual(result[2]['nickname'], "Snack")
        self.assertEqual(result[3]['nickname'], "Nick")

    @patch('requests.get')
    def test_failed_response(self, mock_get):
        # Mocking a failed response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        # Calling the function
        result = get_users_data({'offset': 0})

        # Asserting the result
        self.assertEqual(result, [])


class TestSetupDbFunction(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_setup_db(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        setup_db()

        # Assert that the connection was made to the correct database.
        mock_connect.assert_called_once_with('D:\\pythonProjects\\IntegrationTests\\online_users.db')

        # Assert that the necessary SQL commands were executed.
        assert mock_cursor.execute.call_count == 4  # We know it should be called thrice for three tables.

        # Assert that the commit method was called
        mock_connection.commit.assert_called_once()

        # Assert that the close method was called
        mock_connection.close.assert_called_once()


class TestWorkerFunction(unittest.TestCase):

    @patch('sqlite3.connect')
    @patch('time.sleep', side_effect=InterruptedError)  # Raise an error after sleeping to exit the loop.
    @patch('worker.get_all_users')  # Replace with appropriate mocked data.
    @patch('time.strftime')
    def test_worker(self, mock_strftime, mock_get_all_users, mock_sleep, mock_connect):
        # Mock the time
        mock_strftime.return_value = '2023-10-12T16:03:12'

        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_get_all_users.return_value = [
            {
                "userId": "e31e41f4-test-cd5d-def4-4c79f86bb0e1",
                "nickname": "Jerry_Adams6",
                "firstName": "Jerry",
                "lastName": "Adams",
                "registrationDate": "2022-09-24T15:33:18.0113307+00:00",
                "lastSeenDate": None,
                "isOnline": True
            }

        ]
        with self.assertRaises(InterruptedError):
            worker()

        # Assert that the connection was made to the correct database.
        self.assertEqual(mock_connect.call_count, 1)

        mock_sleep.assert_called_once_with(20)

        mock_cursor.execute.assert_any_call('SELECT userId FROM forgotten_users WHERE userId = ?',
                                            ('e31e41f4-test-cd5d-def4-4c79f86bb0e1',))
        mock_cursor.execute.assert_any_call('INSERT OR REPLACE INTO user_stats VALUES (?, ?)',
                                            ('2023-10-12T16:03:12', 0))

        # Assert that the necessary SQL commands were executed.
        assert mock_cursor.execute.call_count == 2

        # Assert that the commit method was called
        mock_connection.commit.assert_called_once()

        # Assert that the close method was called
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()