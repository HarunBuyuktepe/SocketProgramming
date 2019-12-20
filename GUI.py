from tkinter import *
import tkinter as ttk
import os

def helloCallBack():
    #os.system('py client.py 2020-01-15 2020-01-20 Hilton THY 2')
    print("Fena tarih")

def reservation():
    if(tkvarAirway.get()!="Please Select" and tkvarHotel.get()!="Please Select"):
        print(tkvarAirway.get())
        print(tkvarHotel.get())
        print("h.o")
        helloCallBack()
    else:
        print("yapma")


root = Tk()
root.title("Network Term Project")

# Add a grid
mainFrame = Frame(root)

mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowconfigure(0, weight=1)
mainFrame.pack(pady=100, padx=100)

#TODO : Control input date
Label(mainFrame, text="Departure ").grid(row=0,column=1)
Label(mainFrame, text="Return    ").grid(row=1,column=1)
e1 = Entry(mainFrame)
e2 = Entry(mainFrame)
e1.insert(10, "2020-12-21")
e2.insert(10, "2020-12-28")
e1.grid(row=0, column=2)
e2.grid(row=1, column=2)


# Create a Tkinter variable
tkvarHotel = StringVar(root)

# Dictionary with options
hotelChoices = {'Hilton', 'Paris', 'Hayat', 'Ramada'}
tkvarHotel.set('Please Select')  # set the default option

popupMenu = OptionMenu(mainFrame, tkvarHotel, *hotelChoices)
Label(mainFrame, text="Choose a Hotel").grid(row=3, column=1)
popupMenu.grid(row=5, column=1)

# Create a Tkinter variable
tkvarAirway = StringVar(root)

# Dictionary with options
hotelChoices = {'Thy', 'Pegasus', 'Anadolu Jet', 'Emirates', 'Air France'}
tkvarAirway.set('Please Select')  # set the default option

popupMenu = OptionMenu(mainFrame, tkvarAirway, *hotelChoices)
Label(mainFrame, text="Choose a Hotel").grid(row=3, column=3)
popupMenu.grid(row=5, column=3)

button = Button(mainFrame,
text="Quit",
fg="red",
command=quit).grid(row=7, column=3)
button1 = Button(mainFrame,
 text="Reservate",
 fg="blue",
 command=reservation).grid(row=7, column=1)
root.mainloop()