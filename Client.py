import socket
from sys import argv
import re

date_pattern = "20[0-9]{2}-(((0)[0-9])|((1)[0-2]))-([0-2][0-9]|(3)[0-1])"  # e.g. 2019-05-14
TRAVEL_AGENCY_IP = '127.0.0.1'  # localhost
TRAVEL_AGENCY_PORT = 12000  # Port to be connected


def contact_travel_agency(socket, request):
    socket.send(request.encode())
    return socket.recv(1024).decode()

def query_reservation(arrival_date, departure_date, preffered_hotel, preffered_airline, number_of_travelers):
    valid = re.search(date_pattern, arrival_date)
    if valid is None:
        print("Arrival date is invalid! Correct format: year-month-day")
        exit(0)
    valid = re.search(date_pattern, departure_date)
    if valid is None:
        print("Departure date is invalid! Correct format: year-month-day")
        exit(0)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    print("Contacting with travel agency...")
    try:
        clientSocket.connect((TRAVEL_AGENCY_IP, TRAVEL_AGENCY_PORT))
    except ConnectionRefusedError:
        print("Travel agency is not responding. Please try again later.")
        exit()

    req = "/" + arrival_date + "/" + departure_date + "/" + preffered_hotel + "/" + preffered_airline + "/" + number_of_travelers
    response = contact_travel_agency(clientSocket, req)
    print(response)
    clientSocket.close()


# Sample call: py client.py 2020-05-06 2020-05-14 Hilton THY 2
