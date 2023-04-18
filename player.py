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
        self.speed = 0.7
        self.delta = np.array( [ np.cos(self.angle), np.sin(self.angle) ] ) * self.speed
        self.rotation = 0.0
        self.size = 32
        self.max_hp = 3
        self.hp = self.max_hp
        
    def draw( self ):
        rot_angle = 270 - self.angle
        rotated = pg.transform.rotate( self.img, rot_angle )
        self.screen.blit( rotated, ( self.x, self.y ) )

    def increment_speed( self ):
        if self.speed <= 0.85: self.speed += 0.05

    def decrement_speed( self ):
        if self.speed > 0.50: self.speed -= 0.05

    def get_rotation_increment( self ):
        # TODO: make the magic numbers a function
        if self.speed > 0.65: return 0.50
        if self.speed > 0.6: return 0.55
        if self.speed > 0.55: return 0.60
        if self.speed > 0.5: return 0.65
        if self.speed > 0.45: return 0.70
        if self.speed > 0.4: return 0.75
        else: return 0.80

    def get_rect( self ):
        return pg.Rect( self.position, ( self.size - 2, self.size - 2 ) )
    
    def hit( self ):
        self.hp -= 1

    def big_hit( self ):
        self.hp -= 2

    def draw_hearts( self, full: pg.image, empty: pg.image, x_coordinate, y_coordinate ):
        for i in range( self.hp ):
            self.screen.blit( full, ( x_coordinate - 20 * i, y_coordinate ) )
        for i in range( self.max_hp - self.hp ):
            self.screen.blit( empty, ( x_coordinate - 20 * ( self.max_hp - 1 - i ), y_coordinate ) )

    def alive( self ):
        if self.hp > 0: return True
        else: return False
