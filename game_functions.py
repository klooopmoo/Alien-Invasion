import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, stats, play_button, ship,aliens,  bullets):
    # watch for keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            hs_file = open("highscore.txt", "w")
            hs_file.write(str(stats.high_score))
            hs_file.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen,stats, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens,bullets,  mouse_x, mouse_y)


def check_keydown_events(event, ai_settings, screen,stats,  ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen,ship, bullets)
    elif event.key == pygame.K_q:
        hs_file = open("highscore.txt", "w")
        hs_file.write(str(stats.high_score))
        hs_file.close()
        sys.exit()



def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, stats, screen, sb,  ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    # redraw all bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    #draw button
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Updates position of bullets """
    bullets.update()
    # get rid of bullets once off screen or memory will be consumed
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen,stats, sb,  ship, aliens, bullets)




def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    #spacing between each alien is = to  1 alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #create first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # create alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)




def get_number_aliens_x(ai_settings, alien_width):
    """returns # of alien that fit in a row """
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int (available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Deternmine # of rows """
    avalible_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(avalible_space_y / (3 * alien_height))
    return number_rows

def update_aliens(ai_settings, stats, screen, ship,  aliens, bullets):
    """updates the position of the aliens """
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # look for alien ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    # look for alien bottom collision
    check_aliens_bottom(ai_settings, stats, screen,ship, aliens,bullets)

def check_fleet_edges(ai_settings, aliens):
    """respond appropiately if any aliens have reached the edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_directions(ai_settings, aliens)
            break


def change_fleet_directions(ai_settings, aliens):
    """drop the entrie fleet down and move opposite direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_alien_collision(ai_settings, screen,stats, sb,  ship, aliens, bullets):
    ## check to see if any bullets hit the aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
    check_high_score(stats, sb)
    if len(aliens) == 0:
        #destory existing bullets and create new fleet
        bullets.empty()
        ai_settings.increase_speed()

        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """respond to ship being hit """
    if stats.ships_left > 1:

        #decrement ship lives
        stats.ships_left -=1

        # empty the list of aliens and bulelts
        aliens.empty()
        bullets.empty()

        #create a new fleet
        create_fleet(ai_settings,screen, ship, aliens)
         #pause
        sleep(.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any alien have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #reaching the bottom is the same as ship getting hit
            ship_hit(ai_settings,stats, screen, ship, aliens, bullets)
            break

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,bullets,  mouse_x, mouse_y):
    '''start a new game when the player clicks play'''

    if not stats.game_active and play_button.rect.collidepoint(mouse_x, mouse_y):
        ai_settings.initilize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active =True

    #emply the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_high_score(stats, sb):
    """"chceck to see high scores"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()