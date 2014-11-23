__author__ = 'San Lee'

from BaseParty import BaseParty
from MonsterUnit import MonsterUnit


class MonsterParty(BaseParty):
    """
    MonsterParty class
    """
    def draw(self, centre_screen):
        BaseParty.draw(self, centre_screen, False)  # monster party is never your party

    def insert_data(self, monster_list):
        """
        :param monster_list: list of 2-tuple (monster_data, monster_position)
        :return: None
        """
        for monster_data, monster_pos in monster_list:
            self._members[monster_pos[0]][monster_pos[1]] = MonsterUnit(monster_pos, monster_data)