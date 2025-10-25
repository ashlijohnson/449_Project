class BaseGameLogic:
    # base class logic for both simple and general games
    def __init__(self, size):
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.scores = {'Blue': 0, 'Red': 0}
        self.winner = None

class SimpleGameLogic(BaseGameLogic):
    # logic for a simple game
    def check_winner(self, player):
        if self.scores[player] > 0:
            self.winner = player
        return self.winner

class GeneralGameLogic(BaseGameLogic):
    # logic for a general game
    def check_winner(self, current_player):
        Blue = self.scores['Blue']
        Red = self.scores['Red']
        if Red > Blue:
            self.winner = 'Red'
        elif Blue > Red:
            self.winner = 'Blue'
        else:
            self.winner = 'Draw' 
        return self.winner