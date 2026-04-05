"""
Configuración centralizada de la aplicación.
Todas las variables de entorno y settings van aquí.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    Lee automáticamente desde variables de entorno o archivo .env
    """
    
    # ====================
    # API Settings
    # ====================
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    api_title: str = "Pong Leaderboard API"
    
    # ====================
    # Database Settings
    # ====================
    database_url: str = "sqlite:///./scores.db"
    
    # ====================
    # Game Settings
    # ====================
    game_title: str = "Pong"
    game_fps: int = 100
    ball_speed_increment: float = 1.05  # 5% más rápido por cada rebote
    ball_max_speed: int = 40
    points_per_goal: int = 100
    
    # ====================
    # API Client Settings
    # ====================
    api_base_url: str = "http://localhost:8000"
    api_timeout: int = 5  # segundos
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna las settings cacheadas.
    Llama una sola vez por aplicación.
    """
    return Settings()
