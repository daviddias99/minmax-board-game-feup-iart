from Eximo import *
from Graphics import *
from Game import *

# python3 main.py --mode C C --heur 3 3 --depth 1 1 --cuts True True --ord True True


def run_times(game_settings, times, f):

    game = Game(*game_settings)
    print("Game: " + game.p1Type + " " + game.p2Type, end=" ", file=f),
    print(game.depths, end=" ", file=f)
    print(game.heuristics, end=" ", file=f)
    print(game.use_cuts, end=" ", file=f)
    print(game.user_state_ordering, end=";", file=f)
    print("", file=f)

    for i in range(times):
        game.run()
        stats = game.get_stats()
        print_stats_csv(stats, f)
        game = Game(*game_settings)


def print_stats_csv(stats, f):

    print(stats[2], end=",", file=f)
    for idx in range(len(stats[0])):
        print(stats[0][idx], end=",", file=f)

    for idx in range(len(stats[1])-1):
        print(stats[1][idx], end=",", file=f)

    print(stats[1][len(stats[1])-1], end=";\n", file=f)


def main():

    f = open('out2.csv', 'w')

    # run_times(['C','C', [1,3], [3,3],[True,True], [True,True]],5, f)
    # run_times(['C','C', [3,1], [3,3],[True,True], [True,True]],5, f)
    # run_times(['C','C', [1,2], [3,3],[True,True], [True,True]],5, f)
    # run_times(['C','C', [2,1], [3,3],[True,True], [True,True]],5, f)
    # run_times(['C','C', [2,3], [3,3],[True,True], [True,True]],5, f)
    # run_times(['C','C', [3,2], [3,3],[True,True], [True,True]],5, f)

    run_times(['C', 'C', [3, 3], [4, 1], [True, True], [True, True]], 5, f)
    run_times(['C', 'C', [3, 3], [1, 4], [True, True], [True, True]], 5, f)
    run_times(['C', 'C', [3, 3], [4, 2], [True, True], [True, True]], 5, f)
    run_times(['C', 'C', [3, 3], [2, 4], [True, True], [True, True]], 5, f)
    run_times(['C', 'C', [3, 3], [4, 3], [True, True], [True, True]], 5, f)
    run_times(['C', 'C', [3, 3], [3, 4], [True, True], [True, True]], 5, f)


if __name__ == "__main__":
    main()
