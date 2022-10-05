from Constants import Data, Type

class Move:
    """ Establishes the characteristics of a Pokemon's move
    
    Attributes:
        name (str) = this move's name
        type (Type) = this move's type
        category (str) = this category of this move
        power (float) = this move's power; is "None" if this move uses no
        damage calculation, and is an int between 0 and 100 otherwise
        accuracy (str or int) = this move's accuracy; is "None" if this
        move cannot miss; is an int between 0 and 100 otherwise
    """

    def __init__(self, move_name):
        move = self.moveInfo(move_name)
        self.name = move_name
        self.type = move.values[0][2]
        self.category = move.values[0][3]
        self.power = self.parsePower(move.values[0][6])
        self.accuracy = self.parseAccuracy(move.values[0][7])

    def moveInfo(self, move_name):
        move = Data.movelist.loc[Data.movelist['Name'] == move_name]
        return move

    def parsePower(self, power): 
        # power can be an int or a string
        if power != "None":
            power = int(power)
        return power
            
    def parseAccuracy(self, accuracy): 
        # accuracy can be an int or a string
        if accuracy != "None":
            accuracy = int(accuracy)
        return accuracy

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getCategory(self):
        return self.category

    def getPower(self):
        return self.power

    def getAccuracy(self):
        return self.accuracy

    def accuracyRoll(self, randNo):
        """ Determines whether or not a move will hit this turn.
        
        Parameters:
            - randNo (int) = number between 0 and 99
            
        Returns:
            - TRUE if the attack will hit
            - FALSE otherwise
        """
        if self.accuracy == "None" or self.accuracy > randNo:
            return True
        if self.accuracy <= randNo:
            return False

    def effect_multiplier(self, type1, type2):
        """ Determines if this move is super effective, not very effective,
            or not effective against the defending Pokemon.
            
        Parameters:
           type1 (str): The defending Pokemon's primary type
           type2 (str): The defending Pokemon's secondary type; equal to "None"
           if the defender has no secondary type.
        
        Returns:
            multiplier (int): is used to multiply the damage output accordingly
        
        Side Effects:
            Prints the result ("it's super effective!" if super effective)
        """
        # Checks primary type
        multiplier = 1
        if type1 in Type.no_effect.get(self.type):
            multiplier = 0
            print("It had no effect.")
            return multiplier
        elif type1 in Type.super_effective.get(self.type):
            multiplier *= 2
        elif type1 in Type.not_very_effective.get(self.type):
            multiplier *= .5

        #Checks secondary type
        if type2 == Type.NONE:
            if multiplier == 2:
                print("It's super effective!")
            elif multiplier == .5:
                print("It's not very effective.")
            elif multiplier == 0:
                print("It had no effect.")
            return multiplier
        elif type2 in Type.no_effect.get(self.type):
            multiplier = 0
            print("It had no effect.")
            return multiplier
        elif type2 in Type.super_effective.get(self.type):
            multiplier *= 2
        elif type2 in Type.not_very_effective.get(self.type):
            multiplier *= .5      
            
        # Prints based on multiplier; "no effect" cases are covered above
        if multiplier == 2:
            print("It's super effective!")
        elif multiplier == .5:
            print("It's not very effective.")
        return multiplier

class StatusMoves:
    """ Various collections of moves with the category "Status" 
    """
    # Moves that inflict status conditions based on movelist
    SLP_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'SLP Inflict']['Name'].tolist()
    PRZ_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'PRZ Inflict']['Name'].tolist()
    TOX_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'TOX Inflict']['Name'].tolist()
    PSN_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'PSN Inflict']['Name'].tolist()
    CON_INFLICT = Data.movelist.loc[Data.movelist['Effect'] == 'Confuse Inflict']['Name'].tolist()

    # Moves that affect stats based on movelist
    ATK_DROP = Data.movelist.loc[Data.movelist['Effect'] == 'ATKdrop']['Name'].tolist()
    ATK_BOOST = Data.movelist.loc[Data.movelist['Effect'] == 'ATKboost']['Name'].tolist() + ["Growth"]
    DEF_DROP = Data.movelist.loc[Data.movelist['Effect'] == 'DEFdrop']['Name'].tolist()
    DEF_DROP_2 = Data.movelist.loc[Data.movelist['Effect'] == 'DEFdrop2']['Name'].tolist()
    DEF_BOOST = Data.movelist.loc[Data.movelist['Effect'] == 'DEFboost']['Name'].tolist()
    DEF_BOOST_2 = Data.movelist.loc[Data.movelist['Effect'] == 'DEFboost2']['Name'].tolist()
    SPATK_BOOST = ["Growth"]
    SPDEF_BOOST_2 = Data.movelist.loc[Data.movelist['Effect'] == 'SpdefBoost2']['Name'].tolist()
    SPEED_DROP = Data.movelist.loc[Data.movelist['Effect'] == 'Speed Drop']['Name'].tolist()
    SPEED_BOOST_2 = Data.movelist.loc[Data.movelist['Effect'] == 'SPEEDboost2']['Name'].tolist()
    CRIT_BOOST = ["Focus Energy"]

    STATUS_INFLICT = SLP_INFLICT + PRZ_INFLICT + PSN_INFLICT + TOX_INFLICT
    STAT_BOOST = ATK_BOOST + DEF_BOOST + DEF_BOOST_2 + SPATK_BOOST + SPDEF_BOOST_2 + SPEED_BOOST_2
    STAT_DROP = ATK_DROP + DEF_DROP + DEF_DROP_2 + SPEED_DROP

