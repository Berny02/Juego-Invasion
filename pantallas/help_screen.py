import pygame


def mostrar_help(screen, font_peq, font_titulo, c):
    screen.fill(c.AZUL_OSCURO_COLOR)
    # Título
    titulo = font_titulo.render("Ayuda", True, c.AMARILLO_COLOR)
    screen.blit(titulo, (c.SCREEN_WIDTH // 2 - titulo.get_width() // 2, 60))

    instrucciones = [
        "Movimientos:",
        "  W / Flecha Arriba    - Mover arriba",
        "  S / Flecha Abajo     - Mover abajo",
        "  A / Flecha Izquierda - Mover izquierda",
        "  D / Flecha Derecha   - Mover derecha",
        "",
        "Disparo:",
        "  Mouse / Click Izquierdo - Disparar",
        "",
        "Objetivo:",
        " - Encuentra la llave eliminando la mayor",
        "   cantidad de enemigos posible.",
        " - Recoge pociones para recuperar vida y",
        "   monedas para aumentar tu puntaje.",
        "",
        "Presiona ESC para volver al menu principal.",
    ]
    subtitulos = {"Movimientos:", "Disparo:", "Objetivo:", " ESC"}
    for i, linea in enumerate(instrucciones):
        color = c.AMARILLO_COLOR if linea in subtitulos else c.BLANCO_COLOR
        texto = font_peq.render(linea, True, color)
        screen.blit(texto, (60, 140 + i * 22))
    pygame.display.update()
