import socket
import http.client
import ssl
from datetime import date, datetime

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
serverSocket.bind(('' , serverPort))
serverSocket.listen(1)  # Allows 1 connection at a time
print('The server is ready to receive')

def contact_hotel_and_airline(request):
    print("Getting result for query", request)  
    tokens = request.split(" ")
    arrival_date = tokens[0]
    departure_date = tokens[1]
    preffered_hotel = tokens[2]
    preffered_airline = tokens[3]
    number_of_travelers = tokens[4]

    today = date.today()
    arrival = datetime.strptime(arrival_date, "%Y-%m-%d")
    departure = datetime.strptime(departure_date, "%Y-%m-%d")
    if arrival.date() < today or departure.date() < today:
        return "You cannot choose a past date!"
    
    connection = http.client.HTTPConnection("127.0.0.1", 33333)
    connection.request("GET", "/" + arrival_date + "/" + departure_date + "/" + preffered_hotel + "/" + number_of_travelers)
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status, response.reason))
    connection.close()
    return "Status: {} and reason: {}".format(response.status, response.reason)

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        print("Got connection from", addr)
        query = connectionSocket.recv(1024).decode()

        result = contact_hotel_and_airline(query)

        connectionSocket.send(result.encode())
        connectionSocket.close()
    except KeyboardInterrupt:
        print("Server has been stopped.")
        raise
