__author__ = 'San Lee'

import BaseUnit


class MonsterUnit(BaseUnit):
    """
    Monster unit, superclass of BossUnit
    """
    def __init__(self, position, data):
        super.__init__(position, data)
