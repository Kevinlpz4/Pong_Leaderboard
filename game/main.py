"""
Pong - Juego clásico de ping pong
=================================================================
ARQUITECTURA:
- main.py: Punto de entrada, solo inicializa
- GameController: Toda la lógica del juego
- Player: Datos de cada jugador
- Scoreboard: Mostrar marcador
- BorderManager: Bordes del campo
- CollisionManager: Detección de colisiones

FLUJO:
1. Crear pantalla
2. Configurar jugadores (PlayerSetup)
3. Crear GameController
4. Iniciar loop: controller.update() -> screen.update()
=================================================================
"""
from turtle import Screen, Turtle
from game.game_controller import GameController
from game.player_setup import PlayerSetup
from game.config import *
import time

def show_menu(screen):
    """Muestra el menú de inicio simple"""
    title = Turtle()
    title.penup()
    title.hideturtle()
    title.color("white")
    
    start_btn = Turtle()
    start_btn.penup()
    start_btn.hideturtle()
    start_btn.color("#22c55e")
    
    instructions = Turtle()
    instructions.penup()
    instructions.hideturtle()
    instructions.color("gray")
    
    game_started = False
    
    def start_game():
        nonlocal game_started
        game_started = True
    
    screen.listen()
    screen.onkeypress(start_game, "Return")
    
    while not game_started:
        w = screen.window_width()
        h = screen.window_height()
        hh = h / 2
        
        title.clear()
        title.goto(0, hh * 0.15)
        title.write("PONG", align="center", font=("Arial", 100, "bold"))
        
        start_btn.clear()
        start_btn.goto(0, -hh * 0.1)
        start_btn.write("START", align="center", font=("Arial", 40, "bold"))
        
        instructions.clear()
        instructions.goto(0, -hh * 0.35)
        instructions.write("Presiona ENTER para comenzar", align="center", font=("Arial", 18, "normal"))
        
        screen.update()
        time.sleep(0.01)
    
    # Limpiar menú
    title.clear()
    start_btn.clear()
    instructions.clear()
    title.hideturtle()
    start_btn.hideturtle()
    instructions.hideturtle()


# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    # 1. Crear pantalla
    screen = Screen()
    screen.title("Pong")
    screen.bgcolor("black")
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.tracer(0)
    
    # Maximizar ventana
    screen.getcanvas().winfo_toplevel().attributes('-zoomed', True)
    
    # 2. Mostrar menú de inicio
    show_menu(screen)
    
    # 3. Configurar jugadores
    player_setup = PlayerSetup(screen)
    left_player, right_player = player_setup.setup_players()
    
    # 4. Crear controlador del juego
    game = GameController(screen, left_player, right_player)
    
    # 5. Loop principal
    while True:
        game.update()
        game.update_screen()
        time.sleep(0.01)  # ~100 FPS