from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from datetime import timedelta, datetime

hotels = {}

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET\nPath: {}\nHeaders:\n{}\n".format(str(self.path), str(self.headers)))
        if self.path == "/allHotels":
            return str(hotels)
        elif "/hotelQuery/" in self.path:
            tokens = self.path.split("/")
            arrival_date = tokens[2]
            departure_date = tokens[3]
            preffered_hotel = tokens[4].lower()
            number_of_travelers = int(tokens[5].strip())
            arrival = datetime.strptime(arrival_date, "%Y-%m-%d")
            departure = datetime.strptime(departure_date, "%Y-%m-%d")
            try:
                hotel = hotels[preffered_hotel]
                if arrival == departure:
                    result = "OK"
                else:
                    total_room_count = hotel["total_room_count"]
                    current = arrival
                    enough_capacity = True
                    while enough_capacity:
                        try:
                            empty_rooms = total_room_count - hotel["reservations"][current.strftime("%Y-%m-%d")]
                            print("total_rooms:", total_room_count, "empty_rooms:", empty_rooms)
                        except KeyError:
                            empty_rooms = total_room_count
                        finally:
                            if number_of_travelers > empty_rooms:
                                enough_capacity = False
                                result = find_all_hotels_by_dates(arrival, departure, number_of_travelers)
                                break
                            elif (current + timedelta(days=1)) == departure:
                                result = "OK"
                                break
                            current += timedelta(days=1)
            except KeyError:
                result = "Invalid hotel name!"
        elif "/hotelReserve" in self.path:
            tokens = self.path.split("/")
            arrival_date = tokens[2]
            departure_date = tokens[3]
            preffered_hotel = tokens[4].lower()
            number_of_travelers = int(tokens[5].strip())
            arrival = datetime.strptime(arrival_date, "%Y-%m-%d")
            departure = datetime.strptime(departure_date, "%Y-%m-%d")
            if arrival == departure:
                result = "OK"
            else:
                current = arrival
                end = False
                while not end:
                    try:
                        hotels[preffered_hotel]["reservations"][current.strftime("%Y-%m-%d")] += number_of_travelers
                    except KeyError:
                        hotels[preffered_hotel]["reservations"][current.strftime("%Y-%m-%d")] = number_of_travelers
                    if (current + timedelta(days=1)) == departure:
                        end = True
                    current += timedelta(days=1)
                with open("h_" + preffered_hotel + ".json", 'w') as outfile:
                    json.dump(hotels[preffered_hotel], outfile)
                result = "OK"
        else:
            result = "Invalid request!"
            
        self._set_response()
        self.wfile.flush()
        self.wfile.write(result.encode())

def find_all_hotels_by_dates(arrival, departure, number_of_travelers):
    result = "alternatives="
    for key in hotels:
        hotel = hotels[key]
        if arrival == departure:
            result += key + ";"
        else:
            total_room_count = hotel["total_room_count"]
            current = arrival
            end = False
            while not end:
                try:
                    empty_rooms = total_room_count - hotel["reservations"][current.strftime("%Y-%m-%d")]
                    print("total_rooms:", total_room_count, "empty_rooms:", empty_rooms)
                except KeyError:
                    empty_rooms = total_room_count
                finally:
                    if number_of_travelers <= empty_rooms:
                        result += key + ";"
                    if (current + timedelta(days=1)) != departure:
                        print("current:", current.strftime("%Y-%m-%d"))
                        current += timedelta(days=1)
                    else:
                        end = True
    if len(result) > 13:  # len(alternatives=) = 13 (There are some suitable hotels)
        return result[0:len(result) - 1]  # hotel1;hotel2;hotel3 (Remove last ;)
    else:
        return "NO"

def find_all_hotels():
    currentDirectory = os.getcwd()
    # r=root, d=directories, f = files
    for r, d, f in os.walk(currentDirectory):
        for file in f:
            if '.json' in file and "h_" in file:
                hotel_name = file[2:len(file) - 5]
                with open(file) as hotel_db:
                    hotels[hotel_name] = json.load(hotel_db)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=33333):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    find_all_hotels()
    print("Hotel server has been started.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Hotel server has been stopped.")
        httpd.server_close()

run()
