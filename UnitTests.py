import unittest
from GUI import GameSetupDialog
from GUI import SOSGame

class TestBoardSizeValidation(unittest.TestCase):
    def test_valid_board_size(self):
        #AC 1.1
        valid_inputs = ['3', '4', '5', '6', '7', '8', '9']
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
            self.assertEqual(message, "Board size must be between 3 and 9.")

def test_invalid_board_size_too_large(self):
    # AC 1.2
    invalid_inputs = ['10', '15', '100']
    for input_val in invalid_inputs:
        valid, message = GameSetupDialog.validate_board_size(input_val)
        self.assertFalse(valid)
        self.assertEqual(message, "Board size must be between 3 and 9.")

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

if __name__ == "__main__":
    unittest.main()