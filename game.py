__author__ = 'San Lee'

import pygame as pg

from data import *

from board import Board
from player import Player, EVENT_GO_FORWARD

from debugger import Debugger as DEBUG


class Game:
    """
    Main game manager class

    """
    def __init__(self, screen, num_human_players, num_bot_players):
        self.num_human_players = num_human_players
        self.num_bot_players = num_bot_players
        self.num_players = self.num_human_players + self.num_bot_players
        self.players = []
        for i in range(self.num_players):
            self.players.append(Player(i, 100))

        self.board = Board(10, 6)
        self.turn = 0
        self.whole_screen = screen
        self.centre_screen = self.whole_screen.subsurface(pg.Rect(TILE_WIDTH,
                                                                  TILE_HEIGHT,
                                                                  WINDOW_WIDTH-2*TILE_WIDTH,
                                                                  WINDOW_HEIGHT-2*TILE_HEIGHT))

    def start(self):
        DEBUG.log("Game started", DEBUG.LEVEL1)
        self.board.draw(self.whole_screen)

        # main loop (one turn per iteration)
        for turn in range(5000):
            self.turn = turn

            # draw all players' tokens
            for player_index in range(self.num_players):
                self.players[player_index].\
                    draw_token(self.whole_screen, self.board.tiles[self.players[player_index].position])
            pg.display.flip()

            # determine who plays this turn
            which_player_turn = self.turn % self.num_players
            player = self.players[which_player_turn]

            # process dice rolling
            dice_result = player.roll_dice(self.centre_screen, EVENT_GO_FORWARD)

            # clear the centre screen and the tile that the player was in, because the player's not there anymore
            self.centre_screen.fill(BACKGROUND_COLOUR)
            self.board.tiles[player.position].draw(self.whole_screen)

            player.position += dice_result
            DEBUG.log("Player {}, moving to position {}".format(which_player_turn+1, player.position), DEBUG.LEVEL1)
            if player.position >= len(self.board.tiles):
                break
            player.draw_token(self.whole_screen, self.board.tiles[player.position])
            player.invoke_tile_action(self.centre_screen, tile_data[player.position])