class SecondaryEffects:
    """ Establishes all of the moves with secondary effects. Many of these
    effects are the chance that something (stat drop, flinch, status, etc)
    will occur."""
    # moves w/chance to flinch (IMPLEMENTED)
    FLINCH_10 = Data.movelist.loc[Data.movelist['Effect'] == 'Flinch10']['Name'].tolist()
    FLINCH_20 = Data.movelist.loc[Data.movelist['Effect'] == 'Flinch20']['Name'].tolist()
    FLINCH_30 = Data.movelist.loc[Data.movelist['Effect'] == 'Flinch30']['Name'].tolist()
    FLINCH_CHANCE = FLINCH_10 + FLINCH_20 + FLINCH_30

    # moves w/chance to inflict a status condition (IMPLEMENTED)
    BRN_10 = Data.movelist.loc[Data.movelist['Effect'] == 'BRN10']['Name'].tolist() + ["Tri Attack"]
    FRZ_10 = Data.movelist.loc[Data.movelist['Effect'] == 'FRZ10']['Name'].tolist() + ["Tri Attack"]
    PRZ_10 = Data.movelist.loc[Data.movelist['Effect'] == 'PRZ10']['Name'].tolist() + ["Tri Attack"]
    PRZ_30 = Data.movelist.loc[Data.movelist['Effect'] == 'PRZ30']['Name'].tolist()
    PSN_30 = Data.movelist.loc[Data.movelist['Effect'] == 'PSN30']['Name'].tolist()
    PSN_40 = Data.movelist.loc[Data.movelist['Effect'] == 'PRZ40']['Name'].tolist()
    CON_10 = Data.movelist.loc[Data.movelist['Effect'] == 'Confuse10']['Name'].tolist()
    CON_20 = Data.movelist.loc[Data.movelist['Effect'] == 'Confuse20']['Name'].tolist()
    STATUS_INFLICT_CHANCE = BRN_10 + FRZ_10 + PRZ_10 + CON_10 + CON_20 + PRZ_30 + PSN_30 + PSN_40

    # moves w/chance to drop the opponent's stats (IMPLEMENTED)
    ATTACK_DROP_10 = Data.movelist.loc[Data.movelist['Effect'] == 'AttackDrop10']['Name'].tolist()
    SPDEF_DROP_10 = Data.movelist.loc[Data.movelist['Effect'] == 'SpdefDrop10']['Name'].tolist()
    SPEED_DROP_10 = Data.movelist.loc[Data.movelist['Effect'] == 'SpeedDrop10']['Name'].tolist()
    STAT_DROP_CHANCE = ATTACK_DROP_10 + SPDEF_DROP_10 + SPEED_DROP_10

    # moves that always drop stats
    SPEED_DROP_100 = Data.movelist.loc[Data.movelist['Effect'] == 'SpeedDrop100']['Name'].tolist()

    # moves that affect the user's HP in some way (IMPLEMENTED)
    RECOIL_4 = Data.movelist.loc[Data.movelist['Effect'] == 'Recoil4']['Name'].tolist()
    RECOIL_3 = Data.movelist.loc[Data.movelist['Effect'] == 'Recoil3']['Name'].tolist()
    ABSORB = Data.movelist.loc[Data.movelist['Effect'] == 'Absorb']['Name'].tolist()
    CRASH = Data.movelist.loc[Data.movelist['Effect'] == 'Crash']['Name'].tolist()
    RECOIL = RECOIL_3 + RECOIL_4
    
    # moves w/high chance to crit (IMPLEMENTED)
    HIGH_CRIT = Data.movelist.loc[Data.movelist['Effect'] == 'High-Crit']['Name'].tolist()

    # moves that span multiple turns
    RECHARGE = Data.movelist.loc[Data.movelist['Effect'] == 'Recharge']['Name'].tolist()
    THRASH_LIKE = Data.movelist.loc[Data.movelist['Effect'] == 'Thrash-Like']['Name'].tolist()
    TWO_TURN = Data.movelist.loc[Data.movelist['Effect'] == '2Turn']['Name'].tolist()
    CONSECUTIVE = Data.movelist.loc[Data.movelist['Effect'] == 'SpeedDrop10']['Name'].tolist()

    # moves involving multiple hits or chip damage
    TWO_HIT = Data.movelist.loc[Data.movelist['Effect'] == '2Hit']['Name'].tolist()
    MULTI_HIT = Data.movelist.loc[Data.movelist['Effect'] == 'Multi-Hit']['Name'].tolist()
    TRAP = Data.movelist.loc[Data.movelist['Effect'] == 'Trap']['Name'].tolist()

    # move(s) with higher priority (may not implement)
    PRIORITY_1 = Data.movelist.loc[Data.movelist['Effect'] == 'Priority1']['Name'].tolist()