from player import Player

class RandomPlayer(Player):
    """RandomPlayer class that attacks randomly until it wins a battle or can't attack anymore, and moves randomly

       Attributes:
           name (str): Player name
           random (random): Random engine
           last_attacked_territory (str): Territory last attacked
    """

    def __init__(self, name, random):
        """Initialize player

           Args:
               name (str): Player name
               random (random): Random engine
        """
        super(RandomPlayer, self).__init__(name)
        self.random = random
        self.last_attacked_territory = None

    def place_troops(self, board, n_troops):
        """Place troops on territories

           Args:
               board (Gameboard): The gameboard
               n_troops (int): Number of new troops to deploy

           Returns:
               (dict(str, int)): Dictionary of territories with number of troops to be deployed
        """
        territories = board.get_territories(self.name)
        placements = {}
        for i in range(n_troops):
            territory = self.random.choice(territories)
            if territory in placements: placements[territory] += 1
            else: placements[territory] = 1
        return placements

    def do_attack(self, board):
        """Decide whether or not to continue attacking

           Args:
               board (Gameboard): The gameboard

           Returns:
               (bool): Whether or not to continue attacking
        """
        if self.last_attacked_territory and (board.get_owner(self.last_attacked_territory) == self.name):
            self.last_attacked_territory = None
            return False
        return len(board.get_attacking_territories(self.name)) > 0

    def attack(self, board):
        """Attack phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str): from_territory, to_territory
        """
        from_territory = self.random.choice(board.get_attacking_territories(self.name))
        to_territory = self.random.choice(board.get_hostile_neighbors(from_territory))
        self.last_attacked_territory = to_territory
        return from_territory, to_territory

    def do_move_troops(self, board):
        """Decide whether or not to move troops

           Args:
               board (Gameboard): The gameboard

           Returns:
               (bool): Whether or not to move troops
        """
        return len(board.get_moving_territories(self.name)) > 0

    def move_troops(self, board):
        """Troop movement phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str, int): from_territory, to_territory, n_troops
        """
        from_territory = self.random.choice(board.get_moving_territories(self.name))
        to_territory = self.random.choice(board.get_friendly_neighbors(from_territory))
        n_troops = board.get_n_troops(from_territory) - 1
        return from_territory, to_territory, n_troops
