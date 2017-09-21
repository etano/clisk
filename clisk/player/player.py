class Player(object):
    """Player class

       Attributes:
           name (str): Player name
           territories (dict(str, int)): Dictionary of territories and troops
    """

    def __init__(self, name):
        """Initialize player

           Args:
               name (str): Player name
        """
        self.name = name
        self.territories = {}

    def place_troops(self, board, n_troops):
        """Place troops on territories

           Args:
               board (Gameboard): The gameboard
               n_troops (int): Number of new troops to deploy

           Returns:
               (dict(str, int)): Dictionary of territories with number of troops to be deployed
        """
        raise NotImplementedError('place_troops not implemented')

    def attack(self, board):
        """Attack phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str): from_territory, to_territory
        """
        raise NotImplementedError('attack not implemented')

    def move_troops(self, board):
        """Troop movement phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str, int): from_territory, to_territory, n_troops
        """
        raise NotImplementedError('move_troops not implemented')
