import sys

import pygame

from settings import Settings

class OhMummy:
    '''main class to manage gameplay and behaviour'''

    def __init__(self):
        '''initialise the game'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Oh Mummy")

        # set background colour to black
        self.bg_colour = (0, 0, 0)

    def run_game(self):
        '''start the main game loop'''
        while True:
            # manage keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # redraw the screen
            self.screen.fill(self.bg_colour)

            # draw updated screen
            pygame.display.flip()

if __name__ == "__main__":
    # make a game instance and run the game
    om = OhMummy()
    om.run_game()