import sys
import argparse

"""
    This module is used to parse the eximo game's command line arguments

"""

def normalize_input_matrix(types,depth,heur,cuts, ords):

    """
    Change the format of the matrices in games where there exists only one computer (e.g. [False] to [None, False])
    """
    newDepth = []
    newHeur = []
    newCuts = []
    newOrds = []

    for tp in types:

        if tp == 'C':
            newDepth.append(depth[0])
            newHeur.append(heur[0])
            newCuts.append(cuts[0])
            newOrds.append(ords[0])
        else:
            newDepth.append(None)
            newHeur.append(None)
            newCuts.append(None)
            newOrds.append(None)


    return newDepth,newHeur,newCuts,newOrds

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_arguments(parser):

    parser.add_argument('--mode', choices=['P','C'],required=True, nargs= 2, help="Mode of player 1 and player 2 ('P' for human, 'C' for computer)")
    parser.add_argument('--heur', type=int, choices=range(1,5), nargs = '+', help="Name(s) of the heuristic functions to be used in each player (only needed if (one or more) of the players is AI player)", default=[None,None])
    parser.add_argument('--depth', type=int, choices=range(1,10), nargs = '+', help="Depth(s), of search (only needed if (one or more) of the players is AI player)", default=[None,None])
    parser.add_argument('--cuts',type=str2bool, nargs = '+', help="True or False choice if the computers should use cuts", default=[True,True])
    parser.add_argument('--ord',type=str2bool, nargs = '+', help="True or False choice if the computers should use state choice ordering", default=[True,True])

    args = parser.parse_args()

    computerCount = args.mode.count('C')
    depthCount = len(args.depth)
    heurCount = len(args.heur)
    if computerCount != 0:
        if heurCount > computerCount:
            parser.print_help()
            print('You chose too many heuristic functions...')
            sys.exit(-1)
        elif heurCount < computerCount:
            parser.print_help()
            print('You need to choose one heuristic function for each AI player...')
            sys.exit(-1)
        else:

            if depthCount > computerCount:
                parser.print_help()
                print('You chose too many depth limits...')
                sys.exit(-1)
            elif depthCount < computerCount:
                parser.print_help()
                print('You need to choose one depth limit for each AI player...')
                sys.exit(-1)

    mode = args.mode
    heur = args.heur
    depth = args.depth
    cuts = args.cuts
    ords = args.ord

    if computerCount == 1:
        depth,heur,cuts,ords = normalize_input_matrix(mode,depth,heur,cuts,ords)

    return mode, heur, depth, cuts, ords

