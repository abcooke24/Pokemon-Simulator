""" Human and computer tic tac toe players. """

import random, math
from PokemonGenerator import Pokemon
from Constants import Statuses

class Player:
    """ Base class for the Player
    
    Attributes:
        name (str): the player's name
    """
    def __init__(self, name):
        self.name = name
        self.pokemon = Pokemon(random.randint(0,97)) # Can't hit 98?

    def getPokemon(self):
        return self.pokemon

    def getName(self):
        return self.name

    def criticalHit(self, randNo):
        """ Determines whether or not a critical hit will occur. Called at the
        end of damage calculation (damageCalc function). The chances of this
        happening are normally 1/16, but can increase up to 1/4.
        
        Parameters:
            randNo: Randomly generated number between 0 and 15
        """
        if randNo == 0:
            return True
        else:
            return False

    def damageCalc(self, selected, defender):
        """ Calculates damage based on the official formula as displayed on
        Bulbapedia. I have posted the link to it below:
        https://bulbapedia.bulbagarden.net/wiki/Damage#Damage_calculation

        Due to the limitations of the current state of the project, this 
        function uses the Generation V+ of the formula but excludes several
        variables that have yet to be implemented. All variables from
        the Generation I calculator are present. Each Pokemon's level is
        assumed to be 100.

        Attributes:
            selected (Move): the selected move
            defender (Pokemon): the opposing Pokemon
        """
        # Attack / Defense (depicted as "A/D" on bulbapedia)
        if selected.getCategory() == "Physical":
            ad_ratio = self.pokemon.getAttack() / defender.getDefense()
        elif selected.getCategory() == "Special":
            ad_ratio = self.pokemon.getSpAtk() / defender.getSpdef()
        else:
            print("status")
            return 0
            # Status moves have yet to be implemented, so no damage is returned
        damage = ((42 * selected.getPower() * ad_ratio) / 50) + 2
        # Checks for a critical hit
        if self.criticalHit(random.randint(0,15)):
            damage *= 2
            print("A critical hit!")
        # Checks for same type attack bonus (STAB)
        if (selected.getType() == self.pokemon.getTypes(0)
        or selected.getType() == self.pokemon.getTypes(1)):
            damage *= 1.5
        # Checks if super effective, not very effective, or not effective
        damage = damage * selected.effect_multiplier(
            defender.getTypes(0), defender.getTypes(1))
        damage *= (random.randint(85,100) / 100)
        damage = math.floor(damage)
        return damage
    
    def take_turn(self):
        """ Selects a move and calculates the damage.
        
        Args:
            other_pkmn (Pokemon): the opposing Pokemon.
        
        Side effects:
            Does damage to opposing Pokemon.
        """
        raise NotImplementedError


class ComputerPlayer(Player):
    """ A computer tic tac toe player. Chooses its moves at random. """
    def take_turn(self, other_pkmn):
        """ Randomly selects a move.
        
        Args:
            other_pkmn (Pokemon): the opposing Pokemon.
        
        Side effects:
            Does damage to opposing Pokemon.
        """
        index = random.randint(0,3)
        move = self.pokemon.getMoves(index)

        print(self.pokemon.getName() + " used " + move.getName() + "!")
        if not move.accuracyRoll(random.randint(0,99)):
            print("The attack missed!")
            return
        else:
            damage = super().damageCalc(move, other_pkmn)
            other_pkmn.setCurrentHP(damage)
            return

    def __str__(self):
        pkmn_string = "{} {}/{}".format(self.pokemon.getName(),
        self.pokemon.getCurrentHP(),
        self.pokemon.getMaxHP())
        return pkmn_string

class HumanPlayer(Player):
    """ The human player. Makes their own decisions.
    """

    def getPokemon(self):
        return super().getPokemon()

    def damageCalc(self, selected, defender):
        return super().damageCalc(selected, defender)

    def take_turn(self, other_pkmn):
        """ Selects a move and calculates the damage.
        
        Args:
            other_pkmn (Pokemon): the opposing Pokemon.
        
        Side effects:
            Does damage to opposing Pokemon.
        """
        while True:
            select = input("Select a move by typing the corresponding number: ")
            try:
                index = int(select)
            except ValueError:
                print("Please enter a number")
                continue
            if index >= 1 and index <= 4:
                move = self.pokemon.getMoves(index - 1)
                print(self.pokemon.getName() + " used " + move.getName() + "!")
                if move.getAccuracy() != "None":
                    if not move.accuracyRoll(random.randint(0,99)):
                        print("The attack missed!")
                        return
                    else:
                        damage = super().damageCalc(move, other_pkmn)
                        other_pkmn.setCurrentHP(damage)
                        return
                else:
                    damage = super().damageCalc(move, other_pkmn)
                    other_pkmn.setCurrentHP(damage)
                    return
            else:
                print("Please enter a number between 1 and 4")
    
    def __str__(self):
        pkmn_string = self.pokemon.getName() + """ {}/{}
        \nMove selection: \n1. {} \n2. {} \n3. {} \n4. {}""".format(
            self.pokemon.getCurrentHP(),
            self.pokemon.getMaxHP(),
            self.pokemon.getMoves(0).getName(),
            self.pokemon.getMoves(1).getName(),
            self.pokemon.getMoves(2).getName(),
            self.pokemon.getMoves(3).getName()
        )
        return pkmn_string