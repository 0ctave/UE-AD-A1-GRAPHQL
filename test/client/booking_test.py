import os
import json
from dotenv import load_dotenv
import requests
from pathlib import Path
import grpc

from protos import base_pb2
from protos import booking_pb2
from protos import booking_pb2_grpc
dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

BOOKING_PORT = os.getenv('BOOKING_PORT')

# BOOKINGS
def get_booking_by_userId(stub: booking_pb2_grpc.BookingStub, userId):
    booking = stub.GetBookingByUserId(userId)
    print(booking)


def get_list_bookings(stub: booking_pb2_grpc.BookingStub):
    bookings = stub.GetAllBookings(base_pb2.Empty())
    for booking in bookings:
        print("Booking from %s" % (booking.userId))


# Booking service tester
def main():
    with grpc.insecure_channel(f'127.0.0.1:{BOOKING_PORT}') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        print("-------------- GetBookingById --------------")
        userId = base_pb2.UserID(id="dwight_schrute")
        get_booking_by_userId(stub=stub, userId=userId)

        print("-------------- GetListBookings --------------")
        get_list_bookings(stub=stub)

        channel.close()