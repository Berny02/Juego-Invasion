import pygame
from Personajes import Personaje
from Personajes import Boss
import constantes as c
from armas import Arma
from text import Damagetext
from items import Item, Explosion
from mundo import Mundo
import math
import csv
import os
import random
from pantallas.help_screen import mostrar_help
from pantallas.scores_screen import mostrar_scores
from pantallas.registro_screen import pedir_nombre
from pantallas.credits_screen import mostrar_credits

"""
Invasion: The Key to Survival
-----------------------------
Juego tipo top-down shooter con niveles, enemigos, items y jefe final.
Este archivo contiene la lógica principal del juego, inicialización de recursos,
bucle principal y gestión de eventos.

Estructura principal:
- Inicialización de pygame y recursos (imágenes, sonidos, fuentes)
- Carga de mapas y niveles
- Bucle principal de juego y eventos
- Gestión de jugador, enemigos, items y colisiones
"""


# Funcion escalar imagen
def escalar_imagen(imagen, escala):
    """Escala una imagen de pygame por un factor dado."""
    return pygame.transform.scale(
        imagen, (imagen.get_width() * escala, imagen.get_height() * escala)
    )


# Funcion para contar elementos
def contar_elementos(directorio):
    """Cuenta el número de archivos en un directorio."""
    return len(os.listdir(directorio))


# Funcion para listar nombres de elementos
def nombres_carpetas(directorio):
    """Lista los nombres de los archivos en un directorio."""
    return os.listdir(directorio)


# Funcion para dibujar la vida del jugador
def vida_jugador():
    """Dibuja la barra de vida del jugador en pantalla."""
    c_mitad_dibujado = False
    for i in range(4):
        if jugador.energia >= ((i + 1) * 25):
            screen.blit(corazon_lleno, (10 + (i * 40), 10))
        elif jugador.energia % 25 > 0 and c_mitad_dibujado == False:
            screen.blit(corazon_mitad, (10 + (i * 40), 10))
            c_mitad_dibujado = True
        else:
            screen.blit(corazon_vacio, (10 + (i * 40), 10))


# Funcion para dibujar el texto de daño
def dibujar_texto(texto, fuente, color, x, y):
    """Dibuja un texto en pantalla en la posición indicada."""
    img = fuente.render(texto, True, color)
    screen.blit(img, (x, y))


def dibujar_barra_boss(screen, boss):
    """Dibuja la barra de vida del jefe en pantalla."""
    if boss.vivo:
        barra_ancho = 300
        barra_alto = 20
        barra_x = c.SCREEN_WIDTH // 2 - barra_ancho // 2
        barra_y = 20
        pygame.draw.rect(screen, (0, 0, 0), (barra_x, barra_y, barra_ancho, barra_alto))
        vida_actual = int(barra_ancho * (boss.energia / 500))
        pygame.draw.rect(
            screen, (255, 0, 0), (barra_x, barra_y, vida_actual, barra_alto)
        )
        fuente = pygame.font.SysFont(None, 30)
        texto = fuente.render(boss.nombre, True, (255, 255, 255))
        screen.blit(texto, (barra_x, barra_y - 25))


pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Invasion: The Key to Survival")

# Inicializa el mixer antes de cargar la música
pygame.mixer.init()

# Carga y reproduce la música de fondo en loop infinito
pygame.mixer.music.load("assets/sounds/horror_music.mp3")
pygame.mixer.music.set_volume(0.2)  # Ajusta el volumen de la música
pygame.mixer.music.play(-1)  # -1 significa loop infinito

# Variables
posicion_camara = [0, 0]
nivel = 1
boss_sonando = False
mostrar_help_screen = False
mostrar_scores_screen = False
mostrar_credits_screen = False
tiempo_inicio = 0


# iniciar fuentes
font = pygame.font.Font("assets/fonts/Pixelfont.ttf", 15)
font_game_over = pygame.font.Font("assets/fonts/Pixelfont.ttf", 70)

font_inicio = pygame.font.Font("assets/fonts/Pixelfont.ttf", 30)
font_titulo = pygame.font.Font("assets/fonts/Pixelfont.ttf", 50)


