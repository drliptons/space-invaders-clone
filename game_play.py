import random

import pygame
from player import Player
from alien import Alien
import settings
from explosion import Explosion


class GamePlay:
    def __init__(self, screen):
        self.screen = screen

        self.main_menu = None
        self.button_font = pygame.font.SysFont('fonts/editundo.ttf', 25)

        # Game states
        self.has_play_game_over_sound = False
        self.is_game_over = False

        # Set back button
        self.button_color = (62, 250, 25)
        self.button_over_color = (225, 255, 220)
        self.back_button_width = 100
        self.back_button_height = 30
        self.back_button_rect = [screen.get_width() - self.back_button_width, 0,
                                 self.back_button_width, self.back_button_height]
        self.back_button_text = self.button_font.render('BACK', True, settings.BUTTON_TEXT_COLOR)

        # Set new game button
        self.is_new_game_button_active = False
        self.new_game_button_width = 200
        self.new_game_button_height = 30
        self.new_game_button_rect = [(screen.get_width() - self.new_game_button_width) / 2,
                                     (screen.get_width() - self.new_game_button_height) / 2,
                                     self.new_game_button_width, self.new_game_button_height]
        self.new_game_button_text = self.button_font.render('NEW GAME', True, settings.BUTTON_TEXT_COLOR)

        # Set up mouse
        self.mouse_x, self.mouse_y = (0, 0)
        self.is_scene_active = False

        # Set up player
        self.player = Player(screen, screen.get_width() / 2, screen.get_height() - 100)

        # Set up alien
        self.aliens = []
        self.alien_rows = 5
        self.alien_cols = 15
        self.alien_types = 4
        self.create_aliens()

        # Set screen play value
        self.border_left = 50
        self.border_right = screen.get_width() - self.border_left
        self.dir_x = 2
        self.dir_y = 10
        self.direction = self.dir_x

        # Set explosion list
        self.explosions = []

        # Game over text
        self.font_won = pygame.font.Font('fonts/editundo.ttf', 80)
        self.won_text = self.font_won.render('YOU WON', True, settings.TEXT_COLOR)
        self.won_text_position = ((screen.get_width() - self.won_text.get_width()) / 2,
                                  (screen.get_height() - self.won_text.get_height()) / 3)

        self.font_lost = pygame.font.Font('fonts/editundo.ttf', 80)
        self.lost_text = self.font_lost.render('YOU LOST', True, settings.TEXT_COLOR)
        self.lost_text_position = ((screen.get_width() - self.lost_text.get_width()) / 2,
                                   (screen.get_height() - self.lost_text.get_height()) / 3)

        # Sounds
        self.alien_killed_sound = pygame.mixer.Sound('sounds/alien_killed.wav')
        self.you_won_sound = pygame.mixer.Sound('sounds/you_won.wav')
        self.you_lost_sound = pygame.mixer.Sound('sounds/ship_explode.wav')

    def update(self, events):
        for event in events:
            # Check mouse over button
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_scene_active:
                self.mouse_x, self.mouse_y = event.pos
                # Back button
                if self.back_button_rect[0] <= self.mouse_x <= self.back_button_rect[0] + self.back_button_rect[2] and \
                        self.back_button_rect[1] <= self.mouse_y <= self.back_button_rect[1] + self.back_button_rect[3]:
                    self.reset()
                    self.is_scene_active = False
                    self.main_menu.is_scene_active = True
                    return self.main_menu
                # New game button
                if self.new_game_button_rect[0] <= self.mouse_x <= self.new_game_button_rect[0] + \
                        self.new_game_button_rect[2] and \
                        self.new_game_button_rect[1] <= self.mouse_y <= self.new_game_button_rect[1] + \
                        self.new_game_button_rect[3]:
                    self.reset()
                    self.is_game_over = False
                    # Stop show text
            if event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos

        # To draw player to screen
        self.player.update()

        # Check bullet collision with alien or bullet leave screen
        collide = False  # any collision?
        remove_bullet = []  # collided bullet to remove from screen
        if self.player.bullets != [] and self.aliens != []:  # bullets and aliens aren't empty
            for bullet in self.player.bullets:  # check every bullets
                collide = False  # set collide for each bullet to false before detect collision
                for alien in pygame.sprite.spritecollide(bullet, self.aliens, 0): # check if bullet collide with alien
                    self.aliens.remove(alien)  # if any collision then remove alien from list
                    self.explosions.append(Explosion(alien.x, alien.y))  # add explosion affect when alien died
                    alien.kill()  # destroy alien
                    pygame.mixer.Sound.play(self.alien_killed_sound)
                    self.player.score += alien.score
                    collide = True  # set collision to True
                if collide:  # if any collision
                    remove_bullet.append(bullet)  # add bullet to remove list

        for bullet in remove_bullet:
            self.player.bullets.remove(bullet)  # remove bullet from the player's bullet list
            bullet.kill()  # destroy bullet

        return self

    def draw(self, screen):
        # Draw back button to screen
        if self.is_scene_active:
            self.show_button(screen, self.back_button_text, self.back_button_rect, self.back_button_width,
                             self.back_button_height)

            if self.is_game_over:
                self.show_button(screen, self.new_game_button_text, self.new_game_button_rect,
                                 self.new_game_button_width, self.new_game_button_height)

        # Draw game over text
        if self.player.lives <= 0:
            if not self.has_play_game_over_sound:
                pygame.mixer.Sound.play(self.you_lost_sound)
                self.has_play_game_over_sound = True
            screen.blit(self.lost_text, self.lost_text_position)
            self.is_game_over = True
            return self
        elif len(self.aliens) <= 0:
            if not self.has_play_game_over_sound:
                pygame.mixer.Sound.play(self.you_won_sound)
                self.has_play_game_over_sound = True
            self.is_game_over = True
            screen.blit(self.won_text, self.won_text_position)

        # Draw aliens to screen
        for alien in self.aliens:
            alien.draw(screen)

        # Draw player to screen
        self.player.draw(screen)

        # Draw alien laser to screen
        remove_laser = []
        for laser in settings.alien_lasers:
            if laser.y > screen.get_height():
                remove_laser.append(laser)
            laser.draw(screen)

        # Remove laser
        for laser in remove_laser:
            settings.alien_lasers.remove(laser)

        # Move aliens
        update_y = False
        if (settings.offset_x + self.alien_cols * 32) > self.border_right:  # check right border
            self.direction *= -1  # change direction
            update_y = True
            settings.offset_x = self.border_right - self.alien_cols * 32  # ensure offset align with sprite size/border
        if settings.offset_x < self.border_left:  # check left border
            self.direction *= -1  # change direction
            update_y = True
            settings.offset_x = self.border_left  # ensure offset align with sprite size/border
        settings.offset_x += self.direction  # move aliens in x-axis
        if update_y:
            settings.offset_y += self.dir_y  # move aliens in y-axis

        # Draw explosion animation
        remove_explosion = []
        for explosion in self.explosions:
            explosion.draw(screen)
            if explosion.frame_y < 0:  # check if explosion effect has finshed
                remove_explosion.append(explosion)

        for explosion in remove_explosion:
            self.explosions.remove(explosion)

    def reset(self):
        self.player = Player(self.screen, self.screen.get_width() / 2, self.screen.get_height() - 100)
        self.player.lives = 3
        self.player.score = 0
        self.aliens = []
        self.alien_rows = 5
        self.alien_cols = 15
        settings.offset_x = 10
        settings.offset_y = 50
        settings.alien_lasers = []
        self.create_aliens()
        self.is_game_over = False

    def create_aliens(self):
        for y in range(self.alien_rows):
            for x in range(self.alien_cols):
                self.aliens.append(Alien(2 * x + 1, 2 * y + 1, random.randint(0, self.alien_types - 1)))

    def show_button(self, screen, button_text, button_rect, button_width, button_height):
        if button_rect[0] <= self.mouse_x <= button_rect[0] + button_rect[2] and \
                button_rect[1] <= self.mouse_y <= button_rect[1] + button_rect[3]:
            pygame.draw.rect(screen, self.button_over_color, button_rect)
        else:
            pygame.draw.rect(screen, self.button_color, button_rect)

        screen.blit(button_text,
                    (button_rect[0] + (button_width - button_text.get_width()) / 2,
                     button_rect[1] + (button_height - button_text.get_height()) / 2))

    def click_button(self, button_rect) -> bool:
        if button_rect[0] <= self.mouse_x <= button_rect[0] + button_rect[2] and \
                button_rect[1] <= self.mouse_y <= button_rect[1] + button_rect[3]:
            return True
        else:
            return False
