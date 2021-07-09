Python requirements:
    - Python >= 3.7
    - PyGame >= 1.9

To run the game:
    python3 main.py  --mode  <player1> <player2> [ --heur [ heuristicp1 ] [ heuristicp2 ] --depth [ maxdepthp1 ] [maxdepthp2 ] --cuts [ cutsp1 ] [cutsp2 ] --ord [ ordp1 ] [ordp2] ]

        --mode <player1> <player2>, mode of each player, may be AI (C) or Human player (P).
        --heur  [ heuristicp1 ] [ heuristicp2 ], heuristics used the AI players (1-4).
        --depth [ maxdepthp1 ] [maxdepthp2 ], maxdepth used in the AI player’s search algorithms (1-9).
        --cuts [ cutsp1 ] [cutsp2 ], True if the AI players use’s Alpha-beta pruning, False otherwise
        --ord [ ordp1 ] [ordp2 ], True if the AI players use’s move ordering, False otherwise