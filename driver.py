import sys
import pygame as pg

from button import Button
import eztext
from game import Game

from colour import *
from constants import *

from debugger import Debugger as DEBUG

pg.init()

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen.fill(BACKGROUND_COLOUR)

startButton = Button(screen, (screen.get_width()/2, screen.get_height()*2/3), "Start game")
num_players_textbox = eztext.Input(
                restricted="234",
                color=BLACK,
                maxlength=1,
                prompt="Enter the number of human players who will play (2~{}):".format(MAX_NUM_PLAYERS))
num_human_players = 0

i = 0
while i < 6000:
    i += 1
        
    screen.fill(BACKGROUND_COLOUR)
    events = pg.event.get()

    # Check for quit button
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Initialize before starting game
    if startButton:
        startButton.update_state(event)
        startButton.update()
        if startButton.buttonPressed:
            del startButton
            startButton = None
    elif num_players_textbox:
        num_players_textbox.update(events)
        if not num_players_textbox.return_pressed:
            num_players_textbox.draw(screen)
        else:
            DEBUG.log("num_players_textbox returned", DEBUG.LEVEL1)
            num_human_players = int(num_players_textbox.value)
            num_players_textbox = None

            # Initialize and start the main game engine
            game = Game(screen, num_human_players, 0)
            game.start()
            break

    pg.display.update()

pg.quit()
sys.exit()