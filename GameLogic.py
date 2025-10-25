class BaseGameLogic:
    # base class logic for both simple and general games
    def __init__(self, size):
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.scores = {'Blue': 0, 'Red': 0}
        self.winner = None

    def _check_sequences(self, row, col):
        # checks to see if an SOS sequence was made
        directions = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1),
        (-1, -1), (1, 1),
        (-1, 1), (1, -1)
    ]
        count = 0
        
        for dr, dc in directions:
            # case 1: current cell is in the middle (O)
            if self._is_sos(row - dr, col - dc, row, col, row + dr, col + dc):
                count += 1
            # case 2: current cell is the first S in SOS
            if self._is_sos(row, col, row + dr, col + dc, row + 2*dr, col + 2*dc):
                count += 1
            # case 3: current cell is the last S in SOS
            if self._is_sos(row - 2*dr, col - 2*dc, row - dr, col - dc, row, col):
                count += 1

        return count

    def _is_sos(self, r1, c1, r2, c2, r3, c3):
        # returns true if postions form SOS
        if not (0 <= r1 < self.size and 0 <= c1 < self.size): 
            return False
        if not (0 <= r2 < self.size and 0 <= c2 < self.size): 
            return False
        if not (0 <= r3 < self.size and 0 <= c3 < self.size): 
            return False
        return (
            self.board[r1][c1] == 'S' and
            self.board[r2][c2] == 'O' and
            self.board[r3][c3] == 'S'
        )
    
class SimpleGameLogic(BaseGameLogic):
    # logic for a simple game winner
    def check_winner(self, player):
        if self.scores[player] > 0:
            self.winner = player
        return self.winner

class GeneralGameLogic(BaseGameLogic):
    # logic for a general game winner
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