import pygame
import constantes as c
import math
from armas import Bala

pygame.mixer.init()
sonido_ouch = pygame.mixer.Sound("assets/sounds/ouch.mp3")
pygame.mixer.Sound.set_volume(sonido_ouch, 0.4)


class Personaje:
    """
    Clase base para personajes del juego (jugador y enemigos).
    """

    def __init__(self, x, y, animaciones, energia, tipo):
        """
        Inicializa un personaje.

        Args:
            x (int): Posición X inicial.
            y (int): Posición Y inicial.
            animaciones (list): Lista de imágenes para animación.
            energia (int): Energía inicial.
            tipo (int): 1 para jugador, 2 para enemigo.
        """
        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        self.animacion_actual = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.animacion_actual]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)
        self.tipo = tipo
        self.golpe = False
        self.ultimo_golpe = pygame.time.get_ticks()
        self.cooldown_animacion = 100
        self.nivel_completado = False

    def update(self):
        """
        Actualiza el estado y animación del personaje.
        """
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False
        golpe_cooldown = 2000
        if self.tipo == 2:
            if self.golpe == True:
                if pygame.time.get_ticks() - self.ultimo_golpe >= golpe_cooldown:
                    self.golpe = False

        self.image = self.animaciones[self.animacion_actual]
        if pygame.time.get_ticks() - self.update_time >= self.cooldown_animacion:
            self.animacion_actual += 1
            self.update_time = pygame.time.get_ticks()
        if self.animacion_actual >= len(self.animaciones):
            self.animacion_actual = 0

    def actualizar_coordenadas(self, tupla):
        """
        Actualiza la posición del personaje.

        Args:
            tupla (tuple): Nueva posición (x, y).
        """
        self.shape.center = (tupla[0], tupla[1])

    def mover(self, dx, dy, obstaculos_tile, exit_tiles):
        """
        Mueve al personaje, gestiona colisiones y límites de pantalla.

        Args:
            dx (int): Desplazamiento en X.
            dy (int): Desplazamiento en Y.
            obstaculos_tile (list): Lista de obstáculos.
            exit_tiles (list): Tile de salida.

        Returns:
            tuple: (posicion_camara, nivel_completado)
        """
        posicion_camara = [0, 0]
        nivel_completado = False

        # Actualizar dirección
        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False

        self.shape.x += dx
        for obstaculo in obstaculos_tile:
            if self.shape.colliderect(obstaculo[1]):
                if dx > 0:
                    self.shape.right = obstaculo[1].left
                if dx < 0:
                    self.shape.left = obstaculo[1].right

        self.shape.y += dy
        for obstaculo in obstaculos_tile:
            if self.shape.colliderect(obstaculo[1]):
                if dy > 0:
                    self.shape.bottom = obstaculo[1].top
                if dy < 0:
                    self.shape.top = obstaculo[1].bottom

        # Limitar movimiento y comprobar salida
        if self.tipo == 1:
            if (
                exit_tiles is not None
                and len(exit_tiles) > 1
                and exit_tiles[1] is not None
            ):
                if exit_tiles[1].colliderect(self.shape):
                    self.nivel_completado = True
            if self.shape.right > (c.SCREEN_WIDTH - c.LIMITE_PANTALLA):
                posicion_camara[0] = (
                    c.SCREEN_WIDTH - c.LIMITE_PANTALLA
                ) - self.shape.right
                self.shape.right = c.SCREEN_WIDTH - c.LIMITE_PANTALLA
            if self.shape.left < c.LIMITE_PANTALLA:
                posicion_camara[0] = c.LIMITE_PANTALLA - self.shape.left
                self.shape.left = c.LIMITE_PANTALLA
            if self.shape.bottom > c.SCREEN_HEIGHT - c.LIMITE_PANTALLA:
                posicion_camara[1] = (
                    c.SCREEN_HEIGHT - c.LIMITE_PANTALLA
                ) - self.shape.bottom
                self.shape.bottom = c.SCREEN_HEIGHT - c.LIMITE_PANTALLA
            if self.shape.top < c.LIMITE_PANTALLA:
                posicion_camara[1] = c.LIMITE_PANTALLA - self.shape.top
                self.shape.top = c.LIMITE_PANTALLA
            return posicion_camara, self.nivel_completado

    def enemigos(self, jugador, posicion_camara, obstaculos_tile, exit_tiles):
        """
        Lógica de movimiento y ataque de los enemigos hacia el jugador.

        Args:
            jugador (Personaje): Referencia al jugador.
            posicion_camara (tuple): Desplazamiento de cámara.
            obstaculos_tile (list): Lista de obstáculos.
            exit_tiles (list): Tile de salida.
        """
        ene_dx = 0
        ene_dy = 0
        self.shape.x += posicion_camara[0]
        self.shape.y += posicion_camara[1]

        linea_vision = (
            (self.shape.centerx, self.shape.centery),
            (jugador.shape.centerx, jugador.shape.centery),
        )

        clipped_line = None
        for obs in obstaculos_tile:
            if obs[1].clipline(linea_vision):
                clipped_line = obs[1].clipline(linea_vision)

        distancia = math.sqrt(
            (self.shape.centerx - jugador.shape.centerx) ** 2
            + (self.shape.centery - jugador.shape.centery) ** 2
        )

        if not clipped_line and distancia < c.RANGO_VISION:
            if self.shape.centerx < jugador.shape.centerx:
                ene_dx = c.VELOCIDAD_ENEMIGO
            elif self.shape.centerx > jugador.shape.centerx:
                ene_dx = -c.VELOCIDAD_ENEMIGO
            if self.shape.centery < jugador.shape.centery:
                ene_dy = c.VELOCIDAD_ENEMIGO
            elif self.shape.centery > jugador.shape.centery:
                ene_dy = -c.VELOCIDAD_ENEMIGO

        self.mover(ene_dx, ene_dy, obstaculos_tile, exit_tiles)

        if distancia < c.RANGO_ATAQUE and not self.golpe:
            self.golpe = True
            self.ultimo_golpe = pygame.time.get_ticks()
            jugador.energia -= 10
            sonido_ouch.play()

    def dibujar(self, screen):
        """
        Dibuja el personaje en pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se dibuja el personaje.
        """
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(image_flip, self.shape)
        # pygame.draw.rect(screen, c.ROJO_COLOR, self.shape)


