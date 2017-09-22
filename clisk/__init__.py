from player import *
from gameboard import *

# TODO: Make own random engine for Game object
import random
random.seed(0)

class Game(object):
    """Game class

       Attributes:
           players (list(Player)): List of players
           board (Board): Gameboard
    """

    def __init__(self, n_players):
        """Initialize game

           Args:
               n_players (int): Number of players
        """
        # Set up players
        if n_players < 2: raise ValueError('# of players must be at least 2')
        self.players = []
        for i in range(n_players):
            name = str(i)
            if i == 0:
                self.players.append(HumanPlayer(name))
            else:
                self.players.append(RandomPlayer(name))

        # Set up game
        self.board = Gameboard()
        self.setup_pieces()

        # Start engine
        self.run_engine()

    def setup_pieces(self):
        """Assign territories and troops to players
        """
        # Randomly distribute territories
        territories = self.board.get_territories()
        n_territories = len(territories)
        n_players = len(self.players)
        t_assignment = []
        for player in self.players:
            t_assignment += [player.name] * (n_territories // n_players)
        for player in self.players:
            if len(t_assignment) == n_territories: break
            t_assignment += [player.name]
        random.shuffle(t_assignment)
        for i in range(n_territories):
            territory, player_name = territories[i], t_assignment[i]
            self.board.assign(territory, player_name)
            self.board.set_n_troops(territory, 1)

        # Randomly assign troops
        starting_troops = 45 # TODO: Should be determined from number of players and territories
        for player in self.players:
            territories = self.board.get_territories(player.name)
            total_troops = len(territories)
            while total_troops < starting_troops:
                territory = random.choice(territories)
                self.board.set_n_troops(territory, self.board.get_n_troops(territory) + 1)
                total_troops += 1

    def is_game_over(self):
        """Check if game is over

           Returns:
               (bool): Whether or not the game is over
        """
        n_territories = len(self.board.get_territories())
        for player in self.players:
            if len(self.board.get_territories(player.name)) == n_territories:
                print('Player %s wins!' % (player.name))
                return True
        return False

    def collect_troops(self, player):
        """Collect troops at the beginning of a player's turn

           Args:
               player (Player): Relevant player

           Returns:
               (int): Number of new troops to deploy
        """
        territories = self.board.get_territories(player.name)
        n_territories = len(territories)
        if not n_territories: return 0
        n_troops = max(3, n_territories // 3)
        print('Player %s receives %i extra troops for owning %i territories' % (player.name, n_troops, n_territories))
        for region in self.board.regions:
            n_matching = 0
            for territory in region['territories']:
                if not (territory in territories):
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

    def attack_to_completion(self, from_territory, to_territory):
        """Attack to completion

           Args:
               from_territory (str): Name of territory attacking
               to_territory (str): Name of territory begin attacked
        """
        from_player = self.board.get_owner(from_territory)
        to_player = self.board.get_owner(to_territory)
        while (self.board.get_n_troops(from_territory) > 1):
            n_from_troops = self.board.get_n_troops(from_territory)
            n_to_troops = self.board.get_n_troops(to_territory)

            print('Player %s is attacking %s (o: %s, n: %i) from %s (o: %s, n: %i)' %
                  (from_player, to_territory, to_player, n_to_troops, from_territory, from_player, n_from_troops))

            # Roll the dice
            n_attack_dice = min(3, n_from_troops-1)
            n_defend_dice = min(2, n_to_troops)
            losses = self.roll(n_attack_dice, n_defend_dice)

            # Apply the losses
            self.board.set_n_troops(from_territory, n_from_troops - losses[0])
            self.board.set_n_troops(to_territory, n_to_troops - losses[1])

            # Check if territory is won
            if not self.board.get_n_troops(to_territory):
                self.board.assign(to_territory, from_player)
                n_move_troops = self.board.get_n_troops(from_territory) - 1
                self.board.set_n_troops(to_territory, n_move_troops)
                self.board.set_n_troops(from_territory, 1)
                print('Player %s won %s and is moving %i troops' % (from_player, to_territory, n_move_troops))
                break

    def run_engine(self):
        """Run the main game loop
        """
        while(not self.is_game_over()): # Main loop
            for player in self.players: # Turn loop
                # Draw board
                self.board.draw()

                # Troop placement phase
                n_troops = self.collect_troops(player)
                placements = player.place_troops(self.board, n_troops)
                for territory, n_troops in placements.items():
                    self.board.set_n_troops(territory, self.board.get_n_troops(territory) + n_troops)
                    print('Player %s is placing %i troop(s) on %s' % (player.name, n_troops, territory))

                # Attack phase
                # TODO: multiple attacks
                # TODO: don't always attack until completion
                from_territory, to_territory = player.attack(self.board)
                if from_territory and to_territory:
                    self.attack_to_completion(from_territory, to_territory)

                # Troop move phase
                from_territory, to_territory, n_move_troops = player.move_troops(self.board)
                if from_territory and to_territory and n_move_troops:
                    self.board.set_n_troops(from_territory, self.board.get_n_troops(from_territory) - n_move_troops)
                    self.board.set_n_troops(to_territory, self.board.get_n_troops(to_territory) + n_move_troops)
                    print('Player %s is moving %i troops from %s to %s' % (player.name, n_move_troops, from_territory, to_territory))

                # TODO: Add cards
