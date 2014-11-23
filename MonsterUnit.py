__author__ = 'San Lee'

from BaseUnit import BaseUnit


class MonsterUnit(BaseUnit):
    """
    Monster unit, superclass of BossUnit
    """
    def __init__(self, position, data):
        BaseUnit.__init__(self, position, data)
