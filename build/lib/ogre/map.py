from __future__ import print_function
import random
from ogre.hexagon import *
from ogre.status import *
import ogre.terrain


class Map:
    """
    This class represents a 'Map'.

    The classic OGRE map is a "flat-topped, even-q vertical layout".
    (See http://www.redblobgames.com/grids/hexagon/).

    My code uses axial (q, r) coordinates whenever possible, but converts axial
    coordinates to cube coordinates to simplify some calculations (i.e. 
    distance) when necessary.

    The map uses a 2d array of axial coordinates (e.g. tuples (q, r) to 
    store 'hexagons'.
    """

    def __init__(self, rows, columns):
        """
        The classic OGRE map uses (column, row) coordinates instead of the 
        usual (row, column) format.

        I preserve this notation for the hexagon id numbers printed on the map,
        but use [row][column] access for my algorithms because it is more
        familiar.

        q = columns
        r = rows
        """

        self.q = columns
        self.r = rows

        # Initialize an empty 2d structure to store each 'Hexagon'
        self.hexagons = [[None for i in range(0, self.q)] \
                         for i in range(0, self.r)]

        # Create and store a 'Hexagon' at each (q, r) coordinate on the map
        for r in range(0, self.r):
            for q in range(0, self.q):
                hexagonID = self.getHexIDFromQR(q, r)
                # Store the 'Hexagon' at (r, q)
                self.hexagons[r][q] = Hexagon(hexagonID, Terrain.OPEN)

    def clearUnits(self):
        """
        Remove any units present from every 'Hexagon' on the 'Map'.
        """
        for i in range(0, self.r):
            for j in range(0, self.q):
                self.hexagons[i][j].unitPresent = None

    def getRandomHex(self, maxQ, maxR):
        """
        Returns a hexagon ID of a non-crater hexagon 
        within the range of (q=1, r=1) and (q='maxQ', r='maxR'),
        where 'maxQ' and 'maxR' are integers.
        """
        randomQ = random.randint(1, maxQ)
        randomR = random.randint(1, maxR)
        while self.hexagons[randomR][randomQ].terrainType == Terrain.CRATER:
            randomQ = random.randint(1, maxQ)
            randomR = random.randint(1, maxR)
        randomCol = str(randomQ)
        randomRow = str(randomR)
        if len(randomCol) == 1:
            randomCol = '0'+randomCol
        if len(randomRow) == 1:
            randomRow = '0'+randomRow
        return randomCol + randomRow


    def hexOccupied(self, hexID):
        """
        Returns 'True' if the 'Hexagon' specified by 'hexID' contains a unit,
        or 'False' if there is no unit present.
        """
        occupied = False
        coordinates = self.getQRFromHexID(hexID)
        q, r = coordinates
        if self.hexagons[r][q].unitPresent is not None:
            occupied = True
        return occupied

    def hexIsCrater(self, hexID):
        """
        Returns 'True' if the 'Hexagon' specified by 'hexID' is a crater,
        or 'False' if it is not.
        """
        isCrater = False
        coordinates = self.getQRFromHexID(hexID)
        q, r = coordinates
        if self.hexagons[r][q].terrainType == Terrain.CRATER:
            isCrater = True
        return isCrater

    def getHexIDFromQR(self, q, r):
        """
        Returns a hexagon ID given 'q' and 'r' coordinates, where 'q' is a
        column on the 'Map', and 'r' is a row on the 'Map'.
        """
        qStr = str(q+1)
        rStr = str(r+1)
        if len(qStr) == 1:
            qStr = '0' + qStr
        if len(rStr) == 1:
            rStr = '0' + rStr
        hexagonID = qStr + rStr
        return hexagonID

    def getRQFromHexID(self, hexagonID):
        """
        Hexagon IDs correspond to (q, r) coordinates on the 'Map'. Given a
        'hexagonID", return a tuple of coordinates in the form of (r, q).

        Internal representations of 'Hexagons' are often in the form of (r, q)
        while external representations often use the inverse, (q, r).
        """

        q = int(hexagonID[0:2]) - 1
        r = int(hexagonID[2:4]) - 1
        return (r, q)

    def getQRFromHexID(self, hexagonID):
        """
        Hexagon IDs correspond to (q, r) coordinates on the 'Map'. Given a
        'hexagonID", return a tuple of coordinates in the form of (q, r).

        Internal representations of 'Hexagons' are often in the form of (r, q)
        while external representations often use the inverse, (q, r).
        """
        q = int(hexagonID[0:2]) - 1
        r = int(hexagonID[2:4]) - 1
        return (q, r)

    def changeHexType(self, hexagonID, terrainType):
        """
        Change the terrain type of a hexagon at the specified hexagon id.
        """
        r, q = self.getRQFromHexID(hexagonID)
        self.hexagons[r][q].setTerrainType(terrainType)


    def changeHexLine(self, hexagonID, direction, terrainType):
        # TECHNICAL DEBT: This method is redundant.  'setHexLine' does the same
        #                 thing.
        """
        Change the terrain type of a hex line of a hexagon at the specified 
        hexagon id and direction.
        """
        r, q = self.getRQFromHexID(hexagonID)
        self.hexagons[r][q].setHexLine(direction, terrainType)

    def getNeighbors(self, q, r):
        """
        Given the coordinates 'q' and 'r' of a 'Hexagon', return a list of 
        tuples that represent the coordinates of each immediate neighbor.
        """
        # Generalized neighbor coordinates for both columns
        northNeighbor = (q, r-1)
        southNeighbor = (q, r+1)
        # Determine if we are on an even (offset) or odd column
        if q % 2 == 0:
            # Generalized neighbor coordinates for even (offset) columns
            northeastNeighbor = (q+1, r)
            southeastNeighbor = (q+1, r+1)
            southwestNeighbor = (q-1, r+1)
            northwestNeighbor = (q-1, r)
        else:
            # Generalized neighbor coordinates for odd columns
            northeastNeighbor = (q+1, r-1)
            southeastNeighbor = (q+1, r)
            southwestNeighbor = (q-1, r)
            northwestNeighbor = (q-1, r-1)
        # Check that each neighbor returned has valid coordinates ( q > 0 and 
        # r > 0)
        listOfNeighbors = []
        if self.validCoordinates(northNeighbor):
            listOfNeighbors.append(northNeighbor)
        if self.validCoordinates(northeastNeighbor):
            listOfNeighbors.append(northeastNeighbor)
        if self.validCoordinates(southeastNeighbor):
            listOfNeighbors.append(southeastNeighbor)
        if self.validCoordinates(southNeighbor):
            listOfNeighbors.append(southNeighbor)
        if self.validCoordinates(southwestNeighbor):
            listOfNeighbors.append(southwestNeighbor)
        if self.validCoordinates(northwestNeighbor):
            listOfNeighbors.append(northwestNeighbor)
        # Return a list of neighbors
        return listOfNeighbors

    def convertAxial2Cube(self, q, r):
       """
       Offset axial coordinates (q, r) can be difficult to work with,
       so this helper function can be used to convert axial
       coordinates to cube coordinates (x, y, z) for calculations 
       like distance
       """
       # Convert 'even-q offset' (classic Ogre) axial to cube
       # using bitwise and (&1) instead of modulus 2 (%2) to
       # avoid potentially negative numbers
       x = q
       z = r - (q + (q&1)) / 2
       y = -x - z
       return (x, y, z)

    def getDistance(self, hex1Cube, hex2Cube):
        """
        returns the 'Manhattan distance' between two hexes

        ('Manhattan distance' discounts Diagonal distance and returns simple
         'up and over' distances.)
        """
        x1, y1, z1 = hex1Cube
        x2, y2, z2 = hex2Cube
        return (abs(x1-x2) + abs(y1-y2) + abs(z1-z2)) / 2

    def validCoordinates(self, coordinates):
        """
        Return 'True' of the given 'coordinates' (in the form of (q, r)) are 
        on the map, or 'False' if the 'coordinates' are not on the map.
        """
        q, r = coordinates
        if q % 2 == 0:
            offset = -1
        else:
            offset = 0
        if (q >= 0 and r >= 0) and (q < self.q and r < self.r+offset):
            return True
        else:
            return False

    def __str__(self):
        """
        Returns a string reprentation of the entire 'Map'.

        If the hexagon is clear, the hexagon ID will be displayed (e.g. '0101')

        If the hexagon contains a disabled unit, a lowercase abbreviation of
        the unit will be displayed (e.g. 'hwz' for a disabled howitzer).

        Otherwise an all caps abbreviation of the unit will be displayed (e.g.
        'HWZ' for a normal howitzer).

        Craters are represented as './\.' but ridges are not represented.
        """
        output = '\n'
        for i in range(0, self.r):
           for j in range(0, self.q):
               try:
                   # Print the unit type, if one is present in the hex
                   if self.hexagons[i][j].unitPresent is not None:
                       if self.hexagons[i][j].unitPresent.status \
                           == Status.NORMAL:
                           # Display normal units using all captials
                           output += self.hexagons[i][j].unitPresent.unitType \
                                     + '\t'
                       else:
                           output += \
                           str.lower(self.hexagons[i][j].unitPresent.unitType) \
                           + '\t'
                   # If no unit is present, just print the terrain type
                   elif self.hexagons[i][j].terrainType == Terrain.CRATER:
                       output += './\.' + '\t'
                   # or the hexagon id if the terrainType is clear
                   else:
                       output += self.hexagons[i][j].hexagonID + '\t'
               except TypeError:
                   # If no unit is present, just print the terrain type
                   if self.hexagons[i][j].terrainType == Terrain.CRATER:
                       output += './\.' + '\t'
                   # or the hexagon id
                   else:
                       output += self.hexagons[i][j].hexagonID + '\t'
           output += '\n'
        return output


