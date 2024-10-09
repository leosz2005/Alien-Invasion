from pygame import image

class Settings:
    """Clase para gestionar la configuración del juego"""

    def __init__(self):
        """Inicializa la configuración del juego"""

        # Configuración de la nave
        self.ship_speed = 1.
        self.ship_limit = 3

        # Configuración de los aliens
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction = 1 representa derecha; -1 representa izquierda
        self.fleet_direction = 1
        
        #Configuración de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.back_ground = image.load('images/space_bg.bmp')

        # Configuración de las balas
        self.bullet_speed = 2
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (200, 0, 0)
        self.bullets_allowed = 3