__author__ = 'San Lee'

import pygame as pg
import random
import os
import sys

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
        self.died_position = 0
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
        self.exp = 0

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
        pg.display.update(pg.Rect(TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH-2*TILE_WIDTH, WINDOW_HEIGHT-2*TILE_HEIGHT))

        # dice rolling loop
        while True:
            DEBUG.log("Waiting for player to roll dice", level=3)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONUP:
                    DEBUG.log("Mouse pressed to roll dice", level=2)
                    return self.get_dice_number()

    def draw_token(self, screen, tile):
        screen.blit(self.token_image, (tile.x_pos + self.relative_x, tile.y_pos + self.relative_y))

    def invoke_tile_action(self, centre_screen, tile_value):
        tile_type = tile_value[TILE_TYPE]
        if tile_type is TILE_GOLD:
            if SKIP_GOLD_GET:
                return
            result = self.process_action_gold_get(centre_screen, tile_value[TILE_GOLD_MULTIPLIER])
        elif tile_type is TILE_MONSTER:
            if SKIP_MONSTER_FIGHT:
                return
            result = self.process_action_monster(centre_screen, tile_value[TILE_DATA])
        elif tile_type is TILE_HEAL:
            if SKIP_HEAL:
                return
            result = self.process_action_heal(centre_screen, tile_value[TILE_HEAL_AMOUNT])
        elif tile_type is TILE_RESPAWN:
            if SKIP_RESPAWN:
                return
            result = self.process_action_respawn(centre_screen, self.position)
        elif tile_type is TILE_SHOP:
            if SKIP_SHOP:
                return
            result = self.process_action_shop(centre_screen, tile_value[TILE_DATA])
        else:
            raise TypeError("Undefined type of tile!")
        return result

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
        return ACTION_RESULT_GOLD_GET

    def process_action_monster(self, centre_screen, data):
        fight_condition_num = self.roll_dice(centre_screen, EVENT_MONSTER_FIGHT)

        card_surface = self.draw_monster_card(centre_screen, data)

        fight_scene_surface = centre_screen.subsurface((card_surface.get_width(), 0), card_surface.get_size())
        return self.process_monster_fight(fight_scene_surface, data, fight_condition_num)

    def process_action_heal(self, centre_screen, amount):
        self.current_health = min(self.current_health+amount, self.full_health)
        Player.show_textbox_at_centre(
            centre_screen,
            "Player {} gets treated! HP:{}/{}".format(self.player_id+1, self.current_health, self.full_health),
            1000
        )
        return ACTION_RESULT_HEAL

    def process_action_respawn(self, centre_screen, position):
        self.respawn_pos = position
        Player.show_textbox_at_centre(
            centre_screen,
            "Player {} marks the respawn point here!".format(self.player_id+1),
            1000
        )
        return ACTION_RESULT_RESPAWN

    def process_action_shop(self, centre_screen, data):
        pass

    def draw_monster_card(self, centre_screen, data):
        """
        :param centre_screen: screen excluding the tiles area
        :param data: monster's data
        :return: the surface that the card is drawn
        """
        centre_screen.fill(BACKGROUND_COLOUR)
        try:
            image = pg.image.load(os.path.join(MONSTER_IMG_FILE_PATH, data[MONSTER_IMG_FILE]))
        except RuntimeError as e:
            DEBUG.log(e, level=1)
            image = pg.image.load('smile.png')
        image = pg.transform.scale(image, (centre_screen.get_height(), centre_screen.get_height()))
        DEBUG.log("received image, image={}".format(image), level=3)

        card_surface = centre_screen.subsurface(0, 0, image.get_height(), image.get_height())
        card_surface.blit(image, (0, 0))

        monster_level_textbox = eztext.Input(
            font=pg.font.Font(None, 40),
            maxlength=0,
            prompt="Lv.{}".format(data[MONSTER_LEVEL]),
            x=10, y=10,
        )
        monster_level_textbox.draw(card_surface)

        monster_hp_textbox = eztext.Input(
            font=pg.font.Font(None, 40),
            maxlength=0,
            prompt="HP:{}".format(data[MONSTER_HEALTH]),
            x=10, y=10+monster_level_textbox.get_size()[1],
        )
        monster_hp_textbox.draw(card_surface)

        monster_attack_textbox = eztext.Input(
            font=pg.font.Font(None, 40),
            maxlength=0,
            prompt="ATT:{}".format(data[MONSTER_ATTACK]),
            x=10, y=10+monster_level_textbox.get_size()[1]+monster_hp_textbox.get_size()[1],
        )
        monster_attack_textbox.draw(card_surface)

        monster_defence_textbox = eztext.Input(
            font=pg.font.Font(None, 40),
            maxlength=0,
            prompt="DEF:{}".format(data[MONSTER_DEFENCE]),
            x=10, y=10+monster_level_textbox.get_size()[1]+monster_hp_textbox.get_size()[1]+monster_attack_textbox.get_size()[1],
        )
        monster_defence_textbox.draw(card_surface)

        pg.display.flip()
        return card_surface

    def process_monster_fight(self, fight_scene_surface, data, fight_condition_num):
        monster_fight_scene_textbox = eztext.Input(
            font=pg.font.Font(None, 25),
            maxlength=0,
        )
        monster_current_hp = data[MONSTER_HEALTH]
        # monster attacks first
        MONSTER_TURN = 0
        PLAYER_TURN = 1

        turn = 0
        while True:
            fight_scene_surface.fill(BACKGROUND_COLOUR)
            monster_fight_scene_textbox.set_prompt("Player {}:{}/{}, {}:{}/{}".format(
                self.player_id+1, max(self.current_health, 0), self.full_health,
                data[MONSTER_NAME], max(monster_current_hp, 0), data[MONSTER_HEALTH]
            ))
            monster_fight_scene_textbox.draw(fight_scene_surface)
            pg.display.flip()
            DEBUG.log("Fighting with monster, Player {}:{}/{}    {}:{}/{}".format(
                self.player_id+1, max(self.current_health, 0), self.full_health,
                data[MONSTER_NAME], max(monster_current_hp, 0), data[MONSTER_HEALTH]), level=2)
            pg.time.delay(300)

            if self.current_health <= 0:
                return self.die(fight_scene_surface)
            elif monster_current_hp <= 0:
                return self.win(fight_scene_surface, data)

            if turn % 2 == MONSTER_TURN:
                self.current_health -= (data[MONSTER_ATTACK] - self.current_defence)
            elif turn % 2 == PLAYER_TURN:
                monster_current_hp -= (int(self.current_attack*(9+fight_condition_num)/10) - data[MONSTER_DEFENCE])

            turn += 1

    def die(self, fight_scene_surface):
        msg = "Player {} died!".format(self.player_id+1)
        self.show_textbox_at_centre(fight_scene_surface, msg, 2000)

        self.died_position = self.position
        self.position = self.respawn_pos

        return ACTION_RESULT_DIE

    def win(self, fight_scene_surface, data):
        msg = "Player {} has gained {} exp and {} gold!"\
            .format(self.player_id+1, 10*data[MONSTER_LEVEL], 10*data[MONSTER_LEVEL])
        self.show_textbox_at_centre(fight_scene_surface, msg, 2000)

        # For now, loot is 10*(monster's level)
        self.exp += 10*data[MONSTER_LEVEL]
        self.gold += 10*data[MONSTER_LEVEL]

        return ACTION_RESULT_WIN