from player import Player

# TODO: tab completion
# TODO: prompt for continuing attack

class HumanPlayer(Player):
    """HumanPlayer class

       Attributes:
           name (str): Player name
    """

    def __init__(self, name, seed=0):
        """Initialize player

           Args:
               name (str): Player name
        """
        super(HumanPlayer, self).__init__(name)

    def place_troops(self, board, n_troops):
        """Place troops on territories

           Args:
               board (Gameboard): The gameboard
               n_troops (int): Number of new troops to 

           Returns:
               (dict(str, int)): Dictionary of territories with number of troops to be ed
        """
        print('DEPLOYMENT PHASE')
        board.draw()

        territories = board.get_territories(self.name)
        placements = {}
        n_troops_left = n_troops
        while n_troops_left > 0:
            print('%i troops left to deploy' % n_troops_left)
            territory = self.get_territory(territories, prompt='Enter a territory to deploy troops to: ')
            n_troops_deploy = self.get_n_troops(1, n_troops_left, prompt='Enter number of troops to deploy: ')
            if not (territory in placements): placements[territory] = 0
            placements[territory] += n_troops_deploy
            n_troops_left -= n_troops_deploy
        return placements

    def attack(self, board):
        """Attack phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str): from_territory, to_territory
        """
        print('ATTACK PHASE')
        board.draw()

        from_territory, to_territory = None, None

        # Get all valid attacking territories
        from_territories = board.get_attacking_territories(self.name)
        if not from_territories:
            print('Cannot attack from any territory')
            return from_territory, to_territory

        # Get attack territories from user
        from_territory = self.get_territory(from_territories, prompt='Enter a territory to attack from: ', skipable=True)
        if from_territory:
            to_territory = self.get_territory(board.get_hostile_neighbors(from_territory), prompt='Enter a territory to attack: ', skipable=True)
        return from_territory, to_territory

    def move_troops(self, board):
        """Troop movement phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str, int): from_territory, to_territory, n_troops
        """
        print('MOVE PHASE')
        board.draw()

        from_territory, to_territory, n_troops = None, None, 0

        # Get all valid moving territories
        from_territories = board.get_moving_territories(self.name)
        if not from_territories:
            print('Cannot move from any territory')
            return from_territory, to_territory, n_troops

        # Get moving territories and number of troops from user
        from_territory = self.get_territory(from_territories, prompt='Enter a territory to move from: ', skipable=True)
        if from_territory:
            to_territory = self.get_territory(board.get_friendly_neighbors(from_territory), prompt='Enter a territory to move to: ', skipable=True)
            if to_territory:
                n_troops = self.get_n_troops(1, board.get_n_troops(from_territory)-1, prompt='Enter number of troops to move: ', skipable=True)
        return from_territory, to_territory, n_troops

    def get_territory(self, territories, prompt='Enter a territory: ', skipable=False):
        if skipable: prompt = '(ENTER TO SKIP) '+prompt
        while True:
            try:
                territory = raw_input(prompt)
                if skipable and (not territory):
                    print('SKIPPING')
                    return territory
                if not (territory in territories): raise ValueError('"%s" is not a valid territory' % (territory))
                return territory
            except Exception as e:
                print(e)

    def get_n_troops(self, min_troops, max_troops, prompt='Enter number of troops: ', skipable=False):
        if skipable: prompt = '(ENTER TO SKIP) '+prompt
        while True:
            try:
                n_troops = raw_input(prompt)
                if skipable and (not n_troops):
                    print('SKIPPING')
                    return n_troops
                n_troops = int(n_troops)
                if (n_troops < min_troops): raise ValueError('Number of troops cannot be less than %i' % (min_troops))
                if (n_troops > max_troops): raise ValueError('Number of troops cannot be more than %i' % (max_troops))
                return n_troops
            except Exception as e:
                print(e)
