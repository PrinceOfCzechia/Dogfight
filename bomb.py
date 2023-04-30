import numpy as np
import pygame as pg
from player import Player

class Bomb:
    def __init__( self, screen, player: Player ):
        self.img = pg.transform.rotate( pg.image.load( 'assets/bomb.png' ), 135 - player.angle )
        self.screen = screen
        self.player = player
        self.period = 0
        self.delta = np.copy( player.delta ) / ( np.sqrt( self.period + 1 ) )
        self.position = np.copy( player.position )

    def draw( self ):
        self.screen.blit( self.img, self.position )