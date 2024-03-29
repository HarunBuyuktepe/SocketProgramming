from tkinter import *
from tkinter import messagebox
import tkinter as tk
import os
from datetime import date, datetime, timedelta
import socket
import re

date_pattern = "20[0-9]{2}-(((0)[0-9])|((1)[0-2]))-([0-2][0-9]|(3)[0-1])"  # e.g. 2019-05-14
TRAVEL_AGENCY_IP = '127.0.0.1'  # localhost
TRAVEL_AGENCY_PORT = 12000  # Port to be connected


def contact_travel_agency(socket, request):
    socket.send(request.encode())
    return socket.recv(1024).decode()

def reserve(arrival_date, departure_date, preffered_hotel, preffered_airline, number_of_travelers):  # Sending reservation request
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    print("Contacting with travel agency...")
    info_text.set("Contacting with travel agency...")
    try:
        clientSocket.connect((TRAVEL_AGENCY_IP, TRAVEL_AGENCY_PORT))
        req = "/" + arrival_date + "/" + departure_date + "/" + preffered_hotel + "/" + preffered_airline + "/" + str(number_of_travelers)
        response = contact_travel_agency(clientSocket, req)
        print(response)
        clientSocket.close()
        if "alternatives" in response:
            statuses = response.split("|")
            hotel_status = statuses[0]
            airline_status = statuses[1]
            if hotel_status != "OK":
                alternative_hotels = hotel_status[13:len(hotel_status)].split(";")
            else:
                alternative_hotels = [preffered_hotel]
            if airline_status != "OK":
                alternative_airlines = airline_status[13:len(airline_status)].split(";")
            else:
                alternative_airlines = [preffered_airline]
            for i in range(0, len(alternative_hotels)):
                for j in range(0, len(alternative_airlines)):
                    choice = messagebox.askyesno("Alternative Plan", "Would you like to choose Hotel: " + alternative_hotels[i] + " and Airline: " + alternative_airlines[j] + "?")
                    if choice is True:
                        reserve(arrival_date, departure_date, alternative_hotels[i], alternative_airlines[j], number_of_travelers)
                        tkvarHotel.set(alternative_hotels[i])
                        tkvarAirway.set(alternative_airlines[j])
                        return
            info_text.set("None of alternative plans has been selected!")
        else:
            info_text.set(response)
    except ConnectionRefusedError:
        print("Travel agency is not responding. Please try again later.")
        info_text.set("Travel agency is not responding. Please try again later.")

def query_get_hotels():  # To get hotels' names
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    print("Contacting with travel agency...")
    try:
        clientSocket.connect((TRAVEL_AGENCY_IP, TRAVEL_AGENCY_PORT))
        req = "hotels"
        response = contact_travel_agency(clientSocket, req)
        clientSocket.close()
        return clear(response)
    except ConnectionRefusedError:
        print("Travel agency is not responding. Please try again later.")
        exit()

def query_get_airlines():  # To get airlines' names
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    print("Contacting with travel agency...")
    try:
        clientSocket.connect((TRAVEL_AGENCY_IP, TRAVEL_AGENCY_PORT))
        req = "airlines"
        response = contact_travel_agency(clientSocket, req)
        clientSocket.close()
        return clear(response)
    except ConnectionRefusedError:
        print("Travel agency is not responding. Please try again later.")
        exit()

def query_reservation():  # Checking reservation inputs. If all valid, call reservation function
    try:
        number_of_travelers = int(e3.get())
    except ValueError:
        info_text.set("Please give a positive integer for number of travelers!")
        return
    arrival_date = e1.get().strip()
    departure_date = e2.get().strip()
    arrival = datetime.strptime(arrival_date, "%Y-%m-%d")
    departure = datetime.strptime(departure_date, "%Y-%m-%d")
    if arrival.date() < date.today() or departure.date() < date.today():
        info_text.set("You cannot choose a past date!")
    elif arrival.date() > departure.date():
        info_text.set("Departure must be later than arrival!")
    elif tkvarAirway.get() != "Please Select" and tkvarHotel.get() != "Please Select":
        if number_of_travelers < 1:
            info_text.set("Number of travelers cannot be less than 1!")
        elif re.search(date_pattern, arrival_date) is None:
            print("Arrival date is invalid! Correct format: year-month-day")
            info_text.set("Arrival date is invalid! Correct format: year-month-day")
        elif re.search(date_pattern, departure_date) is None:
            print("Departure date is invalid! Correct format: year-month-day")
            info_text.set("Departure date is invalid! Correct format: year-month-day")
        else:  # Correct input
            print(arrival_date, departure_date, tkvarHotel.get(), tkvarAirway.get(), number_of_travelers)
            reserve(arrival_date, departure_date, tkvarHotel.get(), tkvarAirway.get(), number_of_travelers)
    else:
        info_text.set("Please select both airline and hotel!")

def clear(string_list):
    string_list = string_list.split("," and "[" and "]" and "'")
    rangeof = len(string_list) - 1
    for i in range(rangeof, -1, -1):
        if string_list[i] == ", " or string_list[i] == "[" or string_list[i] == "]" or string_list[i] == "'":
            string_list.remove(string_list[i])
        else:
            string_list[i]=string_list[i][0].upper()+string_list[i][1:]
    return string_list

root = Tk()
root.title("Network Term Project")

# Add a grid
mainFrame = Frame(root)

mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowconfigure(0, weight=1)
mainFrame.pack(pady=100, padx=100)

#TODO : Control input date
Label(mainFrame, text="Arrival ").grid(row=0,column=1)
Label(mainFrame, text="Departure    ").grid(row=1,column=1)
Label(mainFrame, text="No. of Travelers").grid(row=2,column=1)
e1 = Entry(mainFrame)
e2 = Entry(mainFrame)
e3 = Entry(mainFrame)
end = date.today() + timedelta(days=1)
e1.insert(10, date.today().strftime("%Y-%m-%d"))
e2.insert(10, end.strftime("%Y-%m-%d"))
e3.insert(0, "2")
e1.grid(row=0, column=2)
e2.grid(row=1, column=2)
e3.grid(row=2, column=2)

# Create a Tkinter variable
tkvarHotel = StringVar(root)

# Dictionary with options
hotelChoices = query_get_hotels()
print(hotelChoices)
tkvarHotel.set('Please Select')  # set the default option

popupMenu = OptionMenu(mainFrame, tkvarHotel, *hotelChoices)
Label(mainFrame, text="Choose a Hotel").grid(row=3, column=1)
popupMenu.grid(row=5, column=1)

# Create a Tkinter variable
tkvarAirway = StringVar(root)

# Dictionary with options
hotelChoices = query_get_airlines()
tkvarAirway.set('Please Select')  # set the default option

popupMenu = OptionMenu(mainFrame, tkvarAirway, *hotelChoices)
Label(mainFrame, text="Choose an Airline").grid(row=3, column=3)
popupMenu.grid(row=5, column=3)

button = Button(mainFrame, text="Quit", fg="red", command=quit)
button.grid(row=7, column=3)
button1 = Button(mainFrame, text="Reserve", fg="blue", command=query_reservation)
button1.grid(row=7, column=1)
info_text = StringVar(root)
info_label = Label(mainFrame, textvariable=info_text)
info_label.grid(row=8, columnspan=4)
root.mainloop()