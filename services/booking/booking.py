import grpc
from concurrent import futures

from protos import booking_pb2
from protos import booking_pb2_grpc

# Import des types
from protos import showtime_pb2
from protos import movie_pb2

import json

# Crée un élément de type Schedule (voir showtime.proto) à partir d'une date et d'une liste de film
def createScheduleItem(date,movies)->showtime_pb2.Schedule:
    item:showtime_pb2.Schedule = showtime_pb2.Schedule(
        date=showtime_pb2.Date(date=date)
        )
    movies = map(lambda movie: movie_pb2.MovieID(id=movie),movies)
    item.movies.extend(movies)
    return item

# Crée un élément de type Booking (voir booking.proto) à partir de la structure de donnée utilisée dans data/booking.json
def createBookingItem(booking):
    dates = list(map(
                    lambda date:
                        createScheduleItem(date=date["date"],movies=date["movies"]),
                    booking["dates"]
                ))
    booking_data = booking_pb2.BookingData(userId=booking['userid'])
    booking_data.date.extend(dates)
    return booking_data

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db:list[str] = json.load(jsf)["bookings"]

    def GetBookingByUserId(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.id:
                print("Booking found!")
                return createBookingItem(booking)

    def GetAllBookings(self, request, context):
        for booking in self.db:
            yield createBookingItem(booking)

# Main method to run service on port 3002
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
