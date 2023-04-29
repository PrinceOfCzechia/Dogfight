import pygame as pg
import numpy as np
import random as rn
from typing import List
from player import Player
from bullet import Bullet
from zeppelin import Zeppelin
from explosion import Explosion
from enemy import Enemy
from bomb import Bomb
from carrier import Carrier

pg.init()

# environemnent
info = pg.display.Info()
pg.mixer.init()
running = True
display_width = info.current_w
display_height = info.current_h - 75
score = 0
explosion_duration = 50
bullet_img = pg.image.load( 'assets/bullet.png' )
font_std = pg.font.Font('assets/font.ttf', 25 )
font_big = pg.font.Font('assets/font.ttf', 80 )
bg_img = pg.transform.scale( pg.image.load( 'assets/background.jpg' ), ( info.current_w, info.current_h ) )

# display size, name, icon
screen = pg.display.set_mode( ( display_width, display_height ) )
icon = pg.image.load( 'assets/joystick.png' )
pg.display.set_icon( icon )
pg.display.set_caption( 'DogeFight' )

# player
player_img = pg.transform.scale( pg.image.load( 'assets/plane.png' ), ( 32, 32 ) )
player_x = 500.0
player_y = display_height * 7/8
pl = Player( player_x, player_y, player_img, screen )
full_heart_img = pg.image.load( 'assets/full_heart.png' )
empty_heart_img = pg.image.load( 'assets/empty_heart.png' )

# enemy
enemy_img = pg.transform.scale( pg.image.load( 'assets/tank.png' ), ( 32, 32 ) )
enemy_x = display_width / 3
enemy_y = display_height / 4
en = Enemy( enemy_x, enemy_y, enemy_img, screen, pl )

# zeppelin
zep_img = pg.image.load( 'assets/zeppelin.png' )
airships: List[ Zeppelin ] = []
num_zep = rn.randint( 4, 8 )
for i in range( num_zep ):
    zep = Zeppelin( zep_img, screen, display_width, display_height )
    airships.append( zep )

# bullet
bullet_img = pg.transform.scale( pg.image.load( 'assets/bullet.png' ), ( 6, 6 ) )
bullets: List[ Bullet ] = []
bullet_sound = pg.mixer.Sound( 'assets/fire.mp3' )
bullet_sound.set_volume( 0.1 )
empty_sound = pg.mixer.Sound( 'assets/empty.wav' )

# bomb
bomb_img = pg.image.load( 'assets/bomb.png' )
bombs: List[ Bomb ] = []

# explosion
explosion_img = pg.image.load( 'assets/explosion.png' )
explosions: List[ Explosion ] = []
explosion_sound = pg.mixer.Sound( 'assets/explosion_sound.wav' )

# carrier
carrier_img = pg.image.load( 'assets/aircraft-carrier.png' )
carrier = Carrier( display_width - 400, display_height - 300, carrier_img, screen )

# background music
pg.mixer.music.load( 'assets/bg_music.wav' )
pg.mixer.music.set_volume( 0.3 )
# TODO: uncomment pg.mixer.music.play( -1, 0.0, 0 )


# write things
def display_score():
    score_string = 'score: ' + str(score)
    text_surface = font_std.render( score_string, True, (220,220,220) )
    screen.blit( text_surface, ( 20, 10 ) )

def display_stats():
    # speed
    speed_string = 'speed: ' + str( int( np.round(pl.speed * 1000, -1) ) )
    speed_surface = font_std.render( speed_string, True, (220,220,220) )
    screen.blit( speed_surface, ( display_width-120, display_height-50 ) )
    # ammo
    ammo_string = 'ammo: ' + str( pl.ammo )
    ammo_surface = font_std.render( ammo_string, True, (220,220,220) )
    screen.blit( ammo_surface, ( display_width-120, display_height-80 ) )
    # bombs
    bomb_string = 'bombs left: ' + str( pl.bomb_cap )
    bomb_surface = font_std.render( bomb_string, True, (220,220,220) )
    screen.blit( bomb_surface, ( display_width-120, display_height-110 ) )

def display_over():
    sf = pg.Surface( (display_width, display_height), pg.SRCALPHA)
    filler = pg.Color( 0, 100, 100, 96 )
    sf.fill( filler )
    screen.blit( sf, (0, 0) )
    over_string = 'game over'
    text_surface = font_big.render( over_string, True, (220,220,220) )
    screen.blit( text_surface, ( display_width/2 - 100, display_height/2 - 20 ) )

