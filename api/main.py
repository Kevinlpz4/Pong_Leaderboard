"""
FastAPI main application for Pong Leaderboard API
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from api.database import engine, Base, get_db
from api.models import Score
from api.schemas import ScoreCreate, ScoreResponse

# Create FastAPI app
app = FastAPI(title="Pong Leaderboard API")

# Create tables on startup
Base.metadata.create_all(bind=engine)


@app.post("/score", response_model=ScoreResponse)
def create_score(score_data: ScoreCreate, db: Session = Depends(get_db)):
    """
    Create a new score entry.
    
    - **player**: Name of the player
    - **score**: Score value
    """
    new_score = Score(
        player=score_data.player,
        score=score_data.score
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score


@app.get("/scores", response_model=list[ScoreResponse])
def get_scores(db: Session = Depends(get_db)):
    """
    Get top 10 scores ordered by score descending.
    
    Returns the best 10 scores from the leaderboard.
    """
    scores = db.query(Score).order_by(Score.score.desc()).limit(10).all()
    return scores


# ============================================
# How to run
# ============================================
#
# 1. Install dependencies:
#    pip install fastapi sqlalchemy uvicorn
#
# 2. Run the server:
#    uvicorn api.main:app --reload
#
# 3. Test the API:
#    - POST http://localhost:8000/score
#      Body: {"player": "Kevin", "score": 10}
#    - GET http://localhost:8000/scores
#
# ============================================