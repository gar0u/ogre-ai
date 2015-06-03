import random


class Die:
    """
    This class represents a single die for making random game decisions.

    (My daughter Avery was asking about my project, so we wrote this 
     module together so I could teach her some Python.)
    """

    # Die Attributes (nouns; describe an object)
    numberOfSides = 0
    sides = []

    # Die Methods (verbs; things an object can do)
    def __init__(self, numberOfSides):
        """
        Create an instance of 'Die', where 'numberOfSides' is the
        number of sides on the die.  Some games use dice with
        different numbers of sides; common dice are 1d4, 1d6, 1d8,
        1d12, and 1d20, but OGRE only uses a regular 1d6.
        """
        self.numberOfSides = numberOfSides

        for i in range(1, numberOfSides+1):
            self.sides.append(i)

    def roll(self):
        """
        Roll the die and return the result.
        """
        return random.choice(self.sides)


if __name__ == '__main__':
    # Self test
    myDie = Die(6)
    result = myDie.roll()
    print(result)
