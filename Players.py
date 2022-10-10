""" Human and computer Pokemon players """

import random, math
from PokemonGenerator import Pokemon
from Constants import Statuses, Type
from Moves import SecondaryEffects, StatusMoves

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
        print("Crit roll: {}".format(randNo))
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
        print("Flinch roll: {}".format(flinch_roll))
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
    
    def statusChanceHandler(self, status_move, defender):
        """ Determines whether or not the defending pokemon will be inflicted
        with a certain status condition. Chances range from 10-40%. 
        
        Confusion is the only status condition that can stack on top of another
        """
        status_roll = random.randint(1, 10)
        print("Status roll: {}".format(status_roll))
        name = status_move.getName()
        # I need to optimize this, it hurts to look at
        if name == "Tri Attack" and defender.getStatus == Statuses.HEALTHY:
            tri_roll = random.randint(1,3)
            if tri_roll == 1 and not Type.FIRE in defender.getBothTypes():
                defender.setStatus(Statuses.BRN)
            elif tri_roll == 1 and Type.FIRE in defender.getBothTypes():
                tri_roll = random.randint(2,3)
            elif tri_roll == 2:
                defender.setStatus(Statuses.FRZ)
            elif tri_roll == 3:
                defender.setStatus(Statuses.PRZ)
        else:
            if (name in SecondaryEffects.BRN_10 and status_roll == 1
            and defender.getStatus() == Statuses.HEALTHY and not Type.FIRE
            in defender.getBothTypes()):
                defender.setStatus(Statuses.BRN)
            elif (name in SecondaryEffects.FRZ_10 and status_roll == 1
            and defender.getStatus() == Statuses.HEALTHY and not Type.ICE
            in defender.getBothTypes()):
                defender.setStatus(Statuses.FRZ)
            elif (name in SecondaryEffects.PRZ_10 and status_roll == 1
            and defender.getStatus() == Statuses.HEALTHY):
                defender.setStatus(Statuses.PRZ)
            elif (name in SecondaryEffects.CON_10 and status_roll == 1):
                defender.set_confusion(True)
            elif (name in SecondaryEffects.CON_20 and (status_roll == 1
            or status_roll == 2)):
                defender.set_confusion(False)
            elif (name in SecondaryEffects.PRZ_30 and status_roll >= 1
            and status_roll <= 3 and defender.getStatus() == Statuses.HEALTHY):
                defender.setStatus(Statuses.PRZ)
            elif (name in SecondaryEffects.PSN_30 and status_roll >= 1
            and status_roll <= 3 and defender.getStatus() == Statuses.HEALTHY
            and not Type.POISON in defender.getBothTypes()):
                defender.setStatus(Statuses.PSN)
            elif (name in SecondaryEffects.PSN_40 and status_roll >= 1
            and status_roll <= 4 and defender.getStatus() == Statuses.HEALTHY
            and not Type.POISON in defender.getBothTypes()):
                defender.setStatus(Statuses.PSN)

    def statDropHandler(self, move, defender):
        """ Handles moves that have a chance to drop the defending Pokemon's stats
        
        Parameters:
            move (Move) = the move with a chance to drop one of the defending 
            Pokemon's stats
            defender (Pokemon) = the defending Pokemon

        Side Effects:
            Calls the Pokemon setCurrentStat method
        """
        # HANDLE PRINTS HERE
        name = move.getName()
        if name in SecondaryEffects.SPEED_DROP_100:
            defender.setCurrentStat("Speed", -1)
        stat_drop_roll = random.randint(1,10)
        print("Stat drop roll: {}".format(stat_drop_roll))
        if stat_drop_roll == 1:
            if name in SecondaryEffects.ATTACK_DROP_10:
                defender.setCurrentStat("Attack", -1)
            elif name in SecondaryEffects.SPDEF_DROP_10:
                defender.setCurrentStat("SpDef", -1)
            elif name in SecondaryEffects.SPEED_DROP_10:
                defender.setCurrentStat("Speed", -1)

    def HPchange(self, move, damage_dealt):
        """ Calculates recoil or drained HP based on Bulbapedia's list of moves
        with recoil damage. The link to these are below:
        https://bulbapedia.bulbagarden.net/wiki/Recoil#Moves_with_recoil_damage
        https://bulbapedia.bulbagarden.net/wiki/Category:HP-draining_moves

        Parameters:
            move (Move) = the move with recoil used by the attacking Pokemon.
            It can be assumed that this move is in the RECOIL list.
            damage_dealt (int) = the amount of damage the attacking Pokemon dealt
            with the recoil move.

        Returns:
            recoil (int): the amount of recoil damage the attacking Pokemon 
            will take.
        """
        name = move.getName()
        if name in SecondaryEffects.RECOIL_3:
            net_change = math.floor(damage_dealt / 3)
            print("Recoil: {}".format(net_change))
        elif name in SecondaryEffects.RECOIL_4:
            net_change = math.floor(damage_dealt / 4)
            print("Recoil: {}".format(net_change))
        elif name in SecondaryEffects.ABSORB:
            net_change = math.floor(damage_dealt / -2)
            print("Drained: {}".format(net_change * -1))
        return net_change

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
        name = selected.getName()
        # evaluates the number of attacks the move will do
        attacks_remaining = 1
        if name in SecondaryEffects.TWO_HIT:
            attacks_remaining = 2
        elif name in SecondaryEffects.MULTI_HIT:
            multi_hit_roll = random.randint(1,8)
            if multi_hit_roll >= 1 and multi_hit_roll <= 3:
                attacks_remaining = 2
            elif multi_hit_roll >= 4 and multi_hit_roll <= 6:
                attacks_remaining = 3
            elif multi_hit_roll == 7:
                attacks_remaining = 4
            else: # multi_hit_roll == 8
                attacks_remaining = 5
        print_num = 0
        if attacks_remaining > 1:
            print_num = attacks_remaining
        while attacks_remaining > 0:
            # Attack / Defense (depicted as "A/D" on bulbapedia)
            if selected.getCategory() == "Physical":
                ad_ratio = self.pokemon.getAttack() / defender.getDefense()
            else: # selected.getCategory() == "Special"
                ad_ratio = self.pokemon.getSpAtk() / defender.getSpdef()
                # Status moves have yet to be implemented, so no damage is returned
            damage = ((42 * selected.getPower() * ad_ratio) / 50) + 2
            # Checks if super effective, not very effective, or not effective
            damage = damage * selected.effect_multiplier(
                defender.getTypes(0), defender.getTypes(1))
            # Checks for a critical hit
            if self.pokemon.hasCritBoost():
                if name in SecondaryEffects.HIGH_CRIT:
                    crit_check = 0
                else: # not a high-crit move
                    crit_check = random.randint(0,1)
            else: # not crit-boosted
                if name in SecondaryEffects.HIGH_CRIT:
                    crit_check = random.randint(0,7)
                else: # not a high-crit move
                    crit_check = random.randint(0,15)
            if self.criticalHit(crit_check):
                damage *= 2
                print("A critical hit!")
            # Checks for same type attack bonus (STAB)
            if selected.getType() in self.pokemon.getBothTypes():
                damage *= 1.5
            damage *= (random.randint(85,100) / 100)
            damage = math.floor(damage) # debugging purposes
            print("Damage: {}".format(damage))
            if (self.pokemon.getSpeed() >= defender.getSpeed() and 
            name in SecondaryEffects.FLINCH_CHANCE):
                flinched = self.flinch(selected)
                if flinched:
                    defender.setFlinch(True)
            # decrement the number of attacks remaining, ends the turn if 0
            attacks_remaining -= 1
        if print_num != 0:
            print("It hit {} times".format(print_num))
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
        if move in StatusMoves.STATUS_INFLICT:
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
                    if move in StatusMoves.SLP_INFLICT:
                        defender.setStatus(Statuses.SLP)
                        return
                    elif move in StatusMoves.PRZ_INFLICT:
                        defender.setStatus(Statuses.PRZ)
                        return 
                    # elif move in Statuses.BRN_INFLICT:
                        # defender.setStatus(Statuses.BRN)
                        # return
                    elif move in StatusMoves.PSN_INFLICT:
                        defender.setStatus(Statuses.PSN)
                        return
                    elif move in StatusMoves.CON_INFLICT:
                        defender.set_confusion(True)
                    else: # move == "Toxic" (not implemented yet)
                        defender.setStatus(Statuses.TOX)
                        return
        elif move in StatusMoves.STAT_BOOST or move in StatusMoves.STAT_DROP:
            # there will be more
            # PRINT HERE
            pkmn = user.getName()
            other_pkmn = defender.getName()
            if move in StatusMoves.ATK_BOOST:
                user.setCurrentStat("Attack", 1)
                print(pkmn + "'s attack rose!")
            elif move in StatusMoves.ATK_DROP:
                defender.setCurrentStat("Attack", -1)
                print(other_pkmn + "'s attack fell!")
            if move in StatusMoves.DEF_BOOST:
                user.setCurrentStat("Defense", 1)
                print(pkmn + "'s defense rose!")
            elif move in StatusMoves.DEF_BOOST_2:
                user.setCurrentStat("Defense", 2)
                print(pkmn + "'s defense rose!")
            elif move in StatusMoves.DEF_DROP:
                defender.setCurrentStat("Defense", -1)
                print(other_pkmn + "'s defense fell!")
            elif move in StatusMoves.DEF_DROP_2:
                defender.setCurrentStat("Defense", -2)
                print(other_pkmn + "'s defense fell!")
            if move in StatusMoves.SPATK_BOOST:
                user.setCurrentStat("SpAtk", 1)
                print(pkmn + "'s special attack rose!")
            if move in StatusMoves.SPDEF_BOOST_2:
                user.setCurrentStat("SpDef", 2)
                print(pkmn + "'s special defense rose!")
            if move in StatusMoves.SPEED_BOOST_2:
                user.setCurrentStat("Speed", 2)
                print(pkmn + "'s speed rose!")
            elif move in StatusMoves.SPEED_DROP:
                defender.setCurrentStat("Speed", -1)
                print(other_pkmn + "'s speed fell!")
            return
        else: # move in Statuses.CRIT_BOOST (assumed to be "Focus Energy" for now)
            if user.hasCritBoost():
                print("But it failed!")
            else: # user is not yet crit-boosted
                print(user.getName() + " is getting pumped!")
                user.setCritBoost()
            return
    
    def secondaryEffectHandler(self, name, move, damage, defender):
        if name in SecondaryEffects.RECOIL or name in SecondaryEffects.ABSORB:
            change = self.HPchange(move, damage)
            self.pokemon.setCurrentHP(change)
        elif name in SecondaryEffects.STAT_DROP_CHANCE:
            self.statDropHandler(move, defender)
        elif name in SecondaryEffects.STATUS_INFLICT_CHANCE:
            self.statusChanceHandler(move, defender)
        elif name in SecondaryEffects.RECHARGE:
            self.pokemon.setRecharging(True)

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
    def damageCalc(self, selected, defender):
        return super().damageCalc(selected, defender)
    
    def HPchange(self, move, damage_dealt):
        return super().HPchange(move, damage_dealt)

    def secondaryEffectHandler(self, name, move, damage, defender):
        return super().secondaryEffectHandler(name, move, damage, defender)

    def take_turn(self, other_pkmn):
        """ Randomly selects a move.
        
        Args:
            other_pkmn (Pokemon): the opposing Pokemon.
        
        Side effects:
            Does damage to opposing Pokemon unless the move misses
            May inflict crash damage to attacking Pokemon
        """
        if self.pokemon.is_charging():
                move = self.pokemon.getChargingMove()
                print(self.pokemon.getName() + " used " + move.getName() + "!")
                damage = self.damageCalc(move, other_pkmn)
                other_pkmn.setCurrentHP(damage)
                self.pokemon.resetChargingMove()
                self.pokemon.set_charging(False)
                return
        else:
            index = random.randint(0,3)
            move = self.pokemon.getMoves(index)
            name = move.getName()
            print(self.pokemon.getName() + " used " + name + "!")
            if name in SecondaryEffects.TWO_TURN:
                print(self.pokemon.getName() + " is charging") # generic message, replace soon
                self.pokemon.set_charging(True)
                self.pokemon.setChargingMove(move)
                print(move)
                return
            if move.getAccuracy() != "None":
                if not move.accuracyRoll(random.randint(0,99)):
                    if name in SecondaryEffects.CRASH:
                        print(self.pokemon.getName() + " kept going and crashed!")
                        crash_damage = math.floor(self.pokemon.getMaxHP / 2)
                        self.pokemon.setCurrentHP(crash_damage)
                    else: # move does not inflict crash damage
                        print("The attack missed!")
                    return
            if (move.getCategory() == "Physical" 
            or move.getCategory() == "Special"):
                damage = self.damageCalc(move, other_pkmn)
                other_pkmn.setCurrentHP(damage)
                self.secondaryEffectHandler(name, move, damage, other_pkmn)
                return
            else: # Move type is "Status"
                self.executeStatus(move, other_pkmn)
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
    
    def secondaryEffectHandler(self, name, move, damage, defender):
        return super().secondaryEffectHandler(name, move, damage, defender)

    def take_turn(self, other_pkmn):
        """ Selects a move and calculates the damage.
        
        Args:
            other_pkmn (Pokemon): the opposing Pokemon.
        
        Side effects:
            Does damage to opposing Pokemon unless the move misses
            May inflict crash damage to attacking Pokemon
        """
        while True:
            if self.pokemon.is_charging():
                move = self.pokemon.getChargingMove()
                print(self.pokemon.getName() + " used " + move.getName() + "!")
                damage = self.damageCalc(move, other_pkmn)
                other_pkmn.setCurrentHP(damage)
                self.pokemon.resetChargingMove()
                self.pokemon.set_charging(False)
                return
            else:
                select = input("Select a move by typing the corresponding number: ")
                try:
                    index = int(select)
                except ValueError:
                    print("Please enter a number")
                    continue
                if index >= 1 and index <= 4:
                    move = self.pokemon.getMoves(index - 1)
                    name = move.getName()
                    print(self.pokemon.getName() + " used " + name + "!")
                    if name in SecondaryEffects.TWO_TURN:
                        print(self.pokemon.getName() + " is charging") # generic message, replace soon
                        self.pokemon.set_charging(True)
                        self.pokemon.setChargingMove(move)
                        print(move)
                        return
                    if move.getAccuracy() != "None":
                        if not move.accuracyRoll(random.randint(0,99)):
                            if name in SecondaryEffects.CRASH:
                                print(self.pokemon.getName() + " kept going and crashed!")
                                crash_damage = math.floor(self.pokemon.getMaxHP / 2)
                                self.pokemon.setCurrentHP(crash_damage)
                            else: # move does not inflict crash damage
                                print("The attack missed!")
                            return
                    if (move.getCategory() == "Physical" 
                    or move.getCategory() == "Special"):
                        damage = self.damageCalc(move, other_pkmn)
                        other_pkmn.setCurrentHP(damage)
                        self.secondaryEffectHandler(name, move, damage, other_pkmn)
                        return  
                    else: # Move type is "Status"
                        self.executeStatus(move, other_pkmn)
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