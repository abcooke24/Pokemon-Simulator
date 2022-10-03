""" Human and computer Pokemon players """

import random, math
from PokemonGenerator import Pokemon
from Constants import Statuses, Type, SecondaryEffects

class Player:
    """ Base class for the Player
    
    Attributes:
        name (str): the player's name
        pokemon (Pokemon): the player's Pokemon
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
    
    def flinch(self, flinch_move):
        """ Determines whether or not the defending pokemon will flinch assuming
        a move with a chance to flinch is used AND the defender is slower than
        the attacker.
        
        Moves have either a 10, 20, or 30 percent chance to cause flinching.
        """
        flinch_roll = random.randint(1, 10)
        move_name = flinch_move.getName()
        if move_name in SecondaryEffects.FLINCH_10:
            if flinch_roll == 1:
                return True
        elif move_name in SecondaryEffects.FLINCH_20:
            if flinch_roll == 1 or flinch_roll == 2:
                return True
        elif move_name in SecondaryEffects.FLINCH_30:
            if flinch_roll >= 1 and flinch_roll <= 3:
                return True
        return False
    
    def statusChanceHandler(status_move, defender):
        """ Determines whether or not the defending pokemon will be inflicted
        with a certain status condition. Chances range from 10-40%. 
        
        Confusion is the only status condition that can stack on top of another
        """
        status_roll = random.randint(1, 10)
        name = status_move.getName()
        # I need to optimize this, it hurts to look at
        if (name in SecondaryEffects.BRN_10 and status_roll == 1
        and defender.getStatus() == Statuses.HEALTHY):
            defender.setStatus(Statuses.BRN)
        elif (name in SecondaryEffects.FRZ_10 and status_roll == 1
        and defender.getStatus() == Statuses.HEALTHY):
            defender.setStatus(Statuses.FRZ)
        elif (name in SecondaryEffects.PRZ_10 and status_roll == 1
        and defender.getStatus() == Statuses.HEALTHY):
            defender.setStatus(Statuses.PRZ)
        elif (name in SecondaryEffects.CON_10 and status_roll == 1):
            defender.setStatus(Statuses.CON)
        elif (name in SecondaryEffects.CON_10 and (status_roll == 1
        or status_roll == 2)):
            defender.setStatus(Statuses.CON)
        elif (name in SecondaryEffects.PRZ_30 and status_roll >= 1
        and status_roll <= 3 and defender.getStatus() == Statuses.HEALTHY):
            defender.setStatus(Statuses.PRZ)
        elif (name in SecondaryEffects.PSN_30 and status_roll >= 1
        and status_roll <= 3 and defender.getStatus() == Statuses.HEALTHY):
            defender.setStatus(Statuses.PSN)
        elif (name in SecondaryEffects.PSN_40 and status_roll >= 1
        and status_roll <= 4 and defender.getStatus() == Statuses.HEALTHY):
            defender.setStatus(Statuses.PSN)

    def damageCalc(self, selected, defender):
        """ Calculates damage based on the official formula as displayed on
        Bulbapedia. I have posted the link to it below:
        https://bulbapedia.bulbagarden.net/wiki/Damage#Damage_calculation

        Due to the limitations of the current state of the project, this 
        function uses the Generation V+ of the formula but excludes several
        variables that have yet to be implemented. All variables from
        the Generation I calculator are present. Each Pokemon's level is
        assumed to be 100.

        Parameters:
            selected (Move): the selected move
            defender (Pokemon): the opposing Pokemon
        """
        # Attack / Defense (depicted as "A/D" on bulbapedia)
        if selected.getCategory() == "Physical":
            ad_ratio = self.pokemon.getAttack() / defender.getDefense()
        else: # selected.getCategory() == "Special"
            ad_ratio = self.pokemon.getSpAtk() / defender.getSpdef()
            # Status moves have yet to be implemented, so no damage is returned
        damage = ((42 * selected.getPower() * ad_ratio) / 50) + 2
        # Checks for a critical hit
        if self.pokemon.hasCritBoost():
            crit_check = random.randint(0,3)
        else: # not crit-boosted
            crit_check = random.randint(0,15)
        if self.criticalHit(crit_check):
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
        print(damage)
        if (self.pokemon.getSpeed() >= defender.getSpeed() and 
        selected in SecondaryEffects.FLINCH_CHANCE):
            flinched = self.flinch(selected, defender)
            if flinched:
                defender.setFlinch(True)
        if selected in SecondaryEffects.STATUS_INFLICT_CHANCE:
            self.statusChanceHandler(selected, defender)
        return damage

    def executeStatus(self, selected, defender):
        """ Uses the specified status move.
        
        Parameters:
            selected (Move): the selected move
            defender (Pokemon): the opposing Pokemon

        Side Effects:
            prints a message based on the move's effect
        """
        user = self.getPokemon()
        move = selected.getName()
        if move in Statuses.STATUS_INFLICT:
            if defender.getStatus() != Statuses.HEALTHY:
                print("But it failed!") # should swap spots with next piece of code
                return
            else: # defending Pokemon's current status is Healthy
                if ((move == "Thunder Wave" and Type.GROUND in
                defender.getBothTypes()) or (selected.getType == Type.POISON 
                and Type.POISON in defender.getBothTypes)):
                    # Thunder Wave doesn't hit ground types
                    # poison types cannot get poisoned.
                    print ("It had no effect!")
                    return
                else: # the move does affect the defending Pokemon
                    name = defender.getName()
                    if move in Statuses.SLP_INFLICT:
                        defender.setStatus(Statuses.SLP)
                        print(name + " fell asleep")
                        return
                    elif move in Statuses.PRZ_INFLICT:
                        defender.setStatus(Statuses.PRZ)
                        print(name + " is paralyzed.")
                        print("It may be unable to move!")
                        return 
                    elif move in Statuses.BRN_INFLICT:
                        defender.setStatus(Statuses.BRN)
                        print(name + " was burned!")
                        return
                    elif move in Statuses.PSN_INFLICT:
                        defender.setStatus(Statuses.PSN)
                        print(name + " was poisoned!")
                        return
                    else: # move == "Toxic" (not implemented yet)
                        defender.setStatus(Statuses.TOX)
                        print(name + " was badly poisoned!")
                        return
        elif move in Statuses.STAT_BOOST or move in Statuses.STAT_DROP:
            # there will be more
            if move in Statuses.ATK_BOOST:
                user.setCurrentStat("Attack", 1)
            elif move in Statuses.ATK_DROP:
                defender.setCurrentStat("Attack", -1)
            if move in Statuses.DEF_BOOST:
                user.setCurrentStat("Defense", 1)
            if move in Statuses.SPATK_BOOST:
                user.setCurrentStat("Special Attack", 1)
            return
        else: # move in Statuses.CRIT_BOOST (assumed to be "Focus Energy" for now)
            if user.hasCritBoost():
                print("But it failed!")
            else: # user is not yet crit-boosted
                print(user.getName() + " is getting pumped!")
                user.setCritBoost()
            return
    
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
        if move.getAccuracy() != "None":
            if not move.accuracyRoll(random.randint(0,99)):
                print("The attack missed!")
                return
        if (move.getCategory() == "Physical" 
        or move.getCategory() == "Special"):
            damage = super().damageCalc(move, other_pkmn)
            other_pkmn.setCurrentHP(damage)
            return
        else: # Move type is "Status"
            super().executeStatus(move, other_pkmn)
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
                if (move.getCategory() == "Physical" 
                or move.getCategory() == "Special"):
                    damage = super().damageCalc(move, other_pkmn)
                    other_pkmn.setCurrentHP(damage)
                    return
                else: # Move type is "Status"
                    super().executeStatus(move, other_pkmn)
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