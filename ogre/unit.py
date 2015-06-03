DEBUG = False


from ogre.a_star import *
from ogre.behavior import *
from ogre.status import *
from ogre.unitType import *


class Unit:
    """
    This class is an abstraction used to represent specific types of units
    like 'Infantry', 'Armor', etc.
    """

    # Unit methods
    """
    Create an instance of a defender unit.  Units usually include a
    'unitName', which is just a string representation of the object for
    use by other objects, a 'unitType' which is a 'UnitType' constant,
    a 'points' value used for tracking setup and victory conditions,
    a current 'hexLocation' on the 'Map', and the usual game values
    such as 'movementPoints', 'attackStrength', 'range_', and
    'defenseStrength'.
    """
    def __init__(self, unitName, unitType, points, hexLocation,
                 movementPoints=0, attackStrength=0, range_=0,
                 defenseStrength=0):
        self.unitName = unitName
        self.unitType = unitType
        self.points = points
        self.hexLocation = hexLocation
        self.movementPoints = movementPoints
        self.attackStrength = attackStrength
        self.range_ = range_
        self.defenseStrength = defenseStrength
        self.status = Status.NORMAL
        self.behavior = Behavior.BRAVE
        # Technical debt: implement other behaviors

    def __str__(self):
        """
        Returns a string representation of a 'Unit', which is
        the 'unitName' followed by it's 'hexLocation'
        """
        return str(self.unitName + ' (' + self.hexLocation + ')')

    def getDBID(self, unitName):
        """
        A helper function that returns the primary key of each
        unit type as represented in a MySQL database
        """
        # TECHNICAL DEBT: These should be looked up instead of
        #                 hard coded in case they change in the
        #                 database for some reason.
        if unitName[0:3].lower() == 'inf':
            if unitName[3:4].lower() == '1':
               unitTypeID = '1'
            elif unitName[3:4].lower() == '2':
               unitTypeID = '2'
            elif unitName[3:4].lower() == '3':
               unitTypeID = '3'
        elif unitName[0:3].lower() == 'gev':
            unitTypeID = '4'
        elif unitName[0:3].lower() == 'hvy':
            unitTypeID = '5'
        elif unitName[0:3].lower() == 'hwz':
            unitTypeID = '6'
        elif unitName[0:3].lower() == 'msl':
            unitTypeID = '7'
        elif unitName[0:3].lower() == 'cp':
            unitTypeID = '8'

        return unitTypeID

    def setLocation(self, hexID):
        """
        Set the 'hexLocation' of a 'Unit' to the given 'hexID'
        """
        self.hexLocation = hexID

    def move(self, map, ogreHexID, cpHexID):
        """
        Given a 'map', move a 'Unit' baed on it's 'Behavior' towards or away
        from an 'Ogre' or the 'CommandPost'.
        """
        if self.movementPoints > 0:
            start = map.getQRFromHexID(self.hexLocation)
            # Select a destination based on the unit's behavior
            if self.behavior == Behavior.COWARDLY:
                if cpHexID is not None:
                    destination = map.getQRFromHexID(cpHexID)
            elif self.behavior == Behavior.DISCIPLINED:
                pass
            elif self.behavior == Behavior.BRAVE:
                if ogreHexID is not None:
                    destination = map.getQRFromHexID(ogreHexID)
            q_d, r_d = destination
            destinationHex = map.getHexIDFromQR(q_d, r_d)
            path = A_Star(start, destination)
            solution = path.findPath(map, path.S)
            # Check that the hex we move to is not already occupied by another
            # unit if so, move one hex less, until an open hex is found or we
            # stay at our current location.

            # +1 because the first entry in subSolution is the current hex
            subSolution = solution[0:self.movementPoints+1]
            i = len(subSolution)-1
            while i >= 0:
                if map.hexOccupied(subSolution[i]) == False \
                   and not map.hexIsCrater(subsolution[i]):
                    break
                elif map.hexIsCrater(subsolution[i]) == True:
                    i -= 1
                else:
                    i -= 1
            hexToMoveTo = subSolution[i]
            if hexToMoveTo == destinationHex \
               and map.hexagons[r_d][q_d].unitPresent is not None:
                # Stay put
                pass
            else:
                # Get the unit's current location coordinates
                q, r = map.getQRFromHexID(self.hexLocation)
                # Remove the unit from the current location
                map.hexagons[r][q].removeUnit()
                # Move the unit to the new location
                self.hexLocation = hexToMoveTo
                r, q = map.getRQFromHexID(hexToMoveTo)
                # Add the unit to the new location
                map.hexagons[r][q].addUnit(self)
                q_u, r_u = start
                if DEBUG: print('Moved a', self.behavior, self.unitType, 
                                'from', map.getHexIDFromQR(q_u, r_u), 
                                'to', self.hexLocation)

    def selectTarget(ogre, system):
        # Make sure the OGRE is not destroyed
        if not ogre.isDestroyed():
            # See if the targeted system is still functional
            i = ogre.listOfSystems.index(system)
            count = getattr(ogre, system)
            # If the targeted system is already destroyed,
            # select another system
            while count < 1:
                i += 1
                if i > len(ogre.listOfSystems) - 1:
                    i = 0
                system = ogre.listOfSystems[i]
                count = getattr(ogre, system)
            return system
        else:
            return False
