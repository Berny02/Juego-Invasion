import constantes as c
from Personajes import Personaje
from Personajes import Boss
import pygame


def escalar_imagen(imagen, escala):
    """
    Escala una imagen de pygame por un factor dado.

    Args:
        imagen (pygame.Surface): Imagen a escalar.
        escala (float): Factor de escala.

    Returns:
        pygame.Surface: Imagen escalada.
    """
    return pygame.transform.scale(
        imagen, (imagen.get_width() * escala, imagen.get_height() * escala)
    )


# Índices de tiles que se consideran obstáculos en el mapa
obstaculos = [
    0,
    2,
    3,
    4,
    5,
    6,
    7,
    18,
    19,
    20,
    21,
    22,
    23,
    34,
    35,
    36,
    37,
    38,
]


class Mundo:
    """
    Clase que representa el mundo del juego, incluyendo el mapa, obstáculos, enemigos y salida.
    """

    def __init__(self):
        """
        Inicializa el mundo con sus listas de tiles, enemigos y referencias especiales.
        """
        self.boss = None
        self.map_tiles = []
        self.obstaculos_tile = []
        self.exit_tiles = None
        self.lista_enemigos = []

    def procesar_mapa(self, data, tilelist, animaciones_enemigos):
        """
        Procesa la matriz de datos del mapa y genera los tiles, obstáculos, enemigos y salida.

        Args:
            data (list): Matriz de enteros representando el mapa.
            tilelist (list): Lista de imágenes de tiles.
            animaciones_enemigos (list): Lista de animaciones para los enemigos.
        """
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if 0 <= tile < len(tilelist):
                    image = tilelist[tile]
                else:
                    image = tilelist[0]
                image_rect = image.get_rect()
                image_x = x * c.TILE_SIZE
                image_y = y * c.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tiledata = [image, image_rect, image_x, image_y]
                self.map_tiles.append(tiledata)

                if tile in obstaculos:
                    self.obstaculos_tile.append(tiledata)
                elif tile == 191:
                    # Tile de la salida (llave)
                    llave = pygame.image.load("assets\\images\\items\\KeyFly.gif")
                    llave = escalar_imagen(llave, 0.8)
                    tiledata[0] = llave
                    self.exit_tiles = tiledata
                elif tile == 250:
                    # Tile de Santi (enemigo especial)
                    santi = Personaje(
                        image_x, image_y - 10, animaciones_enemigos[0], 200, 2
                    )
                    self.lista_enemigos.append(santi)
                    tiledata[0] = tilelist[0]
                elif tile == 249:
                    # Tile de alejandroloaizagamer (enemigo especial)
                    alejandroloaizagamer = Personaje(
                        image_x, image_y, animaciones_enemigos[2], 200, 2
                    )
                    self.lista_enemigos.append(alejandroloaizagamer)
                    tiledata[0] = tilelist[0]
                elif tile == 245:
                    # Tile de sarita (enemiga)
                    sarita = Personaje(
                        image_x, image_y, animaciones_enemigos[3], 200, 2
                    )
                    self.lista_enemigos.append(sarita)
                    tiledata[0] = tilelist[0]
                elif tile == 248:
                    # Tile del boss
                    boss = Boss(image_x, image_y, animaciones_enemigos[1], 500)
                    self.boss = boss
                    self.lista_enemigos.append(boss)
                    tiledata[0] = tilelist[0]

    def update(self, posicion_camara):
        """
        Actualiza la posición de los tiles del mapa según la posición de la cámara.

        Args:
            posicion_camara (tuple): Nueva posición de la cámara en el formato (x, y).
        """
        for tile in self.map_tiles:
            tile[2] += posicion_camara[0]
            tile[3] += posicion_camara[1]
            tile[1].center = (tile[2], tile[3])

    def dibujar(self, screen):
        """
        Dibuja todos los tiles del mapa en la pantalla.

        Args:
            screen (pygame.Surface): Superficie de pygame donde se dibujará el mapa.
        """
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1])
