import copy
from board import *
import sys


'''

Eximo class

. Class that contains the logic needed to run a Eximo game. Each instance of the Eximo class represents a eximo gamestate. A Eximo state can be represented
by a matrix of values (1 for player1, 2 for player2, 0 for empty), the current player, 1 flag and 1 array. The flag's value indicates if the next move performed
is jump-move, capture-move, add-piece-move, or free-move (ordinary-move or jump-move). The array contains the next valid positions that can be played (piece moved or piece added)
. The game ends when the next-pieces array is empty (there are no valid moves/no pieces left)
. This class was made to be used with minimax. AS such, we supply operation functions that return the state object resultant of applying said operation to the object where
it is called.
. To start the game, the function method "perform_checkup" needs to be called on a newly created Eximo object.
. The function exec_all_moves returns an array with all possible outcomes from the current state (for a resultant state that is obtained by executing several jumps/captures only the final state is returned)
. The move function can be used to obtain the state that results of applying the operation defined by the two given start and end tiles (if such operation exists)
. The operations are divieded into 4 categories (move,jump,capture and add_piece), each has a function for the common preconditions and postconditions. Each operation has individual preconditions


. Possible operations:

    - move_north
    - move_neast
    - move_nwest
    - jump_north
    - jump_neast
    - jump_nwest
    - capture_north
    - capture_neast
    - capture_nwest
    - capture_east
    - capture_west
    - add_piece

'''

