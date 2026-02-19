import pygame.sprite


class Item(pygame.sprite.Sprite):
    """
    Representa un ítem coleccionable en el juego.

    Tipos de ítem:
        0: Moneda de oro (+10 puntos)
        1: Moneda de rubí (+100 puntos)
        2: Moneda de plata (+1 punto)
        3: Poción (+25 energía, máximo 100)
        4: Llave (marca el nivel como completado)
    """

    def __init__(self, x, y, tipo, animacion_list, sonido_consumible=None):
        """
        Inicializa un ítem en la posición (x, y).

        Args:
            x (int): Posición X.
            y (int): Posición Y.
            tipo (int): Tipo de ítem.
            animacion_list (list): Lista de imágenes para la animación.
            sonido_consumible (pygame.mixer.Sound, opcional): Sonido al recoger el ítem.
        """
        super().__init__()
        self.tipo = tipo
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animacion_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.sonido_consumible = sonido_consumible

    def update(self, posicion_camara, personaje):
        """
        Actualiza la posición y animación del ítem, y gestiona la recogida por el jugador.

        Args:
            posicion_camara (tuple): Desplazamiento de la cámara.
            personaje (Personaje): Referencia al jugador.
        """
        # Actualizar posición según la cámara
        self.rect.x += posicion_camara[0]
        self.rect.y += posicion_camara[1]

        # Comprobar colisión con el jugador
        if self.rect.colliderect(personaje.shape):
            if self.tipo in [0, 1, 2] and self.sonido_consumible:
                self.sonido_consumible.play()
            if self.tipo == 3 and self.sonido_consumible:
                self.sonido_consumible.play()
            if self.tipo == 0:
                personaje.score += 10
            elif self.tipo == 1:
                personaje.score += 100
            elif self.tipo == 2:
                personaje.score += 1
            elif self.tipo == 3:
                personaje.energia += 25
                if personaje.energia > 100:
                    personaje.energia = 100
            elif self.tipo == 4:  # Llave
                personaje.nivel_completado = True
            self.kill()

        # Animación del ítem
        cooldown_animation = 200
        self.image = self.animacion_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animacion_list):
            self.frame_index = 0


class Explosion(pygame.sprite.Sprite):
    """
    Representa una animación de explosión temporal en el juego.
    """

    def __init__(self, x, y, animacion_list):
        """
        Inicializa la explosión en la posición (x, y).

        Args:
            x (int): Posición X.
            y (int): Posición Y.
            animacion_list (list): Lista de imágenes para la animación.
        """
        super().__init__()
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.image = self.animacion_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_time = pygame.time.get_ticks()

    def update(self, posicion_camara):
        """
        Actualiza la posición y animación de la explosión.

        Args:
            posicion_camara (tuple): Desplazamiento de la cámara.
        """
        self.rect.x += posicion_camara[0]
        self.rect.y += posicion_camara[1]
        cooldown_animation = 100
        self.image = self.animacion_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animacion_list):
            self.kill()
