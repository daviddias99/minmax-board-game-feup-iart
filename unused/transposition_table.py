class TranspositionTable():
    def __init__(self):
        self.table = { }

    def put(self, board, depth, score):
        key = board.get_key()

        self.table[key] = (score, depth)

    def lookup(self, board, depth):
        key = board.get_key()

        if key not in self.table:
            return None

        score_entry, depth_entry = self.table[key]

        if (depth_entry > depth):
            return score_entry
        else:
            return None