# game loop
while pl.alive() and running:
    for event in pg.event.get():
        # QUIT button
        if event.type == pg.QUIT:
            running = False
        # player controls
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                pl.rotation += pl.get_rotation_increment()
            if event.key ==pg.K_a or event.key == pg.K_LEFT:
                pl.rotation -= pl.get_rotation_increment()
            if event.key == pg.K_w or event.key == pg.K_UP:
                pl.increment_speed()
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                pl.decrement_speed()
            if event.key == pg.K_SPACE:
                if pl.ammo > 0:
                    blt = Bullet( bullet_img, screen, pl )
                    bullets.append( blt )
                    bullet_sound.play()
                    pl.ammo -= 1
                else:
                    empty_sound.play()
            if event.key == pg.K_b:
                if pl.bomb_cap > 0:
                    pl.bomb_cap -= 1
                    bombs.append( Bomb( bomb_img, screen, pl ) )
                else: pass
                
        if event.type == pg.KEYUP:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                pl.rotation = 0
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                pl.rotation = 0

    for blt in bullets:
        blt.position += blt.delta * blt.increment
        for zep in airships:
            if not zep.dead:
                if pg.Rect.colliderect( blt.get_rect(), zep.rect ):
                    zep.hit()
                    bullets.remove( blt )
                    if zep.dead is True:
                        explosions.append( Explosion( zep.x, zep.y, explosion_img, screen ) )
                        explosion_sound.play()
                        score += 50

    for zep in airships:
        if not zep.dead:
            if pg.Rect.colliderect( zep.rect, pl.get_rect() ):
                zep.kill()
                explosions.append( Explosion( zep.x, zep.y, explosion_img, screen ) )
                explosion_sound.play()
                pl.big_hit()

    for bmb in bombs:
        if bmb.period < 200:
            bmb.position += bmb.delta
            bmb.period += 1
        else:
            expl = Explosion( bmb.position[ 0 ], bmb.position[ 1 ], explosion_img, screen )
            explosions.append( expl )
            bombs.remove( bmb )
            explosion_sound.play()
            if not en.dead and pg.Rect.colliderect( expl.rect, en.rect ):
                en.kill()
                score += 500
                explosions.append( Explosion( en.position[ 0 ] + en.size/2, en.position[ 1 ] + en.size/2,
                                              explosion_img, screen ) )
                explosion_sound.play()

    pl.angle += pl.rotation

    pl.delta[ 0 ] = pl.speed * np.cos( pl.angle * np.pi / 180 )
    pl.delta[ 1 ] = pl.speed * np.sin( pl.angle * np.pi / 180 )

    pl.position += pl.delta

    # keep player in borders
    if pl.position[ 0 ] + 5 * pl.delta[ 0 ] < 0: pl.position[ 0 ] = 0
    if pl.position[ 0 ] + 5 * pl.delta[ 0 ] > display_width - pl.size: pl.position[ 0 ] = display_width - pl.size
    if pl.position[ 1 ] + 5 * pl.delta[ 1 ] < 0: pl.position[ 1 ] = 0
    if pl.position[ 1 ] + 5 * pl.delta[ 1 ] > display_height - pl.size: pl.position[ 1 ] = display_height - pl.size

    # enemy movement
    if not en.correctDirection(): en.changeDirection()
    en.rotate()
    
    # draw things
    screen.blit( bg_img, ( 0, 0 ) )
    pl.draw_hearts( full_heart_img, empty_heart_img, display_width - 40, display_height - 130 )
    carrier.draw()
    for zep in airships:
        if not zep.dead: zep.draw()
    for blt in bullets: blt.draw()
    for bmb in bombs: bmb.draw()
    for expl in explosions:
        if expl.visible:
            if expl.timer < expl.duration: expl.draw()
            expl.timer += 1
    if not en.dead: en.draw()
    pl.draw()
    display_score()
    display_stats()


    # the very end of the loop
    pg.display.update()

# draw static images when game over
while not pl.alive() and running:
    for event in pg.event.get():
        # QUIT button
        if event.type == pg.QUIT:
            running = False

    screen.blit( bg_img, ( 0, 0 ) )
    pl.draw_hearts( full_heart_img, empty_heart_img, display_width - 20, display_height - 100 )
    for zep in airships:
        if not zep.dead: zep.draw()
    for blt in bullets: blt.draw()
    for expl in explosions:
        if expl.visible:
            if expl.timer < expl.duration: expl.draw()
            if not pg.Rect.colliderect( expl.rect, pl.get_rect()): expl.timer += 1
    pl.draw()
    en.draw()
    display_score()
    display_stats()
    display_over()

    pg.display.update()
    