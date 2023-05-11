import numpy as np
import pygame as pg
from player import Player

class Enemy:
    def __init__( self, x, y, screen, player: Player ):
        self.img = pg.transform.scale( pg.image.load( 'assets/tank.png' ), ( 32, 32 ) )
        self.screen = screen
        self.player = player
        self.angle = 180.0
        self.draw_angle = 180
        self.position = np.array( [ x, y ] )
        self.delta = ( self.player.position - self.position ) / np.linalg.norm( self.player.position - self.position )
        self.aim = np.array( [ np.cos(self.angle), np.sin(self.angle) ] )
        self.dot = np.dot( self.delta, self.aim )
        self.aim_rect = pg.Rect( self.position[0] + 100 * self.aim[0], self.position[1] + 100 * self.aim[1], 10, 10 )
        self.delta_rect = pg.Rect( self.position[0] + 100*self.delta[0], self.position[1] + 100*self.delta[1], 10, 10 )
        self.rotation_increment = 0.1
        self.direction = 1
        self.size = 32
        self.rect = pg.Rect( self.position, ( self.size, self.size ) )
        self.dead = False
        self.cooldown = 0.2
        
    def draw( self ):
        rotated = pg.transform.rotate( self.img, self.draw_angle )
        self.screen.blit( rotated, ( self.position[ 0 ], self.position[ 1 ] ) )
        pg.draw.rect( self.screen, [255,0,0], self.aim_rect )
        pg.draw.rect( self.screen, [0,0,255], self.delta_rect )

    def kill( self ):
        self.dead = True

    def correct_direction( self ):
        if self.dot > 0: return True
        else: return False

    def correct_aim( self ):
        if pg.Rect.colliderect( self.aim_rect, self.delta_rect ): return True
        else: return False

    def change_direction( self ):
        self.direction = self.direction * -1      
            
    def update( self ):
        self.draw_angle += self.rotation_increment * self.direction
        self.angle += self.rotation_increment * np.pi / 180 * self.direction
        self.aim = [ np.cos( self.angle ), np.sin( self.angle ) ]
        self.delta = ( self.player.position - self.position ) / np.linalg.norm( self.player.position - self.position )
        self.dot = np.dot( self.delta, self.aim )
        self.aim_rect = pg.Rect( self.position[0] + 100*self.aim[0], self.position[1] + 100*self.aim[1], 10, 10 )
        self.delta_rect = pg.Rect( self.position[0] + 100*self.delta[0], self.position[1] + 100*self.delta[1], 10, 10 )
    