class Eximo:

    # Board elements
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

    # Gamestate flags
    FREE = 0            # Next op may be ordinary or jump-move
    JUMP = 1            # Next op must be a jump-move
    CAPT = 2            # Next op must be a capture
    ADDPIECE_1 = 3      # Next op is add (1 left)
    ADDPIECE_2 = 4      # Next op is add (2 left)

    def __init__(self, curr_player = 1, next_move = 0, next_pieces = set(), board = Board()):

        self.board = board
        self.curr_player = curr_player          # Next player that may play
        self.next_move = next_move              # Value of gamestate flag
        self.next_pieces = next_pieces          # Next valid start tiles
        self.last_piece = None                  # Last tile moved
        self.message = ""                       # Next op is add (1 left)


    def get_direction(self):
        """
        Used for piece positioning calculations
        """

        return -1 if self.curr_player == self.PLAYER1 else 1


    """
    Ordenary-move operations
    """

    def op_move_preconditions(self):

        """
        Common precondition checking for move operations. Returns True/False if the current state meets the preconditions
        """

        if(self.next_move != self.FREE):
            return False

        return True

    def op_move_postconditions(self,oldPieceCoords,newPieceCoords):

        """
        Apply post-conditions of the move operation corresponding to the current state and return the resultant state (new state).

            oldPieceCoords -> (x,y) starting coordinates of moved piece
            newPieceCoords -> (x,y) ending coordinates of moved piece

            ret -> resulting state
        """

        # Start of new state constrution
        next_gs_board = Board.from_binary_matrix(self.board)
        next_gs_board.set_element(newPieceCoords[0], newPieceCoords[1], self.curr_player)
        next_gs_board.remove_element(oldPieceCoords[0], oldPieceCoords[1])
        next_gs_next_player = self.curr_player
        next_gs_next_move = self.FREE
        next_gs_next_pieces = set()

        new_gs = Eximo(next_gs_next_player,next_gs_next_move,next_gs_next_pieces,next_gs_board)
        new_gs.last_piece = newPieceCoords

        # Check if moved piece has reached opposite side
        if(new_gs.reach_otherside(newPieceCoords)):
            new_gs.board.remove_element(newPieceCoords[0], newPieceCoords[1])
            new_gs.next_move = self.ADDPIECE_2
            new_gs.next_pieces = new_gs.addition_viable_tiles()
            new_gs.perform_checkup()

        else:
            new_gs.curr_player = self.get_enemy(self.curr_player)

        # Check if the next_piece checkup needs to be made
        if new_gs.curr_player == self.get_enemy(self.curr_player):
            new_gs.perform_checkup()

        return new_gs

    def op_move_north_pre(self,piece):

        """
        Check if the given piece can be moved north.

            piece -> (x,y) starting coordinates of piece to be moved

            ret   -> True/False
        """

        # Check if the pieces are in the end row
        if self.curr_player == self.PLAYER1:
            if piece[1] == 1:
                return False
        else:
            if  piece[1] == 8:
                return False

        dir_ = self.get_direction()
        pieceCoords = (piece[0], piece[1] + (1 * dir_))
        pieceValue = self.board.get_element(*pieceCoords)

        # Check if the piece exists
        if pieceValue != self.EMPTY :
            return False

        return True

    def op_move_north(self,piece):

        """
        Move piece north

            piece -> (x,y) starting coordinates of piece to be moved

            ret -> False if piece can't move or resulting state
        """

        # Check common preconditions
        if(not self.op_move_preconditions()):
            return False

        # Check particular preconditions

        if(not self.op_move_north_pre(piece)):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]

        dir_ = self.get_direction()
        pieceCoords = (piece_x,piece_y + (1 * dir_))

        # End of pre conditions

        return self.op_move_postconditions(piece, pieceCoords)

    def op_move_neast_pre(self,piece):

        """
        Check if the given piece can be moved north-east.

            piece -> (x,y) starting coordinates of piece to be moved

            ret   -> True(false )
        """

        # Check particular preconditions (if the piece is on the right site or end row)
        if self.curr_player == self.PLAYER1:
            if piece[0] == 8 or piece[1] == 1:
                return False
        else:
            if piece[0] == 1 or piece[1] == 8:
                return False

        dir_ = self.get_direction()
        pieceCoords = (piece[0] - (1 * dir_),piece[1] + (1 * dir_))
        pieceValue = self.board.get_element(*pieceCoords)

        # Check if piece exists
        if pieceValue != self.EMPTY :
            return False

        return True

    def op_move_neast(self,piece):


        """
        Move piece northeast

            piece -> (x,y) starting coordinates of piece to be moved

            ret -> False if piece can't move or resulting state
        """

        # Check common preconditions
        if(not self.op_move_preconditions()):
            return False

        # Check particular preconditions
        if(not self.op_move_neast_pre(piece)):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]


        dir_ = self.get_direction()
        pieceCoords = (piece_x - (1 * dir_),piece_y + (1 * dir_))
        pieceValue = self.board.get_element(*pieceCoords)

        # End of pre conditions

        return self.op_move_postconditions(piece, pieceCoords)

    def op_move_nwest_pre(self, piece):

        """
        Check if the given piece can be moved north-west.

            piece -> (x,y) starting coordinates of piece to be moved

            ret   -> True(false )
        """

        # Check particular preconditions (if the piece is on the left site or end row)
        if self.curr_player == self.PLAYER1:
            if piece[0] == 1 or piece[1] == 1:
                return False
        else:
            if piece[0] == 8 or piece[1] == 8:
                return False

        dir_ = self.get_direction()
        pieceCoords = ( piece[0] + (1 * dir_),piece[1] + (1 * dir_))
        pieceValue = self.board.get_element(*pieceCoords)

        # Check if piece exists
        if pieceValue != self.EMPTY :
            return False

        return True

    def op_move_nwest(self,piece):


        """
        Move piece northwest

            piece -> (x,y) starting coordinates of piece to be moved

            ret -> False if piece can't move or resulting state
        """

        # Check common preconditions
        if(not self.op_move_preconditions()):
            return False

        # Check particular preconditions
        if(not self.op_move_nwest_pre(piece) ):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]


        dir_ = self.get_direction()
        pieceCoords = (piece[0] + (1 * dir_),piece[1] + (1 * dir_))
        pieceValue = self.board.get_element(*pieceCoords)

        # End of pre conditions

        return self.op_move_postconditions(piece, pieceCoords)

    """
    Jump-move operations
    """

    def op_jump_preconditions(self,piece):

        """
        Common preconditions checking for jump operations. Returns True/False if the current state meets the preconditions
        """

        # Flag must be FREE or JUMP
        if(self.next_move == self.CAPT or self.next_move == self.ADDPIECE_1 or self.next_move == self.ADDPIECE_2):
            return False

        # Check if the piece is in the next pieces (deals with obligatory jumps)
        if(self.next_move == self.JUMP and  piece not in self.next_pieces):
            return False

        return True

    def op_jump_postconditions(self,oldPieceCoords,newPieceCoords):

        """
        Apply post-conditions of the jump operation corresponding to the current state and return the resultant state (new state).

            oldPieceCoords -> (x,y) starting coordinates of moved piece
            newPieceCoords -> (x,y) ending coordinates of moved piece

            ret -> resulting state
        """

        # Start of new state constrution
        next_gs_board = Board.from_binary_matrix(self.board)
        next_gs_board.set_element(newPieceCoords[0], newPieceCoords[1], self.curr_player)
        next_gs_board.remove_element(oldPieceCoords[0], oldPieceCoords[1])
        next_gs_next_player =  self.curr_player
        next_gs_next_move = self.FREE
        next_gs_next_pieces = set()


        new_gs = Eximo(next_gs_next_player,next_gs_next_move,next_gs_next_pieces,next_gs_board)

        # Check if moved piece has reached opposite side
        if(new_gs.reach_otherside(newPieceCoords)):
            new_gs.board.remove_element(newPieceCoords[0], newPieceCoords[1])
            new_gs.next_move  = self.ADDPIECE_2
            new_gs.next_pieces = new_gs.addition_viable_tiles()
            new_gs.perform_checkup()

        # Check if the next move must also be a jump by the same player
        elif(new_gs.can_jump(newPieceCoords)):
            new_gs.next_move = self.JUMP
            new_gs.next_pieces = {newPieceCoords}

        else:
            new_gs.curr_player = self.get_enemy(self.curr_player)

        # Check if the next_piece checkup needs to be made
        if new_gs.curr_player == self.get_enemy(self.curr_player):
            new_gs.perform_checkup()

        new_gs.last_piece = newPieceCoords

        return new_gs

    def op_jump_north_pre(self,piece):

        """
        Check if the given piece can move jump north.

            piece -> (x,y) starting coordinates of piece to jump

            ret   -> True/False
        """

        # Check particular preconditions

        # Check for board-end colisions
        if self.curr_player == self.PLAYER1:
            if piece[1] <= 2:
                return False
        else:
            if piece[1] >= 7:
                return False

        dir_ = self.get_direction()
        lastPieceCoords = (piece[0],piece[1] + (2 * dir_))
        firPieceValue = self.board.get_element(piece[0], piece[1])
        medPieceValue = self.board.get_element(piece[0], piece[1] + (1 * dir_))
        lstPieceValue = self.board.get_element(*lastPieceCoords)

        # Check if destination tile is available
        if lstPieceValue != self.EMPTY :
            return False

        # Check if the intermediate piece belongs to the jumping player
        if medPieceValue != firPieceValue:
            return False

        return True

    def op_jump_north(self,piece):

        """
        Jump piece north

            piece -> (x,y) starting coordinates of piece to jump

            ret -> False if piece can't jump or resulting state
        """

        # Check common preconditions
        if not self.op_jump_preconditions(piece) :
            return False

        if not self.op_jump_north_pre(piece):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]


        dir_ = self.get_direction()
        lastPieceCoords = (piece_x,piece_y + (2 * dir_))

        # End of pre conditions

        return self.op_jump_postconditions(piece,lastPieceCoords)

    def op_jump_neast_pre(self,piece):

        """
        Check if the given piece can be jump to the north-east.

            piece -> (x,y) starting coordinates of piece to jump

            ret   -> True/False
        """

        # Check particular preconditions

        # Check for board-end/right-side colisions
        if self.curr_player == self.PLAYER1:
            if piece[1] <= 2 or piece[0] >= 7:
                return False
        else:
            if piece[1] >= 7 or piece[0] <= 2:
                return False

        dir_ = self.get_direction()
        lastPieceCoords = (piece[0] - (2 * dir_),piece[1] + (2 * dir_))

        firPieceValue = self.board.get_element(piece[0], piece[1])
        medPieceValue = self.board.get_element(piece[0] - (1 * dir_), piece[1] + (1 * dir_))
        lstPieceValue = self.board.get_element(*lastPieceCoords)

        # Check if destination tile is available
        if lstPieceValue != self.EMPTY :
            return False

        # Check if the intermediate piece belongs to the jumping player
        if medPieceValue != firPieceValue:
            return False

        return True

    def op_jump_neast(self,piece):

        """
        Jump piece north-east

            piece -> (x,y) starting coordinates of piece to jump

            ret -> False if piece can't jump or resulting state
        """

        # Check common preconditions
        if(not self.op_jump_preconditions(piece)):
            return False

        # Check particular preconditions
        if not self.op_jump_neast_pre(piece):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]

        dir_ = self.get_direction()
        lastPieceCoords = (piece_x - (2 * dir_),piece_y + (2 * dir_))

        # End of pre conditions

        return self.op_jump_postconditions(piece,lastPieceCoords)

    def op_jump_nwest_pre(self, piece):

        """
        Check if the given piece can be jump to the north-west.

            piece -> (x,y) starting coordinates of piece to jump

            ret   -> True/False
        """

        # Check particular preconditions

        # Check for board-end/left-side colisions
        if self.curr_player == self.PLAYER1:
            if piece[1] <= 2 or piece[0] <= 2:
                return False
        else:
            if piece[1] >= 7 or piece[0] >= 7:
                return False

        dir_ = self.get_direction()
        lastPieceCoords = ( piece[0] + (2 * dir_),piece[1] + (2 * dir_))

        firPieceValue = self.board.get_element(piece[0], piece[1])
        medPieceValue = self.board.get_element(piece[0] + (1 * dir_),piece[1] + (1 * dir_))
        lstPieceValue = self.board.get_element(*lastPieceCoords)

        # Check if destination tile is available
        if lstPieceValue != self.EMPTY :
            return False

        # Check if the intermediate piece belongs to the jumping player
        if medPieceValue != firPieceValue:
            return False

        return True

    def op_jump_nwest(self,piece):

        """
        Jump piece north-west

            piece -> (x,y) starting coordinates of piece to jump

            ret -> False if piece can't jump or resulting state
        """

        # Check common preconditions
        if(not self.op_jump_preconditions(piece)):
            return False

        # Check particular preconditions

        if not self.op_jump_nwest_pre(piece):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]


        dir_ = self.get_direction()
        lastPieceCoords = ( piece_x + (2 * dir_),piece_y + (2 * dir_),)

        # End of pre conditions

        return self.op_jump_postconditions(piece,lastPieceCoords)

    """
    Capture operations
    """

    def op_capture_preconditions(self,piece):

        """
        Common preconditions checking for capture operations. Returns True/False if the current state meets the preconditions
        """

        # Flag must be CAPT
        if(self.next_move != self.CAPT):
            return False

        # Check if the piece is in the next pieces (deals with obligatory captures)
        if(self.next_move == self.CAPT and len(self.next_pieces) != 0 and piece not in self.next_pieces):
            return False

        return True

    def op_capture_postconditions(self,oldPieceCoords,newPieceCoords,capturedPieceCoords):

        """
        Apply post-conditions of the capture operation corresponding to the current state and return the resultant state (new state).

            oldPieceCoords -> (x,y) starting coordinates of moved piece
            newPieceCoords -> (x,y) ending coordinates of moved piece
            capturedPieceCoords -> (x,y) coordinates of the captured piece

            ret -> resulting state
        """

        # Start of new state constrution
        next_gs_board = Board.from_binary_matrix(self.board)
        next_gs_board.set_element(newPieceCoords[0], newPieceCoords[1], self.curr_player)
        next_gs_board.remove_element(oldPieceCoords[0], oldPieceCoords[1])
        next_gs_board.remove_element(capturedPieceCoords[0], capturedPieceCoords[1])
        next_gs_next_player = self.curr_player
        next_gs_next_move = self.FREE
        next_gs_next_pieces = set()

        new_gs = Eximo(next_gs_next_player,next_gs_next_move,next_gs_next_pieces,next_gs_board)

        # Check if moved piece has reached opposite side
        if(new_gs.reach_otherside(newPieceCoords)):
            new_gs.board.remove_element(newPieceCoords[0], newPieceCoords[1])
            new_gs.next_move = self.ADDPIECE_2
            new_gs.next_pieces = self.addition_viable_tiles()
            new_gs.perform_checkup()

        # Check if the next move must also be a capture by the same player
        elif(new_gs.can_capture(newPieceCoords)):
            new_gs.next_move = self.CAPT
            new_gs.next_pieces = {newPieceCoords}
        else:
            new_gs.curr_player = self.get_enemy(self.curr_player)

        # Check if the next_piece checkup needs to be made
        if new_gs.curr_player == self.get_enemy(self.curr_player):
            new_gs.perform_checkup()

        new_gs.last_piece = newPieceCoords

        return new_gs

    def op_capture_north_pre(self,piece):

        """
        Check if the given piece can capture north.

            piece -> (x,y) starting coordinates of piece that captures

            ret   -> True/False
        """

        # Check for end-board colisions
        if self.curr_player == self.PLAYER1:
            if piece[1] <= 2:
                return False
        else:
            if piece[1] >= 7:
                return False

        dir_ = self.get_direction()
        lastPieceCoords = ( piece[0],piece[1] + (2 * dir_))
        medPieceCoords = ( piece[0],piece[1] + (1 * dir_))

        firPieceValue = self.board.get_element(*piece)
        medPieceValue = self.board.get_element(*medPieceCoords)
        lstPieceValue = self.board.get_element(*lastPieceCoords)

        # Check if the destination tile is empty
        if lstPieceValue != self.EMPTY :
            return False

        # Check if the intermediate piece (piece to be captured) belongs to the enemy
        if medPieceValue != self.get_enemy(firPieceValue):
            return False

        return True

    def op_capture_north(self,piece):

        """
        Capture piece to the north

            piece -> (x,y) starting coordinates of piece that captures

            ret -> False if piece can't capture or resulting state
        """

        # Check common preconditions
        if(not self.op_capture_preconditions(piece)):
            return False

        # Check particular preconditions
        if not self.op_capture_north_pre(piece):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]

        dir_ = self.get_direction()
        lastPieceCoords = ( piece_x,piece_y + (2 * dir_))
        medPieceCoords = (piece_x,piece_y + (1 * dir_))

        # End of pre conditions

        return self.op_capture_postconditions(piece,lastPieceCoords,medPieceCoords)

    def op_capture_west_pre(self,piece):

        """
        Check if the given piece can capture to the west.

            piece -> (x,y) starting coordinates of piece that captures

            ret   -> True/False
        """

        # Check particular preconditions

        # Check for side-board colisions
        if self.curr_player == self.PLAYER1:
            if piece[0] <= 2:
                return False
        else:
            if piece[0] >= 7:
                return False

        dir_ = self.get_direction()
        lastPieceCoords = ( piece[0] + (2 * dir_),piece[1])
        medPieceCoords = ( piece[0] + (1 * dir_),piece[1])

        firPieceValue = self.board.get_element(piece[0],piece[1])
        medPieceValue = self.board.get_element(piece[0] + (1 * dir_),piece[1])
        lstPieceValue = self.board.get_element(*lastPieceCoords)

        # Check if the destination tile is empty
        if lstPieceValue != self.EMPTY :
            return False

        # Check if the intermediate piece (piece to be captured) belongs to the enemy
        if medPieceValue != self.get_enemy(firPieceValue):
            return False

        return True

    def op_capture_west(self,piece):

        """
        Capture piece to the west

            piece -> (x,y) starting coordinates of piece that captures

            ret -> False if piece can't capture or resulting state
        """

        # Check common preconditions
        if(not self.op_capture_preconditions(piece)):
            return False

        # Check particular preconditions
        if not self.op_capture_west_pre(piece):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]

        dir_ = self.get_direction()
        lastPieceCoords = ( piece_x + (2 * dir_),piece_y)
        medPieceCoords = (piece_x + (1 * dir_),piece_y)

        # End of pre conditions

        return self.op_capture_postconditions(piece,lastPieceCoords,medPieceCoords)

    def op_capture_east_pre(self,piece):

        """
        Check if the given piece can capture to the east.

            piece -> (x,y) starting coordinates of piece that captures

            ret   -> True/False
        """


        # Check for side-board colisions
        if self.curr_player == self.PLAYER1:
            if piece[0] >= 7:
                return False
        else:
            if piece[0] <= 2:
                return False

        dir_ = self.get_direction()
        lastPieceCoords = ( piece[0] - (2 * dir_),piece[1])
        medPieceCoords = (piece[0] - (1 * dir_),piece[1])

        firPieceValue = self.board.get_element(piece[0], piece[1])
        medPieceValue = self.board.get_element( *medPieceCoords)
        lstPieceValue = self.board.get_element(*lastPieceCoords)

        # Check if the destination tile is empty
        if lstPieceValue != self.EMPTY :
            return False

        # Check if the intermediate piece (piece to be captured) belongs to the enemy
        if medPieceValue != self.get_enemy(firPieceValue):
            return False

        return True

    def op_capture_east(self,piece):

        """
        Capture piece to the east

            piece -> (x,y) starting coordinates of piece that captures

            ret -> False if piece can't capture or resulting state
        """

        # Check common preconditions
        if(not self.op_capture_preconditions(piece)):
            return False

        # Check particular preconditions
        if not self.op_capture_east_pre(piece):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]

        dir_ = self.get_direction()
        lastPieceCoords = (piece_x - (2 * dir_),piece_y)
        medPieceCoords = (piece_x - (1 * dir_),piece_y)

        # End of pre conditions

        return self.op_capture_postconditions(piece,lastPieceCoords,medPieceCoords)

    def op_capture_neast_pre(self,piece):

        """
        Check if the given piece can capture to the north-east.

            piece -> (x,y) starting coordinates of piece that captures

            ret   -> True/False
        """

        # Check colisions with the board's end and the side-board
        if self.curr_player == self.PLAYER1:
            if piece[1] <= 2 or piece[0] >= 7:
                return False
        else:
            if piece[1] >= 7 or piece[0] <= 2:
                return False

        dir_ = self.get_direction()
        lastPieceCoords = ( piece[0] - (2 * dir_),piece[1] + (2 * dir_))
        medPieceCoords = (piece[0] - (1 * dir_),piece[1] + (1 * dir_))

        firPieceValue = self.board.get_element(piece[0], piece[1])
        medPieceValue = self.board.get_element(*medPieceCoords)
        lstPieceValue = self.board.get_element(*lastPieceCoords)

        # Check if the destination tile is empty
        if lstPieceValue != self.EMPTY :
            return False

        # Check if the intermediate piece (piece to be captured) belongs to the enemy
        if medPieceValue != self.get_enemy(firPieceValue):
            return False

        return True

    def op_capture_neast(self,piece):

        """
        Capture piece to the north-east

            piece -> (x,y) starting coordinates of piece that captures

            ret -> False if piece can't capture or resulting state
        """

        # Check common preconditions
        if(not self.op_capture_preconditions(piece)):
            return False

        # Check particular preconditions
        if not self.op_capture_neast_pre(piece):
            return False

            # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]

        dir_ = self.get_direction()
        lastPieceCoords = (piece_x - (2 * dir_),piece_y + (2 * dir_))
        medPieceCoords = ( piece_x - (1 * dir_),piece_y + (1 * dir_))

        # End of pre conditions

        return self.op_capture_postconditions(piece,lastPieceCoords,medPieceCoords)

    def op_capture_nwest_pre(self,piece):

        """
        Check if the given piece can capture to the north-west.

            piece -> (x,y) starting coordinates of piece that captures

            ret   -> True/False
        """

         # Check colisions with the board's end and the side-board
        if self.curr_player == self.PLAYER1:
            if piece[1] <= 2 or piece[0] <= 2:
                return False
        else:
            if piece[1] >= 7 or piece[0] >= 7:
                return False

        dir_ = self.get_direction()
        lastPieceCoords = ( piece[0] + (2 * dir_),piece[1] + (2 * dir_))
        medPieceCoords = ( piece[0] + (1 * dir_), piece[1] + (1 * dir_))

        firPieceValue = self.board.get_element(piece[0], piece[1])
        medPieceValue = self.board.get_element(piece[0] + (1 * dir_),piece[1] + (1 * dir_))
        lstPieceValue = self.board.get_element(*lastPieceCoords)

         # Check if the destination tile is empty
        if lstPieceValue != self.EMPTY :
            return False

        # Check if the intermediate piece (piece to be captured) belongs to the enemy
        if medPieceValue != self.get_enemy(firPieceValue):
            return False

        return True

    def op_capture_nwest(self,piece):

        """
        Capture piece to the north-west

            piece -> (x,y) starting coordinates of piece that captures

            ret -> False if piece can't capture or resulting state
        """

        # Check common preconditions
        if(not self.op_capture_preconditions(piece)):
            return False

        # Check particular preconditions
        if not self.op_capture_nwest_pre(piece):
            return False

        # Variable extraction
        piece_x = piece[0]
        piece_y = piece[1]

        dir_ = self.get_direction()
        lastPieceCoords = ( piece_x + (2 * dir_),piece_y + (2 * dir_))
        medPieceCoords = (piece_x + (1 * dir_),piece_y + (1 * dir_))

        # End of pre conditions

        return self.op_capture_postconditions(piece,lastPieceCoords,medPieceCoords)


    """
    Add-piece operation
    """

    def op_add_piece_preconditions(self):

        """
         Common preconditions checking for piece-adding operation. Returns True/False if the current state meets the preconditions
        """

        # Flag must be an addpiece flag
        if(self.next_move != self.ADDPIECE_1 and self.next_move != self.ADDPIECE_2):
            return False

        # # Check if there are avaibable tiles where pieces can be added
        if(not self.can_add_piece()):
             return False

        #if (self.next_move not in self.next_pieces):
         #   return False


        return True

    def op_add_piece_postconditions(self,newPieceCoords):

        """
        Apply post-conditions of the piece-adding operation corresponding to the current state and return the resultant state (new state).

            newPieceCoords -> (x,y) destination tile of new piece

            ret -> resulting state
        """

        # Start of new state constrution
        next_gs_board = Board.from_binary_matrix(self.board)
        next_gs_board.set_element(newPieceCoords[0], newPieceCoords[1], self.curr_player)
        next_gs_next_player = self.get_enemy(self.curr_player)
        next_gs_next_pieces = set()
        next_gs_next_move = self.FREE

        new_gs = Eximo(next_gs_next_player,next_gs_next_move,next_gs_next_pieces,next_gs_board)

        # Reduce the number of pieces that can be added. If the added piece was the last one rever to FREE flag
        if self.next_move == self.ADDPIECE_2:
            new_gs.next_move = self.ADDPIECE_1
            new_gs.curr_player = self.curr_player
            new_gs.next_pieces = { piece for piece in self.next_pieces }
            new_gs.next_pieces.remove(newPieceCoords)
        elif self.next_move == self.ADDPIECE_1:
            new_gs.next_move = self.FREE

        # Perform checkup to set correct flags (for mandatory captures)
        new_gs.perform_checkup()
        new_gs.last_piece = newPieceCoords
        return new_gs


    def op_add_piece_bot(self, newPieceCoords):
        """
        Add a new piece to the board to when it's a bot playing (different from op_add_piece because some preconditions where irrelevant to the bot)

            piece -> (x,y) destination of the new piece

            ret -> False if piece can't jump or resulting state
        """
        children = []
        empty_pos = list(newPieceCoords)

        next_p = self.get_enemy(self.curr_player)
        next_move = self.FREE

        if len(empty_pos) == 1:
            board = Board.from_binary_matrix(self.board)
            board.set_element(empty_pos[0][0], empty_pos[0][1], self.curr_player)
            child = Eximo(next_p, next_move, set(), board)
            child.perform_checkup()
            children.append(child)

        for idx, pos1 in enumerate(empty_pos):
            curr_children = []
            for pos2 in empty_pos[idx+1:]:
                board = Board.from_binary_matrix(self.board)
                board.set_element(pos1[0], pos1[1], self.curr_player)
                board.set_element(pos2[0], pos2[1], self.curr_player)
                child = Eximo(next_p, next_move, set(), board)
                child.perform_checkup()
                curr_children.append(child)
            children.extend(curr_children)

        return children

    def op_add_piece(self, position):

        """
        Add a new piece to the board

            piece -> (x,y) destination of the new piece

            ret -> False if piece can't jump or resulting state
        """

        # Check common preconditions
        if(not self.op_add_piece_preconditions()):
            return False

        # Variable extraction
        pos_x = position[0]
        pos_y = position[1]

        # Check particular preconditions
        if not (pos_x >= 2 and pos_x < 8):
            return False

        # Check if the destination tile is within the possible bounds
        if self.curr_player == self.PLAYER1:
            if pos_y <= 6:
                return False
        else:
            if pos_y >= 3:
                return False

        firPieceValue = self.board.get_element(pos_x, pos_y)

        # Check if the destination tile is empty
        if firPieceValue != self.EMPTY :
            return False

        # End of pre conditions

        return self.op_add_piece_postconditions(position)

    """
    End of operations
    """

    def reach_otherside(self,piece):

        """
        Check if the given piece coordinates are in the end row (row opposite from the current player's starting side)

            piece -> (x,y) piece to be checked

            ret -> True if p
        """

        piece_y = piece[1]

        if self.curr_player == self.PLAYER1:
            if piece_y == 1:
                return True
        else:
            if piece_y == 8:
                return True

        return False


    def can_add_piece(self):

        '''
        Checks if the possible piece-adding positions of the current player are free
        '''

        final_board = self.board

        if self.curr_player == self.PLAYER1:
            return self.board.test_row_empty(7) or self.board.test_row_empty(8)
        else:
            return self.board.test_row_empty(1) or self.board.test_row_empty(2)

    def addition_viable_tiles(self):

        '''
        Get the list of tile-coordinates where the current player may add a piece

            ret -> list of viable tiles in format (x,y)
        '''

        result = set()

        if self.curr_player == self.PLAYER1:

            for i in range(2,8):
                if self.board.get_element(i,7) == self.EMPTY:
                    result.add((i,7))

                if self.board.get_element(i,8) == self.EMPTY:
                    result.add((i,8))
        else:

            for i in range(2,8):
                if self.board.get_element(i,1) == self.EMPTY:
                    result.add((i,1))

                if self.board.get_element(i,2) == self.EMPTY:
                    result.add((i,2))

        return result

    def get_enemy(self, player):

        '''
        Get the opponent player from the current player

        ret -> number of the enemy of the current player
        '''

        return self.PLAYER1 if player == self.PLAYER2 else self.PLAYER2

    def can_capture(self, piece):

        '''
        Check if the piece at the given coordinates can execute a capture move

        ret -> True if can capture, False otherwise
        '''
        captures_pre = [self.op_capture_north_pre, self.op_capture_east_pre, self.op_capture_west_pre, self.op_capture_nwest_pre, self.op_capture_neast_pre]

        # Check capture preconditions
        for action in captures_pre:
            ret = action(piece)
            if ret:
                return True
        return False

    def can_jump(self, piece):

        '''
        Check if the piece at the given coordinates can execute a jump move

        ret -> True if can do a jump-move, False otherwise
        '''

        jumps = [self.op_jump_north_pre, self.op_jump_nwest_pre, self.op_jump_neast_pre]

        # Check jump preconditions
        if not self.op_jump_preconditions(piece):
            return False

        for action in jumps:
            ret = action(piece)
            if ret:
                return True
        return False

    def can_move(self, piece):

        '''
        Check if the piece at the given coordinates can execute a ordinary move

        ret -> True if can do a ordinary-move, False otherwise
        '''

        moves = [self.op_move_north_pre, self.op_move_nwest_pre, self.op_move_neast_pre]

         # Check move preconditions
        if not self.op_move_preconditions(piece):
            return False

        for action in moves:
            ret = action(piece)
            if ret:
                return True
        return False

    def possible_capture(self):

        '''
        Gets all the possible positions that can capture.

        ret-> (can_capture, other_init) can_capture is a list of piece-coordinates that can execute a capture move and other_init are valid initial pieces
        '''

        can_capture = set()
        other_init = set()
        initial_pos = self.board.pieces(self.curr_player)

        for ipos in initial_pos:
            if self.can_capture(ipos):
                can_capture.add(ipos)
            else:
                other_init.add(ipos)

        return can_capture, other_init

    def perform_full_checkup(self):
        '''
        Store valid next pieces for the current state. Check for mandatory captures
        '''

        # If the next move is a jump-move or a capture, no checkup is needed
        if self.next_move != self.FREE:

            # Except for when a add-piece state has no valid tiles where to put pieces. Reset state to free and do checkup
            if (self.next_move == self.ADDPIECE_1 or self.next_move == self.ADDPIECE_2) and len(self.next_pieces) == 0:
                self.next_move = self.FREE
                self.curr_player = self.get_enemy(self.curr_player)
            else:
                return

        capturingStarts, otherStarts = self.possible_capture()

        # Check for pieces that may capture
        if len(capturingStarts) > 0:

            self.next_move = self.CAPT
            self.next_pieces = capturingStarts

        else:

            self.next_move = self.FREE
            self.next_pieces = otherStarts



    def perform_checkup(self):

        '''
        Store valid next pieces for the current state. Check for mandatory captures
        '''

        # If the next move is a jump-move or a capture, no checkup is needed
        if self.next_move != self.FREE:

            # Except for when a add-piece state has no valid tiles where to put pieces. Reset state to free and do checkup
            if (self.next_move == self.ADDPIECE_1 or self.next_move == self.ADDPIECE_2) and len(self.next_pieces) == 0:
                self.next_move = self.FREE
                self.curr_player = self.get_enemy(self.curr_player)
            else:
                return

        # capturingStarts, otherStarts = self.possible_capture()

        # Check for pieces that may capture
        # if len(capturingStarts) > 0:

        #     self.next_move = self.CAPT
        #     self.next_pieces = capturingStarts

        # else:

        #     self.next_move = self.FREE
        #     self.next_pieces = otherStarts

    def print_state(self,f, turn=None):

        """
        Display the current state

            f       ->  file where to display
            turn    ->  number of the turn (not displayed if None)
        """

        if turn != None:
            print("\n------ Turn " + str(turn) + " ------")

        self.board.print_board(f)
        print('\n CURR_PLAYER: {}  NEXT_MOVE: {}  NEXT_PIECES: {} \n'.format(self.curr_player,self.next_move,self.next_pieces,self.message),file=f)

    def exec_all_moves(self,level=0):

        """
        Get an array with all possible outcomes from the current state (for a resultant state that is obtained by executing several jumps/captures only the final state is returned)

            ret -> array of all possible outcome states
        """

        capts = [self.op_capture_north, self.op_capture_nwest, self.op_capture_neast, self.op_capture_east, self.op_capture_west]
        jmps = [self.op_jump_north, self.op_jump_nwest, self.op_jump_neast]
        moves = [self.op_move_north,self.op_move_nwest, self.op_move_neast]
        result = []
        ops = []

        # Pre-select all operations that may be executed
        if self.next_move == self.FREE:
            capturingStarts, otherStarts = self.possible_capture()

            # Check for pieces that may capture
            if len(capturingStarts) > 0:
                self.next_move = self.CAPT
                self.next_pieces = capturingStarts
            else:
                self.next_move = self.FREE
                jmps.extend(moves)
                ops = jmps
                self.next_pieces = otherStarts

        elif self.next_move == self.CAPT:
            ops = capts
        elif self.next_move == self.JUMP:
            ops = jmps
        elif self.next_move == self.FREE:
            jmps.extend(moves)
            ops = jmps
        elif self.next_move == self.ADDPIECE_2:
            return self.op_add_piece_bot(self.next_pieces)

        # Execute possible operations for all viable pieces
        for pos in self.next_pieces:
            for op in ops:
                newState = op(pos)

                # Check if op succeeded
                if newState:

                    # If the next player is the current player than the function is called recursevely, this is done so that outcomes account for successive plays by the same
                    # player ( successive jumps and captures or piece addition)
                    if newState.curr_player != self.curr_player:
                        result.append(newState)
                    else:
                        result.extend(newState.exec_all_moves(level+1))


        return result


    def move(self, initial_pos, final_pos):

        """
        Execute the operation that corresponds to the given initial and final pos. If the operation is a piece addition final_pos should be None

            initial_pos -> (x,y) inital position of the operation
            final_pos -> (x,y) final position of the operation

            ret -> False if no operation is available or the resulting game-state
        """

        ops = [ self.op_move_north, self.op_move_nwest, self.op_move_neast,
                self.op_jump_north, self.op_jump_nwest, self.op_jump_neast,
                self.op_capture_north, self.op_capture_east, self.op_capture_west,
                self.op_capture_nwest, self.op_capture_neast, self.op_add_piece
                ]

        # Check if the final position is empty
        if final_pos and self.board.get_element(*final_pos) != self.EMPTY:
            return False

        # Check if the intial position is a valid start piece
        if initial_pos not in self.next_pieces:
            return False

        # Test for add piece operation
        if self.next_move == self.ADDPIECE_1 or self.next_move == self.ADDPIECE_2:
            res = self.op_add_piece(initial_pos)
            if type(res) != type(False):
                return res

        # Test for other operations
        for op in ops:
            res = op(initial_pos)

            if type(res) != type(False) and (res.last_piece == final_pos):
                return res

        return False

    def is_game_over(self):

        """
        Check if the current-player has lost the game

            ret -> True if the current player  has lost the game, False otherwise
        """

        if len(self.next_pieces) == 0:
            return True
