# Invasion: The Key to Survival

Top-down shooter desarrollado con **Pygame** donde debes sobrevivir, eliminar enemigos, derrotar al jefe final y encontrar la llave para escapar en cada nivel.

## 🎮 Descripción

En **Invasion: The Key to Survival** controlas a un personaje en un mundo hostil con enemigos que te persiguen por visión y distancia. El objetivo es progresar por los niveles, maximizar tu puntaje y completar la partida en el menor tiempo posible.

El juego incluye:

- Sistema de combate con arma de fuego y daño variable.
- Barra de vida del jugador y del jefe final.
- Ítems coleccionables (monedas, pociones y llave).
- Sistema de niveles cargados desde archivos CSV.
- Registro de puntajes con nombre del jugador y tiempo.

## ✨ Características principales

- **4 niveles** con progresión (`lvl1.csv` a `lvl4.csv`).
- **Enemigos comunes** y **jefe final** con fases.
- **Sonidos y música** de ambiente y combate.
- **Pantalla de inicio** con menú de Play, Help, Scores y Créditos.
- **Tabla de mejores puntajes** (Top 10) en `scores.json`.

## 🕹️ Controles

- **Moverse:** `W A S D` o flechas.
- **Disparar:** clic izquierdo del mouse.
- **Reiniciar tras Game Over:** `R` (o botón de reinicio en pantalla).
- **Salir del juego:** `ESC`.

## 🧪 Mecánicas de juego

- Daño de bala aproximado: **10 a 20** por impacto.
- Daño enemigo al contacto: **10** por golpe (con cooldown).
- Ítems:
  - Moneda oro: `+10` puntos.
  - Moneda rubí: `+100` puntos.
  - Moneda plata: `+1` punto.
  - Poción: `+25` energía (máx. 100).
  - Llave: habilita completar nivel.

## 🧰 Requisitos

- Python 3.10+ (recomendado)
- `pygame`

## 🚀 Instalación y ejecución

1. Clona el repositorio:

	```bash
	git clone https://github.com/Berny02/Juego-Invasion.git
	cd Juego-Invasion
	```

2. (Opcional) Crea un entorno virtual:

	```bash
	python -m venv .venv
	```

	En Windows (PowerShell):

	```powershell
	.\.venv\Scripts\Activate.ps1
	```

3. Instala dependencias:

	```bash
	pip install pygame
	```

4. Ejecuta el juego:

	```bash
	python main.py
	```

## 📁 Estructura del proyecto

```text
Juego/
├── main.py                 # Bucle principal y flujo del juego
├── Personajes.py           # Lógica del jugador, enemigos y boss
├── armas.py                # Arma y balas
├── items.py                # Ítems coleccionables y explosiones
├── mundo.py                # Carga y render del mapa
├── constantes.py           # Configuración global
├── niveles/                # Mapas CSV por nivel
├── pantallas/              # Help, scores, créditos y registro
├── assets/                 # Imágenes, fuentes, sonidos y tiles
└── scores.json             # Puntajes guardados
```

## 🏆 Puntajes

Al terminar el último nivel:

1. Se solicita tu nombre.
2. Se guarda `nombre`, `score` y `tiempo` en `scores.json`.
3. La pantalla de Scores ordena por:
	- Mayor puntaje.
	- Menor tiempo en caso de empate.

## 👥 Créditos

- Desarrollo: **Alejandro Loaiza** y **Bernardo Castaño**.
- Profesor: **Francisco Medina**.
- Recursos:
  - Sonidos: pixabay.com
  - Sprites/Tilesets: itch.io

## 📌 Estado del proyecto

Proyecto académico funcional, en constante mejora. Si quieres proponer mejoras (balance, UI, nuevos niveles o enemigos), puedes abrir un issue o hacer un fork.