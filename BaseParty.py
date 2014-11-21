__author__ = 'San Lee'


PARTY_FRONT_ROW = 0
PARTY_BACK_ROW = 1


class BaseParty:
    """
    Abstract class for party, superclass of PlayerParty and MonsterParty
    """
    def __init__(self):
        self._members = [[None, None, None, None, None],
                         [None, None, None, None, None]]

    def draw(self, centre_screen):
        """
        Implemented by PlayerParty and MonsterParty
        """
        pass