import pygame as pg
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import numpy as np
import random as rn
from typing import List
from time import time
from player import Player
from bullet import Bullet
from zeppelin import Zeppelin
from explosion import Explosion
from enemy import Enemy
from bomb import Bomb
from carrier import Carrier
from crosshair import Crosshair
from enemy_bullet import Enemy_bullet

pg.init()

# environemnent
info = pg.display.Info()
pg.mixer.init()
running = True
menu = True
options = False
playing = False # game or game-over screen running
controls = False # the player still has ammunition
targets = False # there are still targets to shoot
DISPLAY_WIDTH = info.current_w
DISPLAY_HEIGHT = info.current_h - 75
score = 0
DIFFICULTY = None
font_std = pg.font.Font('assets/font.ttf', 25 )
font_big = pg.font.Font('assets/font.ttf', 80 )
bg_img = pg.transform.scale( pg.image.load( 'assets/background.jpg' ), ( info.current_w, info.current_h ) )

# display size, name, icon
screen = pg.display.set_mode( ( DISPLAY_WIDTH, DISPLAY_HEIGHT ) )
icon = pg.image.load( 'assets/joystick.png' )
pg.display.set_icon( icon )
pg.display.set_caption( 'DogeFight' )
sf = pg.Surface( (DISPLAY_WIDTH, DISPLAY_HEIGHT), pg.SRCALPHA ) # surface to fill menu screen
sf.fill( pg.Color( 60, 130, 100, 96 ) ) # permanently camo green

# background music
pg.mixer.music.load( 'assets/bg_music.wav' )
pg.mixer.music.set_volume( 0.3 )

