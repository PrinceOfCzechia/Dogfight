import numpy as np
import pygame as pg
from player import Player

class Enemy:
    def __init__( self, x, y, screen, player: Player ):
        self.img = pg.transform.scale( pg.image.load( 'assets/tank.png' ), ( 32, 32 ) )
        self.screen = screen
        self.player = player
        self.angle = 180.0
        self.draw_angle = 180 / np.pi + 90
        self.position = np.array( [ x, y ] )
        self.center = np.array( [ x+16, y+16 ] )
        self.delta = ( self.player.position - self.center ) / np.linalg.norm( self.player.position - self.center )
        self.aim = np.array( [ np.cos(self.angle-90), np.sin(self.angle-90) ] )
        self.L_aim = np.array( [ np.cos(self.angle-90.1), np.sin(self.angle-90.1) ] )
        self.R_aim = np.array( [ np.cos(self.angle-89.9), np.sin(self.angle-89.9) ] )
        self.backward = -1 * self.aim
        self.aim_rect = pg.Rect( self.center[0] + 100 * self.aim[0], self.center[1] + 100 * self.aim[1], 10, 10 )
        self.L_rect = pg.Rect( self.center[0] + 100 * self.L_aim[0], self.center[1] + 100 * self.L_aim[1], 10, 10 )
        self.R_rect = pg.Rect( self.center[0] + 100 * self.R_aim[0], self.center[1] + 100 * self.R_aim[1], 10, 10 )
        self.delta_rect = pg.Rect( self.center[0] + 100*self.delta[0], self.center[1] + 100*self.delta[1], 10, 10 )
        self.backward_rect = pg.Rect( self.center[0] + 100 * self.backward[0],
                                      self.center[1] + 100 * self.backward[1],
                                      5, 5 )
        self.rotation_increment = 0.1
        self.direction = -1
        self.size = 32
        self.rect = pg.Rect( self.position, ( self.size, self.size ) )
        self.dead = False
        self.cooldown = 0.2
        self.backward_collision = False
        self.L_collision = False
        self.R_collision = False
        
    def draw( self ):
        rotated = pg.transform.rotate( self.img, self.draw_angle )
        self.screen.blit( rotated, ( self.position[ 0 ], self.position[ 1 ] ) )
        # pg.draw.rect( self.screen, [255,0,0], self.aim_rect )
        # pg.draw.rect( self.screen, [0,0,255], self.delta_rect )
        # pg.draw.rect( self.screen, [0,255,0], self.backward_rect )
        # pg.draw.rect( self.screen, [255,255,0], self.L_rect )
        # pg.draw.rect( self.screen, [255,0,255], self.R_rect )

    def kill( self ):
        self.dead = True

    def correct_aim( self ):
        if pg.Rect.colliderect( self.aim_rect, self.delta_rect ): return True
        else: return False

    def check_change( self ):
        if pg.Rect.colliderect( self.delta_rect, self.backward_rect ):
            self.backward_collision = True
        else:
            if self.backward_collision: self.change_direction()
            self.backward_collision = False
        if pg.Rect.colliderect( self.delta_rect, self.L_rect ):
            self.L_collision = True
        else:
            if self.L_collision and self.direction == 1: self.change_direction()
            self.L_collision = False
        if pg.Rect.colliderect( self.delta_rect, self.R_rect ):
            self.R_collision = True
        else:
            if self.R_collision and self.direction == -1: self.change_direction()
            self.R_collision = False

    def change_direction( self ):
        self.direction = self.direction * -1
            
    def update( self ):
        self.draw_angle -= self.rotation_increment * self.direction
        self.angle += self.rotation_increment * np.pi / 180 * self.direction
        self.aim = [ np.cos( self.angle-90 ), np.sin( self.angle-90 ) ]
        self.L_aim = [ np.cos(self.angle-90.1) , np.sin(self.angle-90.1) ]
        self.R_aim = [ np.cos(self.angle-89.9) , np.sin(self.angle-89.9) ]
        self.backward = [ -np.cos( self.angle-90 ), -np.sin( self.angle-90 ) ]
        self.delta = ( self.player.position - self.center ) / np.linalg.norm( self.player.position - self.center )
        self.aim_rect = pg.Rect( self.center[0] + 100*self.aim[0],
                                 self.center[1] + 100*self.aim[1],
                                 10, 10 )
        self.L_rect = pg.Rect( self.center[0] + 100 * self.L_aim[0],
                               self.center[1] + 100 * self.L_aim[1],
                               10, 10 )
        self.R_rect = pg.Rect( self.center[0] + 100 * self.R_aim[0],
                               self.center[1] + 100 * self.R_aim[1],
                               10, 10 )
        self.delta_rect = pg.Rect( self.center[0] + 100*self.delta[0],
                                   self.center[1] + 100*self.delta[1],
                                   10, 10 )
        self.backward_rect = pg.Rect( self.center[0] + 100 * self.backward[0],
                                      self.center[1] + 100 * self.backward[1],
                                      5, 5 )
