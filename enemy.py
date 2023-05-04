import numpy as np
import pygame as pg
from player import Player

class Enemy:
    def __init__( self, x, y, screen, player: Player ):
        self.img = pg.transform.scale( pg.image.load( 'assets/tank.png' ), ( 32, 32 ) )
        self.screen = screen
        self.player = player
        self.angle = 180.0
        self.position = np.array( [ x, y ] )
        self.delta = self.position - self.player.position / np.linalg.norm( self.position - self.player.position )
        self.aim = np.array( [ np.cos(self.angle), np.sin(self.angle) ] )
        self.rotation_increment = 0.05
        self.direction = -1
        self.size = 32
        self.rect = pg.Rect( self.position, ( self.size, self.size ) )
        self.dead = False
        
    def draw( self ):
        rotated = pg.transform.rotate( self.img, self.angle )
        self.screen.blit( rotated, ( self.position[ 0 ], self.position[ 1 ] ) )

    def correct_direction( self ):
        if np.dot( self.aim, self.delta > 0 ): return True
        else: return False

    def kill( self ):
        self.dead = True

    def change_direction( self ):
        self.direction = self.direction * -1

    def rotate( self ):
        self.angle += self.direction * self.rotation_increment

    def update_aim( self ):
        self.aim = np.array( [ np.cos(self.angle), np.sin(self.angle) ] )
