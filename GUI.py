import tkinter as tk
from tkinter import * 
from tkinter import simpledialog


class SOSGame:
    def __init__(self, window):
        #establishes basic board components
        self.window = window
        self.window.title("SOS Game")
        self.window.geometry("600x600")

        self.board = []
        self.size = 0

        self.current_player = "Blue"
        self.game_mode = tk.StringVar(value='Simple')
        self.blue_choice = tk.StringVar(value='S')
        self.red_choice = tk.StringVar(value='S')

        self.setup_menu()

    def setup_menu(self):
        #asks for board size
        self.size = simpledialog.askinteger("Board Size", "Enter board size", minvalue = 3, maxvalue = 10)
        if not self.size:
            self.window.destroy()
            return
        
        self.create_board()

    def create_board(self):
        #creates top frame with game mode 
        top_frame = tk.Frame(self.window, pady=10)
        top_frame.grid(row=0, column=0, columnspan=3)

        tk.Label(top_frame, text = "Select Game Mode:").pack(side=tk.LEFT)
        tk.Radiobutton(top_frame, text="Simple Game", variable=self.game_mode, value="Simple").pack(side=tk.LEFT)
        tk.Radiobutton(top_frame, text="General Game", variable=self.game_mode, value="General").pack(side=tk.LEFT)

        #creates main frame
        main_frame = tk.Frame(self.window)
        main_frame.grid(row=1, column=0, columnspan=3)

        #creates board frame using user input to determine size
        board_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10)
        board_frame.grid(row=1, column=1)

        for row in range(self.size):
            row_buttons = []
            for col in range(self.size):
                btn = tk.Button(board_frame, text = '', width = 4, height = 2,
                                command = lambda r=row, c=col: self.place_letter(r,c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(btn)
            self.board.append(row_buttons)

        #creates blue player's section
        blue_frame = tk.Frame(main_frame, padx=10, pady=10)
        blue_frame.grid(row=1, column=0, sticky='ns')
        tk.Label(blue_frame, text="Blue Player", font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Radiobutton(blue_frame, text="S", variable=self.blue_choice, value='S').pack(anchor=tk.W)
        tk.Radiobutton(blue_frame, text="O", variable=self.blue_choice, value='O').pack(anchor=tk.W)

        #creates red player's section
        red_frame = tk.Frame(main_frame, padx=10, pady=10)
        red_frame.grid(row=1, column=2, sticky='ns')
        tk.Label(red_frame, text="Red Player", font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Radiobutton(red_frame, text="S", variable=self.red_choice, value='S').pack(anchor=tk.W)
        tk.Radiobutton(red_frame, text="O", variable=self.red_choice, value='O').pack(anchor=tk.W)
    
    def place_letter(self, row, col):
        #places selected letter on clicked board spot
        button =self.board[row][col]
        if button['text'] == '':
            button.config(text=self.current_letter.get())




