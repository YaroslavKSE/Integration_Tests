from sql_db_models.setup_database import *


def calculate_daily_average(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(strftime('%s', COALESCE(end_time, datetime('now'))) - strftime('%s', start_time)) 
                          FROM individual_user_online_spans 
                          WHERE userId = ?''', (user_id,))
    total_seconds = cursor.fetchone()[0] or 0

    # Total unique days online
    cursor.execute('''SELECT COUNT(DISTINCT date(start_time)) 
                          FROM individual_user_online_spans 
                          WHERE userId = ?''', (user_id,))
    total_days = cursor.fetchone()[0] or 0

    day_average = total_seconds / total_days if total_days != 0 else None

    return day_average


def calculate_weekly_average(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(strftime('%s', COALESCE(end_time, datetime('now'))) - strftime('%s', start_time)) 
                          FROM individual_user_online_spans 
                          WHERE userId = ?''', (user_id,))
    total_seconds = cursor.fetchone()[0] or 0

    # Total unique weeks online
    cursor.execute('''SELECT COUNT(DISTINCT strftime('%Y', start_time) || strftime('%W', start_time)) 
                          FROM individual_user_online_spans 
                          WHERE userId = ?''', (user_id,))

    total_weeks = cursor.fetchone()[0] or 0

    week_average = total_seconds / total_weeks if total_weeks != 0 else None

    return week_average


def calculate_total_online_seconds(user):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(strftime('%s', COALESCE(end_time, datetime('now'))) - strftime('%s', start_time)) "
        "FROM individual_user_online_spans WHERE userId = ?", (user,))

    result = cursor.fetchone()
    total_time_in_seconds = result[0] if result else None
    return total_time_in_seconds


def calculate_daily_min_seconds(user):
    online_times = get_user_online_times(user)
    if online_times:
        return min(online_times.values())
    return 0


def calculate_daily_max_seconds(user):
    online_times = get_user_online_times(user)
    if online_times:
        return max(online_times.values())
    return 0


def get_user_online_times(user):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    query = """
    SELECT strftime('%Y-%m-%d', start_time), sum(strftime('%s', end_time) - strftime('%s', start_time))
    FROM individual_user_online_spans
    WHERE userId = ?
    GROUP BY strftime('%Y-%m-%d', start_time);
    """

    cursor.execute(query, (user,))
    results = cursor.fetchall()

    # Organizing the results into a dictionary where key is the date and value is the total online time for that date
    online_times = {record[0]: record[1] for record in results if None not in record}

    connection.close()

    return online_times


def user_exists_in_db(user):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if user exists in the individual_user_stats
    cursor.execute("SELECT * FROM individual_user_stats WHERE userId = ?", (user,))
    if not cursor.fetchone():
        return False
    else:
        return True
