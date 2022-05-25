import pygame

class Man:
    '''a class to manage the player controlled man'''

    def __init__(self, om_game):
        '''initialise the man and set his starting position'''
        self.screen = om_game.screen
        self.screen_rect = om_game.screen.get_rect()
        self.settings = om_game.settings
        self.tomb_tiles = om_game.tomb_tiles
        self.revealed_tomb_tiles = om_game.revealed_tomb_tiles
        self.border_tiles = om_game.border_tiles
        self.path_tiles = om_game.path_tiles
        self.spawning_tile = om_game.spawning_tile

        # man movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # borders
        self.border_left = self.settings.border_left
        self.border_right = self.settings.border_right
        self.border_top = self.settings.border_top
        self.border_bottom = self.settings.border_bottom

        # load the man image and set its starting position (rect)
        self.image = pygame.image.load("images/om_man.bmp")
        self.rect = self.image.get_rect(midtop=(self.settings.start_x, self.settings.start_y))

        # start man in the centre top of the maze
        self.draw()

    def update(self):
        if self.moving_right:
            self.rect.x += self.settings.man_speed
            self._keep_within_border()
            self._check_tomb_tile_collision("right", self.tomb_tiles)
            self._check_tomb_tile_collision("right", self.revealed_tomb_tiles)
            self._check_tomb_tile_collision("right", self.spawning_tile)
        if self.moving_left:
            self.rect.x -= self.settings.man_speed
            self._keep_within_border()
            self._check_tomb_tile_collision("left", self.tomb_tiles)
            self._check_tomb_tile_collision("left", self.revealed_tomb_tiles)
            self._check_tomb_tile_collision("left", self.spawning_tile)
        if self.moving_up:
            self.rect.y -= self.settings.man_speed
            self._keep_within_border()
            self._check_tomb_tile_collision("up", self.tomb_tiles)
            self._check_tomb_tile_collision("up", self.revealed_tomb_tiles)
            self._check_tomb_tile_collision("up", self.spawning_tile)
        if self.moving_down:
            self.rect.y += self.settings.man_speed
            self._keep_within_border()
            self._check_tomb_tile_collision("down", self.tomb_tiles)
            self._check_tomb_tile_collision("down", self.revealed_tomb_tiles)
            self._check_tomb_tile_collision("down", self.spawning_tile)

    def _keep_within_border(self):
        if self.rect.right > self.border_right:
            self.rect.right = self.border_right
        if self.rect.left < self.border_left:
            self.rect.left = self.border_left
        if self.rect.top < self.border_top:
            self.rect.top = self.border_top
        if self.rect.bottom > self.border_bottom:
            self.rect.bottom = self.border_bottom

    def _check_tomb_tile_collision(self, direction, group):
        tomb_tile_collision = pygame.sprite.spritecollide(self, group, False, False)
        for tomb_tile in tomb_tile_collision:
            if self.rect.right > tomb_tile.rect.left and direction == "right":
                self.rect.right = tomb_tile.rect.left
            if self.rect.left < tomb_tile.rect.right and direction == "left":
                self.rect.left = tomb_tile.rect.right
            if self.rect.top < tomb_tile.rect.bottom and direction == "up":
                self.rect.top = tomb_tile.rect.bottom
            if self.rect.bottom > tomb_tile.rect.top and direction == "down":
                self.rect.bottom = tomb_tile.rect.top

    def start_new_level(self):
        self.rect = self.image.get_rect(midtop=(self.settings.start_x, self.settings.start_y))
        self.draw()

    def draw(self):
        '''draw the man'''
        self.screen.blit(self.image, self.rect)