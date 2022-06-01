class Settings:
    '''settings class for Oh Mummy'''

    def __init__(self):
        '''initialise the game's settings'''

        # screen settings
        self.screen_width = 1500
        self.screen_height = 900
        self.bg_colour = (0, 0, 0)

        # border settings
        self.border_width = 25
        self.border_left = self.border_width
        self.border_right = self.screen_width - self.border_width - 400
        self.border_top = self.border_width
        self.border_bottom = self.screen_height - self.border_width

        # man settings
        self.man_speed = 10
        self.man_lives = 3
        self.start_x = 550
        self.start_y = 25

        # mummy settings
        # Ashayet
        self.ashayet_image = "images/ashayet.bmp"
        self.ashayet_speed = 5
        self.ashayet_junction_direction_change = 6
        self.ashayet_turn_towards_man_chance = 6

        # Siptah
        self.siptah_image = "images/siptah.bmp"
        self.siptah_speed = 7
        self.siptah_junction_direction_change = 4
        self.siptah_turn_towards_man_chance = 4

        # Pentaweret
        self.pentaweret_image = "images/pentaweret.bmp"
        self.pentaweret_speed = 4
        self.pentaweret_junction_direction_change = 8
        self.pentaweret_turn_towards_man_chance = 8

        self.mummy_start_x = 550
        self.mummy_start_y = 825
        self.mummy_spawn_flash_frequency = 0.3
        self.mummy_spawn_time = 5

        # scoring
        self.found_treasure = 10
        self.used_scroll = 50
        self.finished_level = 100

        # exit settings
        self.exit_flash_frequency = 0.1