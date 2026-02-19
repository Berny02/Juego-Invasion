import pygame
import math
import constantes as c
import random


class Arma:
    """
    Clase que representa un arma que puede disparar balas en el juego.
    """

    def __init__(self, image, img_bala, sonido_disparo):
        """
        Inicializa el arma.

        Args:
            image (pygame.Surface): Imagen del arma.
            img_bala (pygame.Surface): Imagen de la bala.
            sonido_disparo (pygame.mixer.Sound): Sonido que se reproduce al disparar.
        """
        self.img_bala = img_bala
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.forma = self.image.get_rect()
        self.disparado = False
        self.ultimo_disparo = pygame.time.get_ticks()
        self.sonido_disparo = sonido_disparo

    def update(self, personaje):
        """
        Actualiza la posición y el ángulo del arma, y gestiona el disparo de balas.

        Args:
            personaje (Personaje): Referencia al personaje que sostiene el arma.

        Returns:
            Bala o None: Devuelve una instancia de Bala si se dispara, si no devuelve None.
        """
        disparo_cooldown = 200  # tiempo entre disparos en milisegundos
        bala = None
        self.forma.center = personaje.shape.center
        if personaje.flip == False:
            self.forma.x += 15
            self.rotar(False)
        if personaje.flip == True:
            self.forma.x -= 15
            self.rotar(True)
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.forma.centerx
        dy = mouse_pos[1] - self.forma.centery
        self.angle = math.degrees(math.atan2(-dy, dx))

        # detectar clicks del mouse
        if (
            pygame.mouse.get_pressed()[0]
            and self.disparado == False
            and (pygame.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown)
        ):
            bala = Bala(
                self.img_bala, self.forma.centerx, self.forma.centery, self.angle
            )
            self.sonido_disparo.play()
            self.disparado = True
            self.ultimo_disparo = pygame.time.get_ticks()
            return bala
        if pygame.mouse.get_pressed()[0] == False:
            self.disparado = False
            return bala

    def dibujar(self, screen):
        """
        Dibuja el arma en pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se dibuja el arma.
        """
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        screen.blit(self.image, self.forma)

    def rotar(self, rotar):
        """
        Rota el arma según el ángulo calculado y el estado de flip.

        Args:
            rotar (bool): Si True, voltea la imagen horizontalmente.
        """
        angle = self.angle
        if rotar:
            image_flip = pygame.transform.flip(self.original_image, True, False)
            self.image = pygame.transform.rotate(image_flip, -angle)
        else:
            self.image = pygame.transform.rotate(self.original_image, angle)


class Bala(pygame.sprite.Sprite):
    """
    Clase que representa una bala disparada por el arma.
    """

    def __init__(self, image, x, y, angle):
        """
        Inicializa la bala.

        Args:
            image (pygame.Surface): Imagen de la bala.
            x (int): Posición X inicial.
            y (int): Posición Y inicial.
            angle (float): Ángulo de disparo en grados.
        """
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(x, y - 15))
        self.angle = angle
        # Calclulo de velocidad de la bala
        self.delta_x = c.VELOCIDAD_BALA * math.cos(math.radians(self.angle))
        self.delta_y = c.VELOCIDAD_BALA * -math.sin(math.radians(self.angle))

    def update(self, lista_enemigos, obstaculos_tile):
        """
        Actualiza la posición de la bala y gestiona colisiones.

        Args:
            lista_enemigos (list): Lista de enemigos en el juego.
            obstaculos_tile (list): Lista de obstáculos del mapa.

        Returns:
            tuple: (daño causado, posición del daño) o (0, None) si no hay colisión.
        """
        daño = 0
        pos_daño = None

        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        # verificar si la bala sale de la pantalla

        if (
            self.rect.right < 0
            or self.rect.left > c.SCREEN_WIDTH
            or self.rect.bottom < 0
            or self.rect.top > c.SCREEN_HEIGHT
        ):
            self.kill()
        # verificar colision con el enemigo

        for enemigo in lista_enemigos:
            if enemigo.shape.colliderect(self.rect):
                daño = 15 + random.randint(-5, 5)  # Daño aleatorio entre 10 y 20
                pos_daño = enemigo.shape
                enemigo.energia -= daño
                self.kill()
                break
        # verificar colision con obstaculos
        for obstaculo in obstaculos_tile:
            if obstaculo[1].colliderect(self.rect):
                self.kill()
                break

        return daño, pos_daño

    def dibujar(self, screen):
        """
        Dibuja la bala en pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se dibuja la bala.
        """
        screen.blit(self.image, self.rect.center)
