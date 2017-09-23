import sys
from classic_board import ClassicBoard
from grid_board import GridBoard

def create_board(type):
    """Board factory

       Args:
           type (str): Type of board

       Returns:
           (Board): Game board
    """
    if type == 'classic': return ClassicBoard()
    elif type == 'grid': return GridBoard()
    else:
        print('error: Unrecognized board type: %s' % (args.board))
        sys.exit(1)
