import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportamiento del juego"""

    def __init__(self):
        """Inicializa el juego y crea recursos."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
    

    def run_game(self):
        """Inicia el bucle principal del juego"""
        print("Iniciando juego...")
        while True:

            print("El bucle del juego esta corriendo...")
            self._check_events()
            self._update_screen()

            
            # Hace visible la última pantalla dibujada
            pygame.display.flip()

    def _check_events(self):
        # Busca eventos de teclado y ratón
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Cerrando el juego...")
                    sys.exit()

    def _update_screen(self):
        # Actualiza las imagenes en la pantalla y cambia a la pantalla nueva
            self.back_ground = pygame.transform.scale(self.settings.back_ground, 
                          (self.settings.screen_width, self.settings.screen_height))
            # Dibujar la imagen de fondo
            self.screen.blit(self.back_ground, (0, 0))
            # Dibujar la nave
            self.ship.blitme()

        
if __name__ == '__main__':

    # Hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    ai.run_game();


