__author__ = 'San Lee'

import MonsterUnit


class BossUnit(MonsterUnit):
    """
    Boss unit
    Leader of boss party
    """
    def __init__(self, position, data):
        super.__init__(position, data)
