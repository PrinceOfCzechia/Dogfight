import numpy as np
import pygame as pg
from player import Player

class Bullet:
    def __init__( self, img, screen, player: Player ):
        self.x = player.position[ 0 ] + 8
        self.y = player.position[ 1 ] + 8
        self.img = pg.transform.rotate( img, 270 - player.angle )
        self.screen = screen
        self.position = np.array( [ self.x, self.y ] )
        self.delta = np.copy( player.delta ) / np.linalg.norm( player.delta )
        self.increment = 1.5
        self.hit = False

    def draw( self ):
        self.screen.blit( self.img, self.position )

    def get_rect( self ):
        return pg.Rect( self.position[ 0 ], self.position[ 1 ], 4, 4 )
