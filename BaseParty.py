__author__ = 'San Lee'

import pygame as pg
import os

from BaseUnit import UNIT_SIZE
import colour
from constants import TILE_WIDTH, TILE_HEIGHT, MONSTER_IMG_FILE_PATH

PARTY_ROW_NUM = 2
PARTY_FRONT_ROW = 0
PARTY_BACK_ROW = 1


class BaseParty:
    """
    Abstract class for party, superclass of PlayerParty and MonsterParty
    """
    def __init__(self):
        self._members = [[None, None, None, None, None],
                         [None, None, None, None, None]]
        self._member_positions = [[None, None, None, None, None],
                                  [None, None, None, None, None]]

    def draw(self, centre_screen, is_me):
        """
        Implemented by PlayerParty and MonsterParty
        """
        for row_index in range(len(self._members)):
            for unit_index in range(len(self._members[row_index])):
                print "row={}, unit={}".format(row_index, unit_index)
                if is_me:
                    self._member_positions[row_index][unit_index] = \
                        ((PARTY_ROW_NUM-1-row_index)*UNIT_SIZE[0], unit_index*UNIT_SIZE[1])
                else:
                    screen_width = centre_screen.get_width()
                    self._member_positions[row_index][unit_index] = \
                        ((screen_width-PARTY_ROW_NUM*UNIT_SIZE[0])+row_index*UNIT_SIZE[0], unit_index*UNIT_SIZE[1])

                if self._members[row_index][unit_index] is None:
                    surf = centre_screen.subsurface(pg.Rect(self._member_positions[row_index][unit_index], UNIT_SIZE))
                    surf.fill(colour.GRAY)
                else:
                    surf = pg.image.load(
                        os.path.join(MONSTER_IMG_FILE_PATH, self._members[row_index][unit_index].img_file_path))
                    surf = pg.transform.scale(surf, UNIT_SIZE)
                    centre_screen.blit(surf, self._member_positions[row_index][unit_index])
                pg.draw.rect(surf, colour.BLACK, pg.Rect((0, 0), UNIT_SIZE), 1)
        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))
        pg.time.delay(1000)