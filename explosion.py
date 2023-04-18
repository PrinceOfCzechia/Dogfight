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
        self.size = 64
        self.rect = pg.Rect( self.x, self.y, self.size, self.size )

    def draw( self ):
        self.screen.blit( self.img, ( self.x, self.y ) )