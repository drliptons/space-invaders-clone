import pygame
import settings


class Explosion:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/explosion.png')
        self.x = x
        self.y = y
        self.frame_x = 3
        self.frame_y = 1
        self.sprite_size = 16

    def draw(self, screen):
        # Draw explosion image
        screen.blit(self.image,
                    [self.x * self.sprite_size + settings.offset_x,  # where to spawn explosion on x-axis
                     self.y * self.sprite_size + settings.offset_y,  # where to spawn explosion on y-axis
                     self.sprite_size, self.sprite_size],  # sprite size WxH
                    (self.frame_x * self.sprite_size, self.frame_y * self.sprite_size,  # which frame to draw
                     self.sprite_size, self.sprite_size))

        self.frame_x -= 1
        if self.frame_x < 0:
            self.frame_x = 3
            self.frame_y -= 1
