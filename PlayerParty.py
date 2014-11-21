__author__ = 'San Lee'

import pygame as pg

import colour

from constants import TILE_WIDTH, TILE_HEIGHT
from BaseParty import BaseParty, PARTY_FRONT_ROW, PARTY_BACK_ROW
from BaseUnit import UNIT_SIZE


class PlayerParty(BaseParty):
    """
    PlayerParty
    """
    def __init__(self, player_unit):
        BaseParty.__init__(self)
        #super(PlayerParty, self).__init__(self)
        #self._members[PARTY_BACK_ROW][2] = player_unit

    def draw(self, centre_screen):
        #surff = pg.Surface(UNIT_SIZE)
        #pg.draw.rect(surff, colour.BLACK, pg.Rect((500, 300), UNIT_SIZE), 10)
        for row_index in range(len(self._members)):
            for unit_index in range(len(self._members[row_index])):
                print "row={}, unit={}".format(row_index, unit_index)
                pos = (row_index*UNIT_SIZE[0], unit_index*UNIT_SIZE[1])
                if self._members[row_index][unit_index] is None:
                    print "here"
                    surf = centre_screen.subsurface(pg.Rect(pos, UNIT_SIZE))
                    surf.fill(colour.GRAY)
                else:
                    surf = pg.image.load(self._members[row_index][unit_index].img_file_path)
                pg.draw.rect(surf, colour.BLACK, pg.Rect((0, 0), UNIT_SIZE), 1)
        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))
        pg.time.delay(1000)