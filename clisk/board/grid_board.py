from board import Board

class GridBoard(Board):
    """A 2D grid board

       Attributes:
           graph (graphscii.Graph): Board graph
           regions (list(dict(str, val))): Region definitions
    """

    def __init__(self, region_size=2, n_regions_per_side=2):
        """Initialize board
        """
        super(GridBoard, self).__init__()

        # Add nodes and regions
        total_size = region_size * n_regions_per_side
        for i in range(n_regions_per_side):
            for j in range(n_regions_per_side):
                territories = []
                for k in range(region_size):
                    for l in range(region_size):
                        territory = str(i*region_size + k)+'-'+str(j*region_size + l)
                        self.graph.add_node(territory, pos=[float(i*region_size + k)/float(total_size-1), float(j*region_size + l)/float(total_size-1)], show_att=True)
                        territories.append(territory)
                self.regions.append({
                    'name': str(i)+'-'+str(j),
                    'value': region_size * region_size,
                    'territories': territories
                })

        # Add edges
        for i in range(total_size):
            for j in range(total_size-1):
                label = '+' if not ((j+1) % region_size) else ''
                self.graph.add_edge(str(i)+'-'+str(j), str(i)+'-'+str(j+1), label=label)
        for i in range(total_size-1):
            for j in range(total_size):
                label = '+' if not ((i+1) % region_size) else ''
                self.graph.add_edge(str(i)+'-'+str(j), str(i+1)+'-'+str(j), label=label)
