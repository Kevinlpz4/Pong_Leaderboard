"""
Test configuration for pytest
"""
import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def clean_db():
    """Fixture to clean database before each test"""
    from api.database import SessionLocal
    from api.models import Score
    
    db = SessionLocal()
    try:
        db.query(Score).delete()
        db.commit()
    finally:
        db.close()
    
    yield
    
    # Cleanup after test
    db = SessionLocal()
    try:
        db.query(Score).delete()
        db.commit()
    finally:
        db.close()
