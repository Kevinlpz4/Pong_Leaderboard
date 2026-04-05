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
from turtle import Screen, Turtle, textinput
from game.game_controller import GameController, GameState
from game.player_setup import PlayerSetup
from game.config import *
from settings import get_settings
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


def ask_replay(screen):
    """Pregunta si quieren jugar de nuevo
    Retorna:
        'S' - Nueva partida (volver al menú)
        'N' - Salir
    """
    while True:
        response = textinput("Pong", "¿Jugar de nuevo? (S/N):")
        
        if response:
            response = response.strip().upper()
            if response in ["S", "N"]:
                return response
        # Si pone algo más, seguir preguntando


def show_goodbye(screen):
    """Muestra pantalla de despedida"""
    title = Turtle()
    title.penup()
    title.hideturtle()
    title.color("white")
    
    w = screen.window_width()
    h = screen.window_height()
    hh = h / 2
    
    title.goto(0, 0)
    title.write("¡Gracias por jugar!", align="center", font=("Arial", 50, "bold"))
    
    screen.update()
    time.sleep(2)


def init_screen():
    """Inicializa la pantalla una sola vez"""
    # Load settings
    settings = get_settings()
    
    screen = Screen()
    screen.title(settings.game_title)
    screen.bgcolor("black")
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.tracer(0)
    
    # Maximizar ventana
    screen.getcanvas().winfo_toplevel().attributes('-zoomed', True)
    
    return screen


# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    # Load settings
    settings = get_settings()
    
    # Crear screen UNA sola vez al inicio
    screen = init_screen()
    
    while True:
        # Si ya pasaron la primera ronda, solo mostrar menú (no crear screen nuevo)
        show_menu(screen)
        
        # Configurar jugadores (incluye cantidad de goles)
        player_setup = PlayerSetup(screen)
        left_player, right_player, max_goals = player_setup.setup_players()
        
        # Crear controlador del juego
        game = GameController(screen, left_player, right_player, max_goals)
        
        # Loop principal
        while not game.game_over:
            game.update()
            game.update_screen()
            time.sleep(1 / settings.game_fps)  # FPS configurable
        
        # Mostrar pantalla de game over
        result_turtle = game.show_game_over()
        
        # Preguntar si juegan de nuevo
        screen.update()
        time.sleep(0.5)  # Pequeña pausa
        
        response = ask_replay(screen)
        
        # Limpiar resultado y todos los elementos del juego
        if result_turtle:
            result_turtle.clear()
            result_turtle.hideturtle()
        
        # Limpiar completamente el juego anterior
        game.cleanup()
        
        if response == "N":
            # Salir
            show_goodbye(screen)
            break
        # Si response == "S", vuelve al inicio del while (mostrar menú)