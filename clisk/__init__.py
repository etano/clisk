from __future__ import print_function
import argparse, random, sys
from board import create_board
from player import create_player
from game import Game

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='clisk: Command-line interface Risk.')
    parser.add_argument('-p', '--player', metavar=('name', 'type'), nargs=2, action='append',
                        dest='players', help='player type (e.g. ethan human, ai random, etc.)', required=True)
    parser.add_argument('-b', '--board', metavar='board', help='board type (e.g. classic, grid, etc.)', default='classic')
    parser.add_argument('-s', '--seed', metavar='seed', help='random seed', default=0)
    args = parser.parse_args()

    # Additional argument checks
    try:
        if len(args.players) < 2: raise ValueError('error: At least 2 players are required.')
        if len(set([name for [name, type] in args.players])) != len(args.players): raise ValueError('error: Player names must all be different.')
    except Exception as e:
        print(e)
        parser.print_usage()
        sys.exit(1)

    # Set up game
    random.seed(args.seed)
    players = [create_player(name, type, random) for [name, type] in args.players]
    board = create_board(args.board)
    game = Game(players, board, random)

    # Play game
    game.play()
