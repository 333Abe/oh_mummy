import sys

import pygame
from tomb_tiles import TombTile

from settings import Settings
from men import Man

class OhMummy:
    '''main class to manage gameplay and behaviour'''

    def __init__(self):
        '''initialise the game'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Oh Mummy")
        # set background colour to black
        self.bg_colour = (0, 0, 0)

        self.man = Man(self)
        self.tiles = pygame.sprite.Group()
        self._create_tiles()

    def _create_tiles(self):
        '''create the tiles for the level'''
        y = 160
        x_offset = 220
        y_offset = 155
        for i in range(4):
            x = 75
            if i > 0:
                y += y_offset
            for j in range(5):
                if j > 0:
                    x += x_offset
                self.tile = TombTile(self, x, y)
                self.tiles.add(self.tile)

    def run_game(self):
        '''start the main game loop'''
        while True:
            self._manage_events()
            self._redraw_screen()

    def _manage_events(self):
        # manage keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.man.moving_right = True
                if event.key == pygame.K_LEFT:
                    self.man.moving_left = True
                if event.key == pygame.K_UP:
                    self.man.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.man.moving_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.man.moving_right = False
                if event.key == pygame.K_LEFT:
                    self.man.moving_left = False
                if event.key == pygame.K_UP:
                    self.man.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.man.moving_down = False

    def _redraw_screen(self):
        # redraw the screen
        self.screen.fill(self.bg_colour)
        self.tiles.draw(self.screen)
        self.man.update()
        self.man.draw()
        # draw updated screen
        pygame.display.flip()

if __name__ == "__main__":
    # make a game instance and run the game
    om = OhMummy()
    om.run_game()