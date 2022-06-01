import pygame.font


class Scoreboard:
    '''oh mummy scoreboard class'''

    def __init__(self, om_game):
        '''initialise scoreboard'''
        self.screen = om_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = om_game.settings
        self.stats = om_game.stats

        # font settings
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial state for the score, lives and collected tiles
        self.prep_score()
        self.prep_lives()
        self.prep_scroll("images/tile_sand.bmp")
        self.prep_key("images/tile_sand.bmp")
        self.prep_sarcophagus("images/tile_sand.bmp")

    def prep_score(self):
        '''turn the score into a rendered image'''
        score_string = "Score: " + str(self.stats.score)
        self.score_image = self.font.render(score_string, True, self.text_colour, self.settings.bg_colour)

        # display the score in the info pane on the right
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 45
        self.score_rect.top = 50

    def prep_lives(self):
        '''show how many lives are left next to an image of the man'''
        self.man_image = pygame.image.load("images/om_man.bmp")
        self.man_image_rect = self.man_image.get_rect()
        self.man_image_rect.right = self.screen_rect.right - 325
        self.man_image_rect.top = 40

        lives_string = " x " + str(self.stats.man_lives)
        self.lives_image = self.font.render(lives_string, True, self.text_colour, self.settings.bg_colour)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.man_image_rect.right
        self.lives_rect.top = 50

    def prep_scroll(self, image):
        '''prep the scroll to be displayed when it's collected'''
        self.scroll_image = pygame.image.load(image)
        self.scroll_rect = self.scroll_image.get_rect()
        self.scroll_rect.left = 1212
        self.scroll_rect.top = 150

    def prep_key(self, image):
        '''prep the key to be displayed when it's collected'''
        self.key_image = pygame.image.load(image)
        self.key_rect = self.key_image.get_rect()
        self.key_rect.left = 1212
        self.key_rect.top = 325

    def prep_sarcophagus(self, image):
        '''prep the sarcophagus to be displayed when it's collected'''
        self.sarcophagus_image = pygame.image.load(image)
        self.sarcophagus_rect = self.sarcophagus_image.get_rect()
        self.sarcophagus_rect.left = 1212
        self.sarcophagus_rect.top = 500

    def show_score(self):
        '''draw the score to the screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.man_image, self.man_image_rect)
        self.screen.blit(self.lives_image, self.lives_rect)
        self.screen.blit(self.scroll_image, self.scroll_rect)
        self.screen.blit(self.key_image, self.key_rect)
        self.screen.blit(self.sarcophagus_image, self.sarcophagus_rect)