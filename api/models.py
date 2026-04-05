"""
Database models using SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from api.database import Base


class Score(Base):
    """Score model for leaderboard"""
    
    __tablename__ = "scores"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Player name
    player = Column(String, index=True, nullable=False)
    
    # Score value
    score = Column(Integer, nullable=False)
    
    # Date when score was recorded
    date = Column(DateTime, default=datetime.utcnow)