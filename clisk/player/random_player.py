import random
from player import Player

class RandomPlayer(Player):
    """RandomPlayer class

       Attributes:
           name (str): Player name
           territories (dict(str, int)): Dictionary of territories and troops
           seed (int): Random seed
    """

    def __init__(self, name, seed=0):
        """Initialize player

           Args:
               name (str): Player name
               seed (int): Random seed
        """
        super(RandomPlayer, self).__init__(name)
        random.seed(seed)

    def place_troops(self, board, n_troops):
        """Place troops on territories

           Args:
               board (Gameboard): The gameboard
               n_troops (int): Number of new troops to deploy

           Returns:
               (dict(str, int)): Dictionary of territories with number of troops to be deployed
        """
        placements = {}
        for i in range(n_troops):
            territory = random.choice(self.territories.keys())
            if territory in placements: placements[territory] += 1
            else: placements[territory] = 1
        return placements

    def attack(self, board):
        """Attack phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str): from_territory, to_territory
        """
        from_territory, to_territory = None, None

        # Get all loaded territories
        loaded_territories = [x for x in self.territories.keys() if self.territories[x] > 1]
        if not loaded_territories:
            return from_territory, to_territory

        # Choose a random loaded territory and a random non-owned neighbor to attack
        random.shuffle(loaded_territories)
        for i in range(len(loaded_territories)):
            from_territory = loaded_territories[i]
            neighbor_territories = [x for x in board.get_neighbors(from_territory) if not (x in self.territories.keys())]
            if neighbor_territories:
                to_territory = random.choice(neighbor_territories)
                return from_territory, to_territory
        return from_territory, to_territory

    def move_troops(self, board):
        """Troop movement phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str, int): from_territory, to_territory, n_troops
        """
        from_territory, to_territory, n_troops = None, None, 0

        # Get all loaded territories
        loaded_territories = [x for x in self.territories.keys() if self.territories[x] > 1]
        if not loaded_territories:
            return from_territory, to_territory, n_troops

        # Choose a random loaded territory and a random owned neighbor to move to
        random.shuffle(loaded_territories)
        for i in range(len(loaded_territories)):
            from_territory = loaded_territories[i]
            neighbor_territories = [x for x in board.get_neighbors(from_territory) if (x in self.territories.keys())]
            if neighbor_territories:
                # Move all but 1
                n_troops = self.territories[from_territory] - 1
                to_territory = random.choice(neighbor_territories)
                return from_territory, to_territory, n_troops
        return from_territory, to_territory, n_troops
