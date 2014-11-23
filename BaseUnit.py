__author__ = 'San Lee'

from data import MONSTER_TYPE, MONSTER_NAME, MONSTER_IMG_FILE, MONSTER_LEVEL, MONSTER_HEALTH, MONSTER_ATTACK, MONSTER_DEFENCE
from constants import *

UNIT_SIZE = (80, 80)


class BaseUnit:
    """
    Abstract class for units in parties
    Superclass of MonsterUnit and AlliedUnit
    """
    def __init__(self, position, data):
        """
        :param position: 2-tuple, position in formation
        :return: None
        """
        self.position = position

        if data[MONSTER_TYPE] == MONSTER_TYPE_BOSS:
            self.is_leader = True
        else:
            self.is_leader = False

        self.name = data[MONSTER_NAME]
        self.img_file_path = data[MONSTER_IMG_FILE]
        self.level = data[MONSTER_LEVEL]
        self.health = data[MONSTER_HEALTH]
        self.base_attack = data[MONSTER_ATTACK]
        self.base_defence = data[MONSTER_DEFENCE]