game_over_text = font_game_over.render("GAME OVER", True, c.BLANCO_COLOR)
restart_text = font.render("Press R to restart", True, c.BLANCO_COLOR)

# Boton de inicio
button_play = pygame.Rect(c.SCREEN_WIDTH / 2 - 100, c.SCREEN_HEIGHT / 2 - 50, 200, 50)
button_exit = pygame.Rect(c.SCREEN_WIDTH / 2 - 100, c.SCREEN_HEIGHT / 2 + 50, 200, 50)

text_button_play = font_inicio.render("Play", True, c.BLANCO_COLOR)
text_button_exit = font_inicio.render("Exit", True, c.BLANCO_COLOR)

# Botones adicionales
button_help = pygame.Rect(c.SCREEN_WIDTH / 2 - 100, c.SCREEN_HEIGHT / 2 + 150, 200, 50)
button_scores = pygame.Rect(
    c.SCREEN_WIDTH / 2 - 100, c.SCREEN_HEIGHT / 2 + 250, 200, 50
)
button_credits = pygame.Rect(
    c.SCREEN_WIDTH / 2 - 100, c.SCREEN_HEIGHT / 2 + 350, 200, 50
)

font_titulo_peq = pygame.font.Font("assets/fonts/Pixelfont.ttf", 40)
text_button_help = font_inicio.render("Help", True, c.BLANCO_COLOR)
text_button_scores = font_inicio.render("Scores", True, c.BLANCO_COLOR)
text_button_credits = font_inicio.render("Creditos", True, c.BLANCO_COLOR)



def pantalla_inicio():
    screen.fill(c.AZUL_OSCURO_COLOR)
    # Título en dos líneas, fuente más pequeña
    titulo1 = "Invasion:"
    titulo2 = "The Key to Survival"
    titulo1_img = font_titulo_peq.render(titulo1, True, c.BLANCO_COLOR)
    titulo2_img = font_titulo_peq.render(titulo2, True, c.BLANCO_COLOR)
    titulo1_rect = titulo1_img.get_rect(
        center=(c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 160)
    )
    titulo2_rect = titulo2_img.get_rect(
        center=(c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 120)
    )
    screen.blit(titulo1_img, titulo1_rect)
    screen.blit(titulo2_img, titulo2_rect)

    # Configuración de botones
    button_width = 200
    button_height = 40
    offset = 10  # Espacio vertical entre botones
    y_start = c.SCREEN_HEIGHT / 2 - 20

    botones = [
        (button_play, text_button_play, y_start),
        (button_help, text_button_help, y_start + (button_height + offset) * 1),
        (button_scores, text_button_scores, y_start + (button_height + offset) * 2),
        (button_credits, text_button_credits, y_start + (button_height + offset) * 3),
        (button_exit, text_button_exit, y_start + (button_height + offset) * 4),
    ]

    for boton_rect, boton_texto, y in botones:
        # Actualiza la posición del rectángulo del botón
        boton_rect.x = c.SCREEN_WIDTH // 2 - button_width // 2
        boton_rect.y = int(y)
        boton_rect.width = button_width
        boton_rect.height = button_height
        pygame.draw.rect(screen, c.VERDE_AGUAMARINA_COLOR, boton_rect, border_radius=8)
        # Centra el texto dentro del botón
        text_rect = boton_texto.get_rect(center=boton_rect.center)
        screen.blit(boton_texto, text_rect)

    pygame.display.update()


# Energia
corazon_vacio = pygame.image.load("assets/images/items/empty_heart.png")
corazon_vacio = escalar_imagen(corazon_vacio, c.SCALA_CORAZON)
corazon_mitad = pygame.image.load("assets/images/items/Medio.png")
corazon_mitad = escalar_imagen(corazon_mitad, c.SCALA_CORAZON)
corazon_lleno = pygame.image.load("assets/images/items/heart.png")
corazon_lleno = escalar_imagen(corazon_lleno, c.SCALA_CORAZON)

