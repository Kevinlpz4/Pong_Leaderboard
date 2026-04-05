"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ScoreCreate(BaseModel):
    """Schema for creating a new score"""
    player: str = Field(min_length=1, max_length=50, description="Player name")
    score: int = Field(ge=0, description="Score value (must be non-negative)")


class ScoreResponse(BaseModel):
    """Schema for score response"""
    id: int
    player: str
    score: int
    date: datetime
    
    model_config = ConfigDict(from_attributes=True)