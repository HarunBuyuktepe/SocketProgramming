import socket
import http.client
from datetime import date, datetime

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
serverSocket.bind(('' , serverPort))
serverSocket.listen(1)  # Allows 1 connection at a time
print('The server is ready to receive')

HOTEL_PORT = 33333
AIRLINE_PORT = 44444


def contact_with_port(port, request):
    print("Getting result for query", request)  
    connection = http.client.HTTPConnection("127.0.0.1", port)
    connection.request("GET", request)
    response = connection.getresponse()
    asd = response.read().decode()
    print(asd)
    connection.close()
    return asd

try:
    print("asdasda")
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Got connection from", addr)
        query = connectionSocket.recv(1024).decode()

        if query == "hotels":
            result = contact_with_port(HOTEL_PORT, "/allHotels")
        elif query == "airlines":
             result = contact_with_port(AIRLINE_PORT, "/allAirlines")
        else:
            tokens = query.split(" ")
            arrival_date = tokens[0]
            departure_date = tokens[1]
            preffered_hotel = tokens[2]
            preffered_airline = tokens[3]
            number_of_travelers = tokens[4]

            today = date.today()
            arrival = datetime.strptime(arrival_date, "%Y-%m-%d")
            departure = datetime.strptime(departure_date, "%Y-%m-%d")
            if arrival.date() < today or departure.date() < today:
                result = "You cannot choose a past date!"
            else:
                result = contact_with_port(HOTEL_PORT, query)

        connectionSocket.send(result.encode())
        connectionSocket.close()
except KeyboardInterrupt:
    print("Server has been stopped.")
    serverSocket.close()
