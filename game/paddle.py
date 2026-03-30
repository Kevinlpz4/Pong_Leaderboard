from turtle import Turtle
from game.config import *

class Paddle(Turtle):

    def __init__(self, position, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=PADDLE_STRETCH, stretch_len=PADDLE_WIDTH)  # paleta vertical
        self.penup()
        self.goto(position)

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
 