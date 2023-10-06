from models import get_all_users
from setup_database import *
from sql_online_check_models import *
import time

users_data = get_all_users()

setup_db()


def worker():
    while True:
        current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        online_count = 0

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        for user in users_data:
            if user["isOnline"]:
                online_count += 1

            user_id = user["userId"]
            is_online = user["isOnline"]
            current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
            last_seen = user["lastSeenDate"]

            if is_online and not_was_online_before(user_id):
                # Insert new online span with start time
                cursor.execute("INSERT INTO individual_user_online_spans (userId, start_time) VALUES (?, ?)",
                               (user_id, current_time))

            elif not is_online and was_online_before(user_id):
                # Update the end time for the most recent online span
                cursor.execute(
                    "UPDATE individual_user_online_spans SET end_time = ? WHERE userId = ? AND end_time IS NULL",
                    (current_time, user_id))

            cursor.execute('''INSERT OR REPLACE INTO individual_user_stats 
                           (userId, isOnline, currentOnlineTime, lastSeenDate) 
                           VALUES (?, ?, ?, ?)''',
                           (user_id, is_online, current_time if is_online else None, last_seen))

        cursor.execute("INSERT OR REPLACE INTO user_stats VALUES (?, ?)",
                       (current_time, online_count))

        conn.commit()
        conn.close()

        time.sleep(20)


if __name__ == '__main__':
    worker()
