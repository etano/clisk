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
        # TODO: Optimize
        return [x for x in self.graph.nodes.keys() if self.graph.nodes[x].att['o'] == player]

    def get_attacking_territories(self, player):
        """Return a list of territories that are able to attack

           Args:
               player (Player): Relevant player

           Returns:
               (list): List of territories
        """
        return [x for x in self.get_territories(player) if (self.get_n_troops(x) > 1) and len(self.get_hostile_neighbors(x))]

    def get_moving_territories(self, player):
        """Return a list of territories that are able to move

           Args:
               player (Player): Relevant player

           Returns:
               (list): List of territories
        """
        return [x for x in self.get_territories(player) if (self.get_n_troops(x) > 1) and len(self.get_friendly_neighbors(x))]

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
        return [x for x in self.get_neighbors(territory) if self.get_owner(x) == self.get_owner(territory)]

    def get_hostile_neighbors(self, territory):
        """Return a list of territories neighboring a given territory

           Args:
               territory (str): Name of territory

           Returns:
               (list): List of territories
        """
        return [x for x in self.get_neighbors(territory) if self.get_owner(x) != self.get_owner(territory)]

    def get_regions(self, player=None):
        """Return a list of regions

           Args:
               player (Player): Relevant player (if None, use all players)

           Returns:
               (list(dict(str, value)): List of regions
        """
        if not player: return self.regions
        # TODO: Optimize
        territories = self.get_territories(player)
        regions = []
        for region in self.regions:
            n_matching = 0
            for territory in region['territories']:
                if not (territory in territories):
                    break
                n_matching += 1
            if n_matching == len(region['territories']):
                regions.append(region)
        return regions

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
        territories = self.get_territories()
        players = list(set([self.get_owner(x) for x in territories]))
        for player in players:
            print('Player %s: territories: %i, regions: %i' % (player, len(self.get_territories(player)), len(self.get_regions(player))))
        print('---')
