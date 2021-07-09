import copy
from bitarray import bitarray
import sys

PLAYER_1, PLAYER_2 = 0, 1


class NewBinaryMatrix():
    def __init__(self, boards=None):
        self.columns = 8
        self.rows = 8
        self.size = self.columns * self.rows
        self.nplayers = 2
        self.boards = self.new_game_boards() if boards is None else boards

    def new_game_boards(self):
        """
            Initializes the game
        """
        boards = [None, None]

        boards[PLAYER_1] = bitarray('0000000000000000000000000000000000000000011001100111111001111110')
        # self.boards[PLAYER_1] =   0x0040000000667E76

        boards[PLAYER_2] = bitarray('0111111001111110011001100000000000000000000000000000000000000000')
        # self.boards[PLAYER_2] = 0x40000000000

        return boards

    def get_element(self, column, row):
        """
            Gets piece at row, column. Row and Column from 1 to 8
            Returns 0 if empty, player_number otherwise
        """
        idx = (row - 1) * self.columns + column - 1

        if self.boards[PLAYER_1][idx]:
            return 1
        elif self.boards[PLAYER_2][idx]:
            return 2
        else:
            return 0

    def set_element(self, column, row, player):
        """
            Sets player piece at row, column. Row and Column from 1 to 8
            Player is from 1 to N
        """
        idx = (row - 1) * self.columns + column - 1
        #import pdb; pdb.set_trace()
        board = self.boards[player - 1]
        board[idx] = True

    def remove_element(self, column, row):
        """
            Remove piece from position row, column
            (Sets cell to 0)
        """
        idx = (row - 1) * self.columns + column - 1

        self.boards[PLAYER_1][idx] = False
        self.boards[PLAYER_2][idx] = False

    def test_row_empty(self, row):
        """
            Test if there is empty spaces in a row
        """
        idx_start = (row - 1) * self.columns
        idx_end = idx_start + self.columns

        row_p1 = self.boards[PLAYER_1][idx_start:idx_end]
        row_p2 = self.boards[PLAYER_2][idx_start:idx_end]

        return not row_p1.any() or not row_p2.any()

    def pieces(self, player):
        """
            Player must be either 1 or 2
            Returns where all the pieces off the player are in a list with column, row tuples
        """
        board = self.boards[player - 1]

        pos = [(idx % 8 + 1, idx // 8 + 1) for idx, val in enumerate(board) if val]

        return pos

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


    @classmethod
    def from_binary_matrix(cls, bm):

        new_boards = [None, None]
        new_boards[PLAYER_1] = bitarray(bm.boards[PLAYER_1])
        new_boards[PLAYER_2] = bitarray(bm.boards[PLAYER_2])

        return cls(boards=new_boards)