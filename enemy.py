import numpy as np
import pygame as pg
from player import Player

class Enemy:
    def __init__( self, x, y, img, screen ):
        self.x = x
        self.y = y
        self.img = img
        self.screen = screen
        self.angle = 90.0
        self.position = np.array( [ self.x, self.y ] )
        self.speed = 0.2
        self.delta = np.array( [ np.cos(self.angle), np.sin(self.angle) ] ) * self.speed
        self.rotation = 0.1
        self.direction = 1
        self.size = 32
        self.rect = pg.Rect( self.position, ( self.size, self.size ) )
        self.max_hp = 5
        self.hp = self.max_hp
        self.dead = False
        
    def draw( self ):
        rot_angle = 90.0 - self.angle
        rotated = pg.transform.rotate( self.img, rot_angle )
        self.screen.blit( rotated, ( self.position[ 0 ], self.position[ 1 ] ) )

    def get_rect( self ):
        return pg.Rect( self.position, ( self.size - 2, self.size - 2 ) )

    def getDirection( self, player: Player ):
        return True
    
    def hit( self ):
        self.hp -= 1

    def kill( self ):
        self.dead = True


