import sys
import pygame
import random
import time

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
        self.exit_activated = pygame.sprite.Group()
        self.spawning_tile = pygame.sprite.Group()
        self.mummies = pygame.sprite.Group()
        self.mummy_spawn_flash_frequency = 0.3
        self.mummy_spawn_time = 5
        self.exit_flash_frequency = 0.1
        self.man = Man(self)
        self.man_start_x = self.settings.start_x
        self.man_start_y = self.settings.start_y
        self.mummy_start_x = self.settings.mummy_start_x
        self.mummy_start_y = self.settings.mummy_start_y
        self.open_tomb_rooms = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5]
        self._start_new_game()

    def _start_new_game(self):
        self._populate_from_map("map/1100x900_border.txt")
        self.man_lives = self.settings.man_lives
        self.number_of_mummies = 0
        self.score = 0
        self._set_up_new_level()

    def _set_up_new_level(self):
        self.mummy_spawning = False
        self.mummy_spawn_flash_count = 0
        self.spawn_reveal_time = None
        self.scroll = False
        self.number_of_mummies += 1
        for mummy in self.mummies:
            self.mummies.remove(mummy)
        for tile in self.revealed_tomb_tiles:
            self.revealed_tomb_tiles.remove(tile)
        for tile in self.tomb_tiles:
            self.tomb_tiles.remove(tile)
        for tile in self.visited_path_tiles:
            self.visited_path_tiles.remove(tile)
        for tile in self.path_tiles:
            self.path_tiles.remove(tile)
        for tile in self.spawning_tile:
            self.spawning_tile.remove(tile)
        self._populate_from_map("map/1100x900_tiles.txt")
        self.man.start_new_level()
        self._create_mummies(self.mummy_start_x, self.mummy_start_y)
        self.key = False
        self.sarcophagus = False
        self.exit_flash_count = 0
        self.exit_tile = ExitTile(self, (random.randint(0, 5) * 200) + 25, (random.randint(0, 4) * 200) + 25)

    def _create_mummies(self, x, y):
        for mummy in range(self.number_of_mummies):
            self.mummy = Mummy(self, x, y)
            self.mummies.add(self.mummy)

    def _populate_from_map(self, map_file):
        '''create the border and path tiles'''
        shuffled_tombs = random.sample(self.open_tomb_rooms, 20)
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
                    self.tomb_tile = TombTile(self, x, y, shuffled_tombs.pop())
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
            self._exit_level()
            self._redraw_screen()

    def _manage_events(self):
        # manage keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    self.man.moving_right = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_k:
                    self.man.moving_left = True
                if event.key == pygame.K_UP or event.key == pygame.K_a:
                    self.man.moving_up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_z:
                    self.man.moving_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    self.man.moving_right = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_k:
                    self.man.moving_left = False
                if event.key == pygame.K_UP or event.key == pygame.K_a:
                    self.man.moving_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_z:
                    self.man.moving_down = False

    def _mummy_attacks(self):
        '''check for mummy collisions'''
        mummy_man_collision = pygame.sprite.spritecollide(self.man, self.mummies, True)
        for collison in mummy_man_collision:
            if self.scroll == False:
                self.man_lives -= 1
                self._lose_a_life()
            else:
                self.scroll = False
                self.score += 50
            self.number_of_mummies -= 1
            if self.man_lives <= 0:
                print(f"You scored {self.score}")
                sys.exit()

    def _exit_level(self):
        '''check for man getting to the exit'''
        man_exit = pygame.sprite.spritecollide(self.man, self.exit_activated, True)
        if man_exit:
            self.score += 100
            self._set_up_new_level()

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
                if tomb_tile.tomb_type == 1:
                    tomb_tile.image = pygame.image.load("images/treasure.bmp")
                    self.score += 10
                elif tomb_tile.tomb_type == 2:
                    tomb_tile.image = pygame.image.load("images/scroll.bmp")
                    self.scroll = True
                elif tomb_tile.tomb_type == 3:
                    tomb_tile.image = pygame.image.load("images/key.bmp")
                    self.key = True
                    if self.sarcophagus:
                        self.exit_activated.add(self.exit_tile)
                        self.exit_opening_time = time.time()
                elif tomb_tile.tomb_type == 4:
                    tomb_tile.image = pygame.image.load("images/sarcophagus.bmp")
                    self.sarcophagus = True
                    if self.key:
                        self.exit_activated.add(self.exit_tile)
                        self.exit_opening_time = time.time()
                elif tomb_tile.tomb_type == 5:
                    tomb_tile.image = pygame.image.load("images/mummy_2.bmp")
                    self.mummy_spawning = True
                    self.spawn_reveal_time = time.time()
                    self.mummy_spawn_flash_count = 0
                if tomb_tile.tomb_type == 5:
                    self.spawning_tile.add(tomb_tile)
                else:
                    self.revealed_tomb_tiles.add(tomb_tile)
                self.tomb_tiles.remove(tomb_tile)

    def spawn_mummy_from_tomb(self, tomb_tile):
        spawn_position = random.randint(1, 4)
        if spawn_position == 1:
            self.mummy = Mummy(self, tomb_tile.rect.x - 25, tomb_tile.rect.y - 50)
        elif spawn_position == 2:
            self.mummy = Mummy(self, tomb_tile.rect.x - 25 , tomb_tile.rect.y + 150)
        elif spawn_position == 3:
            self.mummy = Mummy(self, tomb_tile.rect.x + 175, tomb_tile.rect.y + 150)
        else:
            self.mummy = Mummy(self, tomb_tile.rect.x + 200, tomb_tile.rect.y - 50)
        self.mummies.add(self.mummy)
        self.number_of_mummies += 1
        self.mummy_spawning = False
        self.revealed_tomb_tiles.add(tomb_tile)
        self.spawning_tile.remove(tomb_tile)
        self.spawn_reveal_time = None

    def _lose_a_life(self):
        time_of_death = time.time()
        man_flash_count = 0
        while time.time() < time_of_death + 1:
            if man_flash_count % 2 == 0:
                image_file = pygame.image.load("images/dead_om_man.bmp")
            else:
                image_file = pygame.image.load("images/om_man.bmp")
            if time.time() >= time_of_death + (0.1 * man_flash_count):
                self.man.draw(image_file)
                man_flash_count += 1
                pygame.display.flip()

    def _flash_tile(self, instance_time, frequency, count, tile, group, image_file):
        if time.time() >= instance_time + (frequency * count):
            for tile in group:
                tile.image = pygame.image.load(image_file)
            count += 1
            return count
        return count

    def _redraw_screen(self):
        # redraw the screen
        self.screen.fill(self.bg_colour)
        self.path_tiles.draw(self.screen)
        self.visited_path_tiles.draw(self.screen)
        self.tomb_tiles.draw(self.screen)
        self.revealed_tomb_tiles.draw(self.screen)
        self.border_tiles.draw(self.screen)
        if self.mummy_spawning == True:
            if self.mummy_spawn_flash_count * self.mummy_spawn_flash_frequency >= self.mummy_spawn_time:
                for tile in self.spawning_tile:
                    tile.image = pygame.image.load("images/mummy_1.bmp")
                    self.spawn_mummy_from_tomb(tile)
                    self.mummy_spawn_flash_count = 0
            else:
                if self.mummy_spawn_flash_count % 2 == 0:
                    image_file = "images/mummy_2.bmp"
                else:
                    image_file = "images/mummy_1.bmp"
                for tile in self.spawning_tile:
                    self.mummy_spawn_flash_count = self._flash_tile(
                        self.spawn_reveal_time,
                        self.mummy_spawn_flash_frequency,
                        self.mummy_spawn_flash_count,
                        tile,
                        self.spawning_tile,
                        image_file)
            if self.spawning_tile:
                self.spawning_tile.draw(self.screen)
        for mummy in self.mummies:
            mummy.draw()
        self.man.draw(self.man.image)
        if self.key and self.sarcophagus:
            if self.exit_flash_count % 2 == 0:
                image_file = "images/exit_2.bmp"
            else:
                image_file = "images/exit_1.bmp"
            for tile in self.exit_activated:
                self.exit_flash_count = self._flash_tile(
                    self.exit_opening_time,
                    self.exit_flash_frequency,
                    self.exit_flash_count,
                    tile,
                    self.exit_activated,
                    image_file)
            self.exit_activated.draw(self.screen)
        # draw updated screen
        pygame.display.flip()

if __name__ == "__main__":
    # make a game instance and run the game
    om = OhMummy()
    om.run_game()