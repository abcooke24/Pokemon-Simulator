import pandas as pd, random, math
from Moves import Move
from Constants import Stats, Natures, Statuses

pokedex = pd.read_csv("PokemonSimulator\Kanto_Pokemon_100.csv")

class Pokemon:
    """ Generates a random Pokemon out of 100 possible choices,
        establishing their attributes in the process
        
    Attributes:
        name (str) = this Pokemon's name
        types (str List) = this Pokemon's types. If it only has one type,
        the second type will be "None"
        status (str): String representing this Pokemon's status condition; will
        be "Healthy" by default.
        inflicted_turns (int): The # of turns this Pokemon has been inflicted
        with a status condition for. Relevant for TOX and SLP
        EVs (int List): this Pokemon's Effort Values
        IVs (int List): this Pokemon's Individual Values
        nature (str List): string list representing this Pokemon's nature
        maxHP (int) = the starting # of hit points
        attack (int) = this Pokemon's attack stat
        defense (int) = this Pokemon's defense stat
        spatk (int) = this Pokemon's special attack stat
        spdef (int) = this Pokemon's special defense stat
        speed (int) = this Pokemon's speed stat
        currentHP (int) = the # of hit points this Pokemon has left
        currentAttack (int) = this Pokemon's attack stat after boosts/drops
        currentDefense (int) = this Pokemon's defense stat after boosts/drops
        currentSpAtk (int) = this Pokemon's special attack stat after boosts/drops
        currentSpDef (int) = this Pokemon's special defense stat after boosts/drops
        currentSpeed (int) = this Pokemon's speed stat after boosts/drops
        critBoost (boolean) = whether or not this Pokemon's critical hit ratio
        has been boosted
        moves (list of moves) = the moves this Pokemon has
    """

    def __init__(self, dexno):
        """ Establishes the Pokemon that will be used by the Player object.
        
        Parameters:
            dexno (int): integer between 0 and 98 which represents the
            column of info that this function will isolate and return.
        
        Side Effects:
            Creates a Pokemon object with all of the above attributes
        """
        info = self.pokeInfo(dexno)
        self.name = info.values[1]
        print(self.name)
        self.types = ([info.values[2],info.values[3]])
        self.status = Statuses.HEALTHY
        self.inflicted_turns = 0

        # Sets stats with the setStats; not subject to change
        self.EVs = self.setEVs()
        self.IVs = self.setIVs()
        self.nature = Natures.nature_list.copy()[random.randint(0,24)]
        self.maxHP = self.setStats(int(info.values[4]), "HP")
        self.attack = self.setStats(int(info.values[5]), "Attack")
        self.defense = self.setStats(int(info.values[6]), "Defense")
        self.spatk = self.setStats(int(info.values[7]), "SpAtk")
        self.spdef = self.setStats(int(info.values[8]), "SpDef")
        self.speed = self.setStats(int(info.values[9]), "Speed")

        # This Pokemon's CURRENT stats; subject to change during battle
        self.currentHP = self.maxHP * 1
        self.currentAttack = self.attack * 1
        self.currentDefense = self.defense * 1
        self.currentSpAtk = self.spatk * 1
        self.currentSpDef = self.spdef * 1
        self.currentSpeed = self.speed * 1
        self.critBoost = False

        # A different function will construct each move
        self.moves = self.setMoves((
            info.values[10],info.values[11],info.values[12],info.values[13]))

    def pokeInfo(self, dexno):
        """ Retrieves all information about the Pokemon from the csv file.
        
        Parameters:
            dexno (int): integer between 0 and 98 which represents the
            column of info that this function will isolate and return.
            
        Returns:
            Dataframe representing a column from the Kanto_Pokemon_100 csv file
        """
        col = pokedex.loc[dexno + 1]
        return col
    
    def setEVs(self):
        """ Randomly generates a Pokemon's Effort Values (EVs) according to
        the mechanics present in the Generation VI+ games; more info about EVs
        can be found in the Bulbapedia link below:
        https://bulbapedia.bulbagarden.net/wiki/Effort_values

        Returns:
            ev_list (List): List of six integers depicting each effort value
        """
        count = 0
        remaining = 508
        ev_list = []
        while remaining > 0 or count < 6:
            if count == 5:
                ev = remaining
            elif remaining == 0:
                ev = 0
            else:
                ev = random.randint(0,252)
            ev_list.append(ev)
            remaining -= ev
            count += 1
        return ev_list

    def setIVs(self):
        """ Sets a Pokemon's Individual Values (IVs) in all six stats. IVs are
        a number between 0 and 31 that are used in the calculation of their
        respective stat. More information about IVs can be found below:
        https://bulbapedia.bulbagarden.net/wiki/Individual_values

        Returns:
            iv_list (int List): List of six integers, each of which represent
            one IV and are between 0 and 31.
        """
        hp = random.randint(0,31)
        attack = random.randint(0,31)
        defense = random.randint(0,31)
        spatk = random.randint(0,31)
        spdef = random.randint(0,31)
        speed = random.randint(0,31)
        iv_list = [hp, attack, defense, spatk, spdef, speed]
        return iv_list

    def setStats(self, base_stat, name):
        """ Sets a Pokemon's stats based on their base stats and the official
        formula as displayed on Bulbapedia. The link is posted below:
        https://bulbapedia.bulbagarden.net/wiki/Stat#Generation_III_onward

        The Generation III+ formula is used due to its simplicity. Each Pokemon
        is assumed to be level 100.

        Parameters:
            base_stat (int): the base stat according to the csv file
            name (str): the name of the specified stat; for the purposes of
            calculation, this doesn't change the formula unless it's "HP"

        Returns:
            The calculated stat (int).
        """
        stat_index = Stats.stat_list.index(name)
        ev = self.EVs.copy()[stat_index]
        iv = self.IVs.copy()[stat_index]
        if name == "HP":
            stat = 2 * base_stat + iv + math.floor(ev/4) + 115
        else:
            stat = 2 * base_stat + iv + math.floor(ev/4) + 5
            if self.nature == [".", ".",".", ".", "."]:
                pass
            elif stat_index - 1 == self.nature.index("+"):
                stat *= 1.1
                stat = math.floor(stat)
            elif stat_index - 1 == self.nature.index("-"):
                stat *= .9
                stat = math.floor(stat)
        return stat

    def setMoves(self, moveset):
        """ Sets a Pokemon's moveset as per the csv file.
        
        Parameters:
            moveset (set of moves): the moves this Pokemon will have.
            
        Returns:
            A list of moves in the same order they appeared in.
        """
        move1 = Move(moveset[0])
        move2 = Move(moveset[1])
        move3 = Move(moveset[2])
        move4 = Move(moveset[3])
        the_moves = [move1,move2,move3,move4]
        return the_moves

    def getName(self):
        return self.name

    def getTypes(self, index):
        """ Returns one of this Pokemon's two types.
        
        Parameters:
            index (int): An integer (0 or 1) which represents which of
            this Pokemon's two types will be returned
        """
        return self.types.copy()[index]
    
    def getBothTypes(self):
        return self.types.copy()

    def getMaxHP(self):
        return self.maxHP

    def getAttack(self):
        return self.currentAttack

    def getDefense(self):
        return self.currentDefense

    def getSpAtk(self):
        return self.currentSpAtk

    def getSpdef(self):
        return self.currentSpDef

    def getSpeed(self):
        return self.currentSpeed

    def getMoves(self, index):
        """ Returns one of this Pokemon's four moves.
        
        Parameters:
            index (int): An integer (0 thru 3) which represents which of
            this Pokemon's four moves will be returned
        """
        return self.moves.copy()[index]

    def getCurrentHP(self):
        return self.currentHP

    def getStatus(self):
        return self.status

    def setStatus(self, newStatus): 
        """ Sets this Pokemon's status to a different specified status.

        Parameters:
            newStatus (str): Three letter string representing the status this
            Pokemon will have. WILL NOT BE THE SAME AS THE CURRENT STATUS.

        Side Effects:
            - Changes this Pokemon's status
        """
        # stats can be slightly changed through multiple status changes; will fix later
        if newStatus == Statuses.BRN:
            atk_drop = self.currentAttack / 2
            self.currentAttack = math.ceil(atk_drop)
        elif newStatus == Statuses.PRZ:
            speed_drop = math.ceil(self.currentSpeed / 4)
            self.currentSpeed = speed_drop
        elif newStatus == Statuses.HEALTHY:
            if self.status == Statuses.BRN:
                atk_restored = math.floor(self.currentAttack * 2)
                self.currentAttack = atk_restored
            if self.status == Statuses.PRZ:
                speed_restored = math.floor(self.currentAttack * 2)
                self.currentSpeed = speed_restored
        self.status = newStatus 

    def getInflictedTurns(self):
        return self.inflicted_turns
    
    def setCurrentHP(self, damage):
        """ Inflicts calculated damage to this Pokemon
        
        Args:
            damage (float): the amount of damage done to this Pokemon
        
        Side effects:
            Decrements currentHP accordingly
        """
        self.currentHP -= damage
        if self.currentHP < 0:
            self.currentHP = 0

    def setCurrentStat(self, statname, stages):
        """ Boosts or drops a current stat based on the opponent's move. The
        resulting current stat will be a whole number.
        
        Parameters:
            statname (str): the name of the stat being affected
            stages (float): the # of stages that the specified stat will be
            boosted or dropped by (usually 1 or 2)

        Side Effects:
            Alters a current stat accordingly
        """
        if statname == "Attack":
            if stages > 0:
                net_change = math.floor(self.attack * (stages/2))
                print(self.name + "'s attack rose!")
            elif stages < 0:
                net_change = math.floor(self.attack / (((stages * -1) + 2)/2))
                print(self.name + "'s attack fell!")
            self.currentAttack += net_change
            if self.currentAttack > self.attack * 6:
                self.currentAttack = self.attack * 6
            elif self.currentAttack < self.attack / 6:
                self.currentAttack = self.attack / 6
        if statname == "Defense":
            net_change = math.floor(self.defense * (stages/6))
            if net_change > 0:
                print(self.name + "'s defense rose!")
            elif net_change < 0:
                print(self.name + "'s defense fell!")
            self.currentDefense += net_change
            if self.currentDefense > self.defense * 6:
                self.currentDefense = self.defense * 6
            elif self.currentDefense < self.defense / 6:
                self.currentDefense = self.defense / 6
        if statname == "SpAtk":
            net_change = math.floor(self.spatk * (stages/6))
            if net_change > 0:
                print(self.name + "'s special attack rose!")
            elif net_change < 0:
                print(self.name + "'s special attack fell!")
            self.currentSpAtk += net_change
            if self.currentSpAtk > self.spatk * 6:
                self.currentSpAtk = self.spatk * 6
            elif self.currentSpAtk < self.spatk / 6:
                self.currentSpAtk = self.spatk / 6
        if statname == "SpDef":
            net_change = math.floor(self.spdef * (stages/6))
            if net_change > 0:
                print(self.name + "'s special defense rose!")
            elif net_change < 0:
                print(self.name + "'s special defense fell!")
            self.currentSpDef += net_change
            if self.currentSpDef > self.spdef * 6:
                self.currentSpDef = self.spdef * 6
            elif self.currentSpDef < self.spdef / 6:
                self.currentSpDef = self.spdef / 6
        if statname == "Speed":
            net_change = math.floor(self.speed * (stages/6))
            if net_change > 0:
                print(self.name + "'s speed rose!")
            elif net_change < 0:
                print(self.name + "'s speed fell!")
            self.currentSpeed += net_change
            if self.currentSpeed > self.speed * 6:
                self.currentSpeed = self.speed * 6
            elif self.currentSpeed < self.speed / 6:
                self.currentSpeed = self.speed / 6

    def incrementInflictedTurns(self):
        """Increments the # of turns this Pokemon has has a non-healthy status
        condition. This is relevant for sleeping, badly poisoned, and freezing
        Pokemon."""
        self.inflicted_turns += 1

    def resetInflictedTurns(self): # may combine with setStatus
        "Changes the number of inflicted turns to 0"
        self.inflicted_turns = 0

    def hasCritBoost(self):
        if self.critBoost:
            return True
        else:
            return False
    
    def setCritBoost(self):
        self.critBoost = True