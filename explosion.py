import numpy as np
import pygame as pg

class Explosion:
    def __init__( self, x, y, img, screen ):
        self.x = x
        self.y = y
        self.img = img
        self.screen = screen
        self.visible = True
        self.timer = 0
        self.duration = 150
        self.rect = pg.Rect( self.x + 2, self.y + 2, 60, 60 )

    def draw( self ):
        self.screen.blit( self.img, ( self.x, self.y ) )
        # uncomment to see self.rect
        # pg.draw.rect( self.screen, [255,0,0], self.rect )