__author__ = 'San Lee'

import pygame as pg
from constants import *
from data import *

from debugger import Debugger as DEBUG

NUM_TILES_WIDTH = WINDOW_WIDTH / TILE_HEIGHT
NUM_TILES_HEIGHT = WINDOW_HEIGHT / TILE_HEIGHT
NUM_TILES_TOTAL = 2*(NUM_TILES_WIDTH-1) + 2*(NUM_TILES_HEIGHT-1)


class Tile:
    """
    Tile class
    """
    def __init__(self, index, data):
        self.index = index
        self.data = data

        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT

        # set the position of tile, which goes round the window
        if self.index < NUM_TILES_WIDTH - 1:
            # upper row (excluding top right)
            self.x_pos = self.index * self.width
            self.y_pos = 0
        elif self.index < NUM_TILES_WIDTH + NUM_TILES_HEIGHT - 2:
            # right column (excluding bottom right)
            self.x_pos = WINDOW_WIDTH - self.width
            self.y_pos = (self.index - NUM_TILES_WIDTH + 1) * self.height
        elif self.index < 2*NUM_TILES_WIDTH + NUM_TILES_HEIGHT - 3:
            # lower row (excluding bottom left)
            self.x_pos = WINDOW_WIDTH - ((self.index - (NUM_TILES_WIDTH + NUM_TILES_HEIGHT - 2)) + 1) * self.width
            self.y_pos = WINDOW_HEIGHT - self.height
        elif self.index < 2*NUM_TILES_WIDTH + 2*NUM_TILES_HEIGHT - 4:
            # left column (excluding top left)
            self.x_pos = 0
            self.y_pos = WINDOW_HEIGHT - (self.index - (2*NUM_TILES_WIDTH + NUM_TILES_HEIGHT - 3) + 1) * self.height
        else:
            raise IndexError("Tile index out of range: {}".format(self.index))

        DEBUG.log("initialized tile, index={}, pos=({},{})".format(self.index, self.x_pos, self.y_pos), DEBUG.LEVEL2)

    def draw(self, screen):
        if self.data[TILE_TYPE] == TILE_GOLD:
            self.image = pg.image.load('gold_get.png')
        elif self.data[TILE_TYPE] == TILE_MONSTER:
            self.image = pg.image.load('smile.png')
        elif self.data[TILE_TYPE] == TILE_SHOP:
            self.image = pg.image.load('smile.png')
        elif self.data[TILE_TYPE] == TILE_RESPAWN:
            self.image = pg.image.load('respawn.png')
        elif self.data[TILE_TYPE] == TILE_HEAL:
            self.image = pg.image.load('heal.png')
        elif self.data[TILE_TYPE] == TILE_OTHER_EVENT:
            self.image = pg.image.load('smile.png')

        self.image = pg.transform.scale(self.image, (self.width, self.height))
        DEBUG.log("received image, image={}".format(self.image), DEBUG.LEVEL3)
        screen.blit(self.image, (self.x_pos, self.y_pos))