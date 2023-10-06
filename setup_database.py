import sqlite3

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

    cursor.execute('''CREATE TABLE IF NOT EXISTS individual_user_online_spans
                        (userId text, 
                        start_time text, 
                        end_time text, 
                        PRIMARY KEY(userId, start_time))''')
    conn.commit()
    conn.close()
