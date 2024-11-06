from pygame import image

class Settings:
    """Clase para gestionar la configuración del juego"""

    def __init__(self):
        """Inicializa la configuración estática del juego"""

        # Configuración de la nave
        self.ship_limit = 3

        # Configuración de los aliens
        self.fleet_drop_speed = 10
        
        #Configuración de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.back_ground = image.load('images/space_bg.bmp')
        self.bg_color = (230, 230, 230)

        # Configuración de las balas
        self.bullet_width = 10
        self.bullet_height = 20
        self.bullet_color = (200, 0, 0)
        self.bullets_allowed = 3

        # Velocidad con la que se acelera el juego
        self.speedup_scale = 1.1

        # Indice de aumento de puntos
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa la configuración dinamica del juego"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction de 1 representa la derecha, -1 representa la izquierda.
        self.fleet_direction = 1

        # Puntuación
        self.alien_points = 50

    def increse_speed(self):
        """Aumenta la velocidad del juego y los valores en puntos de los aliens"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)