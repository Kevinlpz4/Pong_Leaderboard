# Pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# posición inicial de las paletas
RIGHT_PADDLE_POSITION = (600, 0)
LEFT_PADDLE_POSITION = (-600, 0)

# Velocidad de movimiento de las paletas
PADDLE_MOVE = 30 

# Dimensiones de las paletas
PADDLE_STRETCH = 6
PADDLE_WIDTH = 1

# Colores de las paletas
RIGHT_PADDLE_COLOR = "cyan"
LEFT_PADDLE_COLOR = "magenta"

# posición inicial de la pelota
BALL_START_POSITION = (0, 0)

# Velocidad de la pelota
BALL_SPEED = 15

# color de la pelota
BALL_COLOR = "white"

# Límites del movimiento
PADDLE_HALF_HEIGHT = PADDLE_STRETCH * 20 / 2  # 20px por unidad turtle

TOP_LIMIT = (SCREEN_HEIGHT / 2) - PADDLE_HALF_HEIGHT
BOTTOM_LIMIT = -(SCREEN_HEIGHT / 2) + PADDLE_HALF_HEIGHT

def calculate_limits(window_height):  ## Devuelve los límites de movimiento superior e inferior para la paleta.
    top = (window_height / 2) - PADDLE_HALF_HEIGHT - TOP_BOTTOM_BORDER_HEIGHT
    bottom = -(window_height / 2) + PADDLE_HALF_HEIGHT + TOP_BOTTOM_BORDER_HEIGHT
    return top, bottom 

# ============================================
# BORDES
# ============================================

# Bordes superiores/inferiores (solo rebote)
TOP_BOTTOM_BORDER_COLOR = "gray"
TOP_BOTTOM_BORDER_WIDTH = 20  # ancho del rectángulo
TOP_BOTTOM_BORDER_HEIGHT = 60  # alto del rectángulo

# Bordes izquierdo/derecho (scoring)
LEFT_BORDER_COLOR = "cyan"
RIGHT_BORDER_COLOR = "magenta"
LEFT_RIGHT_BORDER_WIDTH = 40 
LEFT_RIGHT_BORDER_HEIGHT = 100


