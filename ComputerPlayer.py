from abc import ABC, abstractmethod
import random 
from GameLogic import GeneralGameLogic

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

    def make_move(self, game_logic, current_player):
        move = self.make_winning_move(game_logic, current_player)
        if move:
            return move
        
        if current_player == 'Blue':
            opponent = 'Red'
        else:
            opponent = 'Blue'
        move = self.block_opponent_winning_move(game_logic, opponent)
        if move:
            return move
        
        return self.make_random_move(game_logic, current_player)
    
    def make_random_move(self, game_logic, current_player):
        size = game_logic.size
        empty_cells = [(r, c) for r in range(size)
                       for c in range(size)
                       if game_logic.board[r][c] == '']
        if not empty_cells:
            return None
        
        row, col = random.choice(empty_cells)
        letter = random.choice(['S', 'O'])
        return row, col, letter
    
    def make_winning_move(self, game_logic, player):
        return self.find_sos_move(game_logic, player)
    
    def block_opponent_winning_move(self, game_logic, opponent):
        return self.find_sos_move(game_logic, opponent)
    
    def find_sos_move(self, game_logic, player):
        size = game_logic.size
        for r in range(size):
            for c in range(size):
                if game_logic.board[r][c] != '':
                    continue
                for letter in ['S', 'O']:
                    game_logic.board[r][c] = letter
                    if game_logic.check_sequences(r,c) > 0:
                        game_logic.board[r][c] = ''
                        return r,c,letter
                    game_logic.board[r][c] = ''
        return None
    