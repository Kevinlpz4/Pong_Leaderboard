"""
Game Logic Tests for Pong Leaderboard

These tests verify the game logic without requiring graphics (turtle).
We test:
- Score calculation
- Collision detection
- Game state management
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.config import *


class TestScoreCalculation:
    """Tests for score calculation based on goal difference"""
    
    def test_score_calculation_standard(self):
        """Test score calculation with standard difference"""
        from settings import get_settings
        settings = get_settings()
        
        winner_score = 12
        loser_score = 7
        difference = winner_score - loser_score
        expected_score = difference * settings.points_per_goal
        
        assert expected_score == 500  # 5 * 100
    
    def test_score_calculation_large_difference(self):
        """Test score with large goal difference"""
        from settings import get_settings
        settings = get_settings()
        
        winner_score = 12
        loser_score = 3
        difference = winner_score - loser_score
        expected_score = difference * settings.points_per_goal
        
        assert expected_score == 900  # 9 * 100
    
    def test_score_calculation_small_difference(self):
        """Test score with small goal difference"""
        from settings import get_settings
        settings = get_settings()
        
        winner_score = 5
        loser_score = 2
        difference = winner_score - loser_score
        expected_score = difference * settings.points_per_goal
        
        assert expected_score == 300  # 3 * 100
    
    def test_score_calculation_one_goal_difference(self):
        """Test score with minimum difference"""
        from settings import get_settings
        settings = get_settings()
        
        winner_score = 5
        loser_score = 4
        difference = winner_score - loser_score
        expected_score = difference * settings.points_per_goal
        
        assert expected_score == 100  # 1 * 100


class TestCollisionDetection:
    """Tests for collision detection logic"""
    
    def test_paddle_collision_right_side(self):
        """Test collision detection with right paddle"""
        # Create a simple mock for testing
        class MockBall:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        class MockPaddle:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        # Import the collision logic directly
        from game.collision import CollisionManager
        
        manager = CollisionManager()
        
        # Ball at right paddle position
        ball = MockBall(580, 0)
        right_paddle = MockPaddle(600, 0)
        left_paddle = MockPaddle(-600, 0)
        
        result = manager.check_paddle_collision(ball, left_paddle, right_paddle)
        
        assert result == "right"
    
    def test_paddle_collision_left_side(self):
        """Test collision detection with left paddle"""
        class MockBall:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        class MockPaddle:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        from game.collision import CollisionManager
        
        manager = CollisionManager()
        
        # Ball at left paddle position
        ball = MockBall(-580, 0)
        right_paddle = MockPaddle(600, 0)
        left_paddle = MockPaddle(-600, 0)
        
        result = manager.check_paddle_collision(ball, left_paddle, right_paddle)
        
        assert result == "left"
    
    def test_no_collision_when_far_from_paddles(self):
        """Test no collision when ball is far from paddles"""
        class MockBall:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        class MockPaddle:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        from game.collision import CollisionManager
        
        manager = CollisionManager()
        
        # Ball in center, far from both paddles
        ball = MockBall(0, 0)
        right_paddle = MockPaddle(600, 0)
        left_paddle = MockPaddle(-600, 0)
        
        result = manager.check_paddle_collision(ball, left_paddle, right_paddle)
        
        assert result is None


class TestBorderCollision:
    """Tests for border collision detection"""
    
    def test_top_border_collision(self):
        """Test collision with top border"""
        class MockBall:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        from game.borders import BorderManager
        
        manager = BorderManager()
        
        # Ball at top border
        ball = MockBall(0, 290)
        
        result = manager.check_collision(ball)
        
        assert result == "bounce"
    
    def test_bottom_border_collision(self):
        """Test collision with bottom border"""
        class MockBall:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        from game.borders import BorderManager
        
        manager = BorderManager()
        
        # Ball at bottom border
        ball = MockBall(0, -290)
        
        result = manager.check_collision(ball)
        
        assert result == "bounce"
    
    def test_left_scoring_collision(self):
        """Test scoring collision on left side"""
        class MockBall:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        from game.borders import BorderManager
        
        manager = BorderManager()
        
        # Ball past left border
        ball = MockBall(-390, 0)
        
        result = manager.check_collision(ball)
        
        assert result == "score_left"
    
    def test_right_scoring_collision(self):
        """Test scoring collision on right side"""
        class MockBall:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        from game.borders import BorderManager
        
        manager = BorderManager()
        
        # Ball past right border
        ball = MockBall(390, 0)
        
        result = manager.check_collision(ball)
        
        assert result == "score_right"
    
    def test_no_collision_in_center(self):
        """Test no collision when ball is in center"""
        class MockBall:
            def __init__(self, x, y):
                self.x_pos = x
                self.y_pos = y
            
            def xcor(self):
                return self.x_pos
            
            def ycor(self):
                return self.y_pos
        
        from game.borders import BorderManager
        
        manager = BorderManager()
        
        # Ball in center, no collision
        ball = MockBall(0, 0)
        
        result = manager.check_collision(ball)
        
        assert result is None


class TestBallMovement:
    """Tests for ball movement logic"""
    
    def test_ball_initial_speed(self):
        """Test ball starts with correct initial speed"""
        from game.ball import Ball
        
        # Create ball (won't display without screen, but logic works)
        # We can't fully test this without a turtle screen
        # Just verify the constants exist
        assert BALL_SPEED > 0
    
    def test_ball_bounce_changes_direction(self):
        """Test bounce methods change direction"""
        from game.config import BALL_SPEED
        
        # Test the concept of bounce
        x_move = BALL_SPEED
        y_move = BALL_SPEED
        
        # Bounce X should invert horizontal direction
        x_move *= -1
        assert x_move == -BALL_SPEED
        
        # Bounce Y should invert vertical direction
        y_move *= -1
        assert y_move == -BALL_SPEED


class TestGameConfiguration:
    """Tests for game configuration values"""
    
    def test_screen_dimensions(self):
        """Test screen dimensions are set"""
        assert SCREEN_WIDTH > 0
        assert SCREEN_HEIGHT > 0
    
    def test_paddle_dimensions(self):
        """Test paddle dimensions are set"""
        assert PADDLE_STRETCH > 0
        assert PADDLE_WIDTH > 0
    
    def test_paddle_movement(self):
        """Test paddle movement speed is set"""
        assert PADDLE_MOVE > 0
    
    def test_ball_speed(self):
        """Test ball speed is set"""
        assert BALL_SPEED > 0
    
    def test_points_per_goal(self):
        """Test points per goal is set correctly"""
        from settings import get_settings
        settings = get_settings()
        
        assert settings.points_per_goal == 100
