import pygame
from pygame.sprite import Sprite

class Tile(Sprite):
    '''class for all tiles'''
    def __init__(self, om_game):
        super().__init__()
        self.screen = om_game.screen
        self.settings = om_game.settings

class TombTile(Tile):
    '''a class to create a tombtile'''
    def __init__(self, om_game, x, y):
        '''initialise a tile'''
        super().__init__(om_game)
        self.image = pygame.image.load("images/tile_sand.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # starting coordinates = (75, 210)
        # path between tiles = 50

class BorderTile(Tile):
    '''class to create a border tile'''
    def __init__(self, om_game, x, y):
        '''initialise a border tile'''
        super().__init__(om_game)
        self.image = pygame.image.load("images/border.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PathTile(Tile):
    '''class to create a path tile'''
    def __init__(self, om_game, x, y):
        '''initialise a path tile'''
        super().__init__(om_game)
        self.image = pygame.image.load("images/path_black.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y