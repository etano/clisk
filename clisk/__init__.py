from player import *
from gameboard import *

import random
random.seed(0)

class Game(object):
    """Game class

       Attributes:
           players (dict(str, Player)): Players
           board (Board): Gameboard
    """

    def __init__(self, n_players):
        """Initialize game

           Args:
               n_players (int): Number of players
        """
        # Set up players
        if n_players < 2: raise ValueError('# of players must be at least 2')
        self.players = {}
        for i in range(n_players):
            name = str(i)
            self.players[name] = RandomPlayer(name)

        # Set up gameboard
        self.board = Gameboard()

        # Set up pieces
        self.setup_pieces()

        # Start engine
        self.run_engine()

    def setup_pieces(self):
        """Assign territories and troops to players
        """
        # Randomly distribute territories
        territories = self.board.get_territories()
        n_territories = len(territories)
        t_assignment = []
        for name in self.players.keys():
            t_assignment += [name] * (n_territories // len(self.players))
        for name in self.players.keys():
            if len(t_assignment) == n_territories: break
            t_assignment += [name]
        random.shuffle(t_assignment)
        for i in range(n_territories):
            self.players[t_assignment[i]].territories[territories[i]] = 1

        # Randomly assign troops
        starting_troops = 45 # TODO: Should be determined from number of players and territories
        for p in self.players.values():
            territories = p.territories.keys()
            total_troops = len(territories)
            while total_troops < starting_troops:
                p.territories[random.choice(territories)] += 1
                total_troops += 1

    def is_game_over(self):
        """Check if game is over

           Returns:
               (bool): Whether or not the game is over
        """
        n_territories = len(self.board.get_territories())
        for player in self.players.values():
            if len(player.territories) == n_territories:
                print('%s wins!' % (player.name))
                return True
        return False

    def collect_troops(self, player):
        """Collect troops at the beginning of a player's turn

           Args:
               player (Player): Relevant player

           Returns:
               (int): Number of new troops to deploy
        """
        if not len(player.territories): return 0
        n_troops = max(3, len(player.territories) // 3)
        print('Player %s receives %i extra troops for owning %i territories' % (player.name, n_troops, len(player.territories)))
        for region in self.board.regions:
            n_matching = 0
            for territory in region['territories']:
                if not (territory in player.territories):
                    break
                n_matching += 1
            if n_matching == len(region['territories']):
                print('Player %s receives %i extra troops for owning %s' % (player.name, region['value'], region['name']))
                n_troops += region['value']
        return n_troops

    def roll(self, n_attack_dice, n_defend_dice):
        """Roll the dice and report the losses

           Args:
               n_attack_dice (int): Number of attacking dice
               n_defend_dice (int): Number of defending dice
        """
        attack_dice = sorted([random.randint(1, 6) for x in range(n_attack_dice)], reverse=True)
        defend_dice = sorted([random.randint(1, 6) for x in range(n_defend_dice)], reverse=True)
        print('Attacker rolled %s, defender rolled %s' % (str(attack_dice), str(defend_dice)))
        losses = [0, 0]
        for i in range(min(n_attack_dice, n_defend_dice)):
            if attack_dice[i] > defend_dice[i]:
                losses[1] += 1
            else:
                losses[0] += 1
        print('Attacker loses %i troops, defender loses %i troops' % (losses[0], losses[1]))
        return losses

    def get_player(self, territory):
        """Get player from territory

           Args:
               territory (str): Name of territory

           Returns:
               (Player): Player who owns the territory
        """
        for player in self.players.values():
            if territory in player.territories:
                return player

    def attack_to_completion(self, from_territory, to_territory):
        """Attack to completion

           Args:
               from_territory (str): Name of territory attacking
               to_territory (str): Name of territory begin attacked
        """
        from_player = self.get_player(from_territory)
        to_player = self.get_player(to_territory)
        n_from_troops = from_player.territories[from_territory]
        n_to_troops = to_player.territories[to_territory]
        while (n_from_troops > 1) and (to_territory in to_player.territories):
            print('Player %s is attacking %s (o: %s, n: %i) from %s (o: %s, n: %i)' %
                  (from_player.name, to_territory, to_player.name, n_to_troops, from_territory, from_player.name, n_from_troops))

            # Roll the dice
            n_attack_dice = min(3, n_from_troops-1)
            n_defend_dice = min(2, n_to_troops)
            losses = self.roll(n_attack_dice, n_defend_dice)

            # Apply the losses
            n_from_troops -= losses[0]
            n_to_troops -= losses[1]
            from_player.territories[from_territory] = n_from_troops
            to_player.territories[to_territory] = n_to_troops

            # Check if territory is won
            if not n_to_troops:
                del to_player.territories[to_territory]
                from_player.territories[to_territory] = n_from_troops - 1
                from_player.territories[from_territory] = 1
                print('Player %s won %s and is moving %i troops' % (from_player.name, to_territory, from_player.territories[to_territory]))

    def draw(self):
        """Draw the board
        """
        for player in self.players.values():
            for territory, n_troops in player.territories.items():
                self.board.assign(territory, player.name, n_troops)
        self.board.draw()

    def run_engine(self):
        """Run the main game loop
        """
        while(not self.is_game_over()): # Main loop
            for player in self.players.values(): # Turn loop
                # Troop placement phase
                n_troops = self.collect_troops(player)
                placements = player.place_troops(self.board, n_troops)
                for territory, n_troops in placements.items():
                    player.territories[territory] += n_troops
                    print('Player %s is placing %i troop(s) on %s' % (player.name, n_troops, territory))
                self.draw()

                # Attack phase
                # TODO: multiple attacks
                # TODO: don't always attack until completion
                from_territory, to_territory = player.attack(self.board)
                if from_territory and to_territory:
                    self.attack_to_completion(from_territory, to_territory)
                    self.draw()

                # Troop move phase
                from_territory, to_territory, n_move_troops = player.move_troops(self.board)
                if from_territory and to_territory and n_move_troops:
                    player.territories[from_territory] -= n_move_troops
                    player.territories[to_territory] += n_move_troops
                    print('Player %s is moving %i troops from %s to %s' % (player.name, n_move_troops, from_territory, to_territory))
                    self.draw()
