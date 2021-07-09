import heapq
import sys
import time

import faulthandler
faulthandler.enable()

class Minmax:
    def __init__(self, depth, player, eval_number, use_cuts, use_state_ordering):

        super().__init__()

        self.depth = depth               # Maxium depth of search
        self.player = player             # "Max" player

        # Minimax settings.
        # Use_cuts = True implies the use of alpha-beta prunning
        # use_state_ordering = True implies the use of state ordering
        self.use_cuts = use_cuts
        self.use_state_ordering = use_state_ordering

        # Result game evaluation
        self.res = 0

        # Evaluation functions
        self.evals = [self.eval1, self.eval2, self.eval3, self.eval4]
        self.evaluate = self.evals[eval_number - 1]

        # Statistics
        self.leafCount = 0
        self.cutCount = 0
        self.cutLevels = [0 for i in range(self.depth + 1)]
        self.expansionCount = 0
        self.expansionTotal = 0
        self.execTime = 0

    def move(self, state):

        start = time.time()

        if self.use_state_ordering:
            result = self.max_value_order(state,-float("inf"),float("inf"),self.depth)
        else:
            result = self.max_value(state,-float("inf"),float("inf"),self.depth)

        end = time.time()

        self.execTime = end - start
        self.res = result[0]

        return result[1]

    def stats(self):

        print("- Minimax Statistics\n")
        print("Time: " + str(self.execTime))
        print("Avg ramification factor: " + str(self.expansionTotal/self.expansionCount))
        print("Cut count: " + str(self.cutCount))
        print("Cut levels: " , end="")
        print(self.cutLevels)
        print("Leaf count: " + str(self.leafCount))
        print("Value: " + str(self.res))
        print(self.cutLevels)

        return (self.execTime,self.expansionTotal/self.expansionCount,self.leafCount,self.cutCount,self.cutLevels)

    """"
    Minimax with alpha-beta prunning. Prunning may be disabled
    """

    def max_value(self,current_state,alpha,beta, depth):

        # Leaf node reached
        if depth == 0:
            self.leafCount += 1
            return self.evaluate(current_state, self.player), current_state

        value = -float("inf")

        # Expand current state (obtain all possible resultant gamestates)
        expanded_states = current_state.exec_all_moves(1)

        # Update statistics
        self.expansionCount += 1
        self.expansionTotal += len(expanded_states)

        # State that obtained the max value
        current_max_state = None

        # No posssible successors (gameover)
        if len(expanded_states) == 0:
            return self.evaluate(current_state, self.player), current_state

        for state in expanded_states:

            # Evaluate min's turn
            min_v = self.min_value(state, alpha, beta, depth - 1)[0]

            # Update best state
            if min_v > value :
                current_max_state = state
                value = min_v

            # Execute prunning
            if value >= beta and self.use_cuts:

                self.cutCount +=1
                self.cutLevels[self.depth - depth] += 1
                return value, current_max_state

            alpha = max([alpha,value])

        return value, current_max_state

    def min_value(self,current_state,alpha,beta, depth):

        # Leaf node reached
        if depth == 0:
            self.leafCount += 1
            return self.evaluate(current_state, self.player), current_state

        value = float("inf")

        # Expand current state (obtain all possible resultant gamestates)
        expanded_states = current_state.exec_all_moves(1)

        # Update statistics
        self.expansionCount += 1
        self.expansionTotal += len(expanded_states)

        # State that obtained the minumum value
        current_min_state = None

        # No posssible successors (gameover)
        if len(expanded_states) == 0:
            return self.evaluate(current_state, self.player), current_state

        for state in expanded_states:

            # Evaluate max's turn
            max_v =  self.max_value(state, alpha, beta, depth - 1)[0]

            # Update best state
            if max_v < value:
                current_min_state = state
                value = max_v

            # Execute prunning
            if value <= alpha and self.use_cuts:
                self.cutCount += 1
                self.cutLevels[self.depth - depth] += 1
                return value, current_min_state

            beta = min([beta,value])

        return value,current_min_state

    """"
    Minimax using move ordering and alpha-beta prunning. Uses heaps to order the child states by there evaluation result, this is done in order to better understand
    what would be the bext next move to explore.
    """

    def max_value_order(self,current_state,alpha,beta, depth):

        value = -float("inf")

        # Expand current state (obtain all possible resultant gamestates)
        expanded_states = current_state.exec_all_moves(1)

        # Evaluate tuples and build heap nodes
        for i in range(len(expanded_states)):
            expanded_states[i] = (-self.evaluate(expanded_states[i], self.player),id(expanded_states[i]),expanded_states[i])

        # Create heap
        heapq.heapify(expanded_states)

        # Update statistics
        self.expansionCount += 1
        self.expansionTotal += len(expanded_states)

        # State that obtained the max value
        current_max_state = None

        # No posssible successors (gameover)
        if len(expanded_states) == 0:
            return self.evaluate(current_state, self.player), current_state

        while len(expanded_states) > 0:

            # Get next state
            state = heapq.heappop(expanded_states)

            # If the next state if a leaf, no need to test next states in heap (already the best)
            if depth == 1:
                self.leafCount += 1
                min_v = -state[0]
                expanded_states = []
            else:

                # Evaluate min's turn
                min_v = self.min_value_order(state[2], alpha, beta, depth - 1)[0]

            # Update best state
            if min_v > value :
                current_max_state = state[2]
                value = min_v

            # Execute prunning
            if value >= beta and self.use_cuts:
                self.cutCount +=1
                self.cutLevels[self.depth - depth] += 1
                return value, current_max_state

            alpha = max([alpha,value])

        return value, current_max_state

    def min_value_order(self,current_state,alpha,beta, depth):

        value = float("inf")

        # Expand current state (obtain all possible resultant gamestates)
        expanded_states = current_state.exec_all_moves(1)

        # Evaluate tuples and build heap nodes
        for i in range(len(expanded_states)):
            expanded_states[i] = (self.evaluate(expanded_states[i], self.player),id(expanded_states[i]),expanded_states[i])

        heapq.heapify(expanded_states)

        # Update statistics
        self.expansionCount += 1
        self.expansionTotal += len(expanded_states)

        # State that obtained the minumum value
        current_min_state = None

        # No posssible successors (gameover)
        if len(expanded_states) == 0:
            return self.evaluate(current_state, self.player), current_state

        while len(expanded_states) > 0:

            # Get next state
            state = heapq.heappop(expanded_states)

            # If the next state if a leaf, no need to test next states in heap (already the best)
            if depth == 1:
                self.leafCount += 1
                max_v = state[0]
                expanded_states = []
            else:

                # Evaluate max's turn
                max_v =  self.max_value_order(state[2], alpha, beta, depth - 1)[0]

            # Update best state
            if max_v < value:
                current_min_state = state[2]
                value = max_v

            # Execute prunning
            if value <= alpha and self.use_cuts:
                self.cutCount += 1
                self.cutLevels[self.depth - depth] += 1
                return value, current_min_state

            beta = min([beta,value])

        return value,current_min_state

    """
    Evaluation functions used for the minimax search. These functions return a numeric value of the given board (higher values signify a good gamestate)
    The evaluation is made according to the player given as an argument
    """

    def eval1(self, state, player_perspective):
        enemy = state.get_enemy(player_perspective)

        pieces_count = 0
        enemypieces_count = 0
        dist_sum = 0

        for row in range(1, 9):
            for column in range(1, 9):
                if(state.board.get_element(column, row) == player_perspective):
                    pieces_count += 1
                    if(player_perspective == 1):
                        dist_sum += (9 - row)
                    else:
                        dist_sum += row
                elif(state.board.get_element(column, row) == enemy):
                    enemypieces_count += 1

        # pieces = self.board.normalized_pieces(player_perspective)
        # enemypieces = self.board.pieces(self.get_enemy(player_perspective))
        # distances = [y for (_, y) in pieces]
        random_factor = id(state) // 1000 % 3

        # return sum(distances) + (len(pieces) - len(enemypieces)) + random_factor #+ self.board.column_control(player_perspective)
        # print("Dist: " + str(dist_sum) + "\t Piece Diff: " + str(pieces_count - enemypieces_count))
        return dist_sum + (pieces_count - enemypieces_count) + random_factor #+ self.board.column_control(player_perspective)

    def eval2(self, state, player_perspective):
        enemy = state.get_enemy(player_perspective)

        pieces_count = 0
        enemypieces_count = 0
        dist_sum = 0
        out_columns_player = 0
        out_columns_enemy = 0


        for row in range(1, 9):
            for column in range(1, 9):
                if(column == 1 or column == 8):
                    if(state.board.get_element(column, row) == player_perspective):
                        out_columns_player += 1
                    elif(state.board.get_element(column, row) == enemy):
                        out_columns_enemy += 1
                if(state.board.get_element(column, row) == player_perspective):
                    pieces_count += 1
                    if(player_perspective == 1):
                        dist_sum += (9 - row)
                    else:
                        dist_sum += row
                elif(state.board.get_element(column, row) == enemy):
                    enemypieces_count += 1

        random_factor = id(state) // 1000 % 3

        return dist_sum/3.0 + (pieces_count - enemypieces_count)*3.0 + (out_columns_player)*2 + random_factor

    def eval3(self, state, player_perspective):
        enemy = state.get_enemy(player_perspective)

        pieces_count = 0
        enemypieces_count = 0
        dist_sum = 0
        out_columns_player = 0
        out_columns_enemy = 0


        for row in range(1, 9):
            for column in range(1, 9):
                if(column == 1 or column == 8):
                    if(state.board.get_element(column, row) == player_perspective):
                        out_columns_player += 1
                    elif(state.board.get_element(column, row) == enemy):
                        out_columns_enemy += 1
                if(state.board.get_element(column, row) == player_perspective):
                    pieces_count += 1
                    if(player_perspective == 1):
                        dist_sum += (9 - row)
                    else:
                        dist_sum += row
                elif(state.board.get_element(column, row) == enemy):
                    enemypieces_count += 1

        random_factor = id(state) // 1000 % 3

        return dist_sum/3.0 + (pieces_count - enemypieces_count)*3.0 + (out_columns_player- out_columns_enemy)*2.3 + random_factor

    def eval4(self, state, player_perspective):
        enemy = state.get_enemy(player_perspective)

        pieces_count = 0
        enemypieces_count = 0
        dist_sum = 0

        center = 0

        for row in range(1, 9):
            for column in range(1, 9):
                piece = state.board.get_element(column, row)
                if not piece == player_perspective:
                    continue
                if column == 1 or column == 8:
                    center += 9
                elif column == 2 or column == 7:
                    center += 1
                elif column == 3 or column == 6:
                    center += 2
                elif column == 5 or column == 4:
                    center += 4.5

                # player 1
                if player_perspective == 1:
                    dist_sum += (9 - row)
                # player 2
                else:
                    dist_sum += row

        random_factor = id(state) // 1000 % 3

        return dist_sum/3.0 + (pieces_count - enemypieces_count)*2.4 + center/3.5 + random_factor

