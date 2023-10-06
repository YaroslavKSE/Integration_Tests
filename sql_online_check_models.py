import sqlite3
from setup_database import DB_NAME


def not_was_online_before(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT isOnline FROM individual_user_stats WHERE userId = ?", (user_id,))
    result = cursor.fetchone()
    return result is None or not result[0]


def was_online_before(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT isOnline FROM individual_user_stats WHERE userId = ?", (user_id,))
    result = cursor.fetchone()
    return result is not None and result[0]
