"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ScoreCreate(BaseModel):
    """Schema for creating a new score"""
    player: str
    score: int


class ScoreResponse(BaseModel):
    """Schema for score response"""
    id: int
    player: str
    score: int
    date: datetime
    
    model_config = ConfigDict(from_attributes=True)