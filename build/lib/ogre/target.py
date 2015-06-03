class Target:
    """
    This class is used to represent a potential 'Target'.  Targets are used for
    managing the fire portion of a turn.
    """
    def __init__(self, q, r, hexID):
        """
        Create an instance of a 'Target' given internal coordinates represented
        by 'q' and 'r' as well as a 'hexID'.
        """
        self.q = q
        self.r = r
        self.hexID = hexID
        self.status = None
        self.unitType = None
        self.attackStrength = None
        self.range_ = 0
        self.defenseStrength = None
        self.movementPoints = None
        self.distance = None
        self.offensiveFirePower = 0

    def __str__(self):
        """
        Returns a string representation of a 'Target', including most unit
        attributes such as 'attackStrength', 'range_', and 'defenseStrength'.
        """
        return '{} @ {} ({}/{} D{} M{})'.format(self.unitType, self.hexID, 
               self.attackStrength, self.range_, self.defenseStrength,
               self.movementPoints)
