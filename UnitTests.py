import unittest
from GUI import GameSetupDialog
from GUI import SOSGame
from unittest.mock import patch
import tkinter as tk
from GameLogic import SimpleGameLogic, GeneralGameLogic

class TestBoardSizeValidation(unittest.TestCase):
    def test_valid_board_size(self):
        #AC 1.1
        valid_inputs = ['3', '4', '5', '6', '7', '8', '9', '10']
        for input_val in valid_inputs:
            valid, result = GameSetupDialog.validate_board_size(input_val)
            self.assertTrue(valid)
            self.assertEqual(result, int(input_val))
            
    def test_invalid_board_size_too_small(self):
            # AC 1.2
            invalid_inputs = ['0', '1', '2']
            for input_val in invalid_inputs:
                valid, message = GameSetupDialog.validate_board_size(input_val)
                self.assertFalse(valid)
                self.assertEqual(message, "Board size must be between 3 and 10.")

    def test_invalid_board_size_too_large(self):
        # AC 1.2
        invalid_inputs = ['15', '100']
        for input_val in invalid_inputs:
            valid, message = GameSetupDialog.validate_board_size(input_val)
            self.assertFalse(valid)
            self.assertEqual(message, "Board size must be between 3 and 10.")

    def test_invalid_board_size_non_numeric(self):
        # AC 1.2
        invalid_inputs = ['abc', '', '5.5', ' ']
        for input_val in invalid_inputs:
            valid, message = GameSetupDialog.validate_board_size(input_val)
            self.assertFalse(valid)
            self.assertEqual(message, "Invalid input: not a number.")

    def test_no_selection_of_board_size(self):
        # AC 1.3
        valid, message = GameSetupDialog.validate_board_size('')
        self.assertFalse(valid)
        self.assertEqual(message, "Invalid input: not a number.")

