import numpy as np
import pygame as pg
import random as rn

class Zeppelin():
    def __init__( self, img, screen, display_w, display_h ):
        self.x = rn.randint( 100, display_w - 64 )
        self.y = rn.randint( 100, display_h - 564 )
        self.angle = rn.randint( 0, 359 )
        self.img = img
        self.screen = screen
        self.rect = pg.Rect( self.x + 5, self.y + 5, 54, 54 )
        self.hp = 4
        self.dead = False

    def draw( self ):
        rotated = pg.transform.rotate( self.img, self.angle )
        self.screen.blit( rotated, ( self.x,self.y ) )

    def hit( self ):
        if self.hp > 0: self.hp -= 1
        else: self.dead = True

    def kill( self ):
        self.dead = True
