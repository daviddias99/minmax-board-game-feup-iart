from Eximo import *
from Graphics import *
from Minmax  import *
import sys
from time import sleep

class Game:

    def __init__(self, p1Type, p2Type, depths, heur, cuts, user_state_ordering):

        self.state = Eximo()
        self.state.perform_full_checkup()

        # Init pygame graphics
        self.graphics = EximoGraphics()

        # Init game variables
        self.p1Type = p1Type
        self.p2Type = p2Type
        self.turnCount = 0
        self.depths = depths
        self.heuristics = heur
        self.use_cuts = cuts
        self.user_state_ordering = user_state_ordering


        # Init stats
        cutLevelsP1 = [] if self.depths[0] == None else [0 for i in range(self.depths[0]+1)]
        cutLevelsP2 = [] if self.depths[1] == None else [0 for i in range(self.depths[1]+1)]

        self.statsP1 = {'total_exec_time': 0, 'total_avg_expansion': 0, 'leafCount': 0, 'totalCutCount': 0, 'cutLevels': cutLevelsP1}
        self.statsP2 = {'total_exec_time': 0, 'total_avg_expansion': 0, 'leafCount': 0, 'totalCutCount': 0, 'cutLevels': cutLevelsP2}

        # Start the game
        self.run()


    def get_current_type(self):

        """
        Return the current players type (C or P, for Computer and Player respectively)
        """
        if self.state.curr_player == 1:
            return self.p1Type
        else:
            return self.p2Type

    def is_ai_game(self):

        """
        Check if the game is only played by the computer (AI vs AI)
        """

        return self.p1Type == self.p2Type and self.p1Type == 'C'


    def get_stats(self):

        return [
            [1,
            self.depths[0],
            self.statsP1['total_exec_time'],
            self.turnCount // 2,
            self.statsP1['total_exec_time']/(self.turnCount // 2),
            self.statsP1['total_avg_expansion']/ (self.turnCount // 2),
            self.statsP1['totalCutCount'],
            self.statsP1['totalCutCount'] / (self.turnCount //2),
            self.statsP1['leafCount'],
            self.statsP1['leafCount']  / (self.turnCount //2)
            ],
            [2,
            self.depths[1],
            self.statsP2['total_exec_time'],
            self.turnCount // 2,
            self.statsP2['total_exec_time']/(self.turnCount // 2),
            self.statsP2['total_avg_expansion']/ (self.turnCount // 2),
            self.statsP2['totalCutCount'],
            self.statsP2['totalCutCount'] / (self.turnCount //2),
            self.statsP2['leafCount'],
            self.statsP2['leafCount']  / (self.turnCount //2)
            ],
            self.winner

        ]

    def get_stats_sum(self):

        return [
            [1,
            self.statsP1['total_exec_time'],
            self.turnCount // 2,
            self.statsP1['total_exec_time']/(self.turnCount // 2),
            self.statsP1['total_avg_expansion']/ (self.turnCount // 2),
            self.statsP1['totalCutCount'],
            self.statsP1['totalCutCount'] / (self.turnCount //2),
            self.statsP1['leafCount'],
            self.statsP1['leafCount']  / (self.turnCount //2)
            ],
            [2,
            self.depths[1],
            self.statsP2['total_exec_time'],
            self.turnCount // 2,
            self.statsP2['total_exec_time']/(self.turnCount // 2),
            self.statsP2['total_avg_expansion']/ (self.turnCount // 2),
            self.statsP2['totalCutCount'],
            self.statsP2['totalCutCount'] / (self.turnCount //2),
            self.statsP2['leafCount'],
            self.statsP2['leafCount']  / (self.turnCount //2)
            ],
            self.winner

        ]

    def run(self):

        positions = []
        self.graphics.update(self.state.board)

        self.state.perform_full_checkup()

        while True:

            if self.state.is_game_over():
                 print("GAMEOVER: player " + str(self.state.get_enemy(self.state.curr_player)) + " won!")
                 self.winner = self.state.get_enemy(self.state.curr_player)
                 break


            # Increase the turn count
            self.turnCount += 1

            # Player move?
            if self.get_current_type() == 'P':

                selectedTile = self.graphics.event_loop()

                # New tile choice
                if selectedTile:

                    # Invalid initial tile
                    if len(positions) == 0 and selectedTile not in self.state.next_pieces:
                        positions = []
                        continue

                    positions.append(selectedTile)

                    # If the next move is to add a piece, only one position is necessary
                    if self.state.next_move == self.state.ADDPIECE_1 or self.state.next_move == self.state.ADDPIECE_2:
                        positions.append(None)

                # Got all positions, execute a move
                if(len(positions) == 2):

                    # Apply move
                    newState = self.state.move(positions[0],positions[1])

                    if newState:
                        newState.print_state(sys.stdout,self.turnCount)
                        self.state = newState
                    else:
                        print("Can't execute move")

                    positions = []

            # AI move ?
            else:
                # Run minimax
                mm = Minmax(self.depths[self.state.curr_player - 1],
                            self.state.curr_player,
                            self.heuristics[self.state.curr_player - 1],
                            self.use_cuts[self.state.curr_player - 1],
                            self.user_state_ordering[self.state.curr_player -1] )

                self.state = mm.move(self.state)

                # Print new gamestate
                self.state.print_state(sys.stdout,self.turnCount)

                # Update game variables
                self.update_stats(mm.stats())


            self.state.perform_full_checkup()


            # Update pygame display
            self.graphics.update(self.state.board)



        self.display_statistics()


       # self.graphics.terminate_game()

    def update_stats(self,stats):
        """
        Update the overall game statistics
        """

        if self.state.get_enemy(self.state.curr_player) == 1:
            self.statsP1['total_exec_time'] += stats[0]
            self.statsP1['total_avg_expansion'] += stats[1]
            self.statsP1['leafCount'] += stats[2]
            self.statsP1['totalCutCount'] += stats[3]
            self.statsP1['cutLevels'] = [self.statsP1['cutLevels'][i] + stats[4][i] for i in range(len( stats[4]))]
        else:
            self.statsP2['total_exec_time'] += stats[0]
            self.statsP2['total_avg_expansion'] += stats[1]
            self.statsP2['leafCount'] += stats[2]
            self.statsP2['totalCutCount'] += stats[3]
            self.statsP2['cutLevels'] = [self.statsP2['cutLevels'][i] + stats[4][i] for i in range(len( stats[4]))]

    def display_statistics(self):
        """
        Display the game's statistics
        """

        print("\n________Game Statistics________\n")

        if self.p1Type == 'C':
            print("-- Player 1 (depth = {}):".format(self.depths[0]))
            print("Time: " + str(self.statsP1['total_exec_time']) + " (" + str(self.turnCount // 2) + " turns, "+str(self.statsP1['total_exec_time']/(self.turnCount // 2)) +" avg)")
            print("Avg. branching factor: " + str(self.statsP1['total_avg_expansion']/ (self.turnCount // 2)))
            print("Total cuts: " + str(self.statsP1['totalCutCount']) + " (" + str(self.statsP1['totalCutCount'] / (self.turnCount //2)) + " avg)")
            print("Cut levels: ", end="")
            print(self.statsP1['cutLevels'])
            print("Total leaves: " + str(self.statsP1['leafCount'] ) + " (" + str(self.statsP1['leafCount']  / (self.turnCount //2)) + " avg)")
            print()

        if self.p2Type == 'C':
            print("-- Player 2 (depth = {}):".format(self.depths[0]))
            print("Time: " + str(self.statsP2['total_exec_time']) + " (" + str(self.turnCount // 2) + " turns, "+str(self.statsP2['total_exec_time']/(self.turnCount // 2)) +" avg)")
            print("Avg. branching factor: " + str(self.statsP2['total_avg_expansion']/ (self.turnCount // 2)))
            print("Total cuts: " + str(self.statsP2['totalCutCount']) + " (" + str(self.statsP2['totalCutCount'] / (self.turnCount //2)) + " avg)")
            print("Cut levels: ", end="")
            print(self.statsP2['cutLevels'])
            print("Total leaves: " + str(self.statsP2['leafCount'] ) + " (" + str(self.statsP2['leafCount']  / (self.turnCount //2)) + " avg)")
            print()

