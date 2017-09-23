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
        return (board.get_owner(self.last_attacked_territory) != self.name) if self.last_attacked_territory else True

    def attack(self, board):
        """Attack phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str): from_territory, to_territory
        """
        from_territory, to_territory = None, None

        # Get all loaded territories
        territories = board.get_territories(self.name)
        loaded_territories = [x for x in territories if board.get_n_troops(x) > 1]
        if not loaded_territories:
            return from_territory, to_territory

        # Choose a random loaded territory and a random non-owned neighbor to attack
        self.random.shuffle(loaded_territories)
        for i in range(len(loaded_territories)):
            from_territory = loaded_territories[i]
            neighbor_territories = [x for x in board.get_neighbors(from_territory) if not (x in territories)]
            if neighbor_territories:
                to_territory = self.random.choice(neighbor_territories)
                self.last_attacked_territory = to_territory
                return from_territory, to_territory
        return from_territory, to_territory

    def do_move_troops(self, board):
        """Decide whether or not to move troops

           Args:
               board (Gameboard): The gameboard

           Returns:
               (bool): Whether or not to move troops
        """
        return True

    def move_troops(self, board):
        """Troop movement phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str, int): from_territory, to_territory, n_troops
        """
        self.last_attacked_territory = None
        from_territory, to_territory, n_troops = None, None, 0

        # Get all loaded territories
        territories = board.get_territories(self.name)
        loaded_territories = [x for x in territories if board.get_n_troops(x) > 1]
        if not loaded_territories:
            return from_territory, to_territory, n_troops

        # Choose a random loaded territory and a random owned neighbor to move to
        self.random.shuffle(loaded_territories)
        for i in range(len(loaded_territories)):
            from_territory = loaded_territories[i]
            neighbor_territories = [x for x in board.get_neighbors(from_territory) if (x in territories)]
            if neighbor_territories:
                # Move all but 1
                n_troops = board.get_n_troops(from_territory) - 1
                to_territory = self.random.choice(neighbor_territories)
                return from_territory, to_territory, n_troops
        return from_territory, to_territory, n_troops