# Cargar imagenes de animacion personaje
animaciones = []
for i in range(7):
    img = pygame.image.load(f"assets\\images\\characters\\Player\\Walking_KG_{i}.png")
    img = escalar_imagen(img, c.PLAYER_SCALA)
    animaciones.append(img)

# Cargar animacion de explosion
animacion_explosion = []
for i in range(7):
    img = pygame.image.load(
        f"assets\\images\\characters\\Explosion\\Explosion ({i+1}).png"
    )
    animacion_explosion.append(img)

# Enemies
directorio_enemigos = "assets//images//characters//Enemies"
tipos_enemigos = nombres_carpetas(directorio_enemigos)
animaciones_enemigos = []

for eni in tipos_enemigos:
    lista_temp = []
    ruta_temp = f"assets//images//characters//Enemies//{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    if eni == "Final_Boss":
        escala_actual = c.BOSS_SCALA
    else:
        escala_actual = c.ENEMY_SCALA
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}{i}.png")
        img_enemigo = escalar_imagen(img_enemigo, escala_actual)
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)


# Cargar imagen de arma
img_pistola = pygame.image.load("assets\\images\\weapons\\Usi.png")
img_pistola = escalar_imagen(img_pistola, c.WEAPON_SCALA)


# Cargar balas
img_bala = pygame.image.load("assets\\images\\weapons\\KAKILIANEMBAPE.png")
img_bala = escalar_imagen(img_bala, c.BULLET_SCALA)

