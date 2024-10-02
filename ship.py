import pygame

class Ship:
    """Una clase para gestionar la nave del jugador"""

    def __init__(self, ia_game):
        """ Inicializa la nave y configura su posición inicial"""

        self.screen = ia_game.screen
        self.screen_rect = ia_game.screen.get_rect()

        # Carga la imagen de la nave y obtiene su rect.
        self.image = pygame.image.load('images/nave_jugador.bmp')
        self.rect = self.image.get_rect()

        # Coloca inicialmente cada nave nueva en el centro de la parte inferior de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom;

    def blime(self):
        """Dibuja la nave en su ubicación actual"""
        self.screen.blit(self.image,self.rect)