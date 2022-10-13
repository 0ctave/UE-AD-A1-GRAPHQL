import grpc
from concurrent import futures
from protos import showtime_pb2
from protos import showtime_pb2_grpc

from protos import movie_pb2
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetMoviesByDate(self, request, context):
        for date in self.db:
            if date['date'] == request.date:
                print("Date found!")
                schedule = showtime_pb2.Schedule(date=showtime_pb2.Date(date=date["date"]))
                schedule.movies.extend([movie_pb2.MovieID(id=movie) for movie in date['movies']])
                return schedule
        return showtime_pb2.Schedule(date="")

    def GetTimes(self, request, context):
        for date in self.db:
            schedule = showtime_pb2.Schedule()

            schedule.movies.extend(date['movies'])
            yield schedule
            yield showtime_pb2.Schedule(date=date['date'], movie=date['movies'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
