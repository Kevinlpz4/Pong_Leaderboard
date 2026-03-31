from turtle import Turtle
from game.config import *


class Paddle(Turtle):
    
    # Distancia desde el borde
    EDGE_MARGIN = 100
    
    def __init__(self, position, color, is_left=False):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=PADDLE_STRETCH, stretch_len=PADDLE_WIDTH)
        self.penup()
        self.goto(position)
        
        # Guardar si es paleta izquierda o derecha
        self.is_left = is_left
        
        # Mitad del alto de la paleta
        self.paddle_half_height = PADDLE_STRETCH * 20 / 2
    
    def _get_limits(self):
        height = self.getscreen().window_height()
        return calculate_limits(height)
    
    def move_up(self):
        top_limit, _ = self._get_limits()
        if self.ycor() < top_limit:
            self.goto(self.xcor(), self.ycor() + PADDLE_MOVE)
    
    def move_down(self):
        _, bottom_limit = self._get_limits()
        if self.ycor() > bottom_limit:
            self.goto(self.xcor(), self.ycor() - PADDLE_MOVE)
    
    def update_position(self, window_width, window_height):
        """Actualiza la posición X de la paleta según el tamaño de ventana"""
        half_width = window_width / 2
        
        if self.is_left:
            # Paleta izquierda: a la izquierda
            new_x = -half_width + self.EDGE_MARGIN + (LEFT_RIGHT_BORDER_WIDTH / 2)
        else:
            # Paleta derecha: a la derecha
            new_x = half_width - self.EDGE_MARGIN - (LEFT_RIGHT_BORDER_WIDTH / 2)
        
        # Mantener la posición Y actual, solo actualizar X
        self.goto(new_x, self.ycor())
