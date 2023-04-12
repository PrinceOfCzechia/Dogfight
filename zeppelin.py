import numpy as np
import pygame as pg
import random as rn

class Zeppelin():
    def __init__( self, img, screen ):
        self.x = rn.randint( 100, 836 )
        self.y = rn.randint( 100, 236 )
        self.angle = rn.randint( 0, 359 )
        self.img = img
        self.screen = screen
        self.hp = 5
        self.dead = False

    def draw( self ):
        rotated = pg.transform.rotate( self.img, self.angle )
        self.screen.blit( rotated, ( self.x,self.y ) )

    def hit( self ):
        if self.hp > 0: self.hp -= 1
        else: self.dead = True
