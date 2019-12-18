from tkinter import *

main_window = Tk()
main_window.title("Trip Planner")
Label(main_window, text='Hotel').grid(row=0, column=0) 
Label(main_window, text='Airline').grid(row=0, column=1) 
hotel_list = Listbox(main_window)
hotel_list.grid(row=1, column=0)
airline_list = Listbox(main_window)
airline_list.grid(row=1, column=1)
hotel_list.insert(1, "Hilton")
hotel_list.insert(2, "Palace")
airline_list.insert(1, "THY")
airline_list.insert(2, "Pegasus")
airline_list.insert(3, "Emirates")
Button(main_window, text='Find', command=main_window.destroy).grid(row=2) 

mainloop()