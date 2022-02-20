import time

import pygame
from pygame.locals import *

from bullet import Bullet
import settings

import sys
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        if getattr(sys, 'frozen', False) and hasattr(sys, 'MEIPASS'):
            application_dir = sys._MEIPASS
        else:
            application_dir = os.path.dirname(os.path.abspath(__file__))

        self.image = pygame.image.load(os.path.join(application_dir, 'images/Ship.png'))
        self.screen = screen
        self.x = pos_x
        self.y = pos_y
        self.bullet_speed = 20

        # Image rect position
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        # Bullet shots
        self.can_shoot = False
        self.start_delay = time.time()
        self.bullet_delay = 0.4
        self.bullets = []

        # Player status bar
        self.font = os.path.join(application_dir, 'fonts/editundo.ttf')
        self.font = pygame.font.SysFont(self.font, 25)
        self.lives = 3
        self.score = 0

        # Sound
        self.shoot_sound = pygame.mixer.Sound(os.path.join(application_dir, 'sounds/shoot.wav'))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] and self.x < self.screen.get_width() - self.image.get_width():
            self.x += 5
        elif keys[K_LEFT] and self.x > 0:
            self.x -= 5

        self.rect.topleft = (self.x, self.y)  # update rect position

        if time.time() - self.start_delay > self.bullet_delay:
            self.can_shoot = True

        if keys[K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.start_delay = time.time()
            self.bullets.append(Bullet(self.x + self.image.get_width() / 2, self.y, self.bullet_speed))
            pygame.mixer.Sound.play(self.shoot_sound)

        # Check player collide with alien laser
        for laser in pygame.sprite.spritecollide(self, settings.alien_lasers, False):
            settings.alien_lasers.remove(laser)
            laser.kill()
            self.lives -= 1

    def draw(self, screen):
        # Draw player
        screen.blit(self.image, [self.x, self.y, self.image.get_width(), self.image.get_height()])

        # Draw lives text
        lives_text = self.font.render('LIVES: ' + str(self.lives), True, settings.TEXT_COLOR)
        screen.blit(lives_text, (10, 10))

        # Draw score text
        score_text = self.font.render('SCORE: ' + str(self.score), True, settings.TEXT_COLOR)
        screen.blit(score_text, (100, 10))

        # Draw bullet
        remove_bullets = []
        for bullet in self.bullets:
            if bullet.y < 0:
                remove_bullets.append(bullet)
            bullet.draw(screen)

        # Remove bullet
        for bullet in remove_bullets:
            self.bullets.remove(bullet)
            del bullet

