class GameStats():
    """Class to record game stats"""
    def __init__(self, ai_settings):
        """init stats"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #start alien invasion in an active state
        self.game_active = False
        self.score = 0

        #high score
        a = 0
        with open('highscore.txt') as f:
            for line in f:
                a = line


        self.high_score = int(a)


    def reset_stats(self):
        """reset stats"""
        self.ships_left = self.ai_settings.ship_limit
