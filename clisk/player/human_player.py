import readline
from player import Player

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
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims('')

    def place_troops(self, board, n_troops):
        """Place troops on territories

           Args:
               board (Gameboard): The gameboard
               n_troops (int): Number of new troops to deploy

           Returns:
               (dict(str, int)): Dictionary of territories with number of troops to be ed
        """
        board.draw()

        territories = board.get_territories(self.name)
        placements = {}
        n_troops_left = n_troops
        while n_troops_left > 0:
            print('%i troops left to deploy' % n_troops_left)
            territory = self.get_territory(territories, prompt='Enter a territory to deploy troops to', use_default=False)
            n_troops_deploy = self.get_n_troops(1, n_troops_left, prompt='Enter number of troops to deploy', default=n_troops_left)
            if not (territory in placements): placements[territory] = 0
            placements[territory] += n_troops_deploy
            n_troops_left -= n_troops_deploy
        return placements

    def do_attack(self, board):
        """Decide whether or not to attack

           Args:
               board (Gameboard): The gameboard

           Returns:
               (bool): Whether or not to attack
        """
        board.draw()
        return self.get_choice(prompt='Would you like to attack?')

    def attack(self, board):
        """Attack phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str): from_territory, to_territory
        """
        from_territory, to_territory = None, None

        # Get all valid attacking territories
        from_territories = board.get_attacking_territories(self.name)
        if not from_territories:
            print('Cannot attack from any territory')
            return from_territory, to_territory

        # Get attack territories from user
        from_territory = self.get_territory(from_territories, prompt='Enter a territory to attack from')
        if from_territory:
            to_territory = self.get_territory(board.get_hostile_neighbors(from_territory), prompt='Enter a territory to attack')
        return from_territory, to_territory

    def do_move_troops(self, board):
        """Decide whether or not to move troops

           Args:
               board (Gameboard): The gameboard

           Returns:
               (bool): Whether or not to move troops
        """
        board.draw()
        return self.get_choice(prompt='Would you like to move troops?')

    def move_troops(self, board):
        """Troop movement phase

           Args:
               board (Gameboard): The gameboard

           Returns:
               (str, str, int): from_territory, to_territory, n_troops
        """
        from_territory, to_territory, n_troops = None, None, 0

        # Get all valid moving territories
        from_territories = board.get_moving_territories(self.name)
        if not from_territories:
            print('Cannot move from any territory')
            return from_territory, to_territory, n_troops

        # Get moving territories and number of troops from user
        from_territory = self.get_territory(from_territories, prompt='Enter a territory to move from')
        if from_territory:
            to_territory = self.get_territory(board.get_friendly_neighbors(from_territory), prompt='Enter a territory to move to')
            if to_territory:
                min_troops, max_troops = 1, board.get_n_troops(from_territory)-1
                n_troops = self.get_n_troops(min_troops, max_troops, prompt='Enter number of troops to move', default=max_troops)
        return from_territory, to_territory, n_troops

    def custom_complete(self, commands):
        """Create a custom tab completion function

           Args:
               commands (list(str)): List of commands to tab complete

           Returns:
               (function(str, int) -> str): Completion function
        """
        def complete(text, state):
            for cmd in commands:
                if cmd.startswith(text):
                    if not state:
                        return cmd
                    else:
                        state -= 1
        return complete

    def get_choice(self, prompt='?', use_default=True, default='n'):
        """Get a yes/no choice from the user

           Args:
               prompt (str): Prompt for user entry
               use_default (bool): Whether or not to use the default value
               default (str): Default value

           Returns:
               (bool): Choice
        """
        prompt += ' (yY/nN'
        if use_default: prompt += ', default: %s' % (default)
        prompt += '): '
        while True:
            try:
                choice = raw_input(prompt)
                if not choice: choice = default
                if choice == 'y' or choice == 'Y': return True
                if choice == 'n' or choice == 'N': return False
                raise ValueError('%s is not a valid response.' % (choice))
            except Exception as e:
                print(e)

    def get_territory(self, territories, prompt='Enter a territory', use_default=True, default=None):
        """Get a territory from the user

           Args:
               territories (list(str)): List of territories to choose from
               prompt (str): Prompt for user entry
               use_default (bool): Whether or not to use the default value
               default (str): Default value

           Returns:
               (str): Chosen territory
        """
        readline.set_completer(self.custom_complete(territories))
        if use_default: prompt += ' (default: %s)' % (str(default))
        prompt += ': '
        while True:
            try:
                territory = raw_input(prompt)
                if use_default and (not territory): return default
                if not (territory in territories): raise ValueError('"%s" is not a valid territory' % (territory))
                return territory
            except Exception as e:
                print(e)

    def get_n_troops(self, min_troops, max_troops, prompt='Enter number of troops', use_default=True, default=None):
        """Get a number of troops from the user

           Args:
               min_troops (int): Minimum number of troops
               max_troops (int): Maximum number of troops
               prompt (str): Prompt for user entry
               use_default (bool): Whether or not to use the default value
               default (str): Default value

           Returns:
               (int): Chosen number of troops
        """
        readline.set_completer(self.custom_complete([str(x) for x in range(min_troops, max_troops+1)]))
        prompt += ' (%i-%i' % (min_troops, max_troops)
        if use_default: prompt += ', default: %i' % (default)
        prompt += '): '
        while True:
            try:
                n_troops = raw_input(prompt)
                if use_default and (not n_troops): return default
                if not n_troops.isdigit(): raise TypeError('Must be a positive integer')
                n_troops = int(n_troops)
                if (n_troops < min_troops): raise ValueError('Number of troops cannot be less than %i' % (min_troops))
                if (n_troops > max_troops): raise ValueError('Number of troops cannot be more than %i' % (max_troops))
                return n_troops
            except Exception as e:
                print(e)
