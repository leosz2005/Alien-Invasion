import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

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

        # Crea una instancia para gestionar las estadísticas del juego,
        # y crea un marcador
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Crea el botoón Play
        self.play_button = Button(self, "Play")
    

    def run_game(self):
        """Inicia el bucle principal del juego"""
        print("Iniciando juego...")
        while True:
            self._check_events()

            print("El bucle del juego esta corriendo...")
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Inicia un juego nuevo cuando el jugador hace clic en el botón Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reinicia las configuraciones del juego
            self.settings.initialize_dynamic_settings()

            # Restablece las estadisticas del juego.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Se deshace de los aliens y las balas que quedan.
            self.aliens.empty()
            self.bullets.empty()

            # Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            # Oculta el cursor del ratón.
            pygame.mouse.set_visible(False)
        

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

    def _ship_hit(self):
        """ Responde al impacto de un alien con la nave."""
        if self.stats.ships_left > 0:
            # Decrementa la cantidad de naves restantes y actualiza el marcador
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Limpia la lista de balas y los aliens
            self.bullets.empty()
            self.aliens.empty()

            # Crea una nueva flota y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            # Detiene el juego
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Responde a las colisiones entre balas y aliens."""
        # Elimina las balas y aliens que hayan colisionado
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
  
        if not self.aliens:
            # Elimina las balas restantes y crea una nueva flota
            self.bullets.empty()
            self._create_fleet()
            self.settings.increse_speed()

            # Aumenta el nivel del juego
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """ Comprueba si la flota esta en un borde y actualiza la ubicación de todos los aliens en la flota."""
        self._check_fleet_edges()
        self.aliens.update()

        # Comprueba la colision entre la nave y los aliens
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Comprueba si hay aliens que han alcanzado la parte inferior de la pantalla
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """ COmprueba si algún alien se encuentra debajo de la pantalla."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Trata este caso de colision con la nave
                self._ship_hit()
                break

    def _create_fleet(self):
        """Crea la flota de aliens."""
        # Crea un alien y halla el numero de aliens en una fila
        # Espacio entre aliens es igual a la anchura de un alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avalable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avalable_space_x // (2 * alien_width)

        # Determine el numero de filas de aliens que caben en la pantalla
        ship_height = self.ship.rect.height
        avalable_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height)
        number_rows = avalable_space_y // (2 * alien_height)

        # Crea la flota completa de aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """ Devuelve True si el alien se encuentra en el borde de la pantalla"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Baja la flota y cambia su direccion"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        """Crea un alien y lo coloca en la primera fila"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        """Actualiza las imagenes en la pantalla y cambia a la pantalla nueva"""
        self.back_ground = pygame.transform.scale(self.settings.back_ground, 
                          (self.settings.screen_width, self.settings.screen_height))
            
        # Dibujar la imagen de fondo
        self.screen.blit(self.back_ground, (0, 0))

        # Dibujar la nave
        self.ship.blitme()
        for bullet in self.bullets.sprites():
                bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Dibuja la información de puntuación
        self.sb.show_score()

        # Dibuja el botón para jugar si el juego está iniciado
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        # Hace visible la última pantalla dibujada
        pygame.display.flip()

            

        
if __name__ == '__main__':

    # Hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    ai.run_game();


