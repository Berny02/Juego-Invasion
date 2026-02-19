import pygame
import json
import os


def mostrar_scores(screen, font_peq, font_titulo, c):
    screen.fill(c.AZUL_OSCURO_COLOR)
    # Título
    titulo = font_titulo.render("Mejores Puntajes", True, c.AMARILLO_COLOR)
    screen.blit(titulo, (c.SCREEN_WIDTH // 2 - titulo.get_width() // 2, 60))

    scores_path = "scores.json"
    if os.path.exists(scores_path):
        with open(scores_path, "r") as f:
            scores = json.load(f)
        # Ordena por score descendente y luego por menor tiempo
        scores = sorted(scores, key=lambda x: (-x["score"], x["tiempo"]))
        for i, entry in enumerate(scores[:10]):
            texto = font_peq.render(
                f"{i+1}. {entry['nombre']} - Score: {entry['score']} - Tiempo: {entry['tiempo']}s",
                True,
                c.BLANCO_COLOR,
            )
            screen.blit(texto, (60, 140 + i * 28))
    else:
        texto = font_peq.render("No hay puntajes aun.", True, c.BLANCO_COLOR)
        screen.blit(texto, (60, 140))
    # Instrucción para volver
    volver = font_peq.render(
        "Presiona ESC para volver al menu principal.", True, c.AMARILLO_COLOR
    )
    screen.blit(volver, (60, c.SCREEN_HEIGHT - 60))
    pygame.display.update()
