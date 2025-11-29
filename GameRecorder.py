class GameRecorder:
    def __init__(self):
        self.moves = []
        self.metadata = {}
        self.move_index = 0

    def record_move(self, row, col, letter, player):
        self.moves.append((row, col, letter, player))

    def save_to_file(self, filename="saved_game.txt"):
        if not self.moves:
            print("nothing to save")
            return
    
        with open(filename, "w") as f:
            for key, value in self.metadata.items():
                f.write(f"{key}={value}\n")
            f.write("\n")
            for row, col, letter, player in self.moves:
                f.write(f"{row}, {col}, {letter}, {player}\n")

        self.moves = []
        self.move_index = 0

    def load_from_file(self, filename="saved_game.txt"):
        lines = open(filename).read().strip().split("\n")

        self.metadata = {}
        self.moves = []

        for line in lines:
            if "=" in line:
                key, value = line.split("=")
                self.metadata[key] = value
            elif "," in line:
                row, col, letter, player = line.split(",")
                self.moves.append((int(row), int(col), letter, player))