import numpy as np
import pygame as pg
import random as rn

class Zeppelin():
    def __init__( self, x, y, img, screen ):
        self.x = x
        self.y = y
        self.angle = rn.randint( 0, 359 )
        self.position = np.array( [ self.x, self.y ] )
        self.img = img
        self.screen = screen
        self.hp = 5
        self.dead = False

    def draw( self ):
        rotated = pg.transform.rotate( self.img, self.angle )
        self.screen.blit( rotated, self.position )

    def hit( self ):
        if self.hp > 0: self.hp -= 1
        else: self.dead = True

