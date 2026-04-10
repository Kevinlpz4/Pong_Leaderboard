"""
FastAPI main application for Pong Leaderboard API
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.database import engine, Base, get_db
from api.models import Score
from api.schemas import ScoreCreate, ScoreResponse
from seed_data import SEED_SCORES
from settings import get_settings

# Load settings
settings = get_settings()

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app with settings
app = FastAPI(
    title=settings.api_title,
    debug=settings.api_debug
)

# Add rate limiter to app state
app.state.limiter = limiter


# ============================================
# Exception Handlers
# ============================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global handler for unexpected errors.
    Returns a clean 500 error instead of traceback.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# ============================================
# Middleware for rate limiting
# ============================================

@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    """Add rate limit headers to response"""
    response = await call_next(request)
    
    # Add rate limit headers if available
    if hasattr(request.state, "rate_limit"):
        response.headers["X-RateLimit-Limit"] = str(request.state.rate_limit.limit)
        response.headers["X-RateLimit-Remaining"] = str(request.state.rate_limit.remaining)
    
    return response


# ============================================
# Routes
# ============================================

@app.post("/score", response_model=ScoreResponse, status_code=201)
@limiter.limit("10/minute")  # Rate limit: 10 requests per minute
async def create_score(request: Request, score_data: ScoreCreate, db: Session = Depends(get_db)):
    """
    Create a new score entry.
    
    - **player**: Name of the player (sanitized)
    - **score**: Score value (must be non-negative)
    
    Rate limited to 10 requests per minute per IP.
    """
    new_score = Score(
        player=score_data.player,
        score=score_data.score
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score


@app.post("/seed")
@app.get("/seed")
def seed_scores(db: Session = Depends(get_db)):
    """
    Seed the database with initial top 10 scores.
    Use this to populate the leaderboard with sample data.
    """
    # Verificar si ya hay datos
    existing = db.query(Score).first()
    if existing:
        return {"message": "Database already has scores, skipping seed"}
    
    # Insertar seed data
    for data in SEED_SCORES:
        score = Score(player=data["player"], score=data["score"])
        db.add(score)
    
    db.commit()
    return {"message": f"Seeded {len(SEED_SCORES)} scores"}


@app.get("/scores", response_model=list[ScoreResponse])
def get_scores(db: Session = Depends(get_db)):
    """
    Get top 10 scores ordered by score descending.
    
    Returns the best 10 scores from the leaderboard.
    """
    scores = db.query(Score).order_by(Score.score.desc()).limit(10).all()
    return scores


# ============================================
# Health check
# ============================================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


# ============================================
# How to run
# ============================================
#
# 1. Install dependencies:
#    pip install fastapi sqlalchemy uvicorn pydantic-settings slowapi
#
# 2. Run the server:
#    uvicorn api.main:app --reload
#
# 3. Test the API:
#    - POST http://localhost:8000/score
#      Body: {"player": "Kevin", "score": 10}
#    - GET http://localhost:8000/scores
#
# 4. Environment variables:
#    Create a .env file with:
#    - DATABASE_URL=sqlite:///./scores.db
#    - API_HOST=0.0.0.0
#    - API_PORT=8000
#
# ============================================
