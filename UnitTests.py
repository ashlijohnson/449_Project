import unittest
from GUI import GameSetupDialog
from GUI import SOSGame
from unittest.mock import patch, MagicMock
import tkinter as tk
from GameLogic import SimpleGameLogic, GeneralGameLogic, BaseGameLogic
from PlayerTypes import HumanPlayer, ComputerPlayer

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
        dialog.blue_type = tk.StringVar(value="Human")
        dialog.red_type = tk.StringVar(value="Human")

        dialog.on_ok()
        self.assertEqual(dialog.result, (5, 'Simple', 'Human', 'Human'))

    def test_general_game_selection(self):
        #AC 2.2
        dialog = GameSetupDialog.__new__(GameSetupDialog)  # bypass __init__
        dialog.top = self.root
        dialog.size_var = tk.StringVar(value='7')
        dialog.mode_var = tk.StringVar(value='General')
        dialog.result = None
        dialog.blue_type = tk.StringVar(value="Human")
        dialog.red_type = tk.StringVar(value="Human")

        dialog.on_ok()
        self.assertEqual(dialog.result, (7, 'General', 'Human', 'Human'))

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
        dialog.blue_type = tk.StringVar(value="Human")
        dialog.red_type = tk.StringVar(value="Human")
        return dialog

    @patch('tkinter.messagebox.showerror')
    def test_valid_start_game(self, mock_error):
        """AC 3.1 - Game starts with valid size and mode"""
        dialog = self.create_dialog_without_init()
        dialog.size_var = tk.StringVar(value="6")
        dialog.mode_var = tk.StringVar(value="General")

        dialog.on_ok()

        self.assertEqual(dialog.result, (6, "General", "Human", "Human"))
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

class MockButton:
    def __init__(self):
        self.text = ''
    def config(self, text):
        self.text = text

class TestSimpleGameMove(unittest.TestCase):
    def setUp(self):
        self.game = type('SOSGame', (), {})()
        self.game.current_player = 'Blue'
        self.game.game_active = True
        self.game.board = [[MockButton() for _ in range(3)] for _ in range(3)]
        
        self.game.switch_player = lambda: setattr(self.game, 'current_player', 'Red' if self.game.current_player == 'Blue' else 'Blue')

        def handle_move(row, col, letter):
            button = self.game.board[row][col]
            if button.text != '':
                import tkinter.messagebox as messagebox
                messagebox.showerror("Invalid Move", "This spot is already taken!")
                return
            button.config(text=letter)
            self.game.switch_player()
        self.game.handle_move = handle_move

    # AC 4.1
    def test_place_letter_in_empty_spot(self):
        self.game.handle_move(0, 0, 'S')
        self.assertEqual(self.game.board[0][0].text, 'S')
        self.assertEqual(self.game.current_player, 'Red') 

    # AC 4.2
    @patch('tkinter.messagebox.showerror')
    def test_place_letter_in_taken_spot(self, mock_showerror):
        self.game.board[0][0].text = 'O'
        original_player = self.game.current_player
        self.game.handle_move(0, 0, 'S')
        self.assertEqual(self.game.board[0][0].text, 'O') 
        self.assertEqual(self.game.current_player, original_player)  
        mock_showerror.assert_called_once_with("Invalid Move", "This spot is already taken!")

class TestGeneralGameMove(unittest.TestCase):
    def setUp(self):
        self.game = type('SOSGame', (), {})() 
        self.game.current_player = 'Blue'
        self.game.game_active = True
        self.game.board = [[MockButton() for _ in range(3)] for _ in range(3)]
        
        self.game.switch_player = lambda: setattr(self.game, 'current_player', 'Red' if self.game.current_player == 'Blue' else 'Blue')
        self.game.update_scores = lambda: None
        self.game.end_game = lambda winner: None
        
        self.game.logic = type('Logic', (), {'place_letter': lambda self, r, c, l, p: (0, None), 'is_board_full': lambda self: False})()

        def handle_move(row, col, letter):
            button = self.game.board[row][col]
            if button.text != '':
                import tkinter.messagebox as messagebox
                messagebox.showerror("Invalid Move", "This spot is already taken!")
                return
            button.config(text=letter)
            new_sos, winner = self.game.logic.place_letter(row, col, letter, self.game.current_player)
            self.game.update_scores()
            if winner is not None:
                self.game.end_game(winner)
                return
            elif self.game.logic.is_board_full():
                self.game.end_game("Draw")
                return
            self.game.switch_player()
        self.game.handle_move = handle_move

    # AC 6.1
    def test_place_letter_in_empty_spot(self):
        self.game.handle_move(0, 0, 'S')
        self.assertEqual(self.game.board[0][0].text, 'S')
        self.assertEqual(self.game.current_player, 'Red')  

    # AC 6.2
    @patch('tkinter.messagebox.showerror')
    def test_place_letter_in_taken_spot(self, mock_showerror):
        self.game.board[0][0].text = 'O'
        original_player = self.game.current_player
        self.game.handle_move(0, 0, 'S')
        self.assertEqual(self.game.board[0][0].text, 'O')  
        self.assertEqual(self.game.current_player, original_player) 
        mock_showerror.assert_called_once_with("Invalid Move", "This spot is already taken!")

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

class TestPlayerSelection(unittest.TestCase):
    @patch('GUI.GameSetupDialog')
    def test_one_player_computer(self, MockDialog):
        # AC 8.1
        MockDialog.return_value.result = (5, "Simple", "Computer", "Human")
        
        root = tk.Tk()
        game = SOSGame(root)

        self.assertIsInstance(game.blue_player, ComputerPlayer)
        self.assertIsInstance(game.red_player, HumanPlayer)

        root.destroy()

    @patch('GUI.GameSetupDialog')
    def test_both_players_computer(self, Mockdialog):
        # AC 8.2
        Mockdialog.return_value.result = (5, "Simple", "Computer", "Computer")

        root = tk.Tk()
        game = SOSGame(root)

        self.assertIsInstance(game.blue_player, ComputerPlayer)
        self.assertIsInstance(game.red_player, ComputerPlayer)

        root.destroy()

    @patch('GUI.GameSetupDialog')
    def test_both_players_human(self, Mockdialog):
        # AC 8.3
        Mockdialog.return_value.result = (5, "Simple", "Human", "Human")

        root = tk.Tk()
        game = SOSGame(root)

        self.assertIsInstance(game.blue_player, HumanPlayer)
        self.assertIsInstance(game.red_player, HumanPlayer)

        root.destroy()  

class TestComputerPlayer(unittest.TestCase):
    def setUp(self):
        self.cpu = ComputerPlayer("Blue")

    # AC 9.1 
    def test_computer_finds_sos(self):
        board = [
            ['S', '', 'S'],
            ['', '', ''],
            ['', '', '']
        ]
        size = 3
        game_logic = BaseGameLogic(size, board)
        
        move = self.cpu.make_move(game_logic, 'Blue')
        row, col, letter = move

        self.assertEqual((row, col, letter), (0, 1, 'O'))

    # AC 9.2 
    def test_computer_random_move_no_sos(self):
        board = [
            ['S', 'O', 'S'],
            ['O', 'S', 'O'],
            ['', '', '']
        ]
        size = 3
        game_logic = BaseGameLogic(size, board)

        import random
        original_choice = random.choice
        try:
            random.choice = lambda x: x[0]  
            move = self.cpu.make_move(game_logic, 'Blue')
            row, col, letter = move
            self.assertEqual((row, col), (2,0))
            self.assertIn(letter, ['S','O'])
        finally:
            random.choice = original_choice

if __name__ == "__main__":
    unittest.main()