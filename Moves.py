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
        move cannot miss, and is an int between 0 and 100 otherwise
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
        print(move)
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