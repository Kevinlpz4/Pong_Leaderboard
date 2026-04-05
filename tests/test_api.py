"""
API Tests for Pong Leaderboard

These tests verify the API endpoints work correctly:
- POST /score - Create a new score
- GET /scores - Get top 10 scores
- POST /seed - Seed database
- GET /health - Health check
"""
import pytest
from api.models import Score
from api.database import SessionLocal


class TestScoreEndpoint:
    """Tests for POST /score endpoint"""
    
    def test_create_score_success(self, client, clean_db):
        """Test creating a valid score returns 201"""
        response = client.post("/score", json={
            "player": "Kevin",
            "score": 500
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["player"] == "Kevin"
        assert data["score"] == 500
        assert "id" in data
        assert "date" in data
    
    def test_create_score_sanitizes_player_name(self, client, clean_db):
        """Test that player name is sanitized (no XSS)"""
        response = client.post("/score", json={
            "player": "<script>alert('hack')</script>Kevin",
            "score": 100
        })
        
        assert response.status_code == 201
        data = response.json()
        # Script tags should be removed (all special chars removed)
        assert "<script>" not in data["player"]
        # The name should have been sanitized - original text would have been stripped
        # After removing < > / etc, we get "scriptalerthackscriptKevin"
        # After 30 char limit: "scriptalerthackscriptKevin" -> 28 chars
        assert "script" in data["player"].lower()
    
    def test_create_score_strips_whitespace(self, client, clean_db):
        """Test that whitespace is stripped from player name"""
        response = client.post("/score", json={
            "player": "   Kevin   ",
            "score": 100
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["player"] == "Kevin"
    
    def test_create_score_empty_name_defaults_to_anonymous(self, client, clean_db):
        """Test that empty player name becomes 'Anonymous'"""
        response = client.post("/score", json={
            "player": "",
            "score": 100
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["player"] == "Anonymous"
    
    def test_create_score_max_length_30(self, client, clean_db):
        """Test that player name is limited to 30 characters"""
        response = client.post("/score", json={
            "player": "a" * 50,  # 50 characters
            "score": 100
        })
        
        assert response.status_code == 201
        data = response.json()
        assert len(data["player"]) <= 30
    
    def test_create_score_special_characters_removed(self, client, clean_db):
        """Test that special characters are removed"""
        response = client.post("/score", json={
            "player": "Kevin@#$%^&*()",
            "score": 100
        })
        
        assert response.status_code == 201
        data = response.json()
        # Only alphanumeric, hyphen, underscore, spaces allowed
        assert "@" not in data["player"]
        assert "#" not in data["player"]
    
    def test_create_score_negative_score_fails(self, client, clean_db):
        """Test that negative score returns validation error"""
        response = client.post("/score", json={
            "player": "Kevin",
            "score": -10
        })
        
        assert response.status_code == 422
    
    def test_create_score_missing_player_fails(self, client, clean_db):
        """Test that missing player returns validation error"""
        response = client.post("/score", json={
            "score": 100
        })
        
        assert response.status_code == 422
    
    def test_create_score_missing_score_fails(self, client, clean_db):
        """Test that missing score returns validation error"""
        response = client.post("/score", json={
            "player": "Kevin"
        })
        
        assert response.status_code == 422


class TestScoresEndpoint:
    """Tests for GET /scores endpoint"""
    
    def test_get_scores_empty(self, client, clean_db):
        """Test getting scores when database is empty"""
        response = client.get("/scores")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_scores_returns_top_10(self, client, clean_db):
        """Test that only top 10 scores are returned"""
        db = SessionLocal()
        
        # Create 15 scores
        for i in range(15):
            score = Score(player=f"Player{i}", score=i * 100)
            db.add(score)
        db.commit()
        db.close()
        
        response = client.get("/scores")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10
        # Verify they're ordered by score descending
        scores = [s["score"] for s in data]
        assert scores == sorted(scores, reverse=True)
    
    def test_get_scores_ordered_by_score_descending(self, client, clean_db):
        """Test scores are ordered by score descending"""
        db = SessionLocal()
        
        # Create scores in random order
        scores_data = [
            {"player": "Alice", "score": 300},
            {"player": "Bob", "score": 500},
            {"player": "Charlie", "score": 100},
        ]
        for s in scores_data:
            score = Score(player=s["player"], score=s["score"])
            db.add(score)
        db.commit()
        db.close()
        
        response = client.get("/scores")
        
        assert response.status_code == 200
        data = response.json()
        assert data[0]["player"] == "Bob"  # Highest score first
        assert data[1]["player"] == "Alice"
        assert data[2]["player"] == "Charlie"


class TestSeedEndpoint:
    """Tests for POST /seed endpoint"""
    
    def test_seed_creates_scores(self, client, clean_db):
        """Test seed endpoint creates initial scores"""
        response = client.post("/seed")
        
        assert response.status_code == 200
        assert "Seeded" in response.json()["message"]
        
        # Verify scores were created
        response = client.get("/scores")
        assert len(response.json()) > 0
    
    def test_seed_skips_existing(self, client, clean_db):
        """Test seed doesn't duplicate if scores exist"""
        # First seed
        response1 = client.post("/seed")
        
        # Second seed
        response2 = client.post("/seed")
        
        assert response2.status_code == 200
        assert "already has scores" in response2.json()["message"]


class TestHealthEndpoint:
    """Tests for GET /health endpoint"""
    
    def test_health_returns_ok(self, client):
        """Test health check returns ok status"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestRateLimiting:
    """Tests for rate limiting"""
    
    def test_rate_limit_allows_requests(self, client, clean_db):
        """Test that rate limiting allows requests under the limit"""
        response = client.post("/score", json={
            "player": "TestPlayer",
            "score": 100
        })
        
        # Should succeed (not rate limited)
        assert response.status_code == 201
    
    def test_empty_player_name_sanitized_to_anonymous(self, client, clean_db):
        """Test that empty player name becomes 'Anonymous' (not rejected)"""
        response = client.post("/score", json={
            "player": "",  # Empty name is sanitized to "Anonymous"
            "score": 100
        })
        
        assert response.status_code == 201
        assert response.json()["player"] == "Anonymous"
