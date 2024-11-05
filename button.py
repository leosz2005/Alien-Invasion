import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        """Inicializa los atributos del botón"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # establece las dimensiones y propiedades del botón
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # construye el rectángulo del botón y lo centra
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # el mensaje del botón debe ser preparado solo una vez
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Convierte el mensaje en una superficie renderizada y centra el texto en el botón"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                           self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # dibuja el botón en su ubicación actual
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)