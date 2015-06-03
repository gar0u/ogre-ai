from ogre.terrain import *
from ogre.direction import *


class Hexagon:
    """
    This class represents a 'Hexagon'.  Hexagons are a fundamental
    representation of space on a 'Map' in many wargames, including OGRE.
    """

    # Hexagon Methods
    def __init__(self, hexagonID, terrainType):
        """
        Create an instance of a 'Hexagon', given a 'hexagonID', and a
        'terrainType'.  A 'hexagonID' is a four digit number that 
        indicates a specific 'Hexagon' on the 'Map'.  The first two 
        digits of 'hexagonID' represent a column on the 'Map' and the 
        last two digits represent a row on the 'Map' (e.g. '0101').
        """
        self.r, self.q = self.getRQFromHexID(hexagonID)
        self.G = 0  # Distance from 'S'    (Used by A* path finding algorithm)
        self.H = 0  # Distance from 'D'    (Used by A* path finding algorithm)
        self.P = 0  # Weapon range penalty (Used by A* path finding algorithm)
        self.F = 0  # 'G' + 'H' + 'P'      (Used by A* path finding algorithm)
        self.parent = None  #              (Used by A* path finding algorithm)
        self.hexagonID = hexagonID
        self.terrainType = terrainType
        self.hexLines    = {Direction.NORTH: None,
                            Direction.NORTHEAST: None,
                            Direction.SOUTHEAST: None,
                            Direction.SOUTH: None,
                            Direction.SOUTHWEST: None,
                            Direction.NORTHWEST: None}
        self.unitPresent = None  # Classic OGRE does not allow units to stack, 
                                 # otherwise this would be a list.

    def addUnit(self, unit):
        """
        Assigns a given 'unit' to the 'unitPresent' attribute of a 'hexagon'.
        """
        try:
            if len(self.unitPresent) == 0:
                self.unitPresent = unit.unitName
            else:
                # Raise error (unit cannot move here because there is already 
                # a unit there.)
                pass
        except TypeError:
            # If no unit is there, a TypeError will be thrown, but it is safe
            # to add this unit to that hex.
            self.unitPresent = unit

    def removeUnit(self):
        """
        Sets the 'unitPresent' attribute of a 'Hexagon' to None.
        """
        self.unitPresent = None

    def getRQFromHexID(self, hexagonID):
        """
        a 'hexagonID' correspond to column (q) and row (r) coordinates on the 
        map (e.g. (q, r).  Each 'hexagonID' will be known to the user, but 
        (q, r) coordinates are an abstraction used by the simulation.
        """
        r = int(hexagonID[2:4]) - 1
        q = int(hexagonID[0:2]) - 1
        return (r, q)

    def getHexIDFromQR(self, q, r):
        NotImplemented        

    def __str__(self):
        """
        Returns the 'hexagonID' of a hexagon (e.g. '0101').
        """
        return self.hexagonID

    def setHexLine(self, direction, terrainType):
        """
        Set a specific 'hexline' of a 'Hexagon', given a 'direction' to
        a specific 'terrainType'.  Used for example to make the
        'Direction.NORTH' 'hexline' a 'Terrain.RIDGE'.
        """
        self.hexLines[direction] = terrainType

    def setTerrainType(self, terrainType):
        """
        Set the 'terrainType' of a 'Hexagon' to the specified 
        'terrainType'.  On the classic OGRE map, hexagons are either
        clear (the default) or an impassible crater.
        """
        self.terrainType = terrainType    


if __name__ == '__main__':
    # Self test
    myHexagon = Hexagon('0101', Terrain.OPEN)

    myHexagon.setTerrainType(Terrain.CRATER)
    myHexagon.setHexLine(Direction.NORTH, Terrain.RIDGE)

    print(myHexagon, myHexagon.terrainType)
    
    for hexLine in myHexagon.hexLines:
        print(myHexagon.hexLines[hexLine])

    print('Coordinates: ', myHexagon.r, ',', myHexagon.q)
