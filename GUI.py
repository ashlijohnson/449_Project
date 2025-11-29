import tkinter as tk
from tkinter import messagebox
from GameLogic import SimpleGameLogic, GeneralGameLogic
from PlayerTypes import ComputerPlayer, HumanPlayer
from GameRecorder import GameRecorder

class SOSGame:
    def __init__(self, window):
        #establishes basic board components
        self.window = window
        self.window.title("SOS Game")
        self.window.geometry("600x600")
        self.game_active = True

        self.board = []
        self.size = 0

        self.current_player = "Blue"
        self.game_mode = tk.StringVar(value='Simple')
        self.blue_choice = tk.StringVar(value='S')
        self.red_choice = tk.StringVar(value='S')

        self.logic_board = [['' for _ in range(self.size)] for _ in range(self.size)]

        self.recorder = GameRecorder()

        self.setup_menu()

    def setup_menu(self):
        dialog = GameSetupDialog(self.window)
        if not dialog.result:
            messagebox.showerror("Game Cancelled", "You must complete setup to start the game.")
            self.window.destroy()
            return

        self.size, mode, blue_type, red_type = dialog.result
        self.game_mode.set(mode)
        
        if blue_type == "Computer":
            self.blue_player = ComputerPlayer("Blue")
        else: 
            self.blue_player = HumanPlayer("Blue")

        if red_type == "Computer":
            self.red_player = ComputerPlayer("Red")
        else: 
            self.red_player = HumanPlayer("Red")

        self.recorder.metadata = {
            "size": self.size,
            "mode": self.game_mode.get(),
            "blue": type(self.blue_player).__name__,
            "red": type(self.red_player).__name__
        }

        self.create_board()

    def create_board(self):
        self.board = []
        self.logic_board = [['' for _ in range(self.size)] for _ in range(self.size)]

        #creates top frame with game mode 
        top_frame = tk.Frame(self.window, pady=10)
        top_frame.grid(row=0, column=0, columnspan=3)

        #shows current player
        self.status_label = tk.Label(self.window, text="Current Turn: Blue", font=('Arial', 12, 'bold'))
        self.status_label.grid(row=2, column=0, columnspan=3, pady=10)

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
                                command = lambda r=row, c=col: self.on_button_click(r,c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(btn)
            self.board.append(row_buttons)

        #creates blue player's section
        blue_frame = tk.Frame(main_frame, padx=10, pady=10)
        blue_frame.grid(row=1, column=0, sticky='ns')
        self.blue_score_label = tk.Label(blue_frame, text="Score: 0", font=('Arial', 12))
        self.blue_score_label.pack(pady=5)
        tk.Label(blue_frame, text="Blue Player", font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Radiobutton(blue_frame, text="S", variable=self.blue_choice, value='S').pack(anchor=tk.W)
        tk.Radiobutton(blue_frame, text="O", variable=self.blue_choice, value='O').pack(anchor=tk.W)

        #creates red player's section
        red_frame = tk.Frame(main_frame, padx=10, pady=10)
        red_frame.grid(row=1, column=2, sticky='ns')
        self.red_score_label = tk.Label(red_frame, text="Score: 0", font=('Arial', 12))
        self.red_score_label.pack(pady=5)
        tk.Label(red_frame, text="Red Player", font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Radiobutton(red_frame, text="S", variable=self.red_choice, value='S').pack(anchor=tk.W)
        tk.Radiobutton(red_frame, text="O", variable=self.red_choice, value='O').pack(anchor=tk.W)
    
        #reset game
        new_game_btn = tk.Button(self.window, text = "New Game", command=self.new_game, font=('Arial', 12))
        new_game_btn.grid(row=3, column=0, columnspan=3, pady=10)

        #save game
        save_game = tk.Button(self.window, text= "Save Game", command=self.save_game, font=('Arial', 12))
        save_game.grid(row=5, column=0, columnspan=3, pady= 10)

        self.logic_board = [['' for _ in range(self.size)] for _ in range(self.size)]
        if self.game_mode.get() == 'Simple':
            self.logic = SimpleGameLogic(self.size, self.logic_board)
        else:
            self.logic = GeneralGameLogic(self.size, self.logic_board)

        self.play_turn()

    def on_button_click(self, row, col):
        if not self.game_active:
            return
        
        if self.current_player == "Blue":
            current_player_obj = self.blue_player
        else:
            current_player_obj = self.red_player

        if isinstance(current_player_obj, ComputerPlayer):
            return

        if self.current_player == "Blue":
            self.handle_move(row, col, self.blue_choice.get())
        else:
            self.handle_move(row, col, self.red_choice.get())

    def handle_move(self, row, col, letter):
        button = self.board[row][col]
        if button['text'] != '':
            messagebox.showerror("Invalid Move", "This spot is already taken!")
            return
        
        button.config(text=letter)

        new_sos, winner = self.logic.place_letter(row, col, letter, self.current_player)
        self.update_scores()
        self.recorder.record_move(row, col, letter, self.current_player)

        if winner is not None:
            self.end_game(winner)
            return
        elif self.logic.is_board_full():
            self.end_game("Draw")
            return
        
        self.switch_player()
        
        if self.current_player == "Blue":
            next_player_obj = self.blue_player
        else:
            next_player_obj = self.red_player

        if isinstance(next_player_obj, ComputerPlayer):
            self.window.after(500, self.computer_move)
        else:
            return

    def update_scores(self):
        self.blue_score_label.config(text=f"Score: {self.logic.get_score('Blue')}")
        self.red_score_label.config(text=f"Score: {self.logic.get_score('Red')}")
   
    def switch_player(self):
        self.current_player = "Red" if self.current_player=='Blue' else "Blue"
        self.status_label.config(text=f"Current Turn: {self.current_player}")

    def computer_move(self):
        if not self.game_active:
            return
        
        if self.current_player == "Blue":
             player = self.blue_player
        else:
            player = self.red_player
            
        move = player.make_move(self.logic, self.current_player)

        if move is None:
            if self.logic.is_board_full():
                self.end_game("Draw")
            return

        row, col, letter = move 
        self.handle_move(row, col, letter)

    def play_turn(self):
        if self.current_player == "Blue":
            player = self.blue_player
        else:
            player = self.red_player

        if isinstance(player, HumanPlayer):
            return
        else:
            self.window.after(500, lambda: self.computer_move())

    def end_game(self, winner):
        self.game_active = False
        if winner == "Draw":
            msg = "It's a draw!"
        else:
            msg = f"{winner} wins!"

        if messagebox.askyesno("Game Over", f"{msg} Play again?"):
            self.new_game()
        else:
            for row in self.board:
                for btn in row:
                    btn.config(state=tk.DISABLED)

    def new_game(self):
        #destroy existing board and reset
        for widget in self.window.winfo_children():
            widget.destroy()

        self.board = []
        self.current_player = "Blue"
        self.blue_choice.set('S')
        self.red_choice.set('S')
        self.game_mode.set('Simple')
        self.game_active = True

        if hasattr(self, 'logic'):
            self.logic._scores = {'Blue': 0, 'Red': 0}
            self.logic.winner = None
        if self.game_mode.get() == 'Simple':
           self.logic = SimpleGameLogic(self.size, [['' for _ in range(self.size)] for _ in range(self.size)])
        else:
            self.logic = GeneralGameLogic(self.size, [['' for _ in range(self.size)] for _ in range(self.size)])

        self.setup_menu()

    def save_game(self):
        self.recorder.save_to_file()
        messagebox.showinfo("Saved", "Game saved!")

    def reset_board(self):
        for row in range(self.size):
            for col in range(self.size):
                self.cells[row][col].config(bg="white") 

    def place_token_replay(self, color, row, col):
        widget = self.cells[row][col]

    def start_replay(self):
        self.reset_board()
        self.recorder.move_index = 0
        self.is_replay_mode = True
        self.status_label.config(text= "Replay: Ready")

        print("Replay started. Moves:", len(self.recorder.moves))

    def replay_next_move(self):
        if self.recorder.move_index >= len(self.recorder.moves):
            self.status_label.config(text="Replay finished!")
            return
        
        color, row, col = self.recorder.moves[self.recorder.move_index]
        
        self.place_token_replay(color, row, col)

        self.recorder.move_index += 1

class GameSetupDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Game Setup")
        self.top.geometry("300x500")
        self.top.resizable(False, False)
        self.result = None  #will store (size, mode)

        tk.Label(self.top, text="Enter Board Size (3-10):", font=('Arial', 11)).pack(pady=(10, 5))
        self.size_var = tk.StringVar()
        self.size_entry = tk.Entry(self.top, textvariable=self.size_var)
        self.size_entry.pack()

        tk.Label(self.top, text="Select Game Mode:", font=('Arial', 11)).pack(pady=(15, 5))
        self.mode_var = tk.StringVar(value="Simple")
        tk.Radiobutton(self.top, text="Simple Game", variable=self.mode_var, value="Simple").pack(anchor='w', padx=30)
        tk.Radiobutton(self.top, text="General Game", variable=self.mode_var, value="General").pack(anchor='w', padx=30)

        tk.Label(self.top, text= "Blue Player:", font=('Arial', 11)).pack(pady=(15, 5))
        self.blue_type = tk.StringVar(value= "Human")
        tk.Radiobutton(self.top, text="Human", variable=self.blue_type, value="Human").pack(anchor='w', padx=30)
        tk.Radiobutton(self.top, text="Computer", variable=self.blue_type, value="Computer").pack(anchor='w', padx=30)
        
        tk.Label(self.top, text= "Red Player:", font=('Arial', 11)).pack(pady=(15, 5))
        self.red_type = tk.StringVar(value= "Human")
        tk.Radiobutton(self.top, text="Human", variable=self.red_type, value="Human").pack(anchor='w', padx=30)
        tk.Radiobutton(self.top, text="Computer", variable=self.red_type, value="Computer").pack(anchor='w', padx=30)

        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.RIGHT, padx=5)

        #center and block interaction
        self.top.grab_set()
        parent.wait_window(self.top)

    def is_valid_board_size(self, value):
        try:
            size = int(value)
            return 3 <= size <= 10
        except ValueError:
            return False   

    def validate_board_size(value):
        #test board size is valid input
        try:
            size = int(value)
            if 3 <= size <= 10:
                return True, size
            return False, "Board size must be between 3 and 10."
        except ValueError:
            return False, "Invalid input: not a number."
    
    def on_ok(self):
        #when user clicks "OK"
        try:
            size = int(self.size_var.get())
            if size < 3 or size > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Board size must be a number between 3 and 10.")
            return
        
        mode = self.mode_var.get()
        blue_player_type = self.blue_type.get()
        red_player_type = self.red_type.get()
        self.result = (size, mode, blue_player_type, red_player_type)
        self.top.destroy()

    def on_cancel(self):
        #when user clicks "Cancel"
        self.result = None
        self.top.destroy()



