from Eximo import *
from Graphics import *
from Game import *
from argument_parsing import *

#python3 main.py --mode C C --heur 3 3 --depth 1 1 --cuts True True --ord True True

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Play Eximo.')
    mode, heuristics, depth, cuts, ords = parse_arguments(parser)

    game = Game(mode[0],mode[1], depth, heuristics,cuts, ords)
    game.run()


if __name__ == "__main__":
    main()