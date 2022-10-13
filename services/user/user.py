import json
import time

import requests
from flask import Flask, jsonify, make_response, request

import grpc
from google.protobuf.json_format import MessageToJson
from protos import base_pb2

# To make calls on booking
from protos import booking_pb2_grpc

# .env imports
from dotenv import load_dotenv
from pathlib import Path
import os

# Getting env variables
dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
IMDB_API_KEY = os.getenv('IMDB_KEY')

# Flask app
app = Flask(__name__)

# Variables
PORT = 3004
HOST = '0.0.0.0'
MOVIE_URL = "movie:3001"
BOOKING_URL = "booking:3002"
BASE_URL = f"http://{HOST}:{PORT}"

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_users():
    return make_response(jsonify(users), 200)


@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(userid) == str(user["id"]):
            return make_response(jsonify(user), 200)
    return make_response(jsonify({'error': 'id not found'}))


@app.route("/users/<userid>", methods=['POST'])
def create_user(userid):
    req = request.get_json()

    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "user ID already exists"}), 409)

    res = {
        'id': req["id"],
        'name': req["name"],
        'last_active': int(time.time()),
    }

    users.append(res)
    res = make_response(jsonify({"message": "user added"}), 200)
    return res


@app.route("/booking/<userid>")
def get_users_booking(userid):
    with grpc.insecure_channel(BOOKING_URL) as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        userId = base_pb2.UserID(id=userid)
        booking = stub.GetBookingByUserId(userId)
        return make_response(MessageToJson(booking), 200)


def getMovieById(movieid: str):
    query = {
        "query": "query { movie_with_id(_id:\"movieid\") {title rating director }}".replace("movieid", movieid)
    }
    res = requests.post("http://" + MOVIE_URL + "/graphql", json=query)
    return res.text


@app.route("/allmoviesbooked/<userid>")
def get_all_movies_booked(userid):
    with grpc.insecure_channel(BOOKING_URL) as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        userId = base_pb2.UserID(id=userid)
        booking = stub.GetBookingByUserId(userId)

        dates = json.loads(MessageToJson(booking))
        movie_list = []
        for date in dates['date']:
            for movie in date["movies"]:
                print(movie)
                try:
                    res = json.loads(getMovieById(movie['id']))
                    print(res['data']['movie_with_id'])
                    movie_list.append(res['data']['movie_with_id'])
                except:
                    return make_response(jsonify({'error': 'error fetching movie microservice'}))
        return make_response(jsonify(movie_list))


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