class Boss(Personaje):
    """
    Clase que representa al jefe final del juego.
    """

    def __init__(self, x, y, animaciones, energia, nombre="Devorador"):
        """
        Inicializa el jefe.

        Args:
            x (int): Posición X inicial.
            y (int): Posición Y inicial.
            animaciones (list): Lista de imágenes para animación.
            energia (int): Energía inicial.
            nombre (str): Nombre del jefe.
        """
        super().__init__(x, y, animaciones, energia, tipo=2)
        self.nombre = nombre
        self.fase = 1
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()
        self.cooldown_ataque = 3000
        self.ataque_activo = False
        self.inmunidad_temporal = False
        self.tiempo_inmunidad = 0
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.balas = pygame.sprite.Group()
        self.bala_img = pygame.image.load(
            "assets\images\weapons\Bala_boss.png"
        ).convert_alpha()

    def update(self, jugador):
        """
        Actualiza el estado, animación y ataques del jefe.

        Args:
            jugador (Personaje): Referencia al jugador.
        """
        super().update()
        ahora = pygame.time.get_ticks()

        # Cambio de fase
        if self.energia < 300 and self.fase == 1:
            self.fase = 2
            self.cooldown_ataque = 2000
            animacion_fase_2 = []
            for i in range(3):
                img = pygame.image.load(
                    f"assets\images\characters\Transform_boss\Fase_2({i+1}).png"
                ).convert_alpha()
                img = pygame.transform.scale(
                    img, (img.get_width() * 2, img.get_height() * 2)
                )
                animacion_fase_2.append(img)
            self.animaciones = animacion_fase_2
            self.animacion_actual = 2
            self.cooldown_animacion = 900

        # Ataque especial por fases
        if ahora - self.tiempo_ultimo_ataque > self.cooldown_ataque:
            self.realizar_ataque(jugador)
            self.tiempo_ultimo_ataque = ahora

        self.actualizar_balas(jugador)

        # Termina inmunidad temporal
        if self.inmunidad_temporal and ahora - self.tiempo_inmunidad > 1000:
            self.inmunidad_temporal = False

    def realizar_ataque(self, jugador):
        """
        Realiza el ataque especial del jefe según la fase.

        Args:
            jugador (Personaje): Referencia al jugador.
        """
        if self.fase == 1:
            jugador.energia -= 0
        else:
            dx = jugador.shape.centerx - self.shape.centerx
            dy = jugador.shape.centery - self.shape.centery
            angulo = math.degrees(math.atan2(-dy, dx))
            bala = Bala(self.bala_img, self.shape.centerx, self.shape.centery, angulo)
            self.balas.add(bala)

    def actualizar_balas(self, jugador):
        """
        Actualiza las balas disparadas por el jefe y gestiona colisiones.

        Args:
            jugador (Personaje): Referencia al jugador.
        """
        for bala in self.balas:
            bala.update([jugador], [])
            if bala.rect.colliderect(jugador.shape):
                jugador.energia -= 5
                self.balas.remove(bala)
            elif not c.SCREEN_RECT.colliderect(bala.rect):
                self.balas.remove(bala)

    def dibujar(self, screen):
        """
        Dibuja el jefe y sus balas en pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se dibuja el jefe.
        """
        if not self.inmunidad_temporal or pygame.time.get_ticks() % 300 < 150:
            imagen_volteada = pygame.transform.flip(self.image, self.flip, False)
            screen.blit(imagen_volteada, self.shape)
        for bala in self.balas:
            bala.dibujar(screen)
        # pygame.draw.rect(screen, c.ROJO_COLOR, self.shape)

    def recibir_danio(self, cantidad):
        """
        Aplica daño al jefe y activa inmunidad temporal.

        Args:
            cantidad (int): Cantidad de daño recibido.
        """
        if not self.inmunidad_temporal:
            self.energia -= cantidad
            self.inmunidad_temporal = True
            self.tiempo_inmunidad = pygame.time.get_ticks()
