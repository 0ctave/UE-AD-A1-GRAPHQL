import os
import json
from dotenv import load_dotenv
import requests
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

MOVIE_PORT = os.getenv('MOVIE_PORT')

MOVIE_URL = f"http://127.0.0.1:{MOVIE_PORT}"


def get_movie_by_id(id):
    try:
        query = {
            "query": "query { movie_with_id(_id:\"movieid\") {title rating director }}".replace("movieid", id)
        }
        res = requests.post(f"{MOVIE_URL}/graphql", json=query)
    except:
        return "{'error': 'error fetching movie microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

def get_movies_by_title(title):
    try:
        query = {
            "query": "query { movie_with_title(_title:\"movietitle\") {id rating director }}".replace("movietitle", title)
        }
        res = requests.post(f"{MOVIE_URL}/graphql", json=query)
    except:
        return "{'error': 'error fetching movie microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

def get_movies_by_director(director):
    try:
        query = {
            "query": "query { movie_with_director(_director:\"moviedirector\") {id title rating }}".replace("moviedirector", director)
        }
        res = requests.post(f"{MOVIE_URL}/graphql", json=query)
    except:
        return "{'error': 'error fetching movie microservice'}"
    if not (res.ok): return "{'error': 'error user don\'t have bookings'}"
    response = json.loads(res.text)

    return response

def main():
    print("-------------- GetMovieByID --------------")
    print(get_movie_by_id("a8034f44-aee4-44cf-b32c-74cf452aaaae"))

    print("-------------- GetMoviesByTitle --------------")
    print(get_movies_by_title("Creed"))

    print("-------------- GetMoviesByDirector --------------")
    print(get_movies_by_director("Ridley Scott"))
