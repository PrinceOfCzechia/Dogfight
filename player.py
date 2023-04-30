import numpy as np
import pygame as pg

class Player:
    def __init__( self, x, y, screen ):
        self.x = x
        self.y = y
        self.img = pg.transform.scale( pg.image.load( 'assets/plane.png' ), ( 32, 32 ) )
        self.screen = screen
        self.angle = 270.0
        self.position = np.array( [ self.x, self.y ] )
        self.speed = 0.6
        self.max_speed = 0.8
        self.min_speed = 0.4
        self.speed_increment = 0.05
        self.delta = np.array( [ np.cos(self.angle), np.sin(self.angle) ] ) * self.speed
        self.rotation = 0.0
        self.size = 32
        self.max_hp = 5
        self.hp = self.max_hp
        self.ammo = 100
        self.bomb_cap = 3
        
    def draw( self ):
        rot_angle = 270 - self.angle
        rotated = pg.transform.rotate( self.img, rot_angle )
        self.screen.blit( rotated, ( self.position[ 0 ], self.position[ 1 ] ) )

    def increment_speed( self ):
        if self.speed < self.max_speed: self.speed += self.speed_increment
        if self.speed > self.max_speed: self.speed = self.max_speed

    def decrement_speed( self ):
        if self.speed > self.min_speed: self.speed -= self.speed_increment
        if self.speed < self.min_speed: self.speed = self.min_speed

    def get_rotation_increment( self ):
        # TODO: make the magic numbers a function
        if self.speed > 0.75: return 0.15
        if self.speed > 0.7: return 0.18
        if self.speed > 0.65: return 0.21
        if self.speed > 0.6: return 0.24
        if self.speed > 0.55: return 0.27
        if self.speed > 0.5: return 0.30
        else: return 0.33

    def get_rect( self ):
        return pg.Rect( self.position, ( self.size - 4, self.size - 4 ) )
    
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
