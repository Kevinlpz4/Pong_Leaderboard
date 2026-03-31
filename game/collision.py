from game.config import *


class CollisionManager:
    """Gestiona las colisiones entre la pelota y las paletas"""
    
    def __init__(self):
        # Mitad del alto de la paleta (aproximado)
        self.paddle_half_height = PADDLE_STRETCH * 20 / 2
        # Ancho de la paleta
        self.paddle_width = PADDLE_WIDTH * 20
        # Radio de la pelota
        self.ball_radius = 10
    
    def check_paddle_collision(self, ball, left_paddle, right_paddle):
        """
        Detecta colisión de la pelota con alguna paleta.
        
        Args:
            ball: objeto Ball
            left_paddle: paleta izquierda
            right_paddle: paleta derecha
            
        Retorna:
            "left": si colisiona con paleta izquierda
            "right": si colisiona con paleta derecha
            None: si no hay colisión
        """
        ball_x = ball.xcor()
        ball_y = ball.ycor()
        
        # Obtener posiciones reales de las paletas
        right_paddle_x = right_paddle.xcor()
        right_paddle_y = right_paddle.ycor()
        
        left_paddle_x = left_paddle.xcor()
        left_paddle_y = left_paddle.ycor()
        
        # Verificar paleta derecha
        # La pelota debe estar cerca en X (a la izquierda de la paleta)
        # Y dentro del rango Y de la paleta
        if (ball_x + self.ball_radius >= right_paddle_x - self.paddle_width / 2 and
            ball_x - self.ball_radius <= right_paddle_x + self.paddle_width / 2 and
            ball_y + self.ball_radius >= right_paddle_y - self.paddle_half_height and
            ball_y - self.ball_radius <= right_paddle_y + self.paddle_half_height):
            return "right"
        
        # Verificar paleta izquierda
        if (ball_x - self.ball_radius <= left_paddle_x + self.paddle_width / 2 and
            ball_x + self.ball_radius >= left_paddle_x - self.paddle_width / 2 and
            ball_y + self.ball_radius >= left_paddle_y - self.paddle_half_height and
            ball_y - self.ball_radius <= left_paddle_y + self.paddle_half_height):
            return "left"
        
        return None
