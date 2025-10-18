import tkinter
from tkinter import * 

window = tkinter.Tk() # establish window
window.title("SOS Game") # set title of window
window.geometry("175x175")  # set size of window
title = tkinter.Label(window, text = "Welcome to the game!").pack() # title text at top

v = StringVar(window, "1") #string variable to store any string

# dictionary to create multiple buttons
values = {"Human" : "1",
          "Computer" : "2"}

# loop to create multiple radio buttons
for (text, value) in values.items():
    Radiobutton(window, text = text, variable = v,
                value = value).pack(side = TOP, ipady = 5)
    
# create check button 
checkVar = IntVar()
tkinter.Checkbutton(window, text = "Record Game", variable = checkVar, onvalue = 1, offvalue = 0).pack()

# create lines
canvas = tkinter.Canvas(width = 400, height = 300, bg = "white") # make canvas first
canvas.pack()
canvas.create_line(20,20,180,180, fill = "blue", width = 3)
canvas.create_line(20,180,180,20, fill = "red", width = 3)
window.mainloop()