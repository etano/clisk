from graphscii import Graph

class Board(object):
    """Board class

       Attributes:
           graph (graphscii.Graph): Board graph
           regions (list(dict(str, val))): Region definitions
    """

    def __init__(self):
        """Initialize board
        """
        self.graph = Graph()
        self.regions = []

    def get_territories(self, player=None):
        """Return a list of territories

           Args:
               player (Player): Relevant player (if None, use all players)

           Returns:
               (list(str)): List of territories
        """
        if not player: return self.graph.nodes.keys()
        # TODO: Optimize by storing
        return [t for t in self.graph.nodes.keys() if self.graph.nodes[t].att['o'] == player]

    def get_attacking_territories(self, player):
        """Return a list of territories that are able to attack

           Args:
               player (Player): Relevant player

           Returns:
               (list): List of territories
        """
        return [t for t in self.get_territories(player) if (self.get_n_troops(t) > 1) and len(self.get_hostile_neighbors(t))]

    def get_moving_territories(self, player):
        """Return a list of territories that are able to move

           Args:
               player (Player): Relevant player

           Returns:
               (list): List of territories
        """
        return [t for t in self.get_territories(player) if (self.get_n_troops(t) > 1) and len(self.get_friendly_neighbors(t))]

    def get_neighbors(self, territory):
        """Return a list of territories neighboring a given territory

           Args:
               territory (str): Name of territory

           Returns:
               (list): List of territories
        """
        # TODO: Optimize this by storing neighbors in data structure
        neighbors = []
        for edge in self.graph.edges:
            if territory == edge.n0.label: neighbors.append(edge.n1.label)
            if territory == edge.n1.label: neighbors.append(edge.n0.label)
        return neighbors

    def get_friendly_neighbors(self, territory):
        """Return a list of territories neighboring a given territory

           Args:
               territory (str): Name of territory

           Returns:
               (list): List of territories
        """
        return [t for t in self.get_neighbors(territory) if self.get_owner(t) == self.get_owner(territory)]

    def get_hostile_neighbors(self, territory):
        """Return a list of territories neighboring a given territory

           Args:
               territory (str): Name of territory

           Returns:
               (list): List of territories
        """
        return [t for t in self.get_neighbors(territory) if self.get_owner(t) != self.get_owner(territory)]

    def get_regions(self, territories):
        """Return a list of regions contained in a list of territories

           Args:
               territories (list(str)): List of territories

           Returns:
               (list(dict(str, value)): List of regions
        """
        return [r for r in self.regions if all(t in territories for t in r['territories'])]

    def get_n_troops(self, territory):
        """Get number of troops on a territory

           Args:
               territory (str): Name of territory

           Returns:
               (int): Number of troops on a territory
        """
        return self.graph.nodes[territory].att['n']

    def set_n_troops(self, territory, n_troops):
        """Set number of troops on a territory

           Args:
               territory (str): Name of territory
               n_troops (int): Number of troops
        """
        if n_troops < 0: raise ValueError('# troops must be non-negative')
        self.graph.nodes[territory].att['n'] = n_troops

    def get_owner(self, territory):
        """Get player from territory

           Args:
               territory (str): Name of territory

           Returns:
               (str): Name of player who owns the territory
        """
        return self.graph.nodes[territory].att['o'] if territory in self.graph.nodes else None

    def assign(self, territory, player):
        """Assign a territory to a player

           Args:
               territory (str): Name of territory
               player (str): Name of player
        """
        self.graph.nodes[territory].att['o'] = player

    def draw(self):
        """Draw the board and print stats
        """
        print('---')
        self.graph.draw()
        players = list(set([self.get_owner(t) for t in self.get_territories()])) # TODO: Optimize by storing this
        for player in players:
            territories = self.get_territories(player)
            n_troops = sum([self.get_n_troops(t) for t in territories])
            regions = self.get_regions(territories)
            print('Player %s: troops: %i, territories: %i, regions: %i' % (player, n_troops, len(territories), len(regions)))
        print('---')
