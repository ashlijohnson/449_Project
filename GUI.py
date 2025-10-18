import tkinter as tk
from tkinter import * 
from tkinter import simpledialog


class SOSGame:
    def __init__(self, window):
        self.window = window
        self.window.title("SOS Game")

        self.board = []
        self.size = 0
        self.current_letter = tk.StringVar(value='S')

        self.setup_menu()

    def setup_menu(self):
        #ask for board size
        self.size = simpledialog.askinteger("Board Size", "Enter board size", minvalue = 3, maxvalue = 10)
        if not self.size:
            self.window.destroy()
            return
        
        #letter selection (S or O)
        letter_frame = tk.Frame(self.window)
        letter_frame.pack()

        tk.Label(letter_frame, text = "Choose Letter").pack(side=tk.LEFT)
        tk.Radiobutton(letter_frame, text)





