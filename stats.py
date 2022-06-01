class OM_Statistics:
    '''track game statistics for oh mummy'''

    def __init__(self, om_game):
        '''initalise game stats'''
        self.settings = om_game.settings
        self.new_game_reset_stats()

    def new_game_reset_stats(self):
        '''initialise stats for start of new game'''
        self.man_lives = self.settings.man_lives
        self.score = 0
        self.level = 1
        self.tomb_size = 5 # if a has tomb has 5 levels, second level will be displayed as "Room: 2 of 5"
        self.completed_tombs = 0