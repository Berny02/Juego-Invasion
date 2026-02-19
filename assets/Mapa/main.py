from PIL import Image
import os

def dividir_guardar_imagen(ruta, destino, divisiones_porcol):
    img = Image.open(ruta)
    ancho, alto = img.size

    size_square = ancho // divisiones_porcol
    divisiones_fila = alto // size_square

    os.makedirs(destino, exist_ok=True)
    
    contador = 0
    for i in range(divisiones_fila):
        for j in range(divisiones_porcol):
            x = j * size_square
            y = i * size_square
            derecha = x + size_square
            abajo = y + size_square

            cuadrado = img.crop((x, y, derecha, abajo))
            nombre_archivo = f"Fase_2({contador+1}).png"
            cuadrado.save(os.path.join(destino, nombre_archivo))
            contador += 1

    img.close()

# Ejemplo de uso
dividir_guardar_imagen("assets\images\characters\Transform_boss\Big_bloated_sneer.png", "assets\images\characters\Transform_boss", 4)
