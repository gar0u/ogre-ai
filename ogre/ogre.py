# TECHNICAL DEBT: Implement 'ramming' rules


DEBUG = False


from ogre.a_star import *
from ogre.crt import *
from ogre.status import *
from ogre.target import *
from ogre.unitType import *


class Missile:
    """
    This class represents an OGRE 'Missile' in the game.
    """
    # Missile attributes
    range = 5
    strength = 6
    defense = 3


class MainBattery:
    """
    This class represents an OGRE 'MainBattery' in the game.
    """
    range = 3
    strength = 4
    defense = 3


class SecondaryBattery:
    """
    This class represents an OGRE 'SecondaryBattery' in the game.
    """
    range = 2
    strength = 3
    defense = 3


class Antipersonnel:
    """
    This class represents an OGRE 'AP' (i.e. antipersonnel) weapon system in
    the game.  AP are 1:1 v. infantry and CP units ('X' on a roll of 5 or 
    6), but are ineffective against all other units.
    """
    range = 1
    strength = 1
    defense = 1


class Tread:
    NotImplemented


class Ogre:
    """
    This class represents an 'Ogre'.
    """
    # Ogre methods
    def __init__(self, ogreName, tread, missiles, mainBattery, 
                 secondaryBattery, antipersonnel):
        self.unitName = ogreName
        self.unitType = UnitType.OGRE
        self.tread = tread
        self.missiles = missiles
        self.mainBattery = mainBattery
        self.secondaryBattery = secondaryBattery
        self.antipersonnel = antipersonnel
        self.hexLocation = None
        self.destroyed = False
        self.status = Status.NORMAL
        self.listOfSystems = ['missiles', 'mainBattery', 'secondaryBattery', 
                              'tread']  # Exclude AP because they are a limited
                                        # threat

    def setLocation(self, hexID):
        """
        Set the location of an 'Ogre' given a 'hexID' (e.g. '0101')
        """
        self.hexLocation = hexID

    def isDestroyed(self):
        """
        Checks if every weapon system of the 'Ogre' and all the tread of the
        'Ogre' have been reduced to 0, and therefore the 'Ogre' is destroyed.
        Returns 'True' or 'False', accordingly. 
        """
        if self.missiles <= 0 and self.mainBattery <= 0 \
           and self.secondaryBattery <= 0 and self.tread <= 0:
            self.destroyed = True
            self.status = Status.DESTROYED
        else:
            self.destroyed = False
            self.status = Status.NORMAL
        return self.destroyed


    def getMovementPoints(self):
        """
        'Ogre' movement dependent on the number of tread units remaining.

        Returns the number of movement points (3, 2, 1, or 0) based on
        the number of remaining tread units.
        """
        movementPoints = 0
        if 45 <=self.tread > 30:
           movementPoints = 3
        elif 30 <= self.tread > 15:
            movementPoints = 2
        elif 15 <= self.tread > 0:
            movementPoints = 1
        else:
            movementPoints = 0

        return movementPoints

    def removeTread(self, numberOfTread):
        """
        Removes the given 'numberOfTread' from an 'Ogre'.
        """
        self.tread -= numberOfTread

    def move(self, map, cpHexID):
        """
        Given a 'map' and the location of the command post as 'cpHexID',
        Use the A* algorithm to navigate the 'Ogre' to the 'CommandPost'.
        """
        # At the start of the movement phase, check if the OGRE is destroyed
        if self.status != Status.DESTROYED:
            if self.tread == 0 and \
               self.missiles == 0 and \
               self.mainBattery == 0 and \
               self.secondaryBattery == 0:
                # Ignore AP
                self.status = Status.DESTROYED
                if DEBUG: print('OGRE has been destroyed!')
                # TECHNICAL DEBT: There can still be conditions that result
                #                 in a stalemate, e.g. an OGRE with no tread,
                #                 and therefore no movement points, and a
                #                 functioning main battery, but the only
                #                 remaining defender units are out of range
                #                 and also lack movement points (e.g. a HWZ).
                return False

        start = map.getQRFromHexID(self.hexLocation)
        # If the CP is still on the board, move towards it,
        # otherwise, flee to the south
        if cpHexID is not None:
            destination = map.getQRFromHexID(cpHexID)
        else:
            # TECHNICAL DEBT: Select the 'best' (least resistance) exit row hex
            destination = map.getQRFromHexID('1222')
        q_d, r_d = destination
        destinationHex = map.getHexIDFromQR(q_d, r_d)
        path = A_Star(start, destination)
        solution = path.findPath(map, path.S)
        # Check that the hex we move to is not already occupied by another unit
        # if so, move one hex less, until an open hex is found
        # or we stay at our current location
        movementPoints = self.getMovementPoints()
        if movementPoints > 0:
            # +1 because the first entry in subSolution is the current hex
            subSolution = solution[0:movementPoints+1]
            i = len(subSolution)-1
            while i >= 0:
                if map.hexOccupied(subSolution[i]) == False:
                    break
                i -= 1
            hexToMoveTo = subSolution[i]
            if hexToMoveTo == destinationHex and \
               map.hexagons[r_d][q_d].unitPresent is not None:
                # Stay put
                pass
            else:
                # Get the OGRE's current location coordinates
                q, r = map.getQRFromHexID(self.hexLocation)
                # Remove the OGRE from the current location
                map.hexagons[r][q].removeUnit()
                # Move the OGRE to the new location
                self.setLocation(hexToMoveTo)
                r, q = map.getRQFromHexID(hexToMoveTo)
                # Add the OGRE to the new location
                map.hexagons[r][q].addUnit(self)
                if DEBUG:  print('OGRE moved to', self.hexLocation, '\n')

    def fire(self, map, defenderUnits, disabledDefenderUnits,
             recoverableDefenderUnits, destroyedDefenderUnits):
        # Get the OGRE's current location
        q_c, r_c = map.getQRFromHexID(self.hexLocation)
        ogreCubeCoords = map.convertAxial2Cube(q_c, r_c)

        # Scan the map once to generate a list of potential targets
        listOfTargets = []
        numberOfHWZ = 0
        # Assume destroyed, if it exists, it will be set correctly
        statusOfCP = Status.DESTROYED 
        for i in range(0, map.r):
            for j in range(0, map.q):
                if map.hexagons[i][j].unitPresent is not None and \
                   map.hexagons[i][j].unitPresent.unitType != UnitType.OGRE:
                    target = Target(j, i, map.getHexIDFromQR(j, i))
                    targetCubeCoords = map.convertAxial2Cube(j, i)
                    distance = map.getDistance(ogreCubeCoords,
                               targetCubeCoords)
                    # Keep track of the number of HWZ counters on the board (so
                    # we don't waste missiles)
                    if map.hexagons[i][j].unitPresent.unitType == UnitType.HWZ:
                        numberOfHWZ += 1
                    # Keep track of the command post status
                    if map.hexagons[i][j].unitPresent.unitType == UnitType.CP:
                        statusOfCP = map.hexagons[i][j].unitPresent.status
                    # Do not bother with units that are beyond missile range
                    if distance <= Missile.range:
                        target.distance = distance
                        target.unitName = \
                            map.hexagons[i][j].unitPresent.unitName
                        target.status = map.hexagons[i][j].unitPresent.status
                        target.unitType = \
                            map.hexagons[i][j].unitPresent.unitType
                        target.attackStrength = \
                            map.hexagons[i][j].unitPresent.attackStrength
                        target.range_ = map.hexagons[i][j].unitPresent.range_
                        target.defenseStrength = \
                            map.hexagons[i][j].unitPresent.defenseStrength
                        target.movementPoints = \
                            map.hexagons[i][j].unitPresent.movementPoints
                        listOfTargets.append(target)

        # Fire missiles
        if self.missiles > 0:
            if DEBUG:
                print('Potential targets before firing missiles:')
                for target in listOfTargets:
                    print('  ', target)
            self.fireMissile(listOfTargets, statusOfCP, numberOfHWZ)
            self.resolveCombat(map, listOfTargets, defenderUnits, 
                               disabledDefenderUnits, recoverableDefenderUnits,
                               destroyedDefenderUnits, statusOfCP, numberOfHWZ)
            if DEBUG:
                print('Potential targets after potentially firing missiles:')
                for target in listOfTargets:
                    print('  ', target)

        # Fire AP
        if self.antipersonnel > 0:
            if DEBUG:
                print('Potential targets in range before firing AP:')
                for target in listOfTargets:
                    print('  ', target)
            self.fireAP(listOfTargets)
            self.resolveCombat(map, listOfTargets, defenderUnits,
                               disabledDefenderUnits, recoverableDefenderUnits,
                               destroyedDefenderUnits, statusOfCP, numberOfHWZ)
            if DEBUG:
                print('Potential targets after potentially firing AP:')
                for target in listOfTargets:
                    print('  ', target)

        # Fire batteries
        if self.mainBattery > 0 or self.secondaryBattery > 0:
            if DEBUG:
                print('Potential targets in range before firing batteries:')
                for target in listOfTargets:
                    print('  ', target)
            self.fireBatteries(map, listOfTargets, defenderUnits, 
                               disabledDefenderUnits, recoverableDefenderUnits,
                               destroyedDefenderUnits)
            self.resolveCombat(map, listOfTargets, defenderUnits, 
                               disabledDefenderUnits, recoverableDefenderUnits,
                               destroyedDefenderUnits, statusOfCP, numberOfHWZ)
            if DEBUG:
                print('Potential targets after potentially firing batteries:')
                for target in listOfTargets:
                    print('  ', target)

        # Output some useful lists during development
        """ 
        print('Defender units:')
        for unit in defenderUnits:
            print('  ', unit)

        print('Disabled defender units:')
        for unit in disabledDefenderUnits:
            print('  ', unit)

        print('Recoverable defender units:')
        for unit in recoverableDefenderUnits:
            print('  ', unit)

        print('Destroyed defender units:')
        for unit in destroyedDefenderUnits:
            print('  ', unit)
        """

    def fireBatteries(self, map, listOfTargets, defenderUnits,
                      disabledDefenderUnits, recoverableDefenderUnits,
                      destroyedDefenderUnits):

        # Check if there are any targets within range of batteries
        if len(listOfTargets) > 0:
            # A sortable list of targets by different priorities
            prioritizedTargets = []
            def getAttackStrength(item):
                return item[1]
            def getRange(item):
                return item[2]
            targetsAtMaxRangeMain = 0
            targetsInRangeSecondary = 0
            for target in listOfTargets:
                if target.distance == 3:
                    targetsAtMaxRangeMain += 1
                if target.distance <= 2:
                    targetsInRangeSecondary += 1
            totalTargetsInRangeMain = targetsAtMaxRangeMain + \
                targetsInRangeSecondary
            # If there is only one target, assign maximum batteries
            if totalTargetsInRangeMain == 1:
                # Assign batteries
                for target in listOfTargets:
                    if target.distance <= 3 and self.mainBattery == 1:
                        if DEBUG: print('Assigned main battery +{} at ' + \
                               '{}'.format(MainBattery.strength, target.hexID))
                        target.offensiveFirePower = MainBattery.strength
                        # Assign secondary batteries if they are available and 
                        # target is in range
                        if target.distance <= 2 and self.secondaryBattery > 0:
                            for secondary in range(0, self.secondaryBattery):
                                if DEBUG: print('Assigned secondary battery ' + \
                   '+{} at {}'.format(SecondaryBattery.strength, target.hexID))
                                target.offensiveFirePower += \
                                    SecondaryBattery.strength
            elif targetsAtMaxRangeMain > 1 and targetsInRangeSecondary == 0 \
                 and self.mainBattery > 0:
                # TECHNICAL DEBT:  I'm sure there is a better way to do this 
                #                  than iterating over the list time and time
                #                  again, but I'm adding functionality piece
                #                  by piece, and the worst case 'n' for each
                #                  loop is only 6, so performance is not an
                #                  issue.
                # 
                #                  However, complexity is a concern.  Once
                #                  this is working, if I have time, I will
                #                  make these functions.  I am prouder of more
                #                  pythonic  modules like 'crt.py' (of course
                #                  it is much simpler!)
                highestThreatTarget = None
                highestThreat = 0
                for target in listOfTargets:
                    if target.distance <= 3 and \
                       target.attackStrength > highestThreat:
                        highestThreatTarget = target
                        highestThreat = target.attackStrength
                for target in listOfTargets:
                    if target == highestThreatTarget:
                        target.offensiveFirePower += MainBattery.strength
                        if DEBUG: print('Assigned main battery +{} at ' + \
                              '{}'.format(MainBattery.strength, target.hexID))
            elif targetsInRangeSecondary > 1:
                # Assign batteries to the highest threat unit until there is
                # a 2-1 ratio (50% chance of destroying it)
                highestThreatTarget = None
                highestThreat = 0
                for target in listOfTargets:
                    if target.distance <= 2 \
                       and target.attackStrength > highestThreat:
                        highestThreatTarget = target
                        highestThreat = target.attackStrength
                unassignedSecondaries = self.secondaryBattery
                for target in listOfTargets:
                    if target == highestThreatTarget and self.mainBattery > 0:
                        target.offensiveFirePower += MainBattery.strength
                        if DEBUG: print('Assigned main battery +{} at ' + \
                              '{}'.format(MainBattery.strength, target.hexID))
                        while target.offensiveFirePower / target.defenseStrength \
                              < 2 \
                              and target.distance <= 2 \
                              and unassignedSecondaries:
                            target.offensiveFirePower += \
                                SecondaryBattery.strength
                            unassignedSecondaries -= 1
                            if DEBUG: print('Assigned secondary battery ' + \
                   '+{} at {}'.format(SecondaryBattery.strength, target.hexID))
                # Assign any remaining secondary batteries to other targets
                for target in listOfTargets:
                    if target != highestThreatTarget and target.distance <=2 \
                       and unassignedSecondaries > 0:
                        target.offensiveFirePower += SecondaryBattery.strength
                        unassignedSecondaries -= 1
                        if DEBUG: print('Assigned secondary battery +{} at' + \
                        ' {}'.format(SecondaryBattery.strength, target.hexID))

    def resolveCombat(self, map, listOfTargets, defenderUnits, 
                      disabledDefenderUnits, recoverableDefenderUnits,
                      destroyedDefenderUnits, statusOfCP, numberOfHWZ):
        """
        Given a 'map', and various lists of potential targets 'listOfTargets', 
        and units in varius states; 'defenderUnits', 'disabledDefenderUnits',
        and 'recoverableDefenderUnits', resolve the effects of 'Ogre' combat
        against the defender units, then place any destroyed units on the
        'destroyedDefenderUnits' list.  The 'statusOfCP' and 'numberOfHWZ'
        parameters are also needed to resolve combat.
        """
        for target in listOfTargets:
            if target.status != Status.DESTROYED \
               and target.offensiveFirePower > 0:
                outcome = CRT.crossReference(target.offensiveFirePower,
                                             target.defenseStrength)
                if DEBUG: print('   CRT outcome in hex', target.hexID,
                                ':', outcome)
                if outcome == 'NE':  # NO EFFECT
                    pass
                elif outcome == 'D':  # DISABLED
                    # 'Casualty Reduce' INF3 and INF2 units
                    if target.unitType == UnitType.INF3:
                        # Update local target info
                        target.attackStrength -= 1
                        target.defenseStrength -= 1
                        # Update unit object
                        exec('map.hexagons[' + str(target.r) + '][' + \
                             str(target.q) + '].unitPresent.unitType = ' + \
                             'UnitType.INF2')
                        exec('map.hexagons[' + str(target.r) + '][' + \
                             str(target.q) + '].unitPresent.attackStrength ' + \
                             '-= 1')
                        exec('map.hexagons[' + str(target.r) + '][' + \
                             str(target.q) + '].unitPresent.defenseStrength ' + \
                             '-= 1')
                    elif target.unitType == UnitType.INF2:
                        # Update local target info
                        target.attackStrength -= 1
                        target.defenseStrength -= 1
                        # Update unit object
                        exec('map.hexagons[' + str(target.r) + '][' + \
                             str(target.q) + '].unitPresent.unitType = ' + \
                             'UnitType.INF1')
                        exec('map.hexagons[' + str(target.r) + '][' + \
                             str(target.q) + '].unitPresent.attackStrength ' + \
                             '-= 1')
                        exec('map.hexagons[' + str(target.r) + '][' + \
                             str(target.q) + '].unitPresent.defenseStrength' + \
                             ' -= 1')
                    # Destroy INF1 units
                    elif target.unitType == UnitType.INF1:
                        target.status = Status.DESTROYED
                        destroyedDefenderUnits.append(target.unitName)
                    # Disable all other unit types
                    else:
                        target.status = Status.DISABLED
                        exec('map.hexagons[' + str(target.r) + '][' + \
                             str(target.q) + '].unitPresent.status = ' + \
                             'Status.DISABLED')
                        disabledDefenderUnits.append(target.unitName)
                elif outcome == 'X':
                    target.status = Status.DESTROYED
                    destroyedDefenderUnits.append(target.unitName)
                    # Update local variables used by 'resolveCombat()'
                    if target.unitType == UnitType.CP:
                        statusOfCP = Status.DESTROYED
                    if target.unitType == UnitType.HWZ:
                        numberOfHWZ -= 1
        # Clean up target list beforing firing additional weapons
        # by making a 'copy' of the target list, so that 
        # as targets are removed, the size of the list does not shrink 
        # and we inadvertantly skip targets
        for target in listOfTargets[:]:
            if target.status == Status.DESTROYED:
                listOfTargets.remove(target)
        # Reset remaining targets 'offensive fire power' value to zero
        for target in listOfTargets:
            target.offensiveFirePower = 0

    def fireAP(self, targets):
        # Keep track of how much AP we are expending
        unassignedAP = self.antipersonnel
        # Count the number of availabile infantry targets
        infantryTargets = 0
        for target in targets:
            if (target.unitType == UnitType.INF3 or \
               target.unitType == UnitType.INF2 or \
               target.unitType == UnitType.INF1) and target.distance == 1 \
               and target.status != Status.DESTROYED:
                   infantryTargets += 1
            elif target.unitType == UnitType.CP and target.distance == 1 \
                 and target.status != Status.DESTROYED \
                 and target.offensiveFirePower == 0:
                # AP can be used to destroy command posts
                if DEBUG: print('Assigning +1 AP at', target.hexID)
                target.offensiveFirePower += 1
                unassignedAP -= 1
        if infantryTargets > 0:
            while unassignedAP > 0:
                # Attempt to distribute AP shots in 1:1 ratio
                # across any infantry units in range, then
                # assign left over AP weapons to increase ratio
                # beyond 1:1 until all AP weapons are assigned
                for target in targets:
                    if target.unitType == UnitType.INF3 \
                       and target.distance == 1 \
                       and target.status != Status.DESTROYED:
                        if unassignedAP >= 3:
                            if DEBUG: print('Assigning +3 AP at', target.hexID)
                            target.offensiveFirePower += 3
                            unassignedAP -= 3
                        else:
                            if DEBUG: print('Assigning +{} AP at ' + \
                                       '{}'.format(unassignedAP, target.hexID))
                            target.offensiveFirePower += unassignedAP
                            unassignedAP = 0
                    elif target.unitType == UnitType.INF2 \
                         and target.distance == 1 \
                         and target.status != Status.DESTROYED:
                        if unassignedAP >= 2:
                            if DEBUG: print('Assigning +2 AP at', target.hexID)
                            target.offensiveFirePower += 2
                            unassignedAP -= 2
                        else:
                            if DEBUG: print('Assigning +{} AP at ' + \
                                       '{}'.format(unassignedAP, target.hexID))
                            target.offensiveFirePower += unassignedAP
                            unassignedAP = 0
                    elif target.unitType == UnitType.INF1 \
                         and target.distance == 1 \
                         and target.status != Status.DESTROYED:
                        if unassignedAP >= 1:
                            if DEBUG: print('Assigning +1 AP at', target.hexID)
                            target.offensiveFirePower += 1
                            unassignedAP -= 1
                        else:
                            if DEBUG: print('Assigning +{} AP at ' + \
                                       '{}'.format(unassignedAP, target.hexID))
                            target.offensiveFirePower += unassignedAP
                            unassignedAP = 0

    def fireMissile(self, targets, statusOfCP, numberOfHWZ):
        if self.missiles == 0:
            # No missiles to shoot!
            pass
        elif statusOfCP != Status.DESTROYED and self.missiles < 2:
            # Save last missile for the CP
            # (N.b. this can result in an 'extra' missile if the
            #  OGRE starts its turn outside missile range, and
            #  ends the turn  within battery range or AP range.)
            pass
        else:
            # Do not shoot missiles at HWZ that can be reached with batteries
            # (Credit for this rule goes to my 7 year old son, Ewan, who is
            #  learning to play OGRE, and recognized that you should not waste
            #  missiles on units you can shoot with your batteries!)
            clearToFire = False
            maxThreat = 0
            for target in targets:
                if target.attackStrength > maxThreat:
                    maxThreat = target.attackStrength
                if target.unitType == UnitType.HWZ \
                   and target.distance > MainBattery.range:
                    clearToFire = True
            # Only shoot at HWZ that are in range, or the most powerful unit 
            # in range if there no HWZ left on the board, and we have more 
            # than one missile.
            if (clearToFire or numberOfHWZ < 1) and self.missiles > 1:
                for target in targets:
                    if clearToFire and \
                       target.distance <= Missile.range \
                       and target.attackStrength == maxThreat \
                       and self.missiles > 0:
                        # Fire missile!
                        if DEBUG: print('Firing missile at', target.hexID)
                        self.missiles -= 1
                        target.offensiveFirePower = target.offensiveFirePower \
                            + Missile.strength
    
    def __str__(self):
        return '      Tread: {}\n      Missiles: {}\n      Main: {}\n      Secondary: {} \n      AP: {}\n'.format(self.tread, self.missiles, self.mainBattery, self.secondaryBattery, self.antipersonnel)

