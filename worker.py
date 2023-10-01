from models import get_20_users
import sqlite3
import time

params = {'offset': 1}
users_data = get_20_users(params)

DB_NAME = 'online_users.db'


def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_stats 
                      (date text primary key, online_count integer)''')
    conn.commit()
    conn.close()


def worker():
    setup_db()
    while True:
        current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        online_count = sum(1 for user in users_data if user["isOnline"])

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO user_stats VALUES (?, ?)",
                       (current_time, online_count))
        conn.commit()
        conn.close()

        time.sleep(10)


if __name__ == '__main__':
    worker()

