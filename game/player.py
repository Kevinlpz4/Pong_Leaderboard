"""
Player - Representa un jugador del juego
"""
from game.config import *


class Player:
    """Clase que representa un jugador con sus datos"""
    
    def __init__(self, name, letter, color):
        self.name = name
        self.letter = letter.upper()
        self.color = color
        self.score = 0
    
    def __repr__(self):
        return f"Player({self.name}, {self.letter}, {self.score})"