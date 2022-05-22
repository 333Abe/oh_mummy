class Settings:
    '''settings class for Oh Mummy'''

    def __init__(self):
        '''initialise the game's settings'''

        # screen settings
        self.screen_width = 1100
        self.screen_height = 900
        self.bg_colour = (0, 0, 0)

        # border settings
        self.border_width = 25
        self.border_left = self.border_width
        self.border_right = self.screen_width - self.border_width
        self.border_top = self.border_width
        self.border_bottom = self.screen_height - self.border_width

        # man settings
        self.man_speed = 10
        self.man_lives = 3
        self.start_x = 550
        self.start_y = 25

        # mummy settings
        self.mummy_speed = 10
        self.mummy_start_x = 550
        self.mummy_start_y = 875
        self.mummy_juction_direction_change = 0
        self.mummy_turn_towards_man_chance = 11