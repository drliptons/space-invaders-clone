import pygame
import settings
import sys
import os


class MainMenu:
    def __init__(self, game):
        if getattr(sys, 'frozen', False) and hasattr(sys, 'MEIPASS'):
            application_dir = sys._MEIPASS
        else:
            application_dir = os.path.dirname(os.path.abspath(__file__))

        self.font_path = os.path.join(application_dir, 'fonts/editundo.ttf')
        self.game = game
        self.screen = game.screen
        # Title text
        self.font = pygame.font.Font(self.font_path, 80)
        self.title = self.font.render('ALIEN INVADERS', True, settings.TEXT_COLOR)
        self.title_position = ((self.screen.get_width() - self.title.get_width()) / 2,
                               (self.screen.get_height() - self.title.get_height()) / 3)
        # Credit text
        self.creator_font = pygame.font.Font(self.font_path, 20)
        self.creator_text = self.creator_font.render('MADE BY: DRLIPTONS', True, settings.TEXT_COLOR)
        self.creator_position = (self.screen.get_width() - self.creator_text.get_width() - 10,
                                 self.screen.get_height() - self.creator_text.get_height() - 10)

        # Scene
        self.gameplay_scene = None
        self.credit_scene = None

        # Set up mouse
        self.is_scene_active = True
        self.mouse_x, self.mouse_y = (0, 0)

        # Set up button
        self.button_color = (62, 250, 25)
        self.button_over_color = (225, 255, 220)
        self.button_width = 200
        self.button_height = 30
        self.button_font = pygame.font.SysFont(self.font_path, 25)

        # Set start button
        self.start_button_rect = [(self.screen.get_width() - self.button_width) / 2,
                                  (self.screen.get_height() - self.button_height) / 2,
                                  self.button_width, self.button_height]
        self.start_button_text = self.button_font.render('START', True, settings.BUTTON_TEXT_COLOR)
        # Set credit button
        self.credit_button_rect = [(self.screen.get_width() - self.button_width) / 2,
                                 self.start_button_rect[1] + self.button_height + 10,
                                 self.button_width, self.button_height]
        self.credit_button_text = self.button_font.render('CREDIT', True, settings.BUTTON_TEXT_COLOR)
        # Set quit button
        self.quit_button_rect = [(self.screen.get_width() - self.button_width) / 2,
                                 self.credit_button_rect[1] + self.button_height + 10,
                                 self.button_width, self.button_height]
        self.quit_button_text = self.button_font.render('QUIT', True, settings.BUTTON_TEXT_COLOR)

        # Music
        pygame.mixer.music.load(os.path.join(application_dir, 'sounds/bg.mp3'))
        pygame.mixer.music.play(-1, 0, 0)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_scene_active:
                self.mouse_x, self.mouse_y = event.pos
                if self.click_button(self.start_button_rect):
                    self.is_scene_active = False
                    self.gameplay_scene.is_scene_active = True
                    return self.gameplay_scene
                elif self.click_button(self.quit_button_rect):
                    self.game.game_over = True
                elif self.click_button(self.credit_button_rect):
                    return self.credit_scene
            if event.type == pygame.MOUSEMOTION and self.is_scene_active:
                self.mouse_x, self.mouse_y = event.pos
        return self

    def draw(self, screen):
        # Show title
        screen.blit(self.title, self.title_position)

        # Show start button
        if self.is_scene_active:
            self.draw_button(screen, self.start_button_text, self.start_button_rect)
            self.draw_button(screen, self.quit_button_text, self.quit_button_rect)
            self.draw_button(screen, self.credit_button_text, self.credit_button_rect)

        # Show creator text
        screen.blit(self.creator_text, self.creator_position)

    def draw_button(self, screen, button_text, button_rect):
        # Draw button color
        if button_rect[0] <= self.mouse_x <= button_rect[0] + \
                button_rect[2] and \
                button_rect[1] <= self.mouse_y <= button_rect[1] + \
                button_rect[3]:
            pygame.draw.rect(screen, self.button_over_color, button_rect)
        else:
            pygame.draw.rect(screen, self.button_color, button_rect)

        # Draw button text
        screen.blit(button_text,
                    (button_rect[0] + (self.button_width - button_text.get_width()) / 2,
                     button_rect[1] + (self.button_height - button_text.get_height()) / 2))

    def click_button(self, button_rect) -> bool:
        if button_rect[0] <= self.mouse_x <= button_rect[0] + button_rect[2] and \
                button_rect[1] <= self.mouse_y <= button_rect[1] + button_rect[3]:
            # Button is clicked
            return True
        else:
            # Button is not clicked
            return False
