from abc import ABC, abstractmethod
import random 

class Player(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def make_move(self, game_logic):
        pass
        
class HumanPlayer(Player):
    def make_move(self, game_logic):
        pass

class ComputerPlayer(Player):
    def make_move(self, game_logic):
        size = game_logic.size
        empty_cells = [(r, c) for r in range(size)
                       for c in range(size)
                       if game_logic.board[r][c] == '']
        if not empty_cells:
            return None
        
        row, col = random.choice(empty_cells)
        letter = random.choice(['S', 'O'])
        new_sos, winner = game_logic.placeletter(row, col, letter, self.color)
        return (row, col, letter, winner)

