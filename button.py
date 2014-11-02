import pygame as pg
from pygame.locals import *
from colour import *
from debugger import Debugger as DEBUG


class Button(object):
    """
    Button class
    reference: http://inventwithpython.com/blog/2012/10/30/creating-a-button-ui-module-for-pygame/
    """
    def __init__(self, screen, pos, text, text_size=14, rect=None, colour=GRAY, click_colour=WHITE, border=BLACK, pos_offset=(0,0)):
        if rect is None:
            self._rect = pg.Rect(0, 0, 120, 40)
        else:
            self._rect = pg.Rect(rect)
            
        self._screen = screen
        self.text = text
        self._colour = colour
        self._click_colour = click_colour
        self._visible = True
        self._border = border
        self._mouseDown = False
        self._pos = pos
        self._pos_offset = pos_offset
        
        pg.font.init()
        self._font = pg.font.Font('freesansbold.ttf', text_size)
        
        # state of the button
        self.buttonPressed = False
        self.mouseOver = False
        self.lastPressed = False
        
        # adjust the position so that pos is the centre of button
        self._topLeft = (pos[0]-int(self._rect.width/2), pos[1]-int(self._rect.height/2))
        
        # surface of the text button
        self.surfaceNormal = self._screen.subsurface(self._topLeft + (self._rect.width, self._rect.height))
        self.surfaceDown = self._screen.subsurface(self._topLeft + (self._rect.width, self._rect.height))
        self.surfaceHighlight = self._screen.subsurface(self._topLeft + (self._rect.width, self._rect.height))

    def insert_picture(self, pos, filepath):
        image = pg.image.load(filepath)
        image = pg.transform.scale(image, (self._rect.height, self._rect.height))
        self.surfaceNormal.blit(image, pos)
    
    def update(self):
        w = self._rect.width
        h = self._rect.height
        
        # fill background color for all buttons
        if self.buttonPressed:
            self.surfaceDown.fill(self._click_colour)
        else:
            self.surfaceNormal.fill(self._colour)
        #self.surfaceHighlight.fill(self._colour)
        
        #draw text for all buttons
        text_surf = self._font.render(self.text, True, BLACK)
        
        text_rect = text_surf.get_rect()
        text_rect.center = int(w/2), int(h/2)
        self.surfaceNormal.blit(text_surf, text_rect)
        self.surfaceDown.blit(text_surf, text_rect)
        
        #draw rect for normal
        pg.draw.rect(self.surfaceNormal, self._border, pg.Rect((0,0,w,h)), 1)
        
    def update_state(self, eventObj):
        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
            return
        
        if eventObj.type == pg.MOUSEBUTTONDOWN:
            self._mouseDown = True
        if eventObj.type == pg.MOUSEBUTTONUP and self._mouseDown:
            mouse_pos = pg.mouse.get_pos()
            if self._topLeft[0] <= mouse_pos[0]-self._pos_offset[0] <= self._topLeft[0]+self._rect.width \
               and self._topLeft[1] <= mouse_pos[1]-self._pos_offset[1] <= self._topLeft[1]+self._rect.height:
                DEBUG.log("Button {} pressed".format(self.text), level=3)
                self.buttonPressed = True