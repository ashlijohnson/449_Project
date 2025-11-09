from GameLogic import BaseGameLogic

class ComputerPlayer(BaseGameLogic):
    def __init__(self, size, autoplayer):
        board = [['' for _ in range(size)] for _ in range(size)]
        super().__init__(size, board)
        self.autoplayer = autoplayer
        self.current_player = 'Blue'

        # if computer is starting player, move first automatically
        if self.current_player == autoplayer:
            self.make_move_auto()

    def reset_game(self):
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]
        self._scores = {'Blue': 0, 'Red': 0}
        self.winner = None
        self.current_player = 'Blue'

        if self.current_player == self.autoplayer:
            self.make_auto_move()

    def make_move(self, row, col, letter):
        # human or auto player makes a move
        new_sos, winner = super().place_letter(row, col, letter, self.current_player)

        if self.winner is None and self.current_player == self.autoplayer:
            self.make_auto_move()

        return new_sos, winner
    
    

