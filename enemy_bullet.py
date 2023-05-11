import numpy as np
import pygame as pg
from enemy import Enemy

class Enemy_bullet:
    def __init__( self, screen, enemy: Enemy ):
        self.x = enemy.position[ 0 ] + 8
        self.y = enemy.position[ 1 ] + 8
        self.img = pg.transform.rotate(
                   pg.transform.scale(
                   pg.image.load( 'assets/bullet.png' ), ( 6, 6 ) ),
                   270 - enemy.angle )
        self.screen = screen
        self.position = np.array( [ self.x, self.y ] )
        self.delta = np.copy( enemy.delta ) / np.linalg.norm( enemy.delta )
        self.increment = 2

    def draw( self ):
        self.screen.blit( self.img, self.position )

    def get_rect( self ):
        return pg.Rect( self.position[ 0 ], self.position[ 1 ], 4, 4 )