if __name__ == '__main__':
    # Self test
    #
    # Create a simple map
    myMap = Map(22, 15)
    if isinstance(myMap, Map):
        print("Test: Create 'Map(r, q)': pass")
    else:
        print("Test: Create 'Map(r, q)': FAIL")

    # Check hex creation
    if myMap.hexagons[1][2].terrainType == 'open':
        print("Test: Create 'Hex': pass")
    else:
        print("Test: Create 'Hex': FAIL")

    # Change hex terrain type
    myMap.changeHexType('0302', Terrain.CRATER)    
    if myMap.hexagons[1][2].terrainType == 'crater':
        print("Test: Change 'Hex.terrainType': pass")
    else:
        print("Test: Change 'Hex.terrainType': FAIL")

    # Add a ridge
    myMap.changeHexLine('0102', Direction.SOUTHEAST, Terrain.RIDGE)
    if myMap.hexagons[1][0].hexLines[2] == 'ridge':
        print("Test: Change 'Hex.hexLine': pass")
    else:
        print("Test: Change 'Hex.hexLine': FAIL")

    # GetNeighbors, Top left
    r, q = myMap.getRQFromHexID('0101')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(1, 0), (1, 1), (0, 1)]:
        print("Test: GetNeighbors('0101') (top left): pass")
    else:
        print("Test: GetNeighbors('0101') (top left): FAIL")

    # GetNeighbors, Top right
    r, q = myMap.getRQFromHexID('1501')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(14, 1), (13, 1), (13, 0)]:
        print("Test: GetNeighbors('1501') (top right): pass")
    else:
        print("Test: GetNeighbors('1501') (top right): FAIL")

    # GetNeighbors, Bottom right
    r, q = myMap.getRQFromHexID('1521')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(14, 19), (13, 21), (13, 20)]:
        print("Test: GetNeighbors('1521') (bottom right): pass")
    else:
        print("Test: GetNeighbors('1521') (bottom right): FAIL")

    # GetNeighbors, Bottom left
    r, q = myMap.getRQFromHexID('0121')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(0, 19), (1, 20), (1, 21)]:
        print("Test: GetNeighbors('0121') (bottom left): pass")
    else:
        print("Test: GetNeighbors('0121') (bottom left): FAIL")

    # GetNeighbors, Top row, offset
    r, q = myMap.getRQFromHexID('0401')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(4, 0), (3, 1), (2, 0)]:
        print("Test: GetNeighbors('0401') (top row, offset): pass")
    else:
        print("Test: GetNeighbors('0401') (top row, offset): FAIL")

    # GetNeighbors, Top row, not offset
    r, q = myMap.getRQFromHexID('0501')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(5, 0), (5, 1), (4, 1), (3, 1), (3, 0)]:
        print("Test: GetNeighbors('0501') (top row, not offset): pass")
    else:
        print("Test: GetNeighbors('0501') (top row, not offset): FAIL")

    # GetNeighbors, right column
    r, q = myMap.getRQFromHexID('1505')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(14, 3), (14, 5), (13, 5), (13, 4)]:
        print("Test: GetNeighbors('1505') (right column): pass")
    else:
        print("Test: GetNeighbors('1505') (right column): FAIL")

    # GetNeighbors, left column
    r, q = myMap.getRQFromHexID('0105')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(0, 3), (1, 4), (1, 5), (0, 5)]:
        print("Test: GetNeighbors('0105') (left column): pass")
    else:
        print("Test: GetNeighbors('0105') (left column): FAIL")

    # GetNeighbors, bottom row, offset
    r, q = myMap.getRQFromHexID('0422')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(3, 20), (4, 20), (2, 20)]:
        print("Test: GetNeighbors('0422') (bottom row, offset): pass")
    else:
        print("Test: GetNeighbors('0422') (bottom row, offset): FAIL")

    # GetNeighbors, bottom row, not offset
    r, q = myMap.getRQFromHexID('0521')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(4, 19), (5, 20), (5, 21), (3, 21), (3, 20)]:
        print("Test: GetNeighbors('0521') (bottom row, not offset): pass")
    else:
        print("Test: GetNeighbors('0521') (bottom row, not offset): FAIL")

    # GetNeighbors, Middle (normal) hex, offset
    r, q = myMap.getRQFromHexID('0812')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(7, 10), (8, 10), (8, 11), (7, 12), (6, 11), 
                           (6, 10)]:
        print("Test: GetNeighbors('0812') (middle (normal) hex, offset): pass")
    else:
        print("Test: GetNeighbors('0812') (middle (noraml) hex, offset): FAIL")

    # GetNeighbors, Middle (normal) hex, not offset
    r, q = myMap.getRQFromHexID('0912')
    listOfNeighbors = myMap.getNeighbors(q, r)
    if listOfNeighbors == [(8, 10), (9, 11), (9, 12), (8, 12), (7, 12), 
                           (7, 11)]:
        print("Test: GetNeighbors('0912') (middle (normal) hex, not " + \
              "offset): pass")
    else:
        print("Test: GetNeighbors('0912') (middle (noraml) hex, not " + \
              "offset): FAIL")

    # Useful for debugging
    """
    myMap = Map(2, 2)
    myMap.changeHexType('0102', Terrain.CRATER)
    myMap.changeHexLine('0102', Direction.SOUTHEAST, Terrain.RIDGE)
    myMap.changeHexLine('0202', Direction.NORTH, Terrain.RIDGE)
    """

    # Check the map
    """
    print('')
    print('Map ({} rows, {} columns):'.format(myMap.r, myMap.q))
    for r in range(0, myMap.r):
        for q in range(0, myMap.q):
            print('{} {} ({},{})'.format(myMap.hexagons[r][q].hexagonID, 
                  myMap.hexagons[r][q].terrainType, r, q), end='\t\t')
        print('\n')
    """
    print(myMap)

    # Check hex lines (useful for debugging)
    """
    print("A list of all the 'hexLine' attributes:")
    for r in range(0, myMap.r):
        for q in range(0, myMap.q):
            print(myMap.hexagons[r][q])
            for direction in myMap.hexagons[r][q].hexLines:
                print(myMap.hexagons[r][q].hexLines[direction])
            print('')
    """
