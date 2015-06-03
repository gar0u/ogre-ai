class Behavior:
    """
    This class represents the various behaviors a unit can exhibit.

    Each unit may have a different behavior, but a single unit's
    behavior is static and once assigned, will not change during the game.

    COWARDLY:

        Movement:  Cowardly units flee the OGRE and attempt to get as close 
                   to the CP as possible.

        Targeting: Cowardly units will randomly select an OGRE target
                   (missiles, main battery, secondary battery, or tread).

        Firing:    Cowardly units will never combine fire with other units.

    DISCIPLINED:

        Movement:  Disciplined units stand their ground and will not move.

        Targeting: Disciplined units will select an OGRE target in descending
                   priority; missiles, main battery, tread, secondary battery.
        Firing:    Disciplined units will always attempt to combine fire for 
                   3-1 odds with other units.

    BRAVE:

        Movement:  Brave units pursue the OGRE.

        Targeting: Brave units will probabalistically select an OGRE target;
                   missiles or main battery (.5), secondary battery (.2), or
                   tread (.3).

        Firing:    Brave units will attempt to combine fire with other units.
    """

    COWARDLY = 'Cowardly'
    DISCIPLINED = 'Disciplined'
    BRAVE = 'Brave'
