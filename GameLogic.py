class BaseGameLogic:
    # base class logic for both simple and general games
    def __init__(self, size):
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.scores = {'Blue': 0, 'Red': 0}
        self.winner = None

class SimpleGameLogic(BaseGameLogic):
    # logic for a simple game

class GeneralGameLogic(BaseGameLogic):
    # logic for a general game