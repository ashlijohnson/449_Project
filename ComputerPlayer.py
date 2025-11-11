from abc import ABC, abstractmethod
import random 

class Player(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def make_move(self, game_logic):
        pass
        
class HumanPlayer(Player):
    def make_move(self, game_logic, current_player):
        return None

class ComputerPlayer(Player):
    def make_move(self, logic_board, current_player):
        size = len(logic_board)
        empty_cells = [(r, c) for r in range(size)
                       for c in range(size)
                       if logic_board[r][c] == '']
        if not empty_cells:
            return None
        
        row, col = random.choice(empty_cells)
        letter = random.choice(['S', 'O'])
        return row, col, letter

