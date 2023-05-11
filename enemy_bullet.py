import numpy as np
import pygame as pg
from enemy import Enemy

class Enemy_bullet:
    def __init__( self, screen, enemy: Enemy ):
        self.x = enemy.center[ 0 ]
        self.y = enemy.center[ 1 ]
        self.img = pg.transform.rotate(
                   pg.transform.scale(
                   pg.image.load( 'assets/bullet.png' ), ( 10, 10 ) ),
                   enemy.draw_angle )
        self.screen = screen
        self.position = np.array( [ self.x, self.y ] )
        self.delta = np.copy( enemy.delta ) / np.linalg.norm( enemy.delta )
        self.increment = 1.5

    def draw( self ):
        self.screen.blit( self.img, self.position )
        # pg.draw.rect( self.screen, [255,0,0], self.get_rect() ) TODO remove when done

    def get_rect( self ):
        return pg.Rect( self.position[ 0 ], self.position[ 1 ], 5, 5 )

