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
    message = response.read().decode()
    print(message)
    connection.close()
    return message

try:
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Got connection from", addr)
        query = connectionSocket.recv(1024).decode()

        if query == "hotels":
            result = contact_with_port(HOTEL_PORT, "/allHotels")
        elif query == "airlines":
             result = contact_with_port(AIRLINE_PORT, "/allAirlines")
        else:
            tokens = query.split("/")
            arrival_date = tokens[1]
            departure_date = tokens[2]
            preffered_hotel = tokens[3]
            preffered_airline = tokens[4]
            number_of_travelers = tokens[5]

            today = date.today()
            arrival = datetime.strptime(arrival_date, "%Y-%m-%d")
            departure = datetime.strptime(departure_date, "%Y-%m-%d")
            if arrival.date() < today or departure.date() < today:
                result = "You cannot choose a past date!"
            else:
                hotel_query = "/hotelQuery/" + arrival_date + "/" + departure_date + "/" + preffered_hotel + "/" + number_of_travelers
                hotel_result = contact_with_port(HOTEL_PORT, hotel_query)
                airline_query = "/airlineQuery/" + arrival_date + "/" + departure_date + "/" + preffered_airline + "/" + number_of_travelers
                airline_result = contact_with_port(AIRLINE_PORT, airline_query)
                if hotel_result == "OK" and airline_result == "OK":
                    hotel_reserve = "/hotelReserve/" + arrival_date + "/" + departure_date + "/" + preffered_hotel + "/" + number_of_travelers
                    contact_with_port(HOTEL_PORT, hotel_reserve)
                    airline_reserve = "/airlineReserve/" + arrival_date + "/" + departure_date + "/" + preffered_airline + "/" + number_of_travelers
                    contact_with_port(AIRLINE_PORT, airline_reserve)
                    result = "Reservation completed succesfully."
                elif hotel_result == "NO" and airline_result == "NO":
                    result = "Unfortunately no hotels and airlines are available for the dates and number of travelers!"
                elif hotel_result == "NO":
                    result = "Unfortunately there is no available hotel for your choices!"
                elif airline_result == "NO":
                    result = "Unfortunately there is no available airline for your choices!"
                else:
                    result = hotel_result + "\n" + airline_result

        connectionSocket.send(result.encode())
        connectionSocket.close()
except KeyboardInterrupt:
    print("Server has been stopped.")
    serverSocket.close()
