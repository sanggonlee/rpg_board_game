__author__ = 'San Lee'

import pygame as pg
import random
import os
import sys

from colour import BLACK, GRAY
from data import *
import eztext
from button import Button

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
        self.player_name = "Player {}".format(self.player_id+1)

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

        self.level = 1
        self.weapon = None
        self.armor = None
        self.inventory = [None, None, None, None, None]
        self.gold = 500
        self.exp = 0

        self.full_health = health
        self.base_attack = 10
        self.base_defence = 0

        self.current_health = self.full_health
        self.current_attack = self.base_attack
        self.current_defence = self.base_defence

        self.action_result = ACTION_RESULT_INVALID

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
        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))

        # dice rolling loop
        while True:
            DEBUG.log("Waiting for player to roll dice", level=3)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    DEBUG.log("Mouse pressed to roll dice", level=2)
                    return self.get_dice_number()
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    DEBUG.log("Pressed enter to show status", level=2)
                    self.show_status(centre_screen)

                    # go back to dice roll / status show UI
                    dice_roll_textbox.draw(centre_of_centre)
                    pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))

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
            result = self.process_action_monster(centre_screen, tile_value[TILE_MONSTER_DATA])
        elif tile_type is TILE_HEAL:
            if SKIP_HEAL:
                return
            result = self.process_action_heal(centre_screen, tile_value[TILE_HEAL_AMOUNT])
        elif tile_type is TILE_RESPAWN:
            if SKIP_RESPAWN:
                return
            result = self.process_action_respawn(centre_screen, self.position)
        elif tile_type is TILE_WEAPON_SHOP or tile_type is TILE_ARMOR_SHOP:
            if SKIP_SHOP:
                return
            result = self.process_action_shop(centre_screen, tile_value)
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
        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))
        pg.time.delay(time)

    def process_action_gold_get(self, centre_screen, gold_multiplier):
        dice_result = self.roll_dice(centre_screen, EVENT_GOLD)
        amount_got = dice_result * gold_multiplier
        self.gold += amount_got
        Player.show_textbox_at_centre(
            centre_screen,
            "Player {} found {} gold and now has {} gold!".format(self.player_id+1, amount_got, self.gold),
            1000)
        self.action_result = ACTION_RESULT_GOLD_GET
        return self.action_result

    def process_action_monster(self, centre_screen, data):
        fight_condition_num = self.roll_dice(centre_screen, EVENT_MONSTER_FIGHT)

        card_surface = self.draw_monster_card(centre_screen, data)

        fight_scene_surface = centre_screen.subsurface((card_surface.get_width(), 0), card_surface.get_size())
        self.process_monster_fight(fight_scene_surface, data, fight_condition_num)
        return self.action_result

    def process_action_heal(self, centre_screen, amount):
        self.current_health = min(self.current_health+amount, self.full_health)
        Player.show_textbox_at_centre(
            centre_screen,
            "Player {} gets treated! HP:{}/{}".format(self.player_id+1, self.current_health, self.full_health),
            1000
        )
        self.action_result = ACTION_RESULT_HEAL
        return self.action_result

    def process_action_respawn(self, centre_screen, position):
        self.respawn_pos = position
        Player.show_textbox_at_centre(
            centre_screen,
            "Player {} marks the respawn point here!".format(self.player_id+1),
            1000
        )
        self.action_result = ACTION_RESULT_RESPAWN
        return self.action_result

    def process_action_shop(self, centre_screen, tile_value):
        self.shop_initial_dialog(centre_screen, tile_value)
        return self.action_result

    @staticmethod
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

        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))
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
                self.die(fight_scene_surface)
            elif monster_current_hp <= 0:
                self.win(fight_scene_surface, data)

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

        self.action_result = ACTION_RESULT_DIE

    def win(self, fight_scene_surface, data):
        msg = "Player {} has gained {} exp and {} gold!"\
            .format(self.player_id+1, 10*data[MONSTER_LEVEL], 10*data[MONSTER_LEVEL])
        self.show_textbox_at_centre(fight_scene_surface, msg, 2000)

        # For now, loot is 10*(monster's level)
        self.exp += 10*data[MONSTER_LEVEL]
        self.gold += 10*data[MONSTER_LEVEL]

        self.action_result = ACTION_RESULT_WIN

    def shop_initial_dialog(self, centre_screen, tile_value):
        centre_screen.fill(BACKGROUND_COLOUR)

        button_rect = pg.Rect(0, 0, 240, 60)
        buy_button = Button(
            centre_screen,
            (centre_screen.get_width()/2, centre_screen.get_height()/2 - button_rect.height),
            "Buy", 20, rect=button_rect, pos_offset=(TILE_WIDTH, TILE_HEIGHT))
        sell_button = Button(
            centre_screen,
            (centre_screen.get_width()/2, centre_screen.get_height()/2),
            "Sell", 20, rect=button_rect, pos_offset=(TILE_WIDTH, TILE_HEIGHT))
        leave_button = Button(
            centre_screen, (centre_screen.get_width()/2, centre_screen.get_height()/2 + button_rect.height),
            "Leave", 20, rect=button_rect, pos_offset=(TILE_WIDTH, TILE_HEIGHT))
        buy_button.update()
        sell_button.update()
        leave_button.update()
        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                buy_button.update_state(event)
                sell_button.update_state(event)
                leave_button.update_state(event)

            if buy_button.buttonPressed:
                DEBUG.log("Buy button pressed", level=2)
                centre_screen.fill(BACKGROUND_COLOUR)
                self.shop_action_buy(centre_screen, tile_value)
                break
            elif sell_button.buttonPressed:
                DEBUG.log("Sell button pressed", level=2)
                centre_screen.fill(BACKGROUND_COLOUR)
                self.shop_action_sell(centre_screen)
                break
            elif leave_button.buttonPressed:
                DEBUG.log("Leave button pressed", level=2)
                self.action_result = ACTION_RESULT_SHOP_LEAVE
                # escape recursion if leaving
                return

        # recursive process for buying/selling
        self.shop_initial_dialog(centre_screen, tile_value)

    def shop_action_buy(self, centre_screen, tile_value):
        shop_type = tile_value[TILE_ITEM_TYPE]
        data = tile_value[TILE_ITEM_DATA]

        item_count = len(data) + 1  # last item is "Cancel" button
        DEBUG.log("Number of items in this shop: {}".format(item_count-1), level=1)
        button_rect = pg.Rect(0, 0, 300, 40)

        centre_screen.fill(BACKGROUND_COLOUR)
        item_button_list = []
        for item_index in range(item_count):
            y_pos = centre_screen.get_height()/2 - ((item_count/2-item_index) * button_rect.height)
            if item_index == item_count-1:
                item_name = "Cancel"
            else:
                item_name = data[item_index][ITEM_NAME]
                if shop_type is TILE_WEAPON_SHOP:
                    item_name += "   ATT:" + str(data[item_index][ITEM_POINT])
                elif shop_type is TILE_ARMOR_SHOP:
                    item_name += "   DEF:" + str(data[item_index][ITEM_POINT])
                item_name += "    " + str(data[item_index][ITEM_PRICE]) + "G"
            DEBUG.log("Item name: {}".format(item_name), level=2)
            item_button = Button(
                centre_screen, (centre_screen.get_width()/2, y_pos),
                item_name, 14, rect=button_rect, pos_offset=(TILE_WIDTH, TILE_HEIGHT))
            if item_name != "Cancel":
                try:
                    item_button.insert_picture((0, 0), os.path.join(ITEM_IMG_FILE_PATH, data[item_index][ITEM_FILENAME]))
                except RuntimeError as e:
                    DEBUG.log(e, level=1)
                    item_button.insert_picture((0, 0), 'smile.png')

            item_button.update()
            item_button_list.append(item_button)
        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                for button in item_button_list:
                    button.update_state(event)

            bought_item = None
            for button_index in range(len(item_button_list)):
                if item_button_list[button_index].buttonPressed:
                    DEBUG.log("{}'th button pressed".format(button_index+1), level=2)
                    if item_button_list[button_index].text == "Cancel":
                        DEBUG.log("Cancel clicked", level=2)
                        return
                    else:
                        bought_item = data[button_index]
                        DEBUG.log("Item {} clicked".format(bought_item[ITEM_NAME]), level=2)
                        break
            if bought_item:
                if bought_item[ITEM_PRICE] >= self.gold:
                    DEBUG.log("Item too expensive.", level=1)
                    self.show_textbox_at_centre(
                        centre_screen, "You don't have enough gold.", 1500)
                    self.shop_action_buy(centre_screen, data)
                elif shop_type is TILE_WEAPON_SHOP:
                    DEBUG.log("Buying weapon", level=1)
                    if self.weapon:
                        DEBUG.log("Already have weapon", level=2)
                        self.show_textbox_at_centre(
                            centre_screen, "You're already equipping a weapon. Sell it first.", 1500)
                        # recursion to go back to buy menu
                        self.shop_action_buy(centre_screen, tile_value)
                    else:
                        DEBUG.log("Bought weapon {}".format(bought_item[ITEM_NAME]))
                        self.weapon = bought_item
                        self.current_attack += bought_item[ITEM_POINT]
                        self.gold -= bought_item[ITEM_PRICE]
                        self.show_textbox_at_centre(
                            centre_screen, "You purchased {}!".format(bought_item[ITEM_NAME]), 1500)

                        self.action_result = ACTION_RESULT_SHOP_BUY
                elif shop_type is TILE_ARMOR_SHOP:
                    DEBUG.log("Buying armor", level=1)
                    if self.armor:
                        DEBUG.log("Already have armor", level=2)
                        self.show_textbox_at_centre(
                            centre_screen, "You're already equipping an armor. Sell it first.", 1500)
                        # recursion to go back to buy menu
                        self.shop_action_buy(centre_screen, tile_value)
                    else:
                        DEBUG.log("Bought weapon {}".format(bought_item[ITEM_NAME]))
                        self.armor = bought_item
                        self.current_defence += bought_item[ITEM_POINT]
                        self.gold -= bought_item[ITEM_PRICE]
                        self.show_textbox_at_centre(
                            centre_screen, "You purchased {}!".format(bought_item[ITEM_NAME]), 1500)

                        self.action_result = ACTION_RESULT_SHOP_BUY
                else:
                    raise TypeError("Invalid type of item")
                return

    def shop_action_sell(self, centre_screen):
        item_count = len(self.inventory) + 3  # weapon, armor, inventory, and cancel
        DEBUG.log("Number of items to sell: {}".format(item_count-1), level=1)
        button_rect = pg.Rect(0, 0, 300, 40)

        centre_screen.fill(BACKGROUND_COLOUR)
        item_button_list = []
        for item_index in range(item_count):
            y_pos = centre_screen.get_height()/2 - ((item_count/2-item_index) * button_rect.height)
            if item_index == item_count-1:
                item_name = "Cancel"
            elif item_index == 0:  # weapon
                if not self.weapon:
                    item_name = "Empty"
                else:
                    item_name = self.weapon[ITEM_NAME]
                    item_name += "   ATT:" + str(self.weapon[ITEM_POINT])
                    item_name += "    " + str(self.weapon[ITEM_PRICE]/4) + "G"
            elif item_index == 1:
                if not self.armor:
                    item_name = "Empty"
                else:
                    item_name = self.armor[ITEM_NAME]
                    item_name += "   DEF:" + str(self.armor[ITEM_POINT])
                    item_name += "    " + str(self.armor[ITEM_PRICE]/4) + "G"
            else:
                if not self.inventory[item_index-2]:
                    item_name = "Empty"
                else:
                    item_name = self.inventory[item_index-2][ITEM_NAME]
                    item_name += "    " + str(self.inventory[item_index-2][ITEM_PRICE]/4) + "G"
            DEBUG.log("Item name: {}".format(item_name), level=2)
            item_button = Button(
                centre_screen, (centre_screen.get_width()/2, y_pos),
                item_name, 14, rect=button_rect, pos_offset=(TILE_WIDTH, TILE_HEIGHT))
            if item_name is not "Cancel" and item_name is not "Empty":
                try:
                    if item_index == 0:
                        item_button.insert_picture((0, 0), os.path.join(ITEM_IMG_FILE_PATH, self.weapon[ITEM_FILENAME]))
                    elif item_index == 1:
                        item_button.insert_picture((0, 0), os.path.join(ITEM_IMG_FILE_PATH, self.armor[ITEM_FILENAME]))
                except RuntimeError as e:
                    DEBUG.log(e, level=1)
                    item_button.insert_picture((0, 0), 'smile.png')

            item_button.update()
            item_button_list.append(item_button)
        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                for button in item_button_list:
                    button.update_state(event)

            sold_item = None
            for button_index in range(len(item_button_list)):
                if item_button_list[button_index].buttonPressed:
                    DEBUG.log("{}'th button pressed".format(button_index+1), level=2)
                    if item_button_list[button_index].text == "Cancel":
                        DEBUG.log("Cancel clicked", level=2)
                        return
                    elif button_index == 0 and self.weapon:
                        sold_item = self.weapon
                        DEBUG.log("Item {} clicked".format(sold_item[ITEM_NAME]), level=2)
                        break
                    elif button_index == 1 and self.armor:
                        sold_item = self.armor
                        DEBUG.log("Item {} clicked".format(sold_item[ITEM_NAME]), level=2)
                        break
                    else:
                        #TODO: Implement other items
                        pass

            if sold_item:
                if sold_item is self.weapon:
                    DEBUG.log("Selling weapon {}".format(sold_item[ITEM_NAME]))
                    self.weapon = None
                    self.current_attack -= sold_item[ITEM_POINT]
                elif sold_item is self.armor:
                    DEBUG.log("Selling armor {}".format(sold_item[ITEM_NAME]))
                    self.armor = None
                    self.current_defence -= sold_item[ITEM_POINT]

                self.gold += sold_item[ITEM_PRICE]/4
                self.show_textbox_at_centre(
                    centre_screen, "You sold {}!".format(sold_item[ITEM_NAME]), 1500)

                self.action_result = ACTION_RESULT_SHOP_SELL
                return

    def show_status(self, centre_screen):
        centre_screen.fill(BACKGROUND_COLOUR)

        status_rect = pg.Rect(
            centre_screen.get_width()/3,
            centre_screen.get_height()/16,
            centre_screen.get_width()/3,
            centre_screen.get_height()*7/8
        )
        status_surface = centre_screen.subsurface(status_rect)
        status_surface.fill(GRAY)

        token_image = pg.transform.scale(self.token_image, (status_rect.width/3, status_rect.width/3))
        status_surface.blit(token_image, (status_rect.width/3, status_rect.height/12))

        current_height = 50+token_image.get_height()
        name_text_surf = pg.font.Font('freesansbold.ttf', 15)\
            .render(self.player_name, True, BLACK)
        status_surface.blit(name_text_surf, name_text_surf.get_rect().move(
            10, current_height))

        current_height += name_text_surf.get_height()+10
        level_text_surf = pg.font.Font('freesansbold.ttf', 15)\
            .render("Lv: {}".format(self.level), True, BLACK)
        status_surface.blit(level_text_surf, level_text_surf.get_rect().move(
            10, current_height))

        current_height += level_text_surf.get_height()+10
        health_text_surf = pg.font.Font('freesansbold.ttf', 15)\
            .render("HP: {}/{}".format(self.current_health, self.full_health), True, BLACK)
        status_surface.blit(health_text_surf, health_text_surf.get_rect().move(
            10, current_height))

        current_height += health_text_surf.get_height()+10
        attack_text_surf = pg.font.Font('freesansbold.ttf', 15)\
            .render("ATT: {} + {}".format(self.base_attack, self.current_attack-self.base_attack), True, BLACK)
        status_surface.blit(attack_text_surf, attack_text_surf.get_rect().move(
            10, current_height))

        current_height += attack_text_surf.get_height()+10
        defence_text_surf = pg.font.Font('freesansbold.ttf', 15)\
            .render("DEF: {} + {}".format(self.base_defence, self.current_defence-self.base_defence), True, BLACK)
        status_surface.blit(defence_text_surf, defence_text_surf.get_rect().move(
            10, current_height))

        current_height += defence_text_surf.get_height()+10
        weapon_text_surf = pg.font.Font('freesansbold.ttf', 15)\
            .render("Weapon: {}".format(self.weapon[ITEM_NAME] if self.weapon else "None"), True, BLACK)
        status_surface.blit(weapon_text_surf, weapon_text_surf.get_rect().move(
            10, current_height))

        current_height += weapon_text_surf.get_height()+10
        armor_text_surf = pg.font.Font('freesansbold.ttf', 15)\
            .render("Armor: {}".format(self.armor[ITEM_NAME] if self.armor else "None"), True, BLACK)
        status_surface.blit(armor_text_surf, armor_text_surf.get_rect().move(
            10, current_height))

        pg.display.update(centre_screen.get_rect(topleft=(TILE_WIDTH, TILE_HEIGHT)))

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN or (event.type == pg.KEYDOWN and event.key == pg.K_RETURN):
                    DEBUG.log("Exiting player status", level=2)
                    centre_screen.fill(BACKGROUND_COLOUR)
                    return
