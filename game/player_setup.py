"""
PlayerSetup - Maneja la configuración inicial de jugadores
"""
import turtle
from turtle import textinput
from game.player import Player
from game.config import *


class PlayerSetup:
    """Maneja la configuración de jugadores antes de iniciar el juego"""
    
    # Colores disponibles para elegir
    AVAILABLE_COLORS = [
        ("cyan", "Cian"),
        ("magenta", "Magenta"),
        ("yellow", "Amarillo"),
        ("orange", "Naranja"),
        ("green", "Verde"),
        ("red", "Rojo"),
    ]
    
    def __init__(self, screen):
        self.screen = screen
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
    
    def setup_players(self):
        """Configura ambos jugadores antes del juego"""
        # Crear ventana de input simple usando turtle
        # Jugador 1 (Izquierda)
        left_player = self._setup_single_player("izquierdo")
        
        # Jugador 2 (Derecha) - asegurar que no repita letra
        right_player = self._setup_single_player("derecho", exclude_letter=left_player.letter)
        
        # Preguntar a cuántos goles jugar
        max_goals = self._setup_max_goals()
        
        return left_player, right_player, max_goals
    
    def _setup_max_goals(self):
        """Configura la cantidad de goles para ganar"""
        self.turtle.clear()
        self.turtle.goto(0, 80)
        self.turtle.color("white")
        self.turtle.write("¿A cuántos goles se juega?", align="center", font=("Arial", 18, "normal"))
        
        # Mostrar sugerencias
        self.turtle.goto(0, 20)
        self.turtle.color("gray")
        self.turtle.write("Opciones: 3, 5, 7, 10 (o escribe la cantidad)", align="center", font=("Arial", 12, "normal"))
        
        goals = self._get_text_input("Goles (número):")
        
        # Validar que sea número válido
        while not goals or not goals.strip().isdigit() or int(goals.strip()) < 1:
            self.turtle.clear()
            self.turtle.goto(0, 50)
            self.turtle.color("red")
            self.turtle.write("Ingresa un número válido mayor a 0", align="center", font=("Arial", 14, "normal"))
            self.turtle.color("white")
            self.turtle.goto(0, -20)
            self.turtle.write("¿A cuántos goles se juega?", align="center", font=("Arial", 18, "normal"))
            goals = self._get_text_input("Goles (número):")
        
        max_goals = int(goals.strip())
        
        # Limpiar
        self.turtle.clear()
        
        return max_goals
    
    def _setup_single_player(self, side, exclude_letter=None):
        """Configura un solo jugador"""
        # Limpiar pantalla previa
        self.turtle.clear()
        
        # Pedir nombre
        self.turtle.goto(0, 100)
        self.turtle.color("white")
        self.turtle.write(f"Jugador {side}: Ingresa tu nombre:", align="center", font=("Arial", 16, "normal"))
        
        # Obtener nombre del jugador
        name = self._get_text_input("Nombre ( ENTER para continuar):")
        
        # Validar nombre
        if not name or name.strip() == "":
            name = f"Jugador_{side[0].upper()}"
        
        name = name.strip()
        
        # Limpiar y pedir letra
        self.turtle.clear()
        self.turtle.goto(0, 100)
        self.turtle.write(f"{name}: Elige una letra representativa:", align="center", font=("Arial", 16, "normal"))
        
        letter = self._get_text_input("Letra (1 carácter):", max_length=1)
        
        # Validar letra (asegurar que no sea None ni vacía)
        while not letter or letter.strip() == "" or len(letter.strip()) != 1 or not letter.strip().isalpha():
            self.turtle.clear()
            self.turtle.goto(0, 50)
            self.turtle.color("red")
            self.turtle.write("Debe ser exactamente 1 letra. Intenta de nuevo.", align="center", font=("Arial", 12, "normal"))
            self.turtle.color("white")
            self.turtle.goto(0, -50)
            self.turtle.write(f"{name}: Elige una letra representativa:", align="center", font=("Arial", 16, "normal"))
            letter = self._get_text_input("Letra (1 carácter):", max_length=1)
            if not letter:
                letter = ""
        
        # Normalizar letra
        if not letter:
            letter = "X"  # Default si cancela
        else:
            letter = letter.strip().upper()
        
        # Si hay letra excluida (para jugador 2)
        if exclude_letter:
            while letter == exclude_letter:
                self.turtle.clear()
                self.turtle.goto(0, 50)
                self.turtle.color("red")
                self.turtle.write(f"La letra {exclude_letter} ya fue usada. Elige otra.", align="center", font=("Arial", 12, "normal"))
                self.turtle.color("white")
                self.turtle.goto(0, -50)
                self.turtle.write(f"{name}: Elige una letra representativa:", align="center", font=("Arial", 16, "normal"))
                letter = self._get_text_input("Letra (1 carácter):", max_length=1)
                if not letter:
                    letter = ""
                if not letter:
                    letter = "X"
                else:
                    letter = letter.upper()
        
        # Limpiar y pedir color
        self.turtle.clear()
        self.turtle.goto(0, 120)
        self.turtle.color("white")
        self.turtle.write(f"{name}: Escribe el color de tu paleta:", align="center", font=("Arial", 16, "normal"))
        
        # Mostrar opciones de color disponibles
        y_pos = 30
        colors_text = []
        for color_name, color_display in self.AVAILABLE_COLORS:
            self.turtle.goto(-100, y_pos)
            self.turtle.color(color_name)
            self.turtle.write(color_display, align="center", font=("Arial", 12, "normal"))
            colors_text.append(color_display.lower())
            y_pos -= 25
        
        # Pedir color como texto
        color_name = self._get_text_input("Color (escribe el nombre):")
        
        # Validar color - buscar por nombre o número
        valid_colors = [c[0] for c in self.AVAILABLE_COLORS]  # nombres técnicos
        valid_names = [c[1].lower() for c in self.AVAILABLE_COLORS]  # nombres legibles
        
        # Normalizar input
        if color_name:
            color_name = color_name.strip().lower()
        
        # Verificar si es válido (por nombre o número)
        while not color_name or (
            color_name not in valid_colors and 
            color_name not in valid_names and 
            not color_name.isdigit()
        ):
            self.turtle.clear()
            self.turtle.goto(0, 80)
            self.turtle.color("red")
            self.turtle.write("Color inválido. Intenta de nuevo.", align="center", font=("Arial", 12, "normal"))
            self.turtle.color("white")
            
            # Mostrar opciones de nuevo
            y_pos = 0
            for color_name_disp, color_display in self.AVAILABLE_COLORS:
                self.turtle.goto(-100, y_pos)
                self.turtle.color(color_name_disp)
                self.turtle.write(color_display, align="center", font=("Arial", 12, "normal"))
                y_pos -= 25
            
            color_name = self._get_text_input("Color (escribe el nombre):")
            if color_name:
                color_name = color_name.strip().lower()
        
        # Determinar el color seleccionado
        if color_name.isdigit():
            # Si escribió número
            color_index = int(color_name) - 1
            selected_color = self.AVAILABLE_COLORS[color_index][0]
        elif color_name in valid_names:
            # Si escribió nombre legible (ej: "cian")
            color_index = valid_names.index(color_name)
            selected_color = self.AVAILABLE_COLORS[color_index][0]
        else:
            # Si escribió nombre técnico (ej: "cyan")
            selected_color = color_name
        
        # Limpiar
        self.turtle.clear()
        
        return Player(name, letter, selected_color)
    
    def _get_text_input(self, prompt, max_length=None):
        """Obtiene entrada de texto del usuario usando turtle textinput"""
        # Usar textinput que permite ingreso de texto
        from turtle import textinput
        result = textinput("Pong", prompt)
        
        if result is None:
            return ""
        
        if max_length:
            result = result[:max_length]
        
        return result