class BaseGameLogic:
    # base class logic for both simple and general games
    def __init__(self, size, board):
        self.size = size
        self.board = board
        self._scores = {'Blue': 0, 'Red': 0}
        self.winner = None

    def get_score(self, player):
        return self._scores[player]
    
    def place_letter(self, row, col, letter, player):
        if self.board[row][col] != '':
            return 0, None 
        
        self.board[row][col] = letter
        new_sos = self.check_sequences(row, col)
        self._scores[player] += new_sos
        print(f" Placed {letter}. SOS found: {new_sos}")
        winner = None
        if hasattr(self, 'check_winner_simple'):
            winner = self.check_winner_simple(player)
        elif hasattr(self, 'check_winner_general'):
            winner = self.check_winner_general(player)

        return new_sos, winner
        
    def check_sequences(self, row, col):
        # checks to see if an SOS sequence was made
        directions = [
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1)
    ]
        count = 0

        for dr, dc in directions:
            # case 1: current cell is in the middle (O)
            if self.is_sos( row - dr, col - dc, row, col, row + dr, col + dc):
                count += 1
            # case 2: current cell is the first S in SOS
            if self.is_sos( row, col, row + dr, col + dc, row + 2*dr, col + 2*dc):
                count += 1
            # case 3: current cell is the last S in SOS
            if self.is_sos( row - 2*dr, col - 2*dc, row - dr, col - dc, row, col):
                count += 1
        return count


    def is_sos(self, r1, c1, r2, c2, r3, c3):
        # returns true if postions form SOS
        if not (0 <= r1 < self.size and 0 <= c1 < self.size): 
            return False
        if not (0 <= r2 < self.size and 0 <= c2 < self.size): 
            return False
        if not (0 <= r3 < self.size and 0 <= c3 < self.size): 
            return False
        
        l1 = self.board[r1][c1] 
        l2=  self.board[r2][c2]
        l3 = self.board[r3][c3]

        return (
            l1 == 'S' and
            l2 == 'O' and
            l3 == 'S'
        )
    
    def is_board_full(self):
        # determine if board is full 
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
class SimpleGameLogic(BaseGameLogic):
    # logic for a simple game winner
    def check_winner_simple(self, player):
        if self.get_score(player) > 0:
            self.winner = player
        elif self.is_board_full() and not self.winner:
            self.winner = "Draw"
        return self.winner

class GeneralGameLogic(BaseGameLogic):
    # logic for a general game winner
    def check_winner_general(self, current_player):
        if self.is_board_full():
            Blue = self.get_score('Blue')
            Red = self.get_score('Red')
            if Red > Blue:
                self.winner = 'Red'
            elif Blue > Red:
                self.winner = 'Blue'
            else:
                self.winner = 'Draw' 
        return self.winner