__author__ = 'San Lee'

import pygame as pg
import random

from colour import *
from data import *
import eztext

from debugger import Debugger as DEBUG, SKIP_GOLD_GET, SKIP_HEAL, SKIP_RESPAWN, SKIP_MONSTER_FIGHT, SKIP_SHOP


# Event types for rolling dice
EVENT_GO_FORWARD = 0
EVENT_GOLD = TILE_GOLD
EVENT_MONSTER_FIGHT = TILE_MONSTER


class Player:
    """
    Player class
    """
    def __init__(self, player_id, health):
        self.player_id = player_id
        assert 0 <= self.player_id < MAX_NUM_PLAYERS
        assert 0 < health

        self.position = 0
        self.respawn_pos = 0
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
        if event_type == EVENT_GO_FORWARD:
            textbox.set_prompt("Player {}, click anywhere to roll dice.".format(self.player_id+1))
        elif event_type == EVENT_GOLD:
            textbox.set_prompt("Click anywhere to find out how much gold you found, Player {}".format(self.player_id+1))
        elif event_type == EVENT_MONSTER_FIGHT:
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
        centre_screen.fill(BACKGROUND_COLOUR)

        # set up textbox for rolling dice
        dice_roll_textbox = self.get_dice_roll_textbox(event_type)
        centre_of_centre = dice_roll_textbox.get_centre_surface(centre_screen)
        dice_roll_textbox.draw(centre_of_centre)

        # dice rolling loop
        while True:
            DEBUG.log("Waiting for player to roll dice", DEBUG.LEVEL3)
            events = pg.event.get()
            dice_roll_textbox.update(events)
            pg.display.flip()

            for event in events:
                if event.type == pg.MOUSEBUTTONUP:
                    DEBUG.log("Mouse pressed to roll dice", DEBUG.LEVEL2)
                    return self.get_dice_number()

    def draw_token(self, screen, tile):
        screen.blit(self.token_image, (tile.x_pos + self.relative_x, tile.y_pos + self.relative_y))

    def invoke_tile_action(self, centre_screen, tile_value):
        tile_type = tile_value[TILE_TYPE]
        if tile_type is TILE_GOLD and not SKIP_GOLD_GET:
            self.process_action_gold_get(centre_screen, tile_value[TILE_GOLD_MULTIPLIER])
        elif tile_type is TILE_MONSTER and not SKIP_MONSTER_FIGHT:
            self.process_action_monster(centre_screen, tile_value[TILE_DATA])
        elif tile_type is TILE_HEAL and not SKIP_HEAL:
            self.process_action_heal(centre_screen, tile_value[TILE_HEAL_AMOUNT])
        elif tile_type is TILE_RESPAWN and not SKIP_RESPAWN:
            self.process_action_respawn(centre_screen, self.position)
        elif tile_type is TILE_SHOP and not SKIP_SHOP:
            self.process_action_shop(centre_screen, tile_value[TILE_DATA])
        else:
            raise TypeError("Undefined type of tile!")

    @staticmethod
    def show_textbox_at_centre(centre_screen, prompt, time):
        centre_screen.fill(BACKGROUND_COLOUR)
        textbox = eztext.Input(
            font=pg.font.Font(None, 30),
            color=BLACK,
            maxlength=0,
            prompt=prompt,
            x=0,
            y=0,
        )
        textbox.draw(textbox.get_centre_surface(centre_screen))
        textbox.update(pg.event.get())
        pg.display.flip()
        pg.time.delay(time)

    def process_action_gold_get(self, centre_screen, gold_multiplier):
        dice_result = self.roll_dice(centre_screen, EVENT_GOLD)
        amount_got = dice_result * gold_multiplier
        self.gold += amount_got
        Player.show_textbox_at_centre(
            centre_screen,
            "Player {} found {} gold and now has {} gold!".format(self.player_id+1, amount_got, self.gold),
            1000)

    def process_action_monster(self, centre_screen, data):
        pass

    def process_action_heal(self, centre_screen, amount):
        self.current_health = min(self.current_health+amount, self.full_health)
        Player.show_textbox_at_centre(
            centre_screen,
            "Player {} gets treated! HP:{}/{}".format(self.player_id+1, self.current_health, self.full_health),
            1000
        )

    def process_action_respawn(self, centre_screen, position):
        self.respawn_pos = position
        Player.show_textbox_at_centre(
            centre_screen,
            "Player {} marks the respawn point here!".format(self.player_id+1),
            1000
        )

    def process_action_shop(self, centre_screen, data):
        pass