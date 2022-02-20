import pygame
import settings

import sys
import os


class Credit:
    def __init__(self, screen):

        if getattr(sys, 'frozen', False) and hasattr(sys, 'MEIPASS'):
            application_dir = sys._MEIPASS
        else:
            application_dir = os.path.dirname(os.path.abspath(__file__))

        self.screen = screen
        self.main_menu = None

        self.text_speed = 1
        self.start_pos = 0

        # Set back button
        self.font_path = os.path.join(application_dir, 'fonts/editundo.ttf')
        self.font = pygame.font.Font(self.font_path, 20)
        self.button_font = pygame.font.SysFont(self.font_path, 25)
        self.button_color = (62, 250, 25)
        self.button_over_color = (225, 255, 220)
        self.back_button_width = 100
        self.back_button_height = 30
        self.back_button_rect = [screen.get_width() - self.back_button_width, 0,
                                 self.back_button_width, self.back_button_height]
        self.back_button_text = self.button_font.render('BACK', True, settings.BUTTON_TEXT_COLOR)

        # Set up mouse
        self.mouse_x, self.mouse_y = (0, 0)

        # Set credit text
        self.text_font = pygame.font.Font(self.font_path, 20)
        self.text = ['FROM THE ORIGINAL TITLE', 'SPACE INVADERS', '',
                     'TAITO CORPORATION', '',
                     '', '',
                     'ALIEN INVADERS',
                     'BY',
                     'DRLIPTONS', '',
                     '', '',
                     'GRAPHIC',
                     'DRLPTIONS',
                     '', '',
                     'BACKGROUND MUSIC',
                     'RETRO PLATFORMING BY DAVID FESLIYAN',
                     '', '',
                     'SOUND EFFECT',
                     'Mixkit',
                     'JUHAN JUNKALA',
                     '', '',
                     'TEXT FONT',
                     'BRIAN KENT'
                     '', '', '', '', '', '',
                     'CREATED FOR EDUCATIONAL PURPOSES',
                     'NOT FOR COMMERCIAL USE'
                     ]
        self.set_credit_text = False
        self.is_credit_end = False
        self.credit_text_height = 0

        # Production text
        self.pro_text_1_font = pygame.font.Font(self.font_path, 60)
        self.pro_text_2_font = pygame.font.Font(self.font_path, 120)
        self.pro_text_1 = self.pro_text_1_font.render('A PRODUCT OF', True, settings.TEXT_COLOR)
        self.pro_text_2 = self.pro_text_2_font.render('DRLIPTONS', True, settings.TEXT_COLOR)
        self.pro_text_1_pos = ((self.screen.get_width() - self.pro_text_1.get_width()) / 2,
                               (self.screen.get_height() + self.pro_text_1.get_height()) / 3)
        self.pro_text_2_pos = ((self.screen.get_width() - self.pro_text_2.get_width()) / 2,
                               self.pro_text_1_pos[1] + self.pro_text_1.get_height() + 10)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = event.pos
                if self.click_button(self.back_button_rect):
                    return self.main_menu
            if event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
        return self

    def draw(self, screen):
        y = 1
        n = self.start_pos

        self.show_button(screen, self.back_button_text, self.back_button_rect, self.back_button_width,
                         self.back_button_height)

        if self.start_pos >= (self.credit_text_height + screen.get_height()) * -1:
            for row in self.text:
                text = self.text_font.render(row, True, settings.TEXT_COLOR)
                text_position = ((self.screen.get_width() - text.get_width()) / 2, self.screen.get_height() + n)
                screen.blit(text, text_position)
                n += text.get_height() + y

            if not self.set_credit_text:
                self.credit_text_height = n
                self.set_credit_text = True
        else:
            screen.blit(self.pro_text_1, self.pro_text_1_pos)
            screen.blit(self.pro_text_2, self.pro_text_2_pos)

        self.start_pos -= self.text_speed

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
            self.reset()
            return True
        else:
            return False

    def reset(self):
        self.start_pos = 0
        self.set_credit_text = False
        self.is_credit_end = False
        self.credit_text_height = 0
