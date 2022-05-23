class Settings:
    '''settings class for Oh Mummy'''

    def __init__(self):
        '''initialise the game's settings'''

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (0, 0, 0)

        # tile settings
        #self.tile_width = 170
        #self.tile_height = 105
        #self.tile_colour = (50, 80, 100)

        # border settings
        self.horizontal_border_width = 1150
        self.horizontal_border_height = 25
        self.vertical_border_width = 25
        self.vertical_border_height = 800
        self.border_colour = (100, 100, 100)

        # man settings
        self.man_speed = 10
        self.man_lives = 3
        self.start_x = 600
        self.start_y = 110