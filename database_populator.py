import sqlite3

from setup_database import DB_NAME


def populate_data(current_time, user_id, is_online, last_seen, start_online_time, end_online_time):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
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