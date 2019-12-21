from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

airlines = {}

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET\nPath: {}\nHeaders:\n{}\n".format(str(self.path), str(self.headers)))
        if self.path == "/allAirlines":  # Burada bütün otellerin json dosyaları bulunup bir stringde birleştirilip gönderilecek
            return str(airlines)
        elif "/airlineQuery/" in self.path:
            tokens = self.path.split("/")
            arrival_date = tokens[2]
            departure_date = tokens[3]
            preffered_airline = tokens[4].lower()
            number_of_travelers = int(tokens[5].strip())
            try:
                airline = airlines[preffered_airline]
            except KeyError:
                result = "Invalid airline name!"
            try:
                passenger_capacity = airline["passenger_capacity"]
                empty_seats1 = passenger_capacity - airline["reservations"][arrival_date]
            except KeyError:  # All seats are empty
                try:
                    empty_seats2 = passenger_capacity - airline["reservations"][departure_date]
                    if empty_seats1 >= number_of_travelers and empty_seats2 >= number_of_travelers:
                        result = "OK"
                    else:
                        result = "Not enough seats!"
                except KeyError:
                    if number_of_travelers <= passenger_capacity:
                        result = "OK"
                    else:
                        result = "Not enough seats!"
            
        elif "/airlineReserve" in self.path:
            tokens = self.path.split("/")
            arrival_date = tokens[2]
            departure_date = tokens[3]
            preffered_airline = tokens[4].lower()
            number_of_travelers = int(tokens[5].strip())
            try:
                airlines[preffered_airline]["reservations"][arrival_date] += number_of_travelers
            except KeyError:
                airlines[preffered_airline]["reservations"][arrival_date] = number_of_travelers
            try:
                airlines[preffered_airline]["reservations"][departure_date] += number_of_travelers
            except KeyError:
                airlines[preffered_airline]["reservations"][departure_date] = number_of_travelers
            with open("a_" + preffered_airline + ".json", 'w') as outfile:
                json.dump(airlines[preffered_airline], outfile)
            result = "OK"
        else:
            result = "Invalid request!"
            
        self._set_response()
        self.wfile.flush()
        self.wfile.write(result.encode())

def find_all_airlines():
    currentDirectory = os.getcwd()
    # r=root, d=directories, f = files
    for r, d, f in os.walk(currentDirectory):
        for file in f:
            if '.json' in file and "a_" in file:
                airline_name = file[2:len(file) - 5]
                with open(file) as airline_db:
                    airlines[airline_name] = json.load(airline_db)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=44444):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    find_all_airlines()
    print("Airline server has been started.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Airline server has been stopped.")
        httpd.server_close()

run()
