import numpy as np
import pygame as pg
import random as rn

class Carrier:
    def __init__( self, x, y, img, screen ):
        self.position = np.array( [ x, y ] )
        self.img = pg.transform.scale( pg.transform.rotate( img, rn.randint( 70, 110 ) ), ( 180, 180 ) )
        self.screen = screen
        self.hp = 2

    def draw( self ):
        self.screen.blit( self.img, self.position )