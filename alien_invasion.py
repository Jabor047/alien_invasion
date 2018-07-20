import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import games_functions as gf
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings,screen, "Play")
    # make a Ship
    ship = Ship(ai_settings,screen)
    #make a group to store bullets and aliens
    bullets = Group()
    aliens = Group()
    stats = Gamestats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    gf.create_fleet(ai_settings,screen,aliens,ship)

    while True:

        gf.check_events(ai_settings,stats,play_button,screen,ship,bullets,aliens,sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,sb,aliens,bullets,stats)
            gf.update_aliens(ai_settings,stats,sb,screen,bullets,aliens,ship)

        gf.update_screen(ai_settings,stats,screen,ship,sb,aliens,bullets,play_button)



run_game()
