import os
import json
from dotenv import load_dotenv
import requests
from pathlib import Path
import grpc

from protos import base_pb2
from protos import showtime_pb2
from protos import showtime_pb2_grpc


dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

SHOWTIME_PORT = os.getenv('SHOWTIME_PORT')

#SHOWTIME
def get_movies_by_date(stub, date):
    movies = stub.GetMoviesByDate(date)
    print(movies)

# Showtime service tester
def main():
    with grpc.insecure_channel(f'127.0.0.1:{SHOWTIME_PORT}') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetMoviesByDate --------------")
        date = showtime_pb2.Date(date="20151202")
        get_movies_by_date(stub=stub, date=date)


        channel.close()