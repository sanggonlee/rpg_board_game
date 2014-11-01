__author__ = 'San Lee'

import pygame as pg
import sys

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
            self.players.append(Player(i, 50))

        self.board = Board(10, 6)
        self.turn = 0
        self.whole_screen = screen
        self.centre_screen = self.whole_screen.subsurface(pg.Rect(TILE_WIDTH,
                                                                  TILE_HEIGHT,
                                                                  WINDOW_WIDTH-2*TILE_WIDTH,
                                                                  WINDOW_HEIGHT-2*TILE_HEIGHT))

    def start(self):
        DEBUG.log("Game started", level=1)
        self.board.draw(self.whole_screen)

        self.update_player_pos()
        # main loop (one turn per iteration)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.turn += 1

            # determine who plays this turn
            which_player_turn = self.turn % self.num_players
            player = self.players[which_player_turn]

            # process dice rolling
            dice_result = player.roll_dice(self.centre_screen, EVENT_GO_FORWARD)

            # clear the centre screen and the tile that the player was in, because the player's not there anymore
            self.centre_screen.fill(BACKGROUND_COLOUR)
            self.board.tiles[player.position].draw(self.whole_screen)

            player.position += dice_result
            DEBUG.log("Player {}, moving to position {}".format(which_player_turn+1, player.position), level=1)
            if player.position >= len(self.board.tiles):
                break

            self.update_player_pos()
            action_result = player.invoke_tile_action(self.centre_screen, tile_data[player.position])
            if action_result == ACTION_RESULT_DIE:
                # if died, clear the player token from the tile
                self.board.tiles[player.died_position].draw(self.whole_screen)
                self.update_player_pos()

    def update_player_pos(self):
        # draw all players' tokens
        for player_index in range(self.num_players):
            self.players[player_index].\
                draw_token(self.whole_screen, self.board.tiles[self.players[player_index].position])
        pg.display.flip()