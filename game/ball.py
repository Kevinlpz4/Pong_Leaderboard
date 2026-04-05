from turtle import Turtle
from game.config import *
from settings import get_settings
import math

# Load settings
settings = get_settings()

# Ángulo máximo de rebote (en radianes)
MAX_BOUNCE_ANGLE = math.pi / 4  # 45 grados


class Ball(Turtle):

    def __init__(self, color, position):
        super().__init__()
        self.shape("circle")
        self.color(color)
        self.penup()
        self.goto(position)
        self.speed("fastest")

        # Velocidad inicial
        self.x_move = BALL_SPEED
        self.y_move = BALL_SPEED
        
        # Track bounces for speed increment
        self.bounce_count = 0
        self.max_speed = settings.ball_max_speed
        self.speed_increment = settings.ball_speed_increment

    # movimiento
    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def _increase_speed(self):
        """Aumenta la velocidad de la pelota después de un rebote"""
        self.bounce_count += 1
        
        # Solo aumentar si no ha alcanzado la velocidad máxima
        current_speed = abs(self.x_move)
        if current_speed < self.max_speed:
            self.x_move *= self.speed_increment
            self.y_move *= self.speed_increment

    # rebote vertical
    def bounce_y(self):
        self.y_move *= -1
        self._increase_speed()
    
    def bounce_x(self, paddle=None, is_left_paddle=True):
        """
        Rebote horizontal con ángulo basado en dónde pega en la pala.
        
        Args:
            paddle: Objeto paleta (opcional)
            is_left_paddle: True si es la paleta izquierda, False si es la derecha
        """
        current_speed = math.sqrt(self.x_move**2 + self.y_move**2)
        
        if paddle is not None:
            # Calcular ángulo basado en posición relativa a la pala
            offset = (self.ycor() - paddle.ycor()) / PADDLE_HALF_HEIGHT
            # Limitar el offset entre -1 y 1
            offset = max(-1, min(1, offset))
            
            # Calcular ángulo de rebote
            angle = offset * MAX_BOUNCE_ANGLE
            
            # Nueva velocidad con ángulo
            self.x_move = -current_speed * math.cos(angle)
            self.y_move = current_speed * math.sin(angle)
        else:
            # Rebote simple si no hay pala
            self.x_move *= -1
        
        self._increase_speed()

    # reiniciar posición
    def reset_position(self):
        self.goto(0, 0)
        self.bounce_x()  # Cambia la dirección horizontal al reiniciar