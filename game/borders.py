from turtle import Turtle
from game.config import *


class Border(Turtle):
    """Un borde individual (rectángulo visual)"""
    
    def __init__(self, x, y, width, height, color, is_scoring=False):
        super().__init__()
        self.is_scoring = is_scoring
        
        # Configuración visual
        self.shape("square")
        self.color(color)
        self.penup()
        
        # Estirar para hacer rectángulo
        self.shapesize(stretch_wid=height / 20, stretch_len=width / 20)
        
        # Posicionar
        self.goto(x, y)
        
        # Guardar configuración original
        self.original_width = width
        self.original_height = height
        self.color_name = color
    
    def update_position(self, x, y, width, height, color=None):
        """Actualiza la posición y tamaño del borde"""
        # Nueva posición
        self.goto(x, y)
        
        # Nuevo tamaño
        self.shapesize(stretch_wid=height / 20, stretch_len=width / 20)
        
        # Nuevo color (si se especifica)
        if color:
            self.color(color)
        
        # Actualizar límites
        self.original_width = width
        self.original_height = height


class BorderManager:
    """Gestiona los 4 bordes del campo de juego"""
    
    def __init__(self):
        self.borders = []
        self.current_width = SCREEN_WIDTH
        self.current_height = SCREEN_HEIGHT
        self._create_borders()
    
    def _create_borders(self):
        """Crea los 4 bordes: top, bottom, left, right"""
        half_width = self.current_width / 2
        half_height = self.current_height / 2
        
        # Borde superior (solo rebote) - línea horizontal
        top = Border(
            x=0,
            y=half_height - TOP_BOTTOM_BORDER_HEIGHT / 2,
            width=self.current_width,  # extiende por todo el ancho
            height=TOP_BOTTOM_BORDER_HEIGHT,
            color=TOP_BOTTOM_BORDER_COLOR,
            is_scoring=False
        )
        
        # Borde inferior (solo rebote) - línea horizontal
        bottom = Border(
            x=0,
            y=-half_height + TOP_BOTTOM_BORDER_HEIGHT / 2,
            width=self.current_width,
            height=TOP_BOTTOM_BORDER_HEIGHT,
            color=TOP_BOTTOM_BORDER_COLOR,
            is_scoring=False
        )
        
        # Borde izquierdo (scoring)
        left = Border(
            x=-half_width + LEFT_RIGHT_BORDER_WIDTH / 2,
            y=0,
            width=LEFT_RIGHT_BORDER_WIDTH,
            height=self.current_height,
            color=LEFT_BORDER_COLOR,
            is_scoring=True
        )
        
        # Borde derecho (scoring)
        right = Border(
            x=half_width - LEFT_RIGHT_BORDER_WIDTH / 2,
            y=0,
            width=LEFT_RIGHT_BORDER_WIDTH,
            height=self.current_height,
            color=RIGHT_BORDER_COLOR,
            is_scoring=True
        )
        
        self.borders = [top, bottom, left, right]
    
    def update_size(self, new_width, new_height):
        """Actualiza los bordes cuando la pantalla cambia de tamaño"""
        if new_width == self.current_width and new_height == self.current_height:
            return  # No hay cambio
        
        self.current_width = new_width
        self.current_height = new_height
        
        half_width = new_width / 2
        half_height = new_height / 2
        
        # Actualizar cada borde
        # Top
        self.borders[0].update_position(
            x=0,
            y=half_height - TOP_BOTTOM_BORDER_HEIGHT / 2,
            width=new_width,
            height=TOP_BOTTOM_BORDER_HEIGHT
        )
        
        # Bottom
        self.borders[1].update_position(
            x=0,
            y=-half_height + TOP_BOTTOM_BORDER_HEIGHT / 2,
            width=new_width,
            height=TOP_BOTTOM_BORDER_HEIGHT
        )
        
        # Left
        self.borders[2].update_position(
            x=-half_width + LEFT_RIGHT_BORDER_WIDTH / 2,
            y=0,
            width=LEFT_RIGHT_BORDER_WIDTH,
            height=new_height,
            color=LEFT_BORDER_COLOR
        )
        
        # Right
        self.borders[3].update_position(
            x=half_width - LEFT_RIGHT_BORDER_WIDTH / 2,
            y=0,
            width=LEFT_RIGHT_BORDER_WIDTH,
            height=new_height,
            color=RIGHT_BORDER_COLOR
        )
    
    def check_collision(self, ball):
        """
        Detecta colisión de la pelota con algún borde.
        
        Retorna:
            - "bounce": si debe rebotar (top/bottom)
            - "score_left": si marcó punto el jugador izquierdo
            - "score_right": si marcó punto el jugador derecho
            - None: si no hay colisión
        """
        ball_x = ball.xcor()
        ball_y = ball.ycor()
        ball_radius = 10  # radio aproximado de la pelota
        
        half_width = self.current_width / 2
        half_height = self.current_height / 2
        
        # Rebote en borde superior
        if ball_y + ball_radius > half_height - TOP_BOTTOM_BORDER_HEIGHT:
            return "bounce"
        
        # Rebote en borde inferior
        if ball_y - ball_radius < -half_height + TOP_BOTTOM_BORDER_HEIGHT:
            return "bounce"
        
        # Scoring en borde izquierdo
        if ball_x - ball_radius < -half_width + LEFT_RIGHT_BORDER_WIDTH:
            return "score_left"
        
        # Scoring en borde derecho
        if ball_x + ball_radius > half_width - LEFT_RIGHT_BORDER_WIDTH:
            return "score_right"
        
        return None
    
    def hide_all(self):
        """Oculta todos los bordes"""
        for border in self.borders:
            border.hideturtle()
