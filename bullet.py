import numpy as np
import pygame as pg
from player import Player

class Bullet:
    def __init__( self, img, screen, player: Player ):
        self.x = player.x + 8
        self.y = player.y + 8
        self.angle = 270 - player.angle
        self.img = pg.transform.rotate( img, self.angle )
        self.screen = screen
        self.position = np.array( [ self.x, self.y ] )
        self.delta = np.copy( player.delta ) / np.linalg.norm( player.delta )
        self.increment = 0.5
        self.hit = False

    def draw( self ):
        self.screen.blit( self.img, self.position )