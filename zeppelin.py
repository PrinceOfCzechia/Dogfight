import numpy as np
import pygame as pg
import random as rn

class Zeppelin():
    def __init__( self, screen, display_w, display_h, n, N ):
        self.x = rn.randint( int((display_w - 164 - 100) * n / N),
                             int((display_w - 164 - 100) * n / N + 100) )
        self.y = rn.randint( 100, display_h * 2 / 3 )
        self.angle = rn.randint( 0, 179 )
        self.img = pg.image.load( 'assets/zeppelin.png' )
        self.screen = screen
        if self.angle < 30 or self.angle > 150:
            self.rect = pg.Rect( self.x + 5, self.y + 20, 64, 40 )
        elif self.angle < 60 or self.angle > 120:
            self.rect = pg.Rect( self.x + 15, self.y + 15, 55, 55 )
        else:
            self.rect = pg.Rect( self.x + 20, self.y + 10, 40, 64 )
        self.hp = 4
        self.dead = False

    def draw( self ):
        rotated = pg.transform.rotate( self.img, self.angle )
        self.screen.blit( rotated, ( self.x,self.y ) )
        # uncomment to see self.rect
        # pg.draw.rect( self.screen, [255,0,0], self.rect )

    def hit( self ):
        if self.hp > 0: self.hp -= 1
        else: self.dead = True

    def kill( self ):
        self.dead = True
