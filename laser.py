import pygame

import settings

import sys
import os


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_speed):
        pygame.sprite.Sprite.__init__(self)

        if getattr(sys, 'frozen', False) and hasattr(sys, 'MEIPASS'):
            application_dir = sys._MEIPASS
        else:
            application_dir = os.path.dirname(os.path.abspath(__file__))

        self.image = pygame.image.load(os.path.join(application_dir, 'images/Laser.png'))
        # Set bullet position
        self.x = x - self.image.get_width() / 2
        self.y = y
        self.dir_y = bullet_speed
        # Set sprite position for collider
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        self.y += self.dir_y  # moving bullet upward
        self.rect.topleft = (self.x, self.y)  # update rect position
        screen.blit(self.image,  # draw bullet image
                    [self.x, self.y, self.image.get_width(), self.image.get_height()]  # bullet position rect format
                    )

        # Destroy bullet if leave screen
        if self.y > screen.get_height():
            settings.alien_lasers.remove(self)
            del self
