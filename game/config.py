SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

RIGHT_PADDLE_POSITION = (600, 0)
LEFT_PADDLE_POSITION = (-600, 0)

PADDLE_MOVE = 25

PADDLE_STRETCH = 6
PADDLE_WIDTH = 1

RIGHT_PADDLE_COLOR = "cyan"
LEFT_PADDLE_COLOR = "magenta"

# Límites del movimiento
PADDLE_HALF_HEIGHT = PADDLE_STRETCH * 20 / 2  # 20px por unidad turtle

TOP_LIMIT = (SCREEN_HEIGHT / 2) - PADDLE_HALF_HEIGHT
BOTTOM_LIMIT = -(SCREEN_HEIGHT / 2) + PADDLE_HALF_HEIGHT

def calculate_limits(window_height):  ## Devuelve los límites de movimiento superior e inferior para la paleta.
    top = (window_height / 2) - PADDLE_HALF_HEIGHT
    bottom = -(window_height / 2) + PADDLE_HALF_HEIGHT
    return top, bottom 

