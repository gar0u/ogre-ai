# TODO: Implement enemy movement and weapon range 'P' value to modify 'F'

from ogre.terrain import *


DEBUG = False


class A_Star:
    """
    This class implement the 'A*' path finding algorithm.
    """
    # Attributes
    r = 0
    q = 0
    hexagons = []

    # Methods
    def __init__(self, startHexQR, destinationHexQR):
        """
        Create an instance of 'A*'

        'startHexQR' is a tuple (q, r) representing the start hex of the 
        current unit to move

        'destinationHexQR' is a tuple (q, r) of the destination hex or the goal
         of the current unit to move
        """
        self.openHexes   = []  # A list of hexes (as (q, r) tuples), to examine
        self.closedHexes = []  # A list of hexes (as (q, r) tuples), to ignore
        self.S = startHexQR
        self.D = destinationHexQR

    def findPath(self, map, currentHexQR):
        """
        Given a 'map' and a 'currentHexQR', which is a tuple in the form of 
        (q, r), 'findPath' will calculate the shortest path from 'currentHexQR'
        (which is initially 'startHexQR', given at the time the 'A*' object is
        created) to a destination, 'destinationHexQR' (which is also given at
        the time the 'A*' object is created) 
        """
        q_s, r_s = self.S  # Start hex (q, r)
        q_d, r_d = self.D  # Destination hex (q, r)
        if DEBUG: q_c, r_c = currentHexQR
        if DEBUG: print('Added', map.getHexIDFromQR(q_c, r_c), 'to open list')
        map.hexagons[r_s][q_s].parent = None
        self.openHexes.append(currentHexQR)
        while len(self.openHexes) > 0:
            if DEBUG: print('\nEntering while loop...')

            # BUG: Units can 'meander' to their destination if there is a
            #      a large diagonal difference between 'S' and 'D'.

            # TECHNICAL DEBT: Because the OGRE and defending units have such a 
            #                 small movement range compared with the board
            #                 size, the bug below does not actually manifest
            #                 itself in a single turn.  The OGRE actually 
            #                 navigates optimally, turn-by-turn.

            #                 E.g. CP @ 1401, MK3 @ 1222; {1420, 1417, 1414, 
            #                      1412, 1409, 1306,1404, 1402, 1401}.

            if self.D in self.openHexes:
                self.closedHexes.append(self.D)
                break

            lowestF = float('inf')

            if DEBUG: print('Looking for lowest F in open list...')

            # Parse the open list 'backwards' to get the most recently added 
            # hex to break ties for lowest F value.

            for hex in self.openHexes[::-1]:
                q_h, r_h = hex
                if map.hexagons[r_h][q_h].F < lowestF:
                    lowestF = map.hexagons[r_h][q_h].F
                    current = hex
                if DEBUG: print('HexID', map.getHexIDFromQR(q_h, r_h), 
                                'F:', map.hexagons[r_h][q_h].F)
            if DEBUG: q_c, r_c = current
            if DEBUG: print('Lowest F is', 
                            map.getHexIDFromQR(q_c, r_c))
            if DEBUG: print('Added', map.getHexIDFromQR(q_c, r_c), 
                            'to closed list')
            self.closedHexes.append(current)
            if DEBUG: print('Removed', map.getHexIDFromQR(q_c, r_c), 
                            'from open list')
            self.openHexes.remove(current)
            if self.D in self.closedHexes:
                if DEBUG: print('Found destination hex in closed list; path' + \
                                ' found, so quit')
                # Path was found, so quit
                break
            q_c, r_c = current
            if DEBUG: print('Getting a list of neighboring hexes...')
            neighbors = map.getNeighbors(q_c, r_c)
            if DEBUG: print('Neighbors:')
            if DEBUG:
                for neighbor in neighbors:
                    q_n, r_n = neighbor
                    print('  ', map.getHexIDFromQR(q_n, r_n))
            parent = self.closedHexes[len(self.closedHexes)-1]  # Parent (q, r)
            for neighbor in neighbors:
                q_n, r_n = neighbor
                if neighbor in self.closedHexes:
                    # Ignore hex
                    if DEBUG: print('Neighbor', map.getHexIDFromQR(q_n, r_n), 
                                    'is already on the closed list; ignoring')
                    pass
                elif neighbor not in self.openHexes:
                    # Calculate values 
                    if DEBUG: print('Neighbor', map.getHexIDFromQR(q_n, r_n), 
                                    'was not on the open list, ' + \
                                    'calculating values...')
                    # TODO: Add Terrain.RIDGE check for certain units
                    if map.hexagons[r_n][q_n].terrainType == Terrain.CRATER:
                        if DEBUG: print('Found a CRATER at', 
                                        map.getHexIDFromQR(q_n, r_n), 
                                        'so do not add it to the open list')
                        G = float('inf')
                    else:
                        G = map.getDistance(map.convertAxial2Cube(q_s, r_s),
                                            map.convertAxial2Cube(q_n, r_n))
                    H = map.getDistance(map.convertAxial2Cube(q_d, r_d), 
                                        map.convertAxial2Cube(q_n, r_n))
                    # TECHNICAL DEBT: Modifying the traditional calculation 
                    #                 for 'F' to include a 'penalty', 'P'
                    #                 for hexagons that are within range of an 
                    #                 enemy unit.
                    #                 P = map.hexagons[r_n][q_n].P
                    # N.b: There is no penalty for moving within range of an 
                    #      enmy unit, so long as you do not end your turn in 
                    #      range of the unit.  (e.g. there are no 'snap shots'
                    #      in OGRE). 

                    F = G + H # + P
                    map.hexagons[r_n][q_n].G = G
                    map.hexagons[r_n][q_n].H = H
                    map.hexagons[r_n][q_n].F = F
                    map.hexagons[r_n][q_n].parent = parent
                    if DEBUG: print(map.getHexIDFromQR(q_n, r_n), 'G =', G, 
                                                       'H =', H, 'F (G+H) =', 
                                                       F, 'parent', parent)
                    if F < float('inf'):
                        if DEBUG: print('Added', map.getHexIDFromQR(q_n, r_n), 
                                        'to the open list')
                        self.openHexes.append(neighbor)
                elif neighbor in self.openHexes:
                    # Calculate F' score from current hex, and if F' < F, 
                    # update neighbor's F value to F' and give neighbor a new 
                    # parent
                    if DEBUG: print('Neighbor', map.getHexIDFromQR(q_n, r_n), 
                                    'was already on the open lsit, ' + \
                                    'calculating new values...')
                    q_p, r_p = parent
                    FPrime = (map.hexagons[r_p][q_p].G + 1) + \
                              map.hexagons[r_n][q_n].H 
                              # + map.hexagons[r_n][q_n].P
                    F = map.hexagons[r_n][q_n].F
                    if DEBUG: print('Comparing F' and F, FPrime, F)
                    if FPrime < map.hexagons[r_n][q_n].F:
                        map.hexagons[r_p][q_p].F = FPrime
                        map.hexagons[r_p][q_p].parent = (q_p, r_p)

        path = []
        if len(self.closedHexes) > 0:
            for hex in self.closedHexes:
                q, r = hex
                hexID = map.getHexIDFromQR(q, r)
                path.append(hexID)
            return path
        else:
            return False


