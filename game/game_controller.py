"""
GameController - Controla la lógica principal del juego

Este archivo contiene toda la lógica del juego, separando la presentación
de la lógica de negocio (SINGLE RESPONSIBILITY PRINCIPLE).
"""
import turtle
import requests
from game.paddle import Paddle
from game.ball import Ball
from game.borders import BorderManager
from game.collision import CollisionManager
from game.scoreboard import Scoreboard
from game.player import Player
from game.config import *

# URL de la API
API_BASE_URL = "http://localhost:8000"


class GameState:
    """Enumeración de estados del juego"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class GameController:
    """
    Controlador principal del juego.
    Maneja toda la lógica: movimiento, colisiones, puntuación, estado.
    """
    
    def __init__(self, screen, left_player: Player, right_player: Player, max_goals: int = 5):
        self.screen = screen
        self.left_player = left_player
        self.right_player = right_player
        self.max_goals = max_goals
        
        # Estado del juego
        self.state = GameState.PLAYING
        self.game_over = False
        self.winner = None
        self.loser = None
        
        # Keys activas para movimiento fluido
        self.keys = {
            "Up": False,
            "Down": False,
            "w": False,
            "s": False,
        }
        
        # Inicializar componentes del juego
        self._init_components()
        
        # Configurar controles
        self._setup_controls()
    
    def _init_components(self):
        """Inicializa todos los componentes del juego"""
        # Bordes del campo
        self.border_manager = BorderManager()
        
        # Paletas con colores de los jugadores
        self.left_paddle = Paddle(LEFT_PADDLE_POSITION, self.left_player.color, is_left=True)
        self.right_paddle = Paddle(RIGHT_PADDLE_POSITION, self.right_player.color, is_left=False)
        
        # Pelota
        self.ball = Ball(BALL_COLOR, BALL_START_POSITION)
        
        # Gestor de colisiones
        self.collision_manager = CollisionManager()
        
        # Marcador con letras de los jugadores
        self.scoreboard = Scoreboard(self.left_player.letter, self.right_player.letter)
        
        # Adaptar al tamaño inicial de pantalla
        width = self.screen.window_width()
        height = self.screen.window_height()
        self._adapt_to_window(width, height)
    
    def _setup_controls(self):
        """Configura los controles del teclado"""
        self.screen.listen()
        
        # Press
        self.screen.onkeypress(lambda: self._on_key_press("Up"), "Up")
        self.screen.onkeypress(lambda: self._on_key_press("Down"), "Down")
        self.screen.onkeypress(lambda: self._on_key_press("w"), "w")
        self.screen.onkeypress(lambda: self._on_key_press("s"), "s")
        
        # Release
        self.screen.onkeyrelease(lambda: self._on_key_release("Up"), "Up")
        self.screen.onkeyrelease(lambda: self._on_key_release("Down"), "Down")
        self.screen.onkeyrelease(lambda: self._on_key_release("w"), "w")
        self.screen.onkeyrelease(lambda: self._on_key_release("s"), "s")
    
    def _on_key_press(self, key):
        """Maneja presión de tecla"""
        if key in self.keys:
            self.keys[key] = True
    
    def _on_key_release(self, key):
        """Maneja liberación de tecla"""
        if key in self.keys:
            self.keys[key] = False
    
    def _adapt_to_window(self, width, height):
        """Adapta todos los elementos al tamaño de ventana"""
        self.border_manager.update_size(width, height)
        self.left_paddle.update_position(width, height)
        self.right_paddle.update_position(width, height)
        self.scoreboard.update_position(width, height)
    
    def update(self):
        """
        Método principal que se llama en cada frame del juego.
        Actualiza el estado del juego.
        """
        # Obtener tamaño actual de ventana
        width = self.screen.window_width()
        height = self.screen.window_height()
        
        # Adaptar si cambió el tamaño
        self._adapt_to_window(width, height)
        
        # Mover paletas según keys activas
        self._move_paddles()
        
        # Mover pelota
        self.ball.move()
        
        # Verificar colisiones
        self._check_collisions()
    
    def _move_paddles(self):
        """Mueve las paletas según las teclas activas"""
        # Paleta derecha
        if self.keys["Up"]:
            self.right_paddle.move_up()
        if self.keys["Down"]:
            self.right_paddle.move_down()
        
        # Paleta izquierda
        if self.keys["w"]:
            self.left_paddle.move_up()
        if self.keys["s"]:
            self.left_paddle.move_down()
    
    def _check_collisions(self):
        """Verifica todas las colisiones del juego"""
        # Colisión con bordes
        collision = self.border_manager.check_collision(self.ball)
        
        if collision == "bounce":
            self.ball.bounce_y()
        
        elif collision == "score_left":
            # Punto para jugador izquierdo
            self._handle_goal("left")
        
        elif collision == "score_right":
            # Punto para jugador derecho
            self._handle_goal("right")
        
        # Colisión con paletas
        paddle_hit = self.collision_manager.check_paddle_collision(
            self.ball, self.left_paddle, self.right_paddle
        )
        
        if paddle_hit:
            self.ball.bounce_x()
    
    def _handle_goal(self, side):
        """
        Maneja cuando se marca un gol.
        - Actualiza el marcador
        - Reinicia la pelota al centro
        - Verifica si alguien ganó
        """
        if side == "left":
            self.left_player.score += 1
            self.scoreboard.increase_left()
        else:
            self.right_player.score += 1
            self.scoreboard.increase_right()
        
        # Verificar si alguien ganó
        if self.left_player.score >= self.max_goals:
            self.game_over = True
            self.winner = self.left_player
            self.loser = self.right_player
            self.state = GameState.GAME_OVER
        elif self.right_player.score >= self.max_goals:
            self.game_over = True
            self.winner = self.right_player
            self.loser = self.left_player
            self.state = GameState.GAME_OVER
        else:
            # Reiniciar pelota solo si el juego no terminó
            self.ball.reset_position()
    
    def _calculate_score(self):
        """
        Calcula el score basado en la diferencia de goles.
        Formula: Diferencia × 100
        Solo el ganador envia su score.
        """
        if not self.winner or not self.loser:
            return 0
        
        winner_score = self.winner.score
        loser_score = self.loser.score
        difference = winner_score - loser_score
        return difference * 100
    
    def _send_score_to_api(self):
        """
        Envia el score del ganador a la API.
        """
        if not self.winner:
            return False
        
        try:
            score_value = self._calculate_score()
            payload = {
                "player": self.winner.name,
                "score": score_value
            }
            response = requests.post(f"{API_BASE_URL}/score", json=payload)
            if response.status_code == 200:
                print(f"✓ Score enviado: {self.winner.name} - {score_value} puntos")
                return True
            else:
                print(f"✗ Error al enviar score: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ No se pudo conectar a la API: {e}")
            return False
    
    def show_game_over(self):
        """Muestra la pantalla de fin de juego"""
        # Limpiar el campo
        self.left_paddle.hideturtle()
        self.right_paddle.hideturtle()
        self.ball.hideturtle()
        self.border_manager.hide_all()
        self.scoreboard.hideturtle()
        
        # Verificar que hay un ganador
        if not self.winner:
            return None
        
        # Calcular y enviar score a la API
        score_value = self._calculate_score()
        self._send_score_to_api()
        
        # Mostrar resultado
        result_turtle = turtle.Turtle()
        result_turtle.penup()
        result_turtle.hideturtle()
        result_turtle.color("white")
        
        w = self.screen.window_width()
        h = self.screen.window_height()
        hh = h / 2
        
        # Ganador
        result_turtle.goto(0, hh * 0.3)
        result_turtle.write(
            f"¡{self.winner.name} ({self.winner.letter})GANÓ!",
            align="center",
            font=("Arial", 50, "bold")
        )
        
        # Score earned
        result_turtle.goto(0, hh * 0.1)
        result_turtle.color("#FFD700")
        result_turtle.write(
            f"+{score_value} PUNTOS",
            align="center",
            font=("Arial", 30, "bold")
        )
        
        # Score final
        result_turtle.goto(0, hh * -0.15)
        result_turtle.color("white")
        result_turtle.write(
            f"Resultado: {self.left_player.letter}:{self.left_player.score} - {self.right_player.score}:{self.right_player.letter}",
            align="center",
            font=("Arial", 24, "normal")
        )
        
        # Preguntar si juegan de nuevo
        result_turtle.goto(0, -hh * 0.4)
        result_turtle.color("gray")
        result_turtle.write("¿Jugar de nuevo? (S/N)", align="center", font=("Arial", 20, "normal"))
        
        return result_turtle
    
    def cleanup(self):
        """Limpia los elementos del juego"""
        self.left_paddle.hideturtle()
        self.right_paddle.hideturtle()
        self.ball.hideturtle()
        self.scoreboard.hideturtle()
        self.border_manager.hide_all()
    
    def update_screen(self):
        """Actualiza la visualización de la pantalla"""
        self.screen.update()