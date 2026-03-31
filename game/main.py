""" Pong - Juego clásico de ping pong """

from turtle import Screen
from game.paddle import Paddle
from game.ball import Ball
from game.borders import BorderManager
from game.collision import CollisionManager
from game.config import *
import time

# ============================================
# INICIALIZACIÓN
# ============================================

# Crear pantalla
screen = Screen()
screen.title("Pong")
screen.bgcolor("black")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)


# ============================================
# CREAR OBJETOS DEL JUEGO
# ============================================

# Paletas
right_paddle = Paddle(RIGHT_PADDLE_POSITION, RIGHT_PADDLE_COLOR, is_left=False)
left_paddle = Paddle(LEFT_PADDLE_POSITION, LEFT_PADDLE_COLOR, is_left=True)

# Pelota
ball = Ball(BALL_COLOR, BALL_START_POSITION)

# Bordes (incluye scoring)
border_manager = BorderManager()

# Gestor de colisiones
collision_manager = CollisionManager()


# ============================================
# CONTROLES - Sistema de keys activas
# ============================================

# Diccionario de keys activas
keys = {
    "Up": False,      # Paleta derecha arriba
    "Down": False,    # Paleta derecha abajo
    "w": False,       # Paleta izquierda arriba
    "s": False,       # Paleta izquierda abajo
}

def on_key_press(key):
    """Se llama cuando se presiona una tecla"""
    if key in keys:
        keys[key] = True

def on_key_release(key):
    """Se llama cuando se suelta una tecla"""
    if key in keys:
        keys[key] = False

screen.listen()
# Press
screen.onkeypress(lambda: on_key_press("Up"), "Up")
screen.onkeypress(lambda: on_key_press("Down"), "Down")
screen.onkeypress(lambda: on_key_press("w"), "w")
screen.onkeypress(lambda: on_key_press("s"), "s")
# Release
screen.onkeyrelease(lambda: on_key_release("Up"), "Up")
screen.onkeyrelease(lambda: on_key_release("Down"), "Down")
screen.onkeyrelease(lambda: on_key_release("w"), "w")
screen.onkeyrelease(lambda: on_key_release("s"), "s")


# ============================================
# GAME LOOP
# ============================================

while True:
    # Verificar cambio de tamaño de ventana
    current_width = screen.window_width()
    current_height = screen.window_height()
    border_manager.update_size(current_width, current_height)
    left_paddle.update_position(current_width, current_height)
    right_paddle.update_position(current_width, current_height)
    
    # Mover paletas según keys activas
    if keys["Up"]:
        right_paddle.move_up()
    if keys["Down"]:
        right_paddle.move_down()
    if keys["w"]:
        left_paddle.move_up()
    if keys["s"]:
        left_paddle.move_down()
    
    # Mover pelota
    ball.move()
    
    # Actualizar pantalla
    screen.update()
    time.sleep(0.01)  # Más fluido (10ms en vez de 50ms)
    
    # Verificar colisión con bordes
    collision = border_manager.check_collision(ball)
    
    if collision == "bounce":
        ball.bounce_y()
    
    elif collision == "score_left":
        # Punto para jugador izquierdo
        print("¡Punto para jugador izquierdo!")
        ball.reset_position()
    
    elif collision == "score_right":
        # Punto para jugador derecho
        print("¡Punto para jugador derecho!")
        ball.reset_position()
    
    # Verificar colisión con paletas
    paddle_hit = collision_manager.check_paddle_collision(
        ball, left_paddle, right_paddle
    )
    
    if paddle_hit:
        ball.bounce_x()
