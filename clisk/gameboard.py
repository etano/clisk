from graphscii import Graph

class Gameboard(object):
    """Gameboard class

       Attributes:
           graph (graphscii.Graph): Gameboard graph
           regions (list(dict(str, val))): Region definitions
    """

    def __init__(self):
        """Initialize gameboard
        """
        self.graph = Graph()
        self.regions = []

        # North America
        self.regions.append({
            'name': 'North America',
            'value': 5,
            'territories': [
                'Alaska', 'Northwest Territory', 'Greenland',
                'Alberta', 'Ontario', 'Quebec',
                'Western US', 'Eastern US', 'Central America'
            ]
        })
        self.graph.add_node('Alaska', pos=[0, 0], show_att=True)
        self.graph.add_node('Northwest Territory', pos=[0.1, 0.1], show_att=True)
        self.graph.add_node('Greenland', pos=[0.3, 0.05], show_att=True)
        self.graph.add_node('Alberta', pos=[0.05, 0.2], show_att=True)
        self.graph.add_node('Ontario', pos=[0.15, 0.3], show_att=True)
        self.graph.add_node('Quebec', pos=[0.25, 0.25], show_att=True)
        self.graph.add_node('Western US', pos=[0.05, 0.4], show_att=True)
        self.graph.add_node('Eastern US', pos=[0.25, 0.45], show_att=True)
        self.graph.add_node('Central America', pos=[0.15, 0.6], show_att=True)
        self.graph.add_edge('Alaska', 'Northwest Territory')
        self.graph.add_edge('Alaska', 'Alberta')
        self.graph.add_edge('Northwest Territory', 'Alberta')
        self.graph.add_edge('Northwest Territory', 'Ontario')
        self.graph.add_edge('Northwest Territory', 'Greenland')
        self.graph.add_edge('Alberta', 'Ontario')
        self.graph.add_edge('Alberta', 'Western US')
        self.graph.add_edge('Ontario', 'Greenland')
        self.graph.add_edge('Ontario', 'Quebec')
        self.graph.add_edge('Ontario', 'Western US')
        self.graph.add_edge('Ontario', 'Eastern US')
        self.graph.add_edge('Greenland', 'Quebec')
        self.graph.add_edge('Western US', 'Eastern US')
        self.graph.add_edge('Western US', 'Central America')
        self.graph.add_edge('Quebec', 'Eastern US')
        self.graph.add_edge('Eastern US', 'Central America')

        # South America
        self.regions.append({
            'name': 'South America',
            'value': 2,
            'territories': [
                'Venezuela', 'Brazil', 'Peru', 'Argentina'
            ]
        })
        self.graph.add_node('Venezuela', pos=[0.2, 0.7], show_att=True)
        self.graph.add_node('Brazil', pos=[0.3, 0.85], show_att=True)
        self.graph.add_node('Peru', pos=[0.15, 0.8], show_att=True)
        self.graph.add_node('Argentina', pos=[0.2, 1.0], show_att=True)
        self.graph.add_edge('Venezuela', 'Brazil')
        self.graph.add_edge('Venezuela', 'Peru')
        self.graph.add_edge('Brazil', 'Peru')
        self.graph.add_edge('Brazil', 'Argentina')
        self.graph.add_edge('Peru', 'Argentina')

        # Africa
        self.regions.append({
            'name': 'Africa',
            'value': 3,
            'territories': [
                'North Africa', 'Egypt', 'East Africa',
                'Congo', 'South Africa', 'Madagascar'
            ]
        })
        self.graph.add_node('North Africa', pos=[0.45, 0.65], show_att=True)
        self.graph.add_node('Egypt', pos=[0.55, 0.6], show_att=True)
        self.graph.add_node('East Africa', pos=[0.65, 0.7], show_att=True)
        self.graph.add_node('Congo', pos=[0.5, 0.8], show_att=True)
        self.graph.add_node('South Africa', pos=[0.55, 1.0], show_att=True)
        self.graph.add_node('Madagascar', pos=[0.6, 0.9], show_att=True)
        self.graph.add_edge('North Africa', 'Egypt')
        self.graph.add_edge('North Africa', 'East Africa')
        self.graph.add_edge('North Africa', 'Congo')
        self.graph.add_edge('Egypt', 'East Africa')
        self.graph.add_edge('East Africa', 'Congo')
        self.graph.add_edge('East Africa', 'Madagascar')
        self.graph.add_edge('Congo', 'South Africa')
        self.graph.add_edge('Madagascar', 'South Africa')

        # Europe
        self.regions.append({
            'name': 'Europe',
            'value': 5,
            'territories': [
                'Western Europe', 'Southern Europe', 'Northern Europe',
                'Great Britain', 'Iceland', 'Scandinavia', 'Ukraine'
            ]
        })
        self.graph.add_node('Western Europe', pos=[0.45, 0.5], show_att=True)
        self.graph.add_node('Southern Europe', pos=[0.6, 0.45], show_att=True)
        self.graph.add_node('Northern Europe', pos=[0.55, 0.35], show_att=True)
        self.graph.add_node('Great Britain', pos=[0.4, 0.3], show_att=True)
        self.graph.add_node('Iceland', pos=[0.4, 0.2], show_att=True)
        self.graph.add_node('Scandinavia', pos=[0.55, 0.1], show_att=True)
        self.graph.add_node('Ukraine', pos=[0.65, 0.2], show_att=True)
        self.graph.add_edge('Western Europe', 'Southern Europe')
        self.graph.add_edge('Western Europe', 'Northern Europe')
        self.graph.add_edge('Western Europe', 'Great Britain')
        self.graph.add_edge('Southern Europe', 'Northern Europe')
        self.graph.add_edge('Southern Europe', 'Ukraine')
        self.graph.add_edge('Northern Europe', 'Great Britain')
        self.graph.add_edge('Northern Europe', 'Ukraine')
        self.graph.add_edge('Northern Europe', 'Scandinavia')
        self.graph.add_edge('Great Britain', 'Scandinavia')
        self.graph.add_edge('Great Britain', 'Iceland')
        self.graph.add_edge('Ukraine', 'Scandinavia')
        self.graph.add_edge('Scandinavia', 'Iceland')

        # Asia
        self.regions.append({
            'name': 'Asia',
            'value': 7,
            'territories': [
                'Middle East', 'Afghanistan', 'India',
                'Ural', 'China', 'Siberia', 'Mongolia',
                'Yakutsk', 'Irkutsk', 'Kamchatka',
                'Japan', 'Siam'
            ]
        })
        self.graph.add_node('Middle East', pos=[0.7, 0.55], show_att=True)
        self.graph.add_node('Afghanistan', pos=[0.75, 0.4], show_att=True)
        self.graph.add_node('India', pos=[0.8, 0.6], show_att=True)
        self.graph.add_node('Ural', pos=[0.75, 0.15], show_att=True)
        self.graph.add_node('China', pos=[0.85, 0.5], show_att=True)
        self.graph.add_node('Siberia', pos=[0.825, 0.2], show_att=True)
        self.graph.add_node('Mongolia', pos=[0.95, 0.4], show_att=True)
        self.graph.add_node('Yakutsk', pos=[0.9, 0.1], show_att=True)
        self.graph.add_node('Irkutsk', pos=[0.9, 0.25], show_att=True)
        self.graph.add_node('Kamchatka', pos=[1.0, 0.0], show_att=True)
        self.graph.add_node('Japan', pos=[1.0, 0.25], show_att=True)
        self.graph.add_node('Siam', pos=[0.9, 0.65], show_att=True)
        self.graph.add_edge('Middle East', 'Afghanistan')
        self.graph.add_edge('Middle East', 'India')
        self.graph.add_edge('Afghanistan', 'India')
        self.graph.add_edge('Afghanistan', 'Ural')
        self.graph.add_edge('Afghanistan', 'China')
        self.graph.add_edge('India', 'China')
        self.graph.add_edge('India', 'Siam')
        self.graph.add_edge('Ural', 'China')
        self.graph.add_edge('Ural', 'Siberia')
        self.graph.add_edge('China', 'Siam')
        self.graph.add_edge('China', 'Siberia')
        self.graph.add_edge('China', 'Mongolia')
        self.graph.add_edge('Siberia', 'Mongolia')
        self.graph.add_edge('Siberia', 'Yakutsk')
        self.graph.add_edge('Siberia', 'Irkutsk')
        self.graph.add_edge('Mongolia', 'Irkutsk')
        self.graph.add_edge('Mongolia', 'Kamchatka')
        self.graph.add_edge('Mongolia', 'Japan')
        self.graph.add_edge('Yakutsk', 'Irkutsk')
        self.graph.add_edge('Yakutsk', 'Kamchatka')
        self.graph.add_edge('Irkutsk', 'Kamchatka')
        self.graph.add_edge('Kamchatka', 'Japan')

        # Australia
        self.regions.append({
            'name': 'Australia',
            'value': 2,
            'territories': [
                'Indonesia', 'New Guinea', 'Western Australia', 'Eastern Australia'
            ]
        })
        self.graph.add_node('Indonesia', pos=[0.85, 0.75], show_att=True)
        self.graph.add_node('New Guinea', pos=[1.0, 0.8], show_att=True)
        self.graph.add_node('Western Australia', pos=[0.8, 0.9], show_att=True)
        self.graph.add_node('Eastern Australia', pos=[0.9, 1.0], show_att=True)
        self.graph.add_edge('Indonesia', 'New Guinea')
        self.graph.add_edge('Indonesia', 'Western Australia')
        self.graph.add_edge('New Guinea', 'Western Australia')
        self.graph.add_edge('New Guinea', 'Eastern Australia')
        self.graph.add_edge('Western Australia', 'Eastern Australia')

        # Connections
        self.graph.add_edge('Siam', 'Indonesia', label='+')
        self.graph.add_edge('Southern Europe', 'Middle East', label='+')
        self.graph.add_edge('Ukraine', 'Ural', label='+')
        self.graph.add_edge('Ukraine', 'Afghanistan', label='+')
        self.graph.add_edge('Ukraine', 'Middle East', label='+')
        self.graph.add_edge('North Africa', 'Western Europe', label='+')
        self.graph.add_edge('North Africa', 'Southern Europe', label='+')
        self.graph.add_edge('Egypt', 'Middle East', label='+')
        self.graph.add_edge('Egypt', 'Southern Europe', label='+')
        self.graph.add_edge('East Africa', 'Middle East', label='+')
        self.graph.add_edge('Brazil', 'North Africa', label='+')
        self.graph.add_edge('Alaska', 'Kamchatka', label='+')
        self.graph.add_edge('Greenland', 'Iceland', label='+')
        self.graph.add_edge('Central America', 'Venezuela', label='+')

    def get_territories(self, player=None):
        """Return a list of territories

           Args:
               player (Player): Relevant player (if None, use all players)

           Returns:
               (list): List of territories
        """
        if not player: return self.graph.nodes.keys()
        # TODO: Optimize
        return [x for x in self.graph.nodes.keys() if self.graph.nodes[x].att['o'] == player]

    def get_neighbors(self, territory):
        """Return a list of territories neighboring a given territory

           Returns:
               (list): List of territories
        """
        # TODO: Optimize this by storing neighbors in data structure
        neighbors = []
        for edge in self.graph.edges:
            if territory == edge.n0.label: neighbors.append(edge.n1.label)
            if territory == edge.n1.label: neighbors.append(edge.n0.label)
        return neighbors

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
        return self.graph.nodes[territory].att['o']

    def assign(self, territory, player):
        """Assign a territory to a player

           Args:
               territory (str): Name of territory
               player (str): Name of player
        """
        self.graph.nodes[territory].att['o'] = player

    def draw(self):
        """Draw the board
        """
        self.graph.draw()
