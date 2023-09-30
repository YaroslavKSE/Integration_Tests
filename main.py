import time
from multiprocessing import Manager
from models import get_20_users


params = {'offset': 1}
users_data = get_20_users(params)


def worker(database):
    while True:
        current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        online_count = sum(1 for user in users_data if user["isOnline"])
        database[current_time] = online_count
        print(database)
        time.sleep(10)  # Wait for 1 minute


if __name__ == '__main__':
    manager = Manager()
    data_storage = manager.dict()

    worker(data_storage)
