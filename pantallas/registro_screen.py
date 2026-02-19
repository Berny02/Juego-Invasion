import pygame
import json
import os


def pedir_nombre(screen, font_peq, font_titulo, c, score, tiempo):
    nombre = ""
    activo = True
    max_caracteres = 20  # Ahora permite nombres más largos
    while activo:
        screen.fill(c.AZUL_OSCURO_COLOR)
        # Mensaje de felicitaciones
        titulo = font_titulo.render("¡Felicitaciones!", True, c.AMARILLO_COLOR)
        screen.blit(titulo, (c.SCREEN_WIDTH // 2 - titulo.get_width() // 2, 60))
        subtitulo = font_peq.render(
            "Lograste escapar de la invasion.", True, c.BLANCO_COLOR
        )
        screen.blit(subtitulo, (c.SCREEN_WIDTH // 2 - subtitulo.get_width() // 2, 120))
        # Score y tiempo
        score_text = font_peq.render(
            f"Score: {score}   Tiempo: {tiempo}s", True, c.BLANCO_COLOR
        )
        screen.blit(
            score_text, (c.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 160)
        )
        # Ingreso de nombre
        nombre_texto = font_peq.render("Ingresa tu nombre:", True, c.AMARILLO_COLOR)
        screen.blit(
            nombre_texto, (c.SCREEN_WIDTH // 2 - nombre_texto.get_width() // 2, 220)
        )
        input_box = pygame.Rect(c.SCREEN_WIDTH // 2 - 180, 260, 360, 40)  # Más ancho
        pygame.draw.rect(screen, c.BLANCO_COLOR, input_box, 2)
        nombre_render = font_peq.render(nombre, True, c.BLANCO_COLOR)
        screen.blit(nombre_render, (input_box.x + 10, input_box.y + 8))
        # Instrucción
        instruccion = font_peq.render(
            "Presiona Enter para guardar.", True, c.BLANCO_COLOR
        )
        screen.blit(
            instruccion, (c.SCREEN_WIDTH // 2 - instruccion.get_width() // 2, 320)
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                activo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nombre:
                    guardar_score(nombre, score, tiempo)
                    activo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < max_caracteres and event.unicode.isprintable():
                    nombre += event.unicode


def guardar_score(nombre, score, tiempo):
    scores_path = "scores.json"
    try:
        with open(scores_path, "r") as f:
            scores = json.load(f)
    except:
        scores = []
    scores.append({"nombre": nombre, "score": score, "tiempo": tiempo})
    with open(scores_path, "w") as f:
        json.dump(scores, f)
