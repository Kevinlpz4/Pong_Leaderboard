from turtle import Turtle
from game.config import *


class Scoreboard(Turtle):
    """Marcador de puntuación del juego"""
    
    def __init__(self, left_letter="I", right_letter="D"):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color(SCOREBOARD_COLOR)
        
        # Letras de los jugadores
        self.left_letter = left_letter.upper()
        self.right_letter = right_letter.upper()
        
        # Puntuación inicial
        self.left_score = 0
        self.right_score = 0
        
        # Posición
        self.current_y = 0
        
        # Mostrar marcador inicial
        self.update_display()
    
    def set_letters(self, left_letter, right_letter):
        """Actualiza las letras de los jugadores"""
        self.left_letter = left_letter.upper()
        self.right_letter = right_letter.upper()
        self.update_display()
    
    def increase_left(self):
        """Aumenta el score del jugador izquierdo"""
        self.left_score += 1
        self.update_display()
    
    def increase_right(self):
        """Aumenta el score del jugador derecho"""
        self.right_score += 1
        self.update_display()
    
    def update_display(self):
        """Actualiza el display del marcador"""
        self.clear()
        
        # Posicionar en el centro-arriba
        # Formato: S:1 - K:7
        self.goto(0, self.current_y)
        self.write(
            f"{self.left_letter}:{self.left_score} - {self.right_letter}:{self.right_score}",
            align=SCOREBOARD_ALIGN,
            font=SCOREBOARD_FONT
        )
    
    def update_position(self, window_width, window_height):
        """Actualiza la posición del marcador según el tamaño de ventana"""
        half_height = window_height / 2
        # Posicionar exactamente debajo del borde superior
        self.current_y = half_height - TOP_BOTTOM_BORDER_HEIGHT - 90
        self.update_display()
    
    def reset(self):
        """Resetea el marcador a 0-0"""
        self.left_score = 0
        self.right_score = 0
        self.update_display()