class TestGameSetupDialog(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent GUI from showing

    def tearDown(self):
        try:
            if self.root:
                self.root.destroy()
        except tk.TclError:
    # Window already destroyed, ignore
            pass

    def test_simple_game_selection(self):
        #AC 2.1
        dialog = GameSetupDialog.__new__(GameSetupDialog)  # bypass __init__
        dialog.top = self.root
        dialog.size_var = tk.StringVar(value='5')
        dialog.mode_var = tk.StringVar(value='Simple')
        dialog.result = None

        dialog.on_ok()
        self.assertEqual(dialog.result, (5, 'Simple'))

    def test_general_game_selection(self):
        #AC 2.2
        dialog = GameSetupDialog.__new__(GameSetupDialog)  # bypass __init__
        dialog.top = self.root
        dialog.size_var = tk.StringVar(value='7')
        dialog.mode_var = tk.StringVar(value='General')
        dialog.result = None

        dialog.on_ok()
        self.assertEqual(dialog.result, (7, 'General'))

class TestGameSetupStart(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent GUI from showing

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def create_dialog_without_init(self):
        # Bypass __init__ to avoid GUI interactions
        dialog = GameSetupDialog.__new__(GameSetupDialog)
        dialog.top = self.root  # Set top to a real root
        dialog.result = None
        return dialog

    @patch('tkinter.messagebox.showerror')
    def test_valid_start_game(self, mock_error):
        """AC 3.1 - Game starts with valid size and mode"""
        dialog = self.create_dialog_without_init()
        dialog.size_var = tk.StringVar(value="6")
        dialog.mode_var = tk.StringVar(value="General")

        dialog.on_ok()

        self.assertEqual(dialog.result, (6, "General"))
        mock_error.assert_not_called()

    @patch('tkinter.messagebox.showerror')
    def test_invalid_size_non_numeric(self, mock_error):
        """AC 3.2 - Invalid size (non-numeric) shows error, does not start game"""
        dialog = self.create_dialog_without_init()
        dialog.size_var = tk.StringVar(value="abc")
        dialog.mode_var = tk.StringVar(value="Simple")

        dialog.on_ok()

        self.assertIsNone(dialog.result)
        mock_error.assert_called_once_with("Invalid Input", "Board size must be a number between 3 and 10.")

    @patch('tkinter.messagebox.showerror')
    def test_invalid_size_too_small(self, mock_error):
        """AC 3.2 - Invalid size (too small) shows error, does not start game"""
        dialog = self.create_dialog_without_init()
        dialog.size_var = tk.StringVar(value="2")
        dialog.mode_var = tk.StringVar(value="Simple")

        dialog.on_ok()

        self.assertIsNone(dialog.result)
        mock_error.assert_called_once()

    @patch('tkinter.messagebox.showerror')
    def test_invalid_size_too_large(self, mock_error):
        """AC 3.2 - Invalid size (too large) shows error, does not start game"""
        dialog = self.create_dialog_without_init()
        dialog.size_var = tk.StringVar(value="15")
        dialog.mode_var = tk.StringVar(value="General")

        dialog.on_ok()

        self.assertIsNone(dialog.result)
        mock_error.assert_called_once()

class TestSimpleGameMove(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        # Create game manually to control setup
        self.game = SOSGame.__new__(SOSGame)
        self.game.window = self.root
        self.game.current_player = "Blue"
        self.game.blue_choice = tk.StringVar(value='S')
        self.game.red_choice = tk.StringVar(value='O')
        self.game.game_mode = tk.StringVar(value='Simple')
        self.game.blue_score = 0
        self.game.red_score = 0
        self.game.size = 3
        self.game.blue_score_label = tk.Label(self.root)
        self.game.red_score_label = tk.Label(self.root)

        # Create a dummy board: 3x3 buttons
        self.game.board = []
        for r in range(3):
            row = []
            for c in range(3):
                btn = tk.Button(self.root, text='', width=4, height=2)
                row.append(btn)
            self.game.board.append(row)

        # Create dummy label for status
        self.game.status_label = tk.Label(self.root)

        self.game.logic = SimpleGameLogic(self.game.size, self.game.board)

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def test_place_letter_in_empty_spot(self):
        """AC 4.1 - Valid move places letter and switches player"""
        self.logic = SimpleGameLogic(self.game.size, self.game.board)
        self.game.place_letter(0, 0)

        # The button should now have 'S' (Blue's choice)
        self.assertEqual(self.game.board[0][0]['text'], 'S')

        # Turn should have switched to Red
        self.assertEqual(self.game.current_player, 'Red')
        self.assertIn("Red", self.game.status_label['text'])

    @patch('tkinter.messagebox.showerror')
    def test_place_letter_in_taken_spot(self, mock_error):
        """AC 4.2 - Invalid move shows error and does not switch turn"""
        # Simulate a taken spot
        self.game.board[1][1].config(text='O')

        # Blue tries to play on the same spot
        self.game.place_letter(1, 1)

        # Error should be shown
        mock_error.assert_called_once_with("Invalid Move", "This spot is already taken!")

        # Player should still be Blue
        self.assertEqual(self.game.current_player, 'Blue')

        # The button text should still be 'O'
        self.assertEqual(self.game.board[1][1]['text'], 'O')

class TestGeneralGameMove(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

        # Create game manually to control setup
        self.game = SOSGame.__new__(SOSGame)
        self.game.window = self.root
        self.game.current_player = "Blue"
        self.game.blue_choice = tk.StringVar(value='S')
        self.game.red_choice = tk.StringVar(value='O')
        self.game.game_mode = tk.StringVar(value='General')
        self.game.blue_score = 0
        self.game.red_score = 0
        self.game.size = 3
        self.game.blue_score_label = tk.Label(self.root)
        self.game.red_score_label = tk.Label(self.root)

        # Create a dummy board: 3x3 buttons
        self.game.board = []
        for r in range(3):
            row = []
            for c in range(3):
                btn = tk.Button(self.root, text='', width=4, height=2)
                row.append(btn)
            self.game.board.append(row)

        # Create dummy label for status
        self.game.status_label = tk.Label(self.root)

        self.game.logic = GeneralGameLogic(self.game.size, self.game.board)
    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def test_place_letter_in_empty_spot(self):
        """AC 6.1 - Valid move places letter and switches player"""
        self.game.place_letter(0, 0)

        # The button should now have 'S' (Blue's choice)
        self.assertEqual(self.game.board[0][0]['text'], 'S')

        # Turn should have switched to Red
        self.assertEqual(self.game.current_player, 'Red')
        self.assertIn("Red", self.game.status_label['text'])

    @patch('tkinter.messagebox.showerror')
    def test_place_letter_in_taken_spot(self, mock_error):
        """AC 6.2 - Invalid move shows error and does not switch turn"""
        # Simulate a taken spot
        self.game.board[1][1].config(text='O')

        # Blue tries to play on the same spot
        self.game.place_letter(1, 1)

        # Error should be shown
        mock_error.assert_called_once_with("Invalid Move", "This spot is already taken!")

        # Player should still be Blue
        self.assertEqual(self.game.current_player, 'Blue')

        # The button text should still be 'O'
        self.assertEqual(self.game.board[1][1]['text'], 'O')

def make_board(size, fill=''):
    # helper to make board
    return [[{'text': fill} for _ in range(size)] for _ in range(size)]

class EndSimpleGameLogic(unittest.TestCase):

    def set_up(self):
        # creates simple game logic instance before test
        self.size = 3
        self.board = make_board(self.size)
        self.logic = SimpleGameLogic(self.size, self.board)

    def player_gets_sos_game_ends(self):
        # AC 5.1
        self.board[1][0]['text'] = 'S'
        self.board[1][1]['text'] = 'O'
        self.board[1][2]['text'] = 'S'

        new_sos = self.logic.check_sequences(1,1)
        self.logic.scores['Blue'] += new_sos

        winner = self.logic.check_winner_simple('Blue')

        self.assertGreater(new_sos, 0)
        self.assertEqual(winner, 'Blue')
        self.assertEqual(self.logic.winner, 'Blue')

    def player_does_not_get_sos(self):
        # AC 5.2 
        self.board[0][0]['text'] = 'S'
        self.board[0][1]['text'] = 'O'
        self.board[1][1]['text'] = 'S'  

        new_sos = self.logic.check_sequences(1, 1)
        self.logic.scores['Red'] += new_sos

        winner = self.logic.check_winner_simple('Red')

        self.assertEqual(new_sos, 0)
        self.assertIsNone(winner)
        self.assertIsNone(self.logic.winner)

    def board_full_no_sos_draw(self):
        # AC 5.3 
        board = make_board(3, fill='O')
        logic = SimpleGameLogic(3, board)

        self.assertTrue(logic.is_board_full())

        winner = logic.check_winner_simple('Blue')

        self.assertEqual(winner, 'Draw')
        self.assertEqual(logic.winner, 'Draw')

class EndGeneralGameLogic(unittest.TestCase):
    
    def setUp(self):
        # creates a general game logic instance before each test
        self.size = 3
        self.board = make_board(self.size)
        self.logic = GeneralGameLogic(self.size, self.board)

    def one_player_has_more_sos_sequences(self):
        # AC 7.1
        self.logic.scores = {'Blue': 3, 'Red': 1}
        full_board = make_board(self.size, fill = 'S')
        self.logic.board = full_board

        self.assertTrue(self.logic.is_board_full())
        winner = self.logic.check_winner_general('Blue')

        self.assertEqual(winner, 'Blue')
        self.assertEqual(self.logic.winner, 'Blue')

    def both_players_same_number_of_sequences(self):
        # AC 7.2
        self.logic.scores = {'Blue': 2, 'Red': 2}
        full_board = make_board(self.size, fill='O')
        self.logic.board = full_board

        self.assertTrue(self.logic.is_board_full())
        winner = self.logic.check_winner_general('Red')

        self.assertEqual(winner, 'Draw')
        self.assertEqual(self.logic.winner, 'Draw')


if __name__ == "__main__":
    unittest.main()