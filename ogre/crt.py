DEBUG = False


from ogre.die import *


class CRT:
    """
    This class represents a 'Combat Results Table' (CRT).  A CRT is a common
    method of determining combat results in hex-based war games.
    """
    combatResultTable = {1: {.5: 'NE', 1: 'NE', 2: 'NE', 3: 'D', 4: 'D'},
                         2: {.5: 'NE', 1: 'NE', 2: 'D',  3: 'D', 4: 'X'},
                         3: {.5: 'NE', 1: 'D',  2: 'D',  3: 'X', 4: 'X'},
                         4: {.5: 'NE', 1: 'D',  2: 'X',  3: 'X', 4: 'X'},
                         5: {.5: 'D',  1: 'X',  2: 'X',  3: 'X', 4: 'X'},
                         6: {.5: 'X',  1: 'X',  2: 'X',  3: 'X', 4: 'X'}}

    def crossReference(attack, defense):
        """
        This method takes two inputs, an 'attack' value and a 'defense'
        value.  A single six-sided dice is rolled, then the die roll
        is cross referenced against the ratio of 'attack':'defense'.

        In OGRE, a ratio of less than 1:2 results in 'NE' (no effect)
        and a ratio of 5:1 or greater is 'X' (automatic destruction).

        Ratios in between are rounded down in favor of the defender.
        """
        if attack > 0 and defense == 0:
            # Automatic destruction
            return 'X'
        else:
            assert(defense > 0)
            try:
                ratio = attack / defense
                if ratio < .5:
                    return 'NE'
                elif ratio < 0 and ratio >= .5:
                    ratio = .5
                else:
                    ratio = attack // defense
                if ratio > 4:
                    return 'X'
                elif ratio == 0:
                    return 'NE'
                else:
                    # Roll a 6-sided die
                    myDie = Die(6)
                    roll = myDie.roll()
                    if DEBUG:  print('   CRT roll: attack:', attack, 
                                     'defense:', defense, 'ratio:', 
                                     ratio, 'roll:', roll) 
                    # Cross-reference combat result table
                    return CRT.combatResultTable[roll][ratio]
            except ZeroDivisionError:
                # (N.b. This should never happen!)
                pass
            except KeyError:
                print('UNHANDLED RATIO!\n   roll', roll, 'ratio', ratio)
