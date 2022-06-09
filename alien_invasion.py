import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from gamestats import GameStats
from pygame import mixer
from button import Button
from scoreboard import ScoreBoard
def run_game():
    pygame.init()
    # initilize game and create a screen object
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(ai_settings, screen)
    #make bullets
    bullets = Group()

    #make alien
    aliens = Group()
    # alien = Alien(ai_settings, screen)

    gf.create_fleet(ai_settings, screen, ship, aliens)

    # create stats
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings,screen,stats)
    #adding music to the game
    mixer.init()
    #load music
    mixer.music.load("music/mario.mp3")
    mixer.music.set_volume(.7)
    mixer.music.play(0)


    #make the Play button
    play_button = Button(ai_settings, screen, "Play")
    #start the game
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats, sb, ship,  aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen,  ship, aliens, bullets)

        gf.update_screen(ai_settings, stats,  screen, sb,  ship, aliens, bullets, play_button)



run_game()
