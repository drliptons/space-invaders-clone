import pygame


class Game:
    def __init__(self, name, w, h):
        self.game_name = name
        self.width = w
        self.height = h

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.game_name)
        self.current_state = None
        self.game_over = False

    def run(self, state):
        # game_over = False
        self.current_state = state
        clock = pygame.time.Clock()

        while not self.game_over:
            clock.tick(30)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.game_over = True
            self.screen.fill((0, 0, 0))
            self.current_state = self.current_state.update(events)
            self.current_state.draw(self.screen)
            pygame.display.update()
        pygame.quit()
