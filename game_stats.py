

class Gamestats():
    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats(self.ai_settings)
        self.game_active = False
        self.score = 0
        self.high_score = 0

    def reset_stats(self,ai_settings):
        self.ships_left = ai_settings.ship_limit
        self.level = 1
