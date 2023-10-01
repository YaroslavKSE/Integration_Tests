import json
import requests

url = "https://sef.podkolzin.consulting/api/users/lastSeen"


def get_20_users(offset):
    # Sending GET request and saving the response as a response object
    response = requests.get(url, params=offset, headers={'accept': 'application/json'})
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

    # Parse JSON response
    json_data = json.loads(response.text)

    # Extracting the list of users from JSON data
    user_list = json_data['data']

    return user_list


def get_all_users():
    params = {'offset': 0}
    all_user_data = []
    while params['offset'] < 217:
        for user in get_20_users(params):
            all_user_data.append(user)
        params['offset'] += 20

    return all_user_data

