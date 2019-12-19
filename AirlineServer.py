from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET\nPath: {}\nHeaders:\n{}\n".format(str(self.path), str(self.headers)))
        if self.path == "/allAirlines":  # Burada bütün otellerin json dosyaları bulunup bir stringde birleştirilip gönderilecek
            currentDirectory = os.getcwd()
            files = ""
            # r=root, d=directories, f = files
            for r, d, f in os.walk(currentDirectory):
                for file in f:
                    if '.json' in file and "a_" in file:
                        files += str(file) + ";"
            result = str(files)
        elif "/airlineQuery/" in self.path:
            tokens = self.path.split("/")
            arrival_date = tokens[2]
            departure_date = tokens[3]
            preffered_airline = tokens[4].lower()
            number_of_travelers = int(tokens[5].strip())
            try:
                with open("a_" + preffered_airline + ".json") as airline_db:
                    airline = json.load(airline_db)
                    passenger_capacity = airline["passenger_capacity"]
                    empty_seats = passenger_capacity - airline["reservations"][arrival_date]
                    if empty_seats > number_of_travelers:
                        result = "OK"
                    else:
                        result = "Not enough seats!"
            except FileNotFoundError:
                result = "Invalid airline name!"
            except KeyError:  # All seats are empty
                if number_of_travelers > passenger_capacity:
                    result = "Not enough seats!"
                else:
                    result = "OK"
        else:
            result = "Invalid request!"
            
        self._set_response()
        self.wfile.flush()
        self.wfile.write(result.encode())

    '''def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode())

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode())'''

def run(server_class=HTTPServer, handler_class=RequestHandler, port=44444):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Airline server has been started.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Airline server has been stopped.")
        httpd.server_close()

run()
