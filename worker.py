from models import get_all_users
import sqlite3
import time

users_data = get_all_users()

DB_NAME = 'online_users.db'


def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_stats 
                      (date text primary key, online_count integer)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS individual_user_stats
                          (userId text primary key, 
                           isOnline bool, 
                           currentOnlineTime text, 
                           lastSeenDate text)''')
    conn.commit()
    conn.close()


def worker():
    setup_db()
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
