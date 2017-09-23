import sys
from human_player import HumanPlayer
from random_player import RandomPlayer

def create_player(name, type, random):
    """Player factory

       Args:
           name (str): Nmae of player
           type (str): Type of player
           random (random): Random engine

       Returns:
           (Player): Player
    """
    if type == 'human': return HumanPlayer(name)
    elif type == 'random': return RandomPlayer(name, random)
    else:
        print('error: Unrecognized player type: %s' % (type))
        sys.exit(1)
