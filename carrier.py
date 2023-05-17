import numpy as np
import pygame as pg
import random as rn

class Carrier:
    def __init__( self, x, y, screen ):
        self.position = np.array( [ x, y ] )
        self.img = pg.transform.scale(
                   pg.transform.rotate(
                   pg.image.load( 'assets/aircraft-carrier.png' ), rn.randint( 80, 100 ) ),
                   ( 180, 180 ) )
        self.fire_img = pg.image.load( 'assets/fire.png' )
        self.screen = screen
        self.hp = 2
        self.rect = pg.Rect( x + 10, y + 55, 160, 70 )
        self.dead = False

    def draw( self ):
        self.screen.blit( self.img, self.position )
        # pg.draw.rect( self.screen, [255,0,0], self.rect )

    def draw_flames( self ):
        self.screen.blit( self.fire_img, self.position + [30,50] )
        self.screen.blit( self.fire_img, self.position + [50,70] )
        self.screen.blit( self.fire_img, self.position + [70,50] )
        self.screen.blit( self.fire_img, self.position + [90,70] )
        self.screen.blit( self.fire_img, self.position + [100,75] )
        self.screen.blit( self.fire_img, self.position + [120,50] )
        self.screen.blit( self.fire_img, self.position + [140,70] )
