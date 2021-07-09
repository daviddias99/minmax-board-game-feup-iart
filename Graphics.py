import pygame
import sys

##COLORS##
#             R    G    B 
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
HIGH     = (160, 190, 255)

class EximoGraphics:

    # Constants
    WINDOW_SIZE = 600
    FPS = 60

    def __init__(self):
        self.caption = "Eximo"

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))

        self.square_size = int(self.WINDOW_SIZE / 8)
        self.piece_size = int(self.square_size / 2)

        self.message = False

    def setup_window(self):

        pygame.init()
        pygame.display.set_caption(self.caption)

    def update_display(self, board, legal_moves, selected_piece):

        self.draw_binary_board(board)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.FPS)

    def update(self,board):

        self.draw_board_squares()
        self.draw_binary_board(board)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.FPS)
        
    def draw_board_squares(self):
        """
        Draw checker's style game board
        """
        color = WHITE

        for x in range(8):

            color = BLACK if color == WHITE else WHITE

            for y in range(8):

                if color == WHITE:
                    color = BLACK
                else:
                    color = WHITE

                pygame.draw.rect(self.screen, color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
    
    def draw_board_pieces(self, matrix):
        """
        Takes a board object and draws all of its pieces to the display
        """
        for x in range(8):
            for y in range(8):
                if matrix[y][x] == 1:

                    coords = self.pixel_coords((x,y))
                    pygame.draw.circle(self.screen, RED, coords, self.piece_size - 5) 
                if matrix[y][x] == 2:
                    pygame.draw.circle(self.screen, BLUE, self.pixel_coords((x,y)), self.piece_size - 5)
    
    def draw_binary_board(self, board):
        """
        Takes a binary board object and draws all of its pieces to the display
        """
        for col in range(board.columns):
            for row in range(board.rows):
                cell = board.get_element(col + 1,row + 1)
                if cell == 1:
                    coords = self.pixel_coords((col,row))
                    pygame.draw.circle(self.screen, RED, coords, self.piece_size - 5) 
                elif cell == 2:
                    coords = self.pixel_coords((col,row))
                    pygame.draw.circle(self.screen, BLUE, coords, self.piece_size - 5)
    

    def pixel_coords(self, board_coords):
        """
        Takes in a tuple of board coordinates (x,y) 
        and returns the pixel coordinates of the center of the square at that location.
        """
        return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    def board_coords(self, pixel_x, pixel_y):
        """
        Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return (int(pixel_x / self.square_size), int(pixel_y / self.square_size))    

    def event_loop(self):
        """
        The event loop. This is where events are triggered 
        (like a mouse click) and then effect the game state.
        """
        pos = pygame.mouse.get_pos()
        self.mouse_pos = self.board_coords(*pos) # what square is the mouse in?

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.terminate_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Coordinates: " + str(self.mouse_pos[0] + 1) + " " + str(self.mouse_pos[1] + 1))
                return (self.mouse_pos[0] + 1, self.mouse_pos[1] + 1)
        return False

    def terminate_game(self):
        """Quits the program and ends the game."""
        pygame.quit()
        sys.exit
