import pygame as pg
from tile import Tile

from data import *

from debugger import Debugger


class Board:
    """
    Game board class
    Member variables:
    (tuple) size  - N x N size of the board
    (list)  tiles - (NxN)-number of tiles in a list
    """
    def __init__(self, size_x, size_y):
        self.tiles = []
        for i in range(2*(size_x-1) + 2*(size_y-1)):
            self.tiles.append(Tile(i, tile_data[i]))

    def draw(self, screen):
        Debugger.log("[Board, draw] ENTERED", Debugger.LEVEL1)
        for tile in self.tiles:
            tile.draw(screen)
            pg.display.flip()