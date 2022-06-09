
class Settings():
    """A classs to store all settings for Alien Invasion."""

    def __init__(self):
        '''Initizile the settings'''
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.ship_speed_factor = 1

        #bullet speed
        self.bullet_speed_factor = 3
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 3

        #alien settings
        self.alien_speed_factor = 5
        self.fleet_drop_speed = 20
        #fleet direction of 1 represnts right; -1 is left
        self.fleet_direction = 1

        #ship settings
        self.ship_limit = 3

        #how quickly the game speeds up
        self.speedup_scale = 1.1
        self.initilize_dynamic_settings()
        #point increases
        self.score_scale = 1.5


        #scoring
        self.alien_points = 50


    def initilize_dynamic_settings(self):
        """init setting that change througout the game """
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 3
        self.alien_speed_factor = .1
        self.fleet_direction = 1

    def increase_speed(self):
        ''' increase speed settings'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

