from turtle import Screen
from game.paddle import Paddle
from game.config import *

# Crear pantalla
screen = Screen()
screen.title("Pong")
screen.bgcolor("black")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

# Crear paletas
right_paddle = Paddle(RIGHT_PADDLE_POSITION, RIGHT_PADDLE_COLOR)
left_paddle = Paddle(LEFT_PADDLE_POSITION, LEFT_PADDLE_COLOR)

# Escuchar teclado
screen.listen()

screen.onkey(right_paddle.move_up, "Up")
screen.onkey(right_paddle.move_down, "Down")

screen.onkey(left_paddle.move_up, "w")
screen.onkey(left_paddle.move_down, "s")

screen.mainloop()
