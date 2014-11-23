__author__ = 'San Lee'

import pygame as pg

import colour

from constants import TILE_WIDTH, TILE_HEIGHT
from BaseParty import BaseParty, PARTY_ROW_NUM, PARTY_FRONT_ROW, PARTY_BACK_ROW
from BaseUnit import UNIT_SIZE


class PlayerParty(BaseParty):
    """
    PlayerParty
    """
    def __init__(self, player_unit):
        BaseParty.__init__(self)
        #super(PlayerParty, self).__init__(self)
        self._members[PARTY_BACK_ROW][2] = player_unit