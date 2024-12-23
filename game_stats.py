import json
import os

HIGH_SCORE_FILE = 'high_score.json'
class GameStats:
    """ Sigue las estadistas del Alien Invasion"""

    def __init__(self, ai_game):
        """ Inicializa las estadísticas"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Inicia Alien invasion en un estado inactivo
        self.game_active = False

        # La puntuación no debería reiniciarse
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                content = f.read()
                if content:
                    self.high_score = json.loads(content)
                else:
                    self.high_score = 0
                
        else:
            with open(HIGH_SCORE_FILE, 'w') as f:
                self.high_score = 0
                json.dump(self.high_score, f)

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump(self.high_score, f) 

    def reset_stats(self):
        """ Inicializa las estadísticas que pueden cambiar durante el juego"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1