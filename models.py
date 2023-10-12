import json
import requests

url = "https://sef.podkolzin.consulting/api/users/lastSeen"
params = {'offset': 0}
total_records = 1
offset_increase = 1


def get_users_data(offset):
    global total_records
    global offset_increase
    # Sending GET request and saving the response as a response object
    response = requests.get(url, params=offset, headers={'accept': 'application/json'})
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

    # Parse JSON response
    json_data = json.loads(response.text)

    # Extracting server info and the list of users from JSON data
    user_list = json_data['data']
    total_records = json_data['total']
    offset_increase = len(user_list)

    # Loop through each user in the list
    return user_list


def get_all_users():
    all_user_data = []
    while params['offset'] < total_records:
        for user in get_users_data(params):
            all_user_data.append(user)
        params['offset'] += offset_increase
    params['offset'] = 0
    return all_user_data
