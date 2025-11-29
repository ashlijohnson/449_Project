class GameRecorder:
    def __init__(self):
        self.moves = []
        self.metadata = {}
        self.move_index = 0

    def record_move(self, row, col, letter, player, blue_score, red_score):
        self.moves.append((row, col, letter, player, blue_score, red_score))

    def save_to_file(self, filename="saved_game.txt"):
        if not self.moves:
            print("nothing to save")
            return
    
        with open(filename, "w") as f:
            for key, value in self.metadata.items():
                f.write(f"{key}={value}\n")
            f.write("\n")
            for row, col, letter, player, blue_score, red_score in self.moves:
                f.write(f"{row},{col},{letter},{player},{blue_score},{red_score} \n")

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
                parts = line.split(",")
                row = int(parts[0])
                col = int(parts[1])
                letter = parts[2].strip()
                player = parts[3].strip()
                blue_score = int(parts[4])
                red_score = int(parts[5])
                self.moves.append((row, col, letter, player, blue_score, red_score))