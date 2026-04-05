"""
Database configuration for SQLite
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import get_settings

# Get settings
settings = get_settings()

# Create engine using config from settings
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

# Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()


def get_db():
    """
    Dependency for FastAPI to get database session.
    Yields session and closes it after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