if __name__ == '__main__':
    # Self-tests    
    from map import *
    from commandPost import *
    from ogre import *

    myMap = Map(22, 15)
    myMap.changeHexType('0303', Terrain.CRATER)
    myMap.changeHexType('0202', Terrain.CRATER)

    commandPost = CommandPost()
    myMap.hexagons[0][1].addUnit(commandPost)

    markIII = Ogre('Mk3',  # name
                      45,  # tread
                       2,  # missiles
                       1,  # main battery
                       4,  # secondary battery
                       8)  # antipersonnel
    myMap.hexagons[2][1].addUnit(markIII)

    if DEBUG: print(myMap)

    if DEBUG: print('CP at:', myMap.getHexIDFromQR(1, 0))
    if DEBUG: print('OGRE at:', myMap.getHexIDFromQR(1, 2))

    # Find a path from the OGRE to the CP
    r, q = myMap.getRQFromHexID('0203')
    path = A_Star((1, 2), (1, 0))
    solution = path.findPath(myMap, path.S)
    print(solution)

    if DEBUG:
        closed = []
        for hex in path.closedHexes:
            q, r = hex
            closed.append(myMap.getHexIDFromQR(q, r))
        print('Closed hexes:', closed)

        hexPath = []
        for hex in path.openHexes:
            q, r = hex
            hexPath.append(myMap.getHexIDFromQR(q, r))
        print('Open hexes:', hexPath)
