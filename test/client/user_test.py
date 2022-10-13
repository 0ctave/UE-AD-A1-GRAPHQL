import os
import json
from dotenv import load_dotenv
import requests
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

USER_PORT = os.getenv('USER_PORT')

USER_URL = f"http://127.0.0.1:{USER_PORT}"

# USER
def get_user_by_id(userId):
    try:
        res = requests.get(f'{USER_URL}/users/{userId}')
    except:
        return "{'error': 'error fetching user microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t exist'}"
    response = json.loads(res.text)

    return response


def get_list_users():
    try:
        res = requests.get(f'{USER_URL}/users')
    except:
        return "{'error': 'error fetching user microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t exist'}"
    response = json.loads(res.text)

    return response


def get_user_bookings(userId):
    try:
        res = requests.get(f'{USER_URL}/booking/{userId}')
    except:
        return "{'error': 'error fetching user microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response


# User service tester
def main():
    print("-------------- GetUserById --------------")
    print(get_user_by_id("chris_rivers"))

    print("-------------- GetAllUsers --------------")
    print(get_list_users())

    print("-------------- GetUserBookings --------------")
    print(get_user_bookings("dwight_schrute"))

