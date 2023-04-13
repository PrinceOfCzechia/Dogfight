import numpy as np
import pygame as pg

class Player:
    def __init__( self, x, y, img, screen ):
        self.x = x
        self.y = y
        self.img = img
        self.screen = screen
        self.angle = 270.0
        self.position = np.array( [ self.x, self.y ] )
        self.speed = 0.3
        self.delta = np.array( [ np.cos(self.angle), np.sin(self.angle) ] ) * self.speed
        self.rotation = 0.0
        self.size = 32
        self.rect = pg.Rect( self.position, ( self.size, self.size ) )
        
    def draw( self ):
        rot_angle = 270 - self.angle
        rotated = pg.transform.rotate( self.img, rot_angle )
        self.screen.blit( rotated, ( self.x, self.y ) )

    def increment_speed( self ):
        if self.speed <= 0.45: self.speed += 0.05

    def decrement_speed( self ):
        if self.speed >= 0.25: self.speed -= 0.05

    def get_rotation_increment( self ):
        # TODO: make this a linear function
        if self.speed > 0.45: return 0.12
        if self.speed > 0.4: return 0.15
        if self.speed > 0.35: return 0.18
        if self.speed > 0.3: return 0.20
        if self.speed > 0.25: return 0.22
        if self.speed > 0.2: return 0.25
        else: return 0.30


