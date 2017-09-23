class Player(object):
    """Player class

       Attributes:
           name (str): Player name
    """

    def __init__(self, name):
        """Initialize player

           Args:
               name (str): Player name
        """
        self.name = name

    def place_troops(self, board, n_troops):
        """Place troops on territories

           Args:
               board (Gameboard): The gameboard
               n_troops (int): Number of new troops to deploy

           Returns:
               (dict(str, int)): Dictionary of territories with number of troops to be deployed
        """
        raise NotImplementedError('place_troops not implemented')

    def do_attack(self, board):
        """Decide whether or not to continue attacking

           Args:
               board (Gameboard): The gameboard

           Returns:
               (bool): Whether or not to continue attacking
        """
        raise NotImplementedError('do_attack not implemented')

    def attack(self, board):
        """Attack phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str): from_territory, to_territory
        """
        raise NotImplementedError('attack not implemented')

    def do_move_troops(self, board):
        """Decide whether or not to move troops

           Args:
               board (Gameboard): The gameboard

           Returns:
               (bool): Whether or not to move troops
        """
        raise NotImplementedError('do_move_troops not implemented')

    def move_troops(self, board):
        """Troop movement phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str, int): from_territory, to_territory, n_troops
        """
        raise NotImplementedError('move_troops not implemented')
