import unittest
from GUI import GameSetupDialog
from GUI import SOSGame
from unittest.mock import patch
import tkinter as tk

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

    def test_invalid_size_input(self):
        dialog = GameSetupDialog.__new__(GameSetupDialog)  # bypass __init__
        dialog.top = self.root
        dialog.size_var = tk.StringVar(value='abc')
        dialog.mode_var = tk.StringVar(value='Simple')
        dialog.result = None

        with unittest.mock.patch('tkinter.messagebox.showerror') as mock_error:
            dialog.on_ok()
            mock_error.assert_called_once_with("Invalid Input", "Board size must be a number between 3 and 10.")
            self.assertIsNone(dialog.result)

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
        self.game.size = 3

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

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def test_place_letter_in_empty_spot(self):
        """AC 4.1 - Valid move places letter and switches player"""
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
        self.game.size = 3

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

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def test_place_letter_in_empty_spot(self):
        """AC 4.1 - Valid move places letter and switches player"""
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

if __name__ == "__main__":
    unittest.main()