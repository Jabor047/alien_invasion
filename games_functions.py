import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings,stats,play_button,screen,ship,bullets,aliens,sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,aliens,stats,sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_buttons(ai_settings,screen,ship,bullets,aliens,stats,play_button,mouse_x, mouse_y,sb)

def check_keydown_events(event,ai_settings,screen,ship,bullets,aliens,stats,sb):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_p:
        start_game(ai_settings,screen,ship,bullets,aliens,stats,sb)
    elif event.key == pygame.K_q:
        sys.exit()

def start_game(ai_settings,screen,ship,bullets,aliens,stats,sb):
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats(ai_settings)
        stats.game_active = True

        sb.prep_score()
        sb.prep_highscore()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()

def check_play_buttons(ai_settings,screen,ship,bullets,aliens,stats,play_button,mouse_x,mouse_y,sb):
    button_click = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_click and not stats.game_active:
        start_game(ai_settings,screen,ship,bullets,aliens,stats,sb)



def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_settings,stats,screen,ship,sb,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    aliens.draw(screen)
    ship.blitme()
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def fire_bullets(ai_settings,screen,ship,bullets):
    """if limit  not exceeded fire bullets"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings,screen,ship,sb,aliens,bullets,stats):
    bullets.update()
    #get rid of disappeared  bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings,screen,ship,sb,aliens,bullets,stats)

def check_bullet_alien_collision(ai_settings,screen,ship,sb,aliens,bullets,stats):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings,screen,aliens,ship)

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_aliens_y(ai_settings,alien_height,ship_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height)- ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (2 * alien_width * alien_number)
    alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(ai_settings,screen,aliens,ship):
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_aliens_y = get_number_aliens_y(ai_settings,alien.rect.height,ship.rect.height)

    #first row of aliens
    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,sb,screen,bullets,aliens,ship):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,sb,screen,bullets,aliens,ship):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,stats,sb,screen,bullets,aliens,ship)
            break

def update_aliens(ai_settings,stats,sb,screen,bullets,aliens,ship):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,bullets,aliens,ship)

    check_aliens_bottom(ai_settings,stats,sb,screen,bullets,aliens,ship)

def check_high_score(stats,sb):
    if stats.score > stats.high_score :
        stats.high_score = stats.score
        sb.prep_highscore()
