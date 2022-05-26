import pygame
from pygame.sprite import Sprite
import random

class Mummy(Sprite):
    '''a class to create an enemy mummy'''
    def __init__(self, om_game, x, y):
        '''initialise the mummy and set his starting position'''
        super().__init__()
        self.screen = om_game.screen
        self.screen_rect = om_game.screen.get_rect()
        self.settings = om_game.settings
        self.tomb_tiles = om_game.tomb_tiles
        self.revealed_tomb_tiles = om_game.revealed_tomb_tiles
        self.border_tiles = om_game.border_tiles
        self.path_tiles = om_game.path_tiles
        self.spawning_tile = om_game.spawning_tile
        self.man = om_game.man

        # mummy movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # borders
        self.border_left = self.settings.border_left
        self.border_right = self.settings.border_right
        self.border_top = self.settings.border_top
        self.border_bottom = self.settings.border_bottom

        # load the mummy image and set its starting position (rect)
        self.image = pygame.image.load("images/om_mummy.bmp")

        # start mummmy in the centre bottom of the maze
        self.rect = self.image.get_rect(midtop=(x, y))
        self.start_mummy()
        self.draw()

    def start_mummy(self):
        initial_direction = random.randint(1, 2)
        if initial_direction == 1:
            self.moving_right = True
        else:
            self.moving_left = True

    def update_mummy(self):
        for speed in range(self.settings.mummy_speed):
            junction = self._notice_junction()
            if junction == True:
                self._make_decision()
            self._move_mummy()

    def _make_decision(self):
        while True:
            # mummy initially decides if they should go straight
            keep_straight = random.randint(1, 10)
            if keep_straight > self.settings.mummy_juction_direction_change:
                #if its not keeping straight, should it chase the man, or choose a random direction?
                turn_towards_man = random.randint(1, 10)
                if turn_towards_man < self.settings.mummy_turn_towards_man_chance:
                    self._chase_man()
                else:
                    self._choose_random_direction()
                            #move mummy
            #check it's not moving into a border or tile
            hit_something = self._move_mummy_with_collision_detection()
            #if nothing has been hit, break loop
            if hit_something == False:
                break
        return

    def _chase_man(self):
        mummy_x = self.rect.x
        mummy_y = self.rect.y
        man_x = self.man.rect.x
        man_y = self.man.rect.y

        x_axis = mummy_x - man_x
        y_axis = mummy_y - man_y

        if abs(x_axis) < abs(y_axis):
            if y_axis > 0:
                self.moving_right = False
                self.moving_left = False
                self.moving_up = True
                self.moving_down = False
            else:
                self.moving_right = False
                self.moving_left = False
                self.moving_up = False
                self.moving_down = True
        else:
            if x_axis > 0:
                self.moving_right = False
                self.moving_left = True
                self.moving_up = False
                self.moving_down = False
            else:
                self.moving_right = True
                self.moving_left = False
                self.moving_up = False
                self.moving_down = False
        return

    def _choose_random_direction(self):
        while True:
            #choose random direction
            direction = random.randint(1, 4)
            if direction == 1:
                self.moving_right = True
                self.moving_left = False
                self.moving_up = False
                self.moving_down = False
            elif direction == 2:
                self.moving_right = False
                self.moving_left = True
                self.moving_up = False
                self.moving_down = False
            elif direction == 3:
                self.moving_right = False
                self.moving_left = False
                self.moving_up = True
                self.moving_down = False
            elif direction == 4:
                self.moving_right = False
                self.moving_left = False
                self.moving_up = False
                self.moving_down = True
            #move mummy
            hit_something = self._move_mummy_with_collision_detection()
            #check nothing has been hit
            if hit_something == False:
                break
            #if nothing has been hit, break loop
        return

    def _notice_junction(self):
        '''check of the mummy is at a junction'''
        pos_x = self.rect.center[0]
        pos_y = self.rect.center[1]
        if (pos_x - 50) % 200 == 0:
            if (pos_y - 50) % 200 == 0:
                return True
        return False

    def _move_mummy(self):
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1
        if self.moving_up:
            self.rect.y -= 1
        if self.moving_down:
            self.rect.y += 1

    def _move_mummy_with_collision_detection(self):
        if self.moving_right:
            self.rect.x += 1
            hit_border = self._keep_within_border()
        if self.moving_left:
            self.rect.x -= 1
            hit_border = self._keep_within_border()
        if self.moving_up:
            self.rect.y -= 1
            hit_border = self._keep_within_border()
        if self.moving_down:
            self.rect.y += 1
            hit_border = self._keep_within_border()
        if hit_border == True:
            return True
        return False

    def _keep_within_border(self):
        '''check if mummy has moved into border'''
        if self.rect.right > self.border_right:
            self.rect.right = self.border_right
            return True
        if self.rect.left < self.border_left:
            self.rect.left = self.border_left
            return True
        if self.rect.top < self.border_top:
            self.rect.top = self.border_top
            return True
        if self.rect.bottom > self.border_bottom:
            self.rect.bottom = self.border_bottom
            return True
        return False

    def _check_tomb_tile_collision(self, direction, group):
        '''check if mummy has moved into a tomb tile'''
        tomb_tile_collision = pygame.sprite.spritecollide(self, group, False, False)
        for tomb_tile in tomb_tile_collision:
            if self.rect.right > tomb_tile.rect.left and direction == "right":
                self.rect.right = tomb_tile.rect.left
                return True
            if self.rect.left < tomb_tile.rect.right and direction == "left":
                self.rect.left = tomb_tile.rect.right
                return True
            if self.rect.top < tomb_tile.rect.bottom and direction == "up":
                self.rect.top = tomb_tile.rect.bottom
                return True
            if self.rect.bottom > tomb_tile.rect.top and direction == "down":
                self.rect.bottom = tomb_tile.rect.top
                return True
        return False

    def draw(self):
        '''draw the mummy'''
        self.screen.blit(self.image, self.rect)