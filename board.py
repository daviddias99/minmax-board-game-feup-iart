import sys


class Board():
    def __init__(self, boards=None):
        self.columns = 8
        self.rows = 8
        self.size = self.columns * self.rows
        self.nplayers = 2
        self.board = self.new_game_boards() if boards is None else boards

    def new_game_boards(self):
        """
            Initializes the game
        """
        board = [
            [0, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 2, 0, 0, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0]
        ]

        return board

    def get_element(self, column, row):
        """
            Gets piece at row, column. Row and Column from 1 to 8
            Returns 0 if empty, player_number otherwise
        """
        return self.board[row - 1][column - 1]

    def set_element(self, column, row, player):
        """
            Sets player piece at row, column. Row and Column from 1 to 8
            Player is from 1 to N
        """
        self.board[row - 1][column - 1] = player

    def remove_element(self, column, row):
        """
            Remove piece from position row, column
            (Sets cell to 0)
        """
        self.board[row - 1][column - 1] = 0

    def test_row_empty(self, row):
        """
            Test if there is empty spaces in a row
        """
        for v in self.board[row - 1]:
            if v == 0:
                return True

        return False

    def pieces(self, player):
        """
            Player must be either 1 or 2
            Returns where all the pieces off the player are in a list with column, row tuples
        """

        return [(x + 1, y + 1) for y, row in enumerate(self.board) for x, piece in enumerate(row) if piece == player]

    def print(self):
        for i in range(self.nplayers):
            print(bin(self.boards[1]))

    def print_board(self, f=sys.stdout):

        print("   1 2 3 4 5 6 7 8  ", file=f)
        print(" -------------------", file=f)
        for i in range(1, 9):

            row = str(i) + "| "
            for j in range(1, 9):

                if(self.get_element(j, i) == 1):
                    row = row + "X"
                elif(self.get_element(j, i) == 2):
                    row = row + "O"
                else:
                    row = row + "."

                row = row + " "

            row = row + "|"

            print(row, file=f)

        print(" -------------------", file=f)

    def init_from_matrix(self, matrix):

        for i in range(1, 9):

            for j in range(1, 9):

                self.remove_element(j, i)

        for i in range(1, 9):

            for j in range(1, 9):

                if(matrix[i-1][j-1] != 0):
                    self.set_element(j, i, matrix[i-1][j-1])
                else:
                    self.remove_element(j, i)

    def normalized_pieces(self, player):
        pieces = self.pieces(player)

        if player == 1:
            pieces = [(x, 9 - y) for (x, y) in pieces]

        return pieces

    def column_control(self, player):

        result = [0 for i in range(8)]

        for i in range(8):
            for j in range(8):

                if self.board[j][i] == player:
                    result[i] = 1
                elif self.board[j][i] != 0:
                    result[i] = 0
                    break

        return sum(result)

    @classmethod
    def from_binary_matrix(cls, bm):

        new_board = [row.copy() for row in bm.board]

        return cls(boards=new_board)
