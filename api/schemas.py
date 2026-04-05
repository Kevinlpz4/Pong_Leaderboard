"""
Pydantic schemas for request/response validation
"""
import re
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ScoreCreate(BaseModel):
    """Schema for creating a new score"""
    player: str = Field(min_length=1, max_length=50, description="Player name")
    score: int = Field(ge=0, description="Score value (must be non-negative)")

    @field_validator('player', mode='before')
    @classmethod
    def sanitize_player_name(cls, v: str) -> str:
        """
        Sanitize player name to prevent XSS and invalid characters.
        
        - Strip whitespace
        - Limit to 30 characters
        - Allow only alphanumeric, hyphen, underscore, and spaces
        - Replace invalid characters with empty string
        - Default to 'Anonymous' if empty
        """
        if not isinstance(v, str):
            return v
        
        # Strip whitespace
        v = v.strip()
        
        # Limit length to 30 characters
        v = v[:30]
        
        # Only allow alphanumeric, hyphen, underscore, and spaces
        v = re.sub(r'[^a-zA-Z0-9\-_\s]', '', v)
        
        # If empty after sanitization, use default
        if not v:
            v = "Anonymous"
        
        return v
    
    @field_validator('score', mode='before')
    @classmethod
    def validate_score(cls, v: int) -> int:
        """Ensure score is non-negative"""
        if v < 0:
            raise ValueError('Score must be non-negative')
        return v


class ScoreResponse(BaseModel):
    """Schema for score response"""
    id: int
    player: str
    score: int
    date: datetime
    
    model_config = ConfigDict(from_attributes=True)
