import socket
from sys import argv
import re

date_pattern = "20[0-9]{2}-(((0)[0-9])|((1)[0-2]))-([0-2][0-9]|(3)[0-1])"  # e.g. 2019-05-14

# Sample call: py client.py 2020-05-06 2020-05-14 Hilton Emirates 2
if len(argv) == 6:
    arrival_date = argv[1]
    departure_date = argv[2]
    preffered_hotel = argv[3]
    preffered_airline = argv[4]
    number_of_travelers = argv[5]
    valid = re.search(date_pattern, arrival_date)
    if valid is None:
        print("Arrival date is invalid! Correct format: year-month-day")
        exit(0)
    valid = re.search(date_pattern, departure_date)
    if valid is None:
        print("Departure date is invalid! Correct format: year-month-day")
        exit(0)
    serverName = '127.0.0.1'  # localhost
    serverPort = 12000  # Port to be connected
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    print("Contacting with travel agency...")
    try:
        clientSocket.connect((serverName, serverPort))
    except ConnectionRefusedError:
        print("Travel agency is not responding. Please try again later.")
        exit()
    request = arrival_date + " " + departure_date + " " + preffered_hotel + " " + preffered_airline + " " + number_of_travelers
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    print(response)
    clientSocket.close()
else:
    print("Invalid arguments! Arguments must be \"ArrivalDate DepartureDate PrefferedHotel PrefferedAirline NumberOfTravelers\" respectively!")
