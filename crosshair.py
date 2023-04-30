import numpy as np
import pygame as pg
from player import Player

class Crosshair:
    def __init__( self, player: Player, screen ):
        self.player = player
        self.position = player.position + 150 * player.delta
        self.img = pg.image.load( 'assets/crosshair.png' )
        self.visible = False
        self.screen = screen

    def show( self ):
        self.visible = not self.visible

    def draw( self ):
        self.screen.blit( self.img, self.position )

    def update( self ):
        self.position = self.player.position + 150 * self.player.delta