while running:
    pg.mixer.music.play( -1, 0.0, 0 )
    # main menu functions
    def start_game():
        global menu, playing, controls, targets, DIFFICULTY
        menu = False
        playing = True
        controls = True
        targets = True
        if DIFFICULTY is not None:
            if options_dropdown.getSelected() is not None:
                DIFFICULTY = options_dropdown.getSelected()
            else: DIFFICULTY = 1
        else: DIFFICULTY = 1

    def display_options():
        global options, menu
        menu = False
        options = True

    def quit_game():
        global running, menu, playing, controls
        running = False
        menu = False
        playing = False
        controls = False

    # main menu elements
    start_button = Button(
        screen,
        DISPLAY_WIDTH/3, DISPLAY_HEIGHT*3/16,
        DISPLAY_WIDTH/3, DISPLAY_HEIGHT/8,
        text = 'Play',
        font = font_big, textColour = ( 230, 230, 230 ),
        margin = 20, radius = 5,
        inactiveColour = ( 40, 110, 80 ), hoverColour = ( 20, 20, 20 ),
        onClick = lambda: start_game()
    )

    options_dropdown = Dropdown(
        screen,
        DISPLAY_WIDTH/3, DISPLAY_HEIGHT*6/16,
        DISPLAY_WIDTH/3, DISPLAY_HEIGHT/8,
        name='Select difficulty',
        choices=[ 'Easy', 'Medium', 'Hard', 'Insane' ],
        values = [ 0, 1, 2, 3 ],
        font = font_big, textColour = ( 230, 230, 230 ),
        borderRadius = 5, colour = ( 40, 110, 80 ), hoverColour = ( 20, 20, 20 ), direction = 'down'
    )

    quit_button = Button(
        screen,
        DISPLAY_WIDTH/3, DISPLAY_HEIGHT*9/16,
        DISPLAY_WIDTH/3, DISPLAY_HEIGHT/8,
        text = 'Quit',
        font = font_big, textColour = ( 230, 230, 230 ),
        margin = 20, radius = 5,
        inactiveColour = ( 40, 110, 80 ), hoverColour = ( 20, 20, 20 ),
        onClick = lambda: quit_game()
    )

    # main menu loop
    while menu:
        screen.blit( sf, (0, 0) )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                menu = False
            
        pw.update( pg.event.get() )
        pg.display.update()

    # player
    player_x = DISPLAY_WIDTH/2 + rn.randint( -200, 200 )
    player_y = DISPLAY_HEIGHT * 9/10
    pl = Player( player_x, player_y, screen )
    full_heart_img = pg.image.load( 'assets/full_heart.png' )
    empty_heart_img = pg.image.load( 'assets/empty_heart.png' )

    # enemy
    enemies: List[ Enemy ] = []
    enemy_x1 = DISPLAY_WIDTH / 4 + rn.randint( -20, 20 )
    enemy_x2 = DISPLAY_WIDTH * 4 / 9 + rn.randint( -20, 20 )
    enemy_y1 = DISPLAY_HEIGHT / 4 + rn.randint( -20, 20 )
    enemy_y2 = DISPLAY_HEIGHT * 3 / 4 + rn.randint( -20, 20 )
    if DIFFICULTY > 0: enemies.append( Enemy( enemy_x1, enemy_y1, screen, pl ) )
    if DIFFICULTY > 1: enemies.append( Enemy( enemy_x1, enemy_y2, screen, pl ) )
    if DIFFICULTY > 2: enemies.append( Enemy( enemy_x2, enemy_y1, screen, pl ) )

    # zeppelin
    airships: List[ Zeppelin ] = []
    num_zep = rn.randint( 4, 8 )
    for i in range( num_zep ):
        zep = Zeppelin( screen, DISPLAY_WIDTH, DISPLAY_HEIGHT, i+1, num_zep )
        airships.append( zep )

    # bullet
    bullets: List[ Bullet ] = []
    bullet_sound = pg.mixer.Sound( 'assets/fire.mp3' )
    bullet_sound.set_volume( 0.1 )
    empty_sound = pg.mixer.Sound( 'assets/empty.wav' )

    # enemy bullet
    enemy_bullets: List[ Enemy_bullet ] = []
    last_shot = time()
    hit_sound = pg.mixer.Sound( 'assets/hit.wav' )

    # bomb
    bombs: List[ Bomb ] = []
    full_bomb_img = pg.transform.rotate( pg.image.load( 'assets/bomb.png' ), 0 )
    empty_bomb_img = pg.transform.rotate( pg.image.load( 'assets/empty_bomb.png' ), 0 )

    # explosion
    explosions: List[ Explosion ] = []
    explosion_sound = pg.mixer.Sound( 'assets/explosion_sound.wav' )

    # carrier
    carrier = Carrier( DISPLAY_WIDTH - 400, DISPLAY_HEIGHT - 300, screen )

    # crosshair
    crosshair = Crosshair( pl, screen )


    # write things
    def display_score():
        score_string = 'score: ' + str(score)
        text_surface = font_std.render( score_string, True, (220,220,220) )
        screen.blit( text_surface, ( 20, 10 ) )

    def display_stats():
        # speed
        speed_string = 'speed: ' + str( int( np.round(pl.speed * 1000, -1) ) )
        speed_surface = font_std.render( speed_string, True, (220,220,220) )
        screen.blit( speed_surface, ( DISPLAY_WIDTH-120, DISPLAY_HEIGHT-50 ) )
        # ammo
        ammo_string = 'ammo: ' + str( pl.ammo )
        ammo_surface = font_std.render( ammo_string, True, (220,220,220) )
        screen.blit( ammo_surface, ( DISPLAY_WIDTH-120, DISPLAY_HEIGHT-80 ) )

    def display_over( mode ):
        screen.blit( sf, (0, 0) )
        if mode == 0:
            text_surface = font_big.render( 'you died', True, (220,220,220) )
            screen.blit( text_surface, ( DISPLAY_WIDTH/2 - 100, DISPLAY_HEIGHT/2 - 20 ) )
        elif mode == 1:
            text_surface = font_big.render( 'out of ammo', True, (220,220,220) )
            screen.blit( text_surface, ( DISPLAY_WIDTH/2 - 120, DISPLAY_HEIGHT/2 - 20 ) )
        else:
            text_surface = font_big.render( 'congratulations', True, (220,220,220) )
            screen.blit( text_surface, ( DISPLAY_WIDTH/2 - 150, DISPLAY_HEIGHT/2 - 20 ) )

    # game loop
    while pl.hp > 0 and playing and controls and targets:
        for event in pg.event.get():
            # QUIT button
            if event.type == pg.QUIT:
                playing = False
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
                        blt = Bullet( screen, pl )
                        bullets.append( blt )
                        bullet_sound.play()
                        pl.ammo -= 1
                    else:
                        empty_sound.play()
                if event.key == pg.K_b:
                    if pl.current_bombs > 0:
                        pl.current_bombs -= 1
                        bombs.append( Bomb( screen, pl ) )
                    else: pass
                if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT:
                    crosshair.show()
                    
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
                            airships.remove( zep )
                            explosions.append( Explosion( zep.x, zep.y, screen ) )
                            explosion_sound.play()
                            score += 30

        for zep in airships:
            if pg.Rect.colliderect( zep.rect, pl.get_rect() ):
                zep.kill()
                airships.remove( zep )
                score += 20
                explosions.append( Explosion( zep.x, zep.y, screen ) )
                explosion_sound.play()
                pl.hp = np.maximum( pl.hp-2, 0 )

        for bmb in bombs:
            if bmb.period < 200:
                bmb.position += bmb.delta
                bmb.period += 1
            else:
                expl = Explosion( bmb.position[ 0 ] - 30, bmb.position[ 1 ] - 30, screen )
                explosions.append( expl )
                bombs.remove( bmb )
                explosion_sound.play()
                for en in enemies:
                    if not en.dead and pg.Rect.colliderect( expl.rect, en.rect ):
                        en.kill()
                        enemies.remove( en )
                        score += 500
                        explosions.append( Explosion( en.position[ 0 ] - en.size/2,
                                                    en.position[ 1 ] - en.size/2,
                                                    screen ) )
                        explosion_sound.play()
                if not carrier.dead and pg.Rect.colliderect( expl.rect, carrier.rect ):
                    carrier.hp -= 1
                    score += 300
                    if carrier.hp == 0:
                        carrier.dead = True

        pl.update()
        crosshair.update()

        # keep player within borders
        pl.check_borders( DISPLAY_WIDTH, DISPLAY_HEIGHT )

        # enemy handling
        for en in enemies:
            en.check_change()
            en.update()
            if en.correct_aim() and time() > last_shot + en.cooldown:
                enemy_bullets.append( Enemy_bullet( screen, en ) )
                bullet_sound.play()
                last_shot = time()

        for blt in enemy_bullets:
            blt.position += blt.delta * blt.increment
            if pg.Rect.colliderect( blt.get_rect(), pl.get_rect() ):
                pl.hp -= 1
                hit_sound.play()
                enemy_bullets.remove( blt )
        
        # draw things
        screen.blit( bg_img, ( 0, 0 ) )
        pl.draw_hearts( full_heart_img, empty_heart_img, DISPLAY_WIDTH - 40, DISPLAY_HEIGHT - 140 )
        pl.draw_bombs( full_bomb_img, empty_bomb_img, DISPLAY_WIDTH - 40, DISPLAY_HEIGHT - 110 )
        for en in enemies: en.draw()
        if not carrier.dead: carrier.draw()
        if carrier.hp == 1: carrier.draw_flames()
        for bmb in bombs: bmb.draw()
        for zep in airships: zep.draw()
        if crosshair.visible: crosshair.draw()
        for blt in bullets: blt.draw()
        for blt in enemy_bullets: blt.draw()
        for expl in explosions:
            if expl.visible:
                if time() - expl.spawn_time < expl.duration: expl.draw()
                else: expl.visible = False
        pl.draw()
        display_score()
        display_stats()

        if pl.current_bombs == 0 and pl.ammo == 0: controls = False
        if not enemies and not airships and carrier.dead: targets = False

        # beware
        # the very end of the loop
        pg.display.update()


    # post-game menu stuff
    death_time = time()
    # draw static images when game over
    while playing and (not pl.hp > 0 or not targets or not controls):
        for event in pg.event.get():
            # QUIT button
            if event.type == pg.QUIT:
                running = False
                menu = False
                playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    death_time = 0

        screen.blit( bg_img, ( 0, 0 ) )
        pl.draw_hearts( full_heart_img, empty_heart_img, DISPLAY_WIDTH - 40, DISPLAY_HEIGHT - 140 )
        pl.draw_bombs( full_bomb_img, empty_bomb_img, DISPLAY_WIDTH - 40, DISPLAY_HEIGHT - 110 )
        for zep in airships:
            if not zep.dead: zep.draw()
            if not carrier.dead: carrier.draw()
        if carrier.hp == 1:
            carrier.draw_flames()
        for blt in bullets: blt.draw()
        for expl in explosions:
            if expl.visible:
                if time() - expl.spawn_time < expl.duration: expl.draw()
                else: expl.visible - False
        pl.draw()
        for en in enemies:
            if not en.dead: en.draw()
        display_score()
        display_stats()
        if time() < death_time + 10:
            if not pl.hp > 0: display_over( 0 )
            if not controls: display_over( 1 )
            if not targets: display_over( 2 )
        else:
            playing = False
            menu = True

        pg.display.update()
    