import pygame as pg
import numpy as np
from typing import List
from player import Player
from bullet import Bullet
from zeppelin import Zeppelin
from explosion import Explosion

pg.init()

# environemnent
running = True
display_width = 1000
display_height = 700
score = 0
explosion_duration = 50
bullet_img = pg.image.load( 'assets/bullet.png' )
font_std = pg.font.Font('assets/font.ttf', 25 )

# display size, name, icon
screen = pg.display.set_mode( ( display_width, display_height ) )
icon = pg.image.load( 'assets/joystick.png' )
pg.display.set_icon( icon )
pg.display.set_caption( 'DogeFight' )

# player
player_img = pg.image.load( 'assets/aircraft.png' )
player_x = 500.0
player_y = 600.0
pl = Player( player_x, player_y, player_img, screen )

# zeppelin
zep_img = pg.image.load( 'assets/zeppelin.png' )
zep = Zeppelin( 400, 200, zep_img, screen )

# bullet
bullet_img = pg.transform.scale( pg.image.load( 'assets/bullet.png' ), ( 4, 4 ) )
bullets: List[ Bullet ] = []

#explosion
explosion_img = pg.image.load( 'assets/explosion.png' )


# write things
def display_score():
    score_string = 'score: ' + str(score)
    text_surface = font_std.render( score_string, True, (220,220,220) )
    screen.blit( text_surface, (20, 0) )

def display_stats():
    speed_string = 'speed: ' + str( int( np.round(pl.speed * 1000, -1) ) )
    text_surface = font_std.render( speed_string, True, (220,220,220) )
    screen.blit( text_surface, (900,650) )

# game loop
while running:
    for event in pg.event.get():
        # QUIT button
        if event.type == pg.QUIT:
            running = False
        # player controls
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                pl.rotation += 0.1
            if event.key ==pg.K_a or event.key == pg.K_LEFT:
                pl.rotation -= 0.1
            if event.key == pg.K_w or event.key == pg.K_UP:
                pl.increment_speed()
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                pl.decrement_speed()
            if event.key == pg.K_SPACE or event.key == pg.K_LSHIFT:
                blt = Bullet( bullet_img, screen, pl )
                bullets.append( blt )
                
        if event.type == pg.KEYUP:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                pl.rotation = 0
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                pl.rotation = 0

    for blt in bullets:
        blt.position += blt.delta
        blt_rect = pg.Rect( blt.position[ 0 ], blt.position[ 1 ], 4, 4 )
        zep_rect = pg.Rect( zep.position[ 0 ], zep.position[ 1 ], 64, 64 )
        if pg.Rect.colliderect( blt_rect, zep_rect ):
            zep.hit()
            bullets.remove( blt )
            if zep.dead is True:
                expl = Explosion( zep.position[ 0 ], zep.position[ 1 ], explosion_img, screen )
            


    pl.angle += pl.rotation

    pl.delta[ 0 ] = pl.speed * np.cos( pl.angle * np.pi / 180 )
    pl.delta[ 1 ] = pl.speed * np.sin( pl.angle * np.pi / 180 )

    pl.position += pl.delta
    pl.x = pl.position[ 0 ]
    pl.y = pl.position[ 1 ]

    # keep player in borders
    if pl.x < 0: pl.x = 0
    if pl.x > display_width - pl.size: pl.x = display_width - pl.size
    if pl.y < 0: pl.y = 0
    if pl.y > display_height - pl.size: pl.y = display_height - pl.size
    
    # draw things
    screen.fill( ( 77, 106, 255 ) )
    if not zep.dead: zep.draw()
    else: expl.draw()
    for blt in bullets: blt.draw()
    pl.draw()
    display_score()
    display_stats()


    # the very end of the loop
    pg.display.update()
    