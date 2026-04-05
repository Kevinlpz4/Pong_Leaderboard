"""
Seed script - Poblador de datos iniciales para el leaderboard.

Uso:
    python scripts/seed.py

Este script se conecta a la API y poblana la base de datos 
con los scores iniciales si está vacía.
"""
import os
import sys
import requests


# Agregar el path del proyecto para poder importar
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from seed_data import SEED_SCORES


def get_api_url() -> str:
    """Obtiene la URL de la API desde variable de entorno o usa default."""
    import os
    return os.environ.get("API_BASE_URL", "http://localhost:8000")


def seed_via_api():
    """
    Intenta hacer seed через la API (recomendado).
    """
    api_url = get_api_url()
    
    try:
        print(f"🌱 Conectando a {api_url}...")
        response = requests.post(f"{api_url}/seed", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('message', 'Seed completado')}")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ No se pudo conectar a la API: {e}")
        return False


def seed_directo():
    """
    Seed directo a la base de datos (sin API).
    Útil si la API no está corriendo.
    """
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime
    
    # Obtener URL de la BD
    db_url = os.environ.get("DATABASE_URL", "sqlite:///./scores.db")
    
    print(f"🔧 Conectando a base de datos: {db_url}...")
    
    try:
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Importar modelo Score
        # Agregar el path del proyecto
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from api.models import Score
        
        # Verificar si ya hay datos
        existing = session.query(Score).first()
        if existing:
            print("⚠️ La base de datos ya tiene datos, saltando seed")
            session.close()
            return True
        
        # Insertar seed data
        for data in SEED_SCORES:
            score = Score(player=data["player"], score=data["score"])
            session.add(score)
        
        session.commit()
        print(f"✅ Seed completado: {len(SEED_SCORES)} scores insertados")
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error con la base de datos: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 50)
    print("🏆 PONG LEADERBOARD - SEED SCRIPT")
    print("=" * 50)
    
    # Primero intentar vía API
    print("\n📡 Método 1: Intentar via API...")
    if seed_via_api():
        return
    
    # Si falla, intentar seed directo
    print("\n💾 Método 2: Seed directo a base de datos...")
    if seed_directo():
        return
    
    print("\n❌ No se pudo completar el seed")
    sys.exit(1)


if __name__ == "__main__":
    main()
