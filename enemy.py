import numpy as np
import pygame as pg
from player import Player

class Enemy:
    def __init__( self, x, y, screen, player: Player ):
        self.img = pg.transform.scale( pg.image.load( 'assets/tank.png' ), ( 32, 32 ) )
        self.screen = screen
        self.player = player
        self.angle = 270.0
        self.position = np.array( [ x, y ] )
        self.delta = np.array( [ np.cos(self.angle), np.sin(self.angle) ] )
        self.rotation_increment = 0.05
        self.direction = 1
        self.size = 32
        self.rect = pg.Rect( self.position, ( self.size, self.size ) )
        self.dead = False
        
    def draw( self ):
        rot_angle = 90 - self.angle
        rotated = pg.transform.rotate( self.img, rot_angle )
        self.screen.blit( rotated, ( self.position[ 0 ], self.position[ 1 ] ) )

    def correctDirection( self ):
        if np.dot( self.player.delta, self.delta > 0 ): return True
        else: return False

    def kill( self ):
        self.dead = True

    def changeDirection( self ):
        self.direction = self.direction * -1

    def rotate( self ):
        self.angle += self.direction * self.rotation_increment
