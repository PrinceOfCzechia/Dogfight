import numpy as np
import pygame as pg
from player import Player

class Bomb:
    def __init__( self, img, screen, player: Player ):
        self.img = pg.transform.rotate( img, 135 - player.angle )
        self.screen = screen
        self.player = player
        self.delta = np.copy( player.delta ) / 2
        self.position = np.copy( player.position )
        self.destination = self.position + ( self.delta * 1 )

    def draw( self ):
        self.screen.blit( self.img, self.position )