import sys, random, math
from argparse import ArgumentParser
from Players import HumanPlayer, ComputerPlayer
from Constants import Statuses

# THIS IS WHERE MAIN IS LOCATED. EXAMPLE TEST SCRIPTS ARE BELOW
# python PokemonSimulator/battle.py computer Player
# python PokemonSimulator/battle.py Player computer

""" This is a Pokemon battle simulator; it is unfinished.

    TO IMPLEMENT:
        - Status Conditions (a few bugs)
        - More Pokemon
        - 2v2 format
        - Smarter AI (!)
        - Misc improvements/implementations
        
    CONSIDER THE FOLLOWING:
        - Held items
        - Abilities
"""

class Battle:
    """ A Pokemon battle with one human player and one computer player.
    
    Attributes:
        player1 (Player) = one of the players
        player2 (Player) = the other player
    """

    def __init__(self, p1, p2):
        self.player1 = p1
        self.player2 = p2

    def is_game_over(self, defender_HP):
        """ Checks if the game is over yet.
        
        Parameters:
            - defender_HP (int): integer representing the defending Pokemon's HP
        
        Returns:
            - TRUE if the defending Pokemon's HP is equal to 0
            - FALSE if the defending Pokemon stil has HP left
        """
        if defender_HP > 0:
            return False
        else:
            return True

    def is_mobile(self, pokemon):
        """ Determines whether or not a paralyzed, frozen, or sleeping Pokemon
        will be able to move this turn.
        
        Parameters:
            pokemon (Pokemon): This player's Pokemon
        
        Returns:
            TRUE if this Pokemon will be able to move next turn
            FALSE otherwise
        
        Side Effects:
            May print something if the Pokemon is immobile this turn or its
            status changes.
        """
        # Make functions out of repeated code (eventually)
        status = pokemon.getStatus()
        name = pokemon.getName()
        if status == Statuses.HEALTHY:
            return True
        elif status == Statuses.PRZ:
            PRZ_roll = random.randint(0,3)
            if PRZ_roll == 0:
                print(name + " is fully paralyzed!")
                return False
            else:
                return True
        elif status == Statuses.SLP:
            sleeping_turns = pokemon.getInflictedTurns()
            if sleeping_turns == 0:
                print(name + " is fast asleep!")
                pokemon.incrementInflictedTurns()
                return False
            elif sleeping_turns >= 1 and sleeping_turns < 3:
                SLP_roll = random.randint(0,2)
                if SLP_roll == 0:
                    print(name + " woke up!")
                    pokemon.setStatus(Statuses.HEALTHY)
                    pokemon.resetInflictedTurns()
                    return True
                else:
                    print(name + " is fast asleep!")
                    pokemon.incrementInflictedTurns()
                    return False
            else: # sleeping_turns == 3
                print(name + " woke up!")
                pokemon.setStatus(Statuses.HEALTHY)
                pokemon.resetInflictedTurns()
                return True
        elif status == Statuses.FRZ:
            FRZ_roll = random.randint(0,4)
            if FRZ_roll == 0:
                print(name + " thawed out!")
                pokemon.setStatus(Statuses.HEALTHY)
                pokemon.resetInflictedTurns()
                return True
            else:
                print(name + " is frozen solid!")
                return False
        else: # status == (TOX, PSN, OR BRN)
            return True
    
    def chip_damage(self, status, pokemon):
        if status == Statuses.BRN or status == Statuses.PSN:
            damage = math.floor(pokemon.getMaxHP() * 0.125)
            pokemon.setCurrentHP(damage)
            pokemon.incrementInflictedTurns()
        else: # status == TOX
            mutliplier = pokemon.getInflictedTurns() + 1
            tox_multiplier = math.floor(0.0625 * mutliplier)
            damage = pokemon.getMaxHP() * tox_multiplier
            pokemon.setCurrentHP(tox_multiplier)
            pokemon.incrementInflictedTurns()

    def start(self):
        """ This is the function that handles the battle.

        Side Effects:
            - Frequently prints important information for battling purposes
        """
        p1_pkmn = self.player1.getPokemon()
        p2_pkmn = self.player2.getPokemon()
        p1_speed = p1_pkmn.getSpeed()
        p2_speed = p2_pkmn.getSpeed()
        battle_over = False

        print("{} has {}. {} has {}.".format(
            self.player1.getName(),
            p1_pkmn.getName(),
            self.player2.getName(),
            p2_pkmn.getName()
        ))
        while True:
            print()
            if p1_speed >= p2_speed:
                # p1 turn
                if self.is_mobile(p1_pkmn):
                    print(self.player1)
                    print()
                    self.player1.take_turn(p2_pkmn)
                    p2_HP = p2_pkmn.getCurrentHP()
                    battle_over = self.is_game_over(p2_HP)
                    if battle_over:
                        break
                # p2 turn
                if self.is_mobile(p2_pkmn):
                    print(self.player2)
                    print()
                    self.player2.take_turn(p1_pkmn)
                    p1_HP = p1_pkmn.getCurrentHP()
                    battle_over = self.is_game_over(p1_HP)
                    if battle_over:
                        break
            else:
                # p2 turn
                if self.is_mobile(p2_pkmn):
                    print(self.player2)
                    print()
                    self.player2.take_turn(p1_pkmn)
                    p1_HP = p1_pkmn.getCurrentHP()
                    battle_over = self.is_game_over(p1_HP)
                    if battle_over:
                        break
                # p1 turn
                if self.is_mobile(p1_pkmn):
                    print(self.player1)
                    print()
                    self.player1.take_turn(p2_pkmn)
                    p2_HP = p2_pkmn.getCurrentHP()
                    battle_over = self.is_game_over(p2_HP)
                    if battle_over:
                        break
                # psn, tox, or burn check (and decrement)
                if p1_pkmn.getStatus() in Statuses.CHIP_DAMAGE:
                    self.chip_damage(p1_pkmn.getStatus(), p1_pkmn)
                    battle_over = self.is_game_over(p1_HP)
                    if battle_over:
                        break
                if p2_pkmn.getStatus() in Statuses.CHIP_DAMAGE:
                    self.chip_damage(p2_pkmn.getStatus(), p2_pkmn)
                    battle_over = self.is_game_over(p2_HP)
                    if battle_over:
                        break
        print()
        if p1_pkmn.getCurrentHP() == 0:
            print(p1_pkmn.getName() + " fainted.")
            print(self.player1.getName() + " lost!")
        else:
            print(p2_pkmn.getName() + " fainted.")
            print(self.player2.getName() + " lost!")

def parse_args(arglist):
    """ Parse command line arguments. """
    parser = ArgumentParser()
    parser.add_argument("player1_name", help="Player 1 name (or 'computer')")
    parser.add_argument("player2_name", help="Player 2 name (or 'computer')")
    args = parser.parse_args(arglist)
    return args

def main(arglist):
    """ Create two Player objects and start a Pokemon battle"""
    args = parse_args(arglist)
    p1 = (ComputerPlayer("Brock") if args.player1_name == "computer"
          else HumanPlayer(args.player1_name))
    p2 = (ComputerPlayer("Misty") if args.player2_name == "computer"
          else HumanPlayer(args.player2_name))
    battle = Battle(p1, p2)
    battle.start()

if __name__ == "__main__":
    main(sys.argv[1:])