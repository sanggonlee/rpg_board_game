__author__ = 'San Lee'

import pygame as pg
import random

from constants import *
from colour import *
from data import *
import eztext

from debugger import Debugger


class Player:
    """
    Player class
    """

    # Event types for rolling dice
    EVENT_GO_FORWARD = 0
    EVENT_GOLD = TILE_GOLD
    EVENT_MONSTER_FIGHT = TILE_MONSTER

    def __init__(self, player_id, health):
        self.player_id = player_id
        assert 0 <= self.player_id < MAX_NUM_PLAYERS
        assert 0 < health

        self.position = 0
        self.token_image = pg.transform.scale(pg.image.load('player_token.png'), (TILE_WIDTH/2, TILE_HEIGHT/2))
        if self.player_id == 0:
            self.relative_x = 0
            self.relative_y = 0
        elif self.player_id == 1:
            self.relative_x = TILE_WIDTH/2
            self.relative_y = 0
        elif self.player_id == 2:
            self.relative_x = 0
            self.relative_y = TILE_HEIGHT/2
        elif self.player_id == 3:
            self.relative_x = TILE_WIDTH/2
            self.relative_y = TILE_HEIGHT/2

        self.weapon = None
        self.armor = None
        self.inventory = [None, None, None, None, None]
        self.gold = 0

        self.full_health = health
        self.base_attack = 10
        self.base_defence = 0

        self.current_health = self.full_health
        self.current_attack = self.base_attack
        self.current_defence = self.base_defence

    @staticmethod
    def get_dice_number():
        return random.randint(1, 6)

    def get_dice_roll_textbox(self, event_type):
        textbox = eztext.Input(
            font=pg.font.Font(None, 30),
            color=BLACK,
            maxlength=0,
            x=0,
            y=0,
        )
        if event_type == self.EVENT_GO_FORWARD:
            textbox.set_prompt("Player {}, click anywhere to roll dice.".format(self.player_id+1))
        elif event_type == self.EVENT_GOLD:
            textbox.set_prompt("Click anywhere to find out how much gold you found, Player {}".format(self.player_id+1))
        elif event_type == self.EVENT_MONSTER_FIGHT:
            textbox.set_prompt("Click anywhere to see your fight condition for today, Player {}".format(self.player_id+1))
        else:
            raise TypeError("get_dice_roll_textbox() got invalid event_type")

        return textbox

    def roll_dice(self, centre_screen, event_type):
        """
        :param centre_screen: (Surface) centre screen area
        :param event_type: (int) EVENT_GO_FORWARD, EVENT_GOLD, or EVENT_MONSTER_FIGHT
        :return: random number from 1~6
        """
        centre_screen.fill(WHITE)

        # set up textbox for rolling dice
        dice_roll_textbox = self.get_dice_roll_textbox(event_type)
        centre_of_centre = dice_roll_textbox.get_centre_surface(centre_screen)
        dice_roll_textbox.draw(centre_of_centre)

        # dice rolling loop
        while True:
            Debugger.log("[Game, start] Waiting for player to roll dice", Debugger.LEVEL3)
            events = pg.event.get()
            dice_roll_textbox.update(events)
            pg.display.flip()

            for event in events:
                if event.type == pg.MOUSEBUTTONUP:
                    Debugger.log("[Game, start] Mouse pressed to roll dice", Debugger.LEVEL2)
                    return self.get_dice_number()

    def draw_token(self, screen, tile):
        screen.blit(self.token_image, (tile.x_pos + self.relative_x, tile.y_pos + self.relative_y))

    def invoke_tile_action(self, centre_screen, tile_value):
        tile_type = tile_value[TILE_TYPE]
        if tile_type is TILE_GOLD:
            self.process_action_gold_get(centre_screen, tile_value[TILE_GOLD_MULTIPLIER])
        elif tile_type is TILE_MONSTER:
            self.process_action_monster(centre_screen, tile_value[TILE_DATA])
        elif tile_type is TILE_HEAL:
            self.process_action_heal(centre_screen, tile_value[TILE_HEAL_AMOUNT])
        elif tile_type is TILE_RESPAWN:
            self.process_action_respawn(centre_screen, self.position)
        elif tile_type is TILE_SHOP:
            self.process_action_shop(centre_screen, tile_value[TILE_DATA])
        else:
            raise TypeError("Undefined type of tile!")

    def process_action_gold_get(self, centre_screen, gold_multiplier):
        if Debugger.SKIP_GOLD_GET:
            pass

        dice_result = self.roll_dice(centre_screen, self.EVENT_GOLD)
        amount_got = dice_result * gold_multiplier
        self.gold += amount_got

        centre_screen.fill(WHITE)
        textbox = eztext.Input(
            font=pg.font.Font(None, 30),
            color=BLACK,
            maxlength=0,
            prompt="Player {} found {} gold and now has {} gold!".format(self.player_id+1, amount_got, self.gold),
            x=0,
            y=0,
        )
        textbox.draw(textbox.get_centre_surface(centre_screen))
        textbox.update(pg.event.get())
        pg.display.flip()
        pg.time.delay(3000)

    def process_action_monster(self, centre_screen, data):
        pass

    def process_action_heal(self, centre_screen, amount):
        pass

    def process_action_respawn(self, centre_screen, position):
        pass

    def process_action_shop(self, centre_screen, data):
        pass