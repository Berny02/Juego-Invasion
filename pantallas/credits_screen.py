import pygame


def mostrar_credits(screen, font_peq, font_titulo, c):
    screen.fill(c.AZUL_OSCURO_COLOR)
    titulo = font_titulo.render("Créditos", True, c.AMARILLO_COLOR)
    screen.blit(titulo, (c.SCREEN_WIDTH // 2 - titulo.get_width() // 2, 60))
    creditos = [
        "Juego desarrollado por: ",
        "Alejandro Loaiza",
        "Bernardo Castaño",
        "Profesor: ",
        "Francisco Medina",
        "Sonidos: pixabay.com",
        "Sprites: itch.io",
        "Tileset: itch.io",
        "",
        "Agradecimientos a la comunidad pygame.",
        "",
        "Presiona ESC para volver al menu principal.",
    ]
    for i, linea in enumerate(creditos):
        texto = font_peq.render(linea, True, c.BLANCO_COLOR)
        screen.blit(texto, (60, 160 + i * 32))
    pygame.display.update()
