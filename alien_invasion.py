import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportamiento del juego"""

    def __init__(self):
        """Inicializa el juego y crea recursos."""
        pygame.init()
        self.settings = Settings()

        # Crea una pantalla completa
        """self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height"""

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
    

    def run_game(self):
        """Inicia el bucle principal del juego"""
        print("Iniciando juego...")
        while True:

            print("El bucle del juego esta corriendo...")
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            
            # Hace visible la última pantalla dibujada
            pygame.display.flip()

    def _check_events(self):
        # Busca eventos de teclado y ratón
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Cerrando el juego...")
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Responde a las pulsaciones de teclas."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            print("Cerrando el juego...")
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responde a las liberaciones de teclas."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
         """Crea una bala y la añade al grupo de balas."""
         if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Actualiza la posición de las balas y elimina las antiguas."""
        # Actualiza la ubicación de las balas
        self.bullets.update()

        # Elimina las balas que han salido de la pantalla
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        # Actualiza las imagenes en la pantalla y cambia a la pantalla nueva
            self.back_ground = pygame.transform.scale(self.settings.back_ground, 
                          (self.settings.screen_width, self.settings.screen_height))
            # Dibujar la imagen de fondo
            self.screen.blit(self.back_ground, (0, 0))
            # Dibujar la nave
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

        
if __name__ == '__main__':

    # Hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    ai.run_game();


