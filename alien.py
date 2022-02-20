import random

import pygame
import settings
from laser import Laser

import sys
import os


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_type):
        pygame.sprite.Sprite.__init__(self)

        if getattr(sys, 'frozen', False) and hasattr(sys, 'MEIPASS'):
            application_dir = sys._MEIPASS
        else:
            application_dir = os.path.dirname(os.path.abspath(__file__))

        # Set alien position
        self.x = x
        self.y = y
        # Set image
        self.type = alien_type
        self.frame = 0
        self.animation_speed = 15
        self.image = pygame.image.load(os.path.join(application_dir, 'images/Aliens.png'))  # load full image sprite
        self.sprite_size = 16  # size of a single sprite
        # Set sprite position for collider
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * self.sprite_size + settings.offset_x,
                             self.y * self.sprite_size + settings.offset_y)
        # Alien stats
        self.random_shoot = 1000
        self.bullet_speed = 5
        self.score = 5

    def change_frame(self):
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0

    def draw(self, screen):
        # Alien shoot bullet
        if random.randint(0, self.random_shoot) < 1:  # prob to tkae a shot
            # Add laser to laser list
            settings.alien_lasers.append(Laser(self.x * self.sprite_size + settings.offset_x,
                                               self.y * self.sprite_size + settings.offset_y,
                                               self.bullet_speed))
        # Change alien frame (create animation)
        if settings.offset_x % self.animation_speed == 0:
            self.change_frame()

        # Update rect position
        self.rect.topleft = (self.x * self.sprite_size + settings.offset_x,
                             self.y * self.sprite_size + settings.offset_y)

        # Draw aliens
        screen.blit(self.image,
                    [self.x * self.sprite_size + settings.offset_x,  # Where to start spawn aliens on x-axis
                     self.y * self.sprite_size + settings.offset_y,  # Where to start spawn aliens on y-axis
                     self.sprite_size, self.sprite_size],  # Sprite size WxH
                    (self.frame * self.sprite_size, self.sprite_size * self.type, self.sprite_size, self.sprite_size))
