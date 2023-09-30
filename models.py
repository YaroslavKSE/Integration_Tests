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

    # Loop through each user in the list
    return user_list

