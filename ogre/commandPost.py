from ogre.behavior import *
from ogre.unit import *
from ogre.unitType import *


class CommandPost(Unit):
    """
    This class represents a 'Command Post'.  Command posts are a special type
    of unit that have strategic value, but unlike other units, most of the
    command post values such as 'movement points' and 'attack value' are 0.
    """

    # 'CommandPost' Methods
    def __init__(self, hexLocation):
        """
        Create an instance of a 'Command Post'.

        The command post will be placed on the map at the 'hexLocation' 
        specified.  (E.g. '0101')
        """
        self.unitName = 'cp'
        self.unitType = UnitType.CP
        self.hexLocation = hexLocation
        self.movementPoints = 0
        self.attackStrength = 0
        self.defenseStrength = 0
        self.range_ = 0
        self.status = Status.NORMAL
        self.behavior = Behavior.DISCIPLINED
        self.points = 0
