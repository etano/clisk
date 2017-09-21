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
            self.players[name] = Player(name)

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

    def place_troops(self, player, n_troops):
        """Place troops at the beginning of a player's turn

           Args:
               player (Player): Relevant player
               n_troops (int): Number of new troops to deploy
        """
        # TODO: Make non-random
        territories = player.territories.keys()
        for i in range(n_troops):
            territory = random.choice(territories)
            print('Player %s is placing %i troop(s) on %s' % (player.name, 1, territory))
            player.territories[territory] += 1

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

    def attack(self, player):
        """Attack phase

           Args:
               player (Player): Relevant player
        """
        # Get all loaded territories
        loaded_territories = [x for x in player.territories.keys() if player.territories[x] > 1]
        if not loaded_territories: return

        # Choose a random loaded territory and attack a random neighbor
        random.shuffle(loaded_territories)
        from_territory, to_territory = None, None
        for i in range(len(loaded_territories)):
            from_territory = loaded_territories[i]
            neighbor_territories = [x for x in self.board.get_neighbors(from_territory) if not (x in player.territories.keys())]
            if neighbor_territories:
                to_territory = random.choice(neighbor_territories)
                break # For now only 1 attack
        if (not from_territory) or (not to_territory): return

        # Get other player
        other_player = None
        for other_player in self.players.values():
            if to_territory in other_player.territories:
                break

        # Attack to completion
        n_from_troops = player.territories[from_territory]
        n_to_troops = other_player.territories[to_territory]
        while (n_from_troops > 1) and (to_territory in other_player.territories):
            print('Player %s is attacking %s (o: %s, n: %i) from %s (o: %s, n: %i)' %
                  (player.name, to_territory, other_player.name, n_to_troops, from_territory, player.name, n_from_troops))

            # Roll the dice
            n_attack_dice = min(3, n_from_troops-1)
            n_defend_dice = min(2, n_to_troops)
            losses = self.roll(n_attack_dice, n_defend_dice)

            # Apply the losses
            n_from_troops -= losses[0]
            n_to_troops -= losses[1]
            player.territories[from_territory] = n_from_troops
            other_player.territories[to_territory] = n_to_troops

            # Check if territory is won
            if not n_to_troops:
                del other_player.territories[to_territory]
                player.territories[to_territory] = n_from_troops - 1
                player.territories[from_territory] = 1
                print('Player %s won %s and is moving %i troops' % (player.name, to_territory, player.territories[to_territory]))

    def troop_move(self, player):
        """Troop movement phase

           Args:
               player (Player): Relevant player
        """
        # Get all loaded territories
        loaded_territories = [x for x in player.territories.keys() if player.territories[x] > 1]
        if not loaded_territories: return

        # Choose a random loaded territory and a random owned neighbor
        random.shuffle(loaded_territories)
        from_territory, to_territory = None, None
        for i in range(len(loaded_territories)):
            from_territory = loaded_territories[i]
            neighbor_territories = [x for x in self.board.get_neighbors(from_territory) if (x in player.territories.keys())]
            if neighbor_territories:
                to_territory = random.choice(neighbor_territories)
                break # For now only 1 attack
        if (not from_territory) or (not to_territory): return

        # Move all but 1
        n_move_troops = player.territories[from_territory] - 1
        player.territories[to_territory] += n_move_troops
        player.territories[from_territory] -= n_move_troops
        print('Player %s is moving %i troops from %s to %s' % (player.name, n_move_troops, from_territory, to_territory))

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
                n_troops = self.collect_troops(player)
                self.place_troops(player, n_troops)
                self.attack(player)
                self.troop_move(player)
                self.draw()
