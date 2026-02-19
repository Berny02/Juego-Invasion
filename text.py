import pygame.sprite


class Damagetext(pygame.sprite.Sprite):
    """
    Sprite que muestra un texto flotante de daño en pantalla.
    """

    def __init__(self, x, y, damage, font, color):
        """
        Inicializa el texto de daño.

        Args:
            x (int): Posición X inicial.
            y (int): Posición Y inicial.
            damage (str): Texto a mostrar (daño).
            font (pygame.font.Font): Fuente para renderizar el texto.
            color (tuple): Color del texto.
        """
        super().__init__()
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.contador = 0

    def update(self, posicion_camara):
        """
        Actualiza la posición y animación del texto de daño.

        Args:
            posicion_camara (tuple): Desplazamiento de la cámara.
        """
        self.rect.x += posicion_camara[0]
        self.rect.y += posicion_camara[1]
        self.rect.y -= 2  # Mueve el texto hacia arriba
        self.contador += 1
        if self.contador >= 30:
            self.kill()