# Cargar imagen de tiles
tile_list = []
for x in range(c.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/tiles/divididos/Mapa ({x+1}).png")
    tile_image = pygame.transform.scale(tile_image, (c.TILE_SIZE, c.TILE_SIZE))
    tile_list.append(tile_image)

# Cargar imagen de items
pocion_roja = pygame.image.load("assets/images/items/Pocion.png")
pocion_roja = escalar_imagen(pocion_roja, 0.1)

# Cargar imagen de llave de salida


# Directorio de monedas
directorio_monedas = "assets//images//items//coin"
tipo_monedas = nombres_carpetas(directorio_monedas)
animaciones_monedas = []

for mon in tipo_monedas:
    lista_temp = []
    ruta_temp = f"assets//images//items//coin//{mon}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_moneda = pygame.image.load(f"{ruta_temp}//{mon}{i}.png")
        img_moneda = escalar_imagen(img_moneda, c.ITEM_SCALA)
        lista_temp.append(img_moneda)
    animaciones_monedas.append(lista_temp)

llave = pygame.image.load("assets/images/items/KeyFly.gif")
llave = escalar_imagen(llave, 0.8)
animaciones_monedas.append([llave])  # Agregar llave como último tipo de item
"""coin_image = []
ruta_temp = "assets//images//items//coin"
num_coin = contar_elementos(ruta_temp)
for i in range(num_coin):
    img_coin = pygame.image.load(f"{ruta_temp}//frame_{i+1}.png")
    img_coin = escalar_imagen(img_coin, c.ITEM_SCALA)
    coin_image.append(img_coin)"""

player = pygame.image.load("assets\\images\\characters\\Player\\Walking_KG_0.png")
player = escalar_imagen(player, c.PLAYER_SCALA)

# Cargar sonido de disparo
sonido_disparo = pygame.mixer.Sound("assets/sounds/bala.mp3")
sonido_explosion = pygame.mixer.Sound("assets/sounds/explosion.mp3")
sonido_coin = pygame.mixer.Sound("assets/sounds/coin.mp3")
sonido_pocion = pygame.mixer.Sound("assets/sounds/slurp.mp3")
sonido_llave = pygame.mixer.Sound("assets/sounds/key.mp3")
sonido_boss = pygame.mixer.Sound("assets/sounds/boss.mp3")


# Ajustar volumen de los sonidos
pygame.mixer.Sound.set_volume(sonido_coin, 0.4)
pygame.mixer.Sound.set_volume(sonido_explosion, 0.4)
pygame.mixer.Sound.set_volume(sonido_disparo, 0.4)
pygame.mixer.Sound.set_volume(sonido_llave, 0.4)
pygame.mixer.Sound.set_volume(sonido_pocion, 0.4)
pygame.mixer.Sound.set_volume(sonido_boss, 0.4)

# crear un arma de clase Arma
pistola = Arma(img_pistola, img_bala, sonido_disparo)


# crear grupo sprites para las balas
damage_text_group = pygame.sprite.Group()
bala_group = pygame.sprite.Group()
# crear grupo sprites para los items
items_group = pygame.sprite.Group()
# crear grupo sprites para los enemigos
explosiones = pygame.sprite.Group()


# Crear moneda

"""
silver_coin = Item(400, 100, 0, animaciones_monedas[0])
gold_coin = Item(200, 100, 1, animaciones_monedas[1])
ruby_coin = Item(300, 100, 2, animaciones_monedas[2])

pocion = Item(300, 200, 3, [pocion_roja])

items_group.add(silver_coin)
items_group.add(gold_coin)
items_group.add(ruby_coin)
items_group.add(pocion)
"""


def resetear_mundo():
    # Reiniciar el mundo
    bala_group.empty()
    items_group.empty()
    damage_text_group.empty()
    jugador.nivel_completado = False

    # Crear nueva matriz vacía para el mundo
    data = []
    for fila in range(c.FILAS):
        filas = [0] * c.COLUMNAS
        data.append(filas)

    return data


world_data = []


for fila in range(c.FILAS):
    filas = [0] * c.COLUMNAS
    world_data.append(filas)

# Cargar el mapa desde un archivo csv
with open("niveles/lvl1.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, column in enumerate(row):
            world_data[x][y] = int(column)


world = Mundo()
world.procesar_mapa(world_data, tile_list, animaciones_enemigos)


def dibujar_grid():
    for x in range(30):
        pygame.draw.line(
            screen,
            c.BLANCO_COLOR,
            (x * c.TILE_SIZE, 0),
            (x * c.TILE_SIZE, c.SCREEN_HEIGHT),
        )
        pygame.draw.line(
            screen,
            c.BLANCO_COLOR,
            (0, x * c.TILE_SIZE),
            (c.SCREEN_WIDTH, x * c.TILE_SIZE),
        )


# crear jugador de clase personaje
jugador = Personaje(100, 100, animaciones, 100, 1)


# crear enemigo de clase personaje


# Lista de enemigos
lista_enemigos = []
for ene in world.lista_enemigos:
    lista_enemigos.append(ene)


clock = pygame.time.Clock()
running = True
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

boton_restart = pygame.Rect(c.SCREEN_WIDTH / 2 - 100, c.SCREEN_HEIGHT / 2 + 50, 235, 50)
mostrar_inicio = True


while running:
    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    mostrar_inicio = False
                    tiempo_inicio = pygame.time.get_ticks()
                if button_exit.collidepoint(event.pos):
                    running = False
                if button_help.collidepoint(event.pos):
                    mostrar_help_screen = True
                if button_scores.collidepoint(event.pos):
                    mostrar_scores_screen = True
                if button_credits.collidepoint(event.pos):
                    mostrar_credits_screen = True

        # Mostrar pantalla de ayuda si corresponde
        while mostrar_help_screen:
            mostrar_help(screen, font, font_titulo, c)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    mostrar_help_screen = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    mostrar_help_screen = False

        # Mostrar pantalla de scores si corresponde
        while mostrar_scores_screen:
            mostrar_scores(screen, font, font_titulo, c)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    mostrar_scores_screen = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    mostrar_scores_screen = False

        # Mostrar pantalla de credits si corresponde
        while mostrar_credits_screen:
            mostrar_credits(screen, font, font_titulo, c)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    mostrar_credits_screen = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    mostrar_credits_screen = False
    else:

        # FPS
        clock.tick(c.FPS)

        # Actualizar el color constantemente para que se vea el movimiento
        screen.fill(c.VERDE_AGUAMARINA_COLOR)

        # Dibujar el mundo
        world.dibujar(screen)

        if jugador.vivo:

            d_x = 0
            d_y = 0
            if mover_arriba:
                d_y = -c.VELOCIDAD
            if mover_abajo:
                d_y = c.VELOCIDAD
            if mover_izquierda:
                d_x = -c.VELOCIDAD
            if mover_derecha:
                d_x = c.VELOCIDAD

            # Movimiento del personaje
            posicion_camara, nivel_completado = jugador.mover(
                d_x, d_y, world.obstaculos_tile, world.exit_tiles
            )

            # Actualizar la camara
            world.update(posicion_camara)

            # Actualizar del personaje
            jugador.update()

            # Actualizar enemigos
            for ene in lista_enemigos:
                if isinstance(ene, Boss):
                    ene.update(jugador)

                else:
                    ene.update()

            # Actualizar el arma
            bala = pistola.update(jugador)
            if bala != None:
                bala_group.add(bala)
            for bala in bala_group:
                damage, pos_damage = bala.update(lista_enemigos, world.obstaculos_tile)
                if damage:
                    damage_text = Damagetext(
                        pos_damage.centerx,
                        pos_damage.centery,
                        str(-damage),
                        font,
                        c.ROJO_COLOR,
                    )
                    damage_text_group.add(damage_text)

            # Actualizar el texto de daño
            damage_text_group.update(posicion_camara)

            # Actualizar items
            items_group.update(posicion_camara, jugador)

            # Actualizar explosiones
            explosiones.update(posicion_camara)

        # Dibujar explosiones
        explosiones.draw(screen)

        # Dibujar el arma
        pistola.dibujar(screen)

        # Dibujar las balas
        for bala in bala_group:
            bala.dibujar(screen)

        # Dibujar la vida del jugador
        vida_jugador()

        # Dibujar el textos
        damage_text_group.draw(screen)
        dibujar_texto(f"Score: {jugador.score}", font, c.AMARILLO_COLOR, 670, 5)
        dibujar_texto(f"Nivel: {nivel}", font, c.BLANCO_COLOR, c.SCREEN_WIDTH / 2, 25)

        # Dibujar items
        items_group.draw(screen)

        # Chequear si el jugador ha completado el nivel
        if nivel_completado == True:
            if nivel < c.NIVEL_MAXIMO:
                # Reiniciar el mundo
                nivel += 1
                world_data = resetear_mundo()
                with open(f"niveles/lvl{nivel}.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, column in enumerate(row):
                            world_data[x][y] = int(column)
                world = Mundo()
                world.procesar_mapa(world_data, tile_list, animaciones_enemigos)
                jugador.actualizar_coordenadas(c.COORDENADAS[str(nivel)])
                # Lista de enemigos
                lista_enemigos = []
                for ene in world.lista_enemigos:
                    lista_enemigos.append(ene)
            else:
                pedir_nombre(screen, font, font_titulo, c, jugador.score, tiempo_actual)
                nivel = 1  # Reinicia el nivel
                world_data = resetear_mundo()
                with open(f"niveles/lvl{nivel}.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, column in enumerate(row):
                            world_data[x][y] = int(column)
                world = Mundo()
                world.procesar_mapa(world_data, tile_list, animaciones_enemigos)
                jugador.actualizar_coordenadas((100, 100))
                lista_enemigos = []
                for ene in world.lista_enemigos:
                    lista_enemigos.append(ene)
                mostrar_inicio = True
                nivel_completado = False  # Resetea el flag

        # Dibujar jugador
        jugador.dibujar(screen)

        # Dibujar la barra de vida del boss
        if world.boss:
            dibujar_barra_boss(screen, world.boss)
        # Dibujar enemigos
        for ene in lista_enemigos:
            if ene.energia <= 0:
                lista_enemigos.remove(ene)

                drop_pos = (
                    ene.shape.center
                )  # Posición donde muere el enemigo y se deja el item
                if ene == world.boss:
                    nuevo_item = Item(
                        drop_pos[0],
                        drop_pos[1],
                        4,  # Llave
                        [llave],
                        sonido_llave,
                    )
                else:

                    tipo = random.choice([0, 1, 2, 3])
                    # Crear un nuevo item en la posición del enemigo
                    # Tipo de item: 0 = moneda oro, 1 = moneda ruby, 2 = moneda plata, 3 = pocion
                    if tipo in [0, 1, 2]:  # Monedas
                        nuevo_item = Item(
                            drop_pos[0],
                            drop_pos[1],
                            tipo,
                            animaciones_monedas[tipo],
                            sonido_coin,
                        )
                    elif tipo == 3:  # Poción
                        nuevo_item = Item(
                            drop_pos[0], drop_pos[1], tipo, [pocion_roja], sonido_pocion
                        )
                # Agregar el nuevo item al grupo de items
                items_group.add(nuevo_item)
                # Implementar la animacion de explosion cuando muere el enemigo
                explosion = Explosion(drop_pos[0], drop_pos[1], animacion_explosion)
                explosiones.add(explosion)
                sonido_explosion.play()  # <-- Reproduce el sonido aquí

            if ene.energia > 0:
                ene.enemigos(
                    jugador, posicion_camara, world.obstaculos_tile, world.exit_tiles
                )
                ene.dibujar(screen)

        if jugador.vivo == False:
            # Mostrar mensaje de game over
            screen.fill(c.AZUL_OSCURO_COLOR)
            text_rect = game_over_text.get_rect(
                center=(c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2)
            )
            screen.blit(game_over_text, text_rect)
            pygame.draw.rect(screen, c.ROJO_COLOR, boton_restart)
            screen.blit(
                restart_text, (c.SCREEN_WIDTH / 2 - 90, c.SCREEN_HEIGHT / 2 + 70)
            )

        # Sonido del boss
        if world.boss and world.boss.vivo:
            distancia = math.hypot(
                jugador.shape.centerx - world.boss.shape.centerx,
                jugador.shape.centery - world.boss.shape.centery,
            )
            if (
                distancia < 400
            ):  # Puedes ajustar la distancia según lo que consideres "cerca"
                if not boss_sonando:
                    sonido_boss.play()
                    boss_sonando = True
            else:
                if boss_sonando:
                    sonido_boss.stop()
                    boss_sonando = False

        tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio) // 1000  # en segundos
        if jugador.vivo:
            dibujar_texto(f"Tiempo: {tiempo_actual}s", font, c.BLANCO_COLOR, 670, 25)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_a:
                    mover_izquierda = True
                if event.key == pygame.K_d:
                    mover_derecha = True
                if event.key == pygame.K_w:
                    mover_arriba = True
                if event.key == pygame.K_s:
                    mover_abajo = True
                if event.key == pygame.K_r:
                    if not jugador.vivo:
                        jugador.vivo = True
                        jugador.energia = 100
                        jugador.score = 0
                        nivel = 1
                        world_data = resetear_mundo()
                        with open(f"niveles/lvl{nivel}.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter=",")
                            for x, row in enumerate(reader):
                                for y, column in enumerate(row):
                                    world_data[x][y] = int(column)
                        world = Mundo()
                        world.procesar_mapa(world_data, tile_list, animaciones_enemigos)
                        jugador.actualizar_coordenadas((100, 100))
                        # Lista de enemigos
                        lista_enemigos = []
                        for ene in world.lista_enemigos:
                            lista_enemigos.append(ene)
                        tiempo_inicio = pygame.time.get_ticks()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_restart.collidepoint(event.pos) and not jugador.vivo:
                    jugador.vivo = True
                    jugador.energia = 100
                    jugador.score = 0
                    nivel = 1
                    world_data = resetear_mundo()
                    with open(f"niveles/lvl{nivel}.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, column in enumerate(row):
                                world_data[x][y] = int(column)
                    world = Mundo()
                    world.procesar_mapa(world_data, tile_list, animaciones_enemigos)
                    jugador.actualizar_coordenadas((100, 100))
                    # Lista de enemigos
                    lista_enemigos = []
                    for ene in world.lista_enemigos:
                        lista_enemigos.append(ene)

pygame.quit()
