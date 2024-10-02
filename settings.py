from pygame import image

class Settings:

    def __init__(self):
        """Inicializa la configuración del juego"""
        
        #Configuración de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.back_ground = image.load('images/space_bg.bmp')