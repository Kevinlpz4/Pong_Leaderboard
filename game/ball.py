from turtle import Turtle
from game.config import *

class Ball(Turtle):

    def __init__(self,color,position):
        super().__init__()
        self.shape("circle")
        self.color(color)
        self.penup()
        self.goto(position)
        self.speed("fastest")

        # velocidad
        self.x_move = BALL_SPEED
        self.y_move = BALL_SPEED

        # movimiento
    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

        # rebote vertical
    def bounce_y(self):
        self.y_move *= -1   
        
        # rebote horizontal
    def bounce_x(self):
        self.x_move *= -1

    # reiniciar posición
    def reset_position(self):
        self.goto(0, 0)
        self.bounce_x()  # Cambia la dirección horizontal al reiniciar