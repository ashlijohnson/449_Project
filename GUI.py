import tkinter as tk
from tkinter import * 
from tkinter import simpledialog


class SOSGame:
    def __init__(self, window):
        #establish basic board components
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
        tk.Radiobutton(letter_frame, text ="S", variable=self.current_letter, value='S').pack(side=tk.LEFT)
        tk.Radiobutton(letter_frame, text ="O", variable=self.current_letter, value='O').pack(side=tk.LEFT)

        self.create_board()

    def create_board(self):

        #uses user input size to create board 
        board_frame = tk.Frame(self.window)
        board_frame.pack()

        for row in range(self.size):
            row_buttons = []
            for col in range(self.size):
                btn = tk.Button(board_frame, text = '', width = 4, height = 2,
                                command = lambda r=row, c=col: self.place_letter(r,c))
                btn.grid(row=row, column=col)
                row_buttons.append(btn)
            self.board.append(row_buttons)

    def place_letter(self, row, col):

        #places selected letter on clicked board spot
        button =self.board[row][col]
        if button['text'] == '':
            button.config(text=self.current_letter.get())




