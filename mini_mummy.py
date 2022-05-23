import sys

import pygame
from tomb_tiles import *

from mini_settings import Settings
from men import Man
from mummy import Mummy

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

        self.tomb_tiles = pygame.sprite.Group()
        self.revealed_tomb_tiles = pygame.sprite.Group()
        self.border_tiles = pygame.sprite.Group()
        self.path_tiles = pygame.sprite.Group()
        self.visited_path_tiles = pygame.sprite.Group()
        self._populate_from_map("map/1100x900_border.txt")
        self._populate_from_map("map/1100x900_tiles.txt")
        self.man = Man(self)
        self.man_lives = self.settings.man_lives
        self.man_start_x = self.settings.start_x
        self.man_start_y = self.settings.start_y
        self.mummies = pygame.sprite.Group()
        self.number_of_mummies = self.settings.number_of_mummies
        self.mummy_start_x = self.settings.mummy_start_x
        self.mummy_start_y = self.settings.mummy_start_y
        self._create_mummies(self.mummy_start_x, self.mummy_start_y)


    def _create_mummies(self, x, y):
        for mummy in range(self.number_of_mummies):
            self.mummy = Mummy(self, x, y)
            self.mummies.add(self.mummy)

    def _populate_from_map(self, map_file):
        '''create the border and path tiles'''
        with open(map_file) as file_object:
            lines = file_object.readlines()
        y = -25
        offset = 25
        for line in lines:
            x = 0
            y += 25
            for char in line:
                if char == "1":
                    self.border_tile = BorderTile(self, x, y)
                    self.border_tiles.add(self.border_tile)
                elif char == "2":
                    self.path_tile = PathTile(self, x, y)
                    self.path_tiles.add(self.path_tile)
                elif char == "3":
                    self.tomb_tile = TombTile(self, x, y)
                    self.tomb_tiles.add(self.tomb_tile)
                x += offset

    def run_game(self):
        '''start the main game loop'''
        while True:
            self._manage_events()
            self.man.update()
            for mummy in self.mummies:
                mummy.update_mummy()
            self._mummy_attacks()
            self._reveal_path()
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

    def _mummy_attacks(self):
        '''check for mummy collisions'''
        mummy_man_collision = pygame.sprite.spritecollide(self.man, self.mummies, True)
        for collison in mummy_man_collision:
            self.man_lives -= 1
            self._create_mummies(self.mummy_start_x, self.mummy_start_y)
            self.man.rect.midtop = (self.man_start_x, self.man_start_y)
            if self.man_lives <= 0:
                sys.exit()

    def _reveal_path(self):
        '''show path tiles which have been visited'''
        path_tile_collision = pygame.sprite.spritecollide(self.man, self.path_tiles, False, False)
        for path_tile in path_tile_collision:
            path_tile.image = pygame.image.load("images/path_dot.bmp")
            self.visited_path_tiles.add(path_tile)
            self.path_tiles.remove(path_tile)
            self._reveal_tomb_tiles()


    def _reveal_tomb_tiles(self):
        '''reveal tomb tiles which have have been surrounded by revealed path tiles'''
        for tomb_tile in self.tomb_tiles:
            number_path_tiles = 0
            tomb_tile_reveal_collision = pygame.sprite.spritecollide(tomb_tile, self.visited_path_tiles, False, False)
            for visited_path_tile in tomb_tile_reveal_collision:
                number_path_tiles += 1
            if number_path_tiles == 8:
                tomb_tile.image = pygame.image.load("images/sarcophagus.bmp")
                self.revealed_tomb_tiles.add(tomb_tile)
                self.tomb_tiles.remove(tomb_tile)

    def _redraw_screen(self):
        # redraw the screen
        self.screen.fill(self.bg_colour)
        self.path_tiles.draw(self.screen)
        self.visited_path_tiles.draw(self.screen)
        self.tomb_tiles.draw(self.screen)
        self.revealed_tomb_tiles.draw(self.screen)
        self.border_tiles.draw(self.screen)
        for mummy in self.mummies:
            mummy.draw()
        self.man.draw()
        # draw updated screen
        pygame.display.flip()

if __name__ == "__main__":
    # make a game instance and run the game
    om = OhMummy()
    om.run_game()