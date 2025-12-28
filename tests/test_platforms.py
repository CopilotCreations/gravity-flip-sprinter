"""
Tests for the platforms module.
"""

import pytest
from src.platforms import Platform, MovingPlatform, GravityPlatform
from src.config import GameConfig


class TestPlatform:
    """Tests for Platform class."""
    
    def test_initialization(self, config):
        """Test platform initialization."""
        platform = Platform(100, 200, 150, 50, config=config)
        
        assert platform.x == 100
        assert platform.y == 200
        assert platform.width == 150
        assert platform.height == 50
    
    def test_default_color(self, config):
        """Test platform uses default color from config."""
        platform = Platform(0, 0, 100, 50, config=config)
        
        assert platform.color == config.platform_color
    
    def test_custom_color(self, config):
        """Test platform with custom color."""
        custom_color = (255, 0, 0)
        platform = Platform(0, 0, 100, 50, color=custom_color, config=config)
        
        assert platform.color == custom_color
    
    def test_rect_property(self, platform):
        """Test rect property returns correct pygame.Rect."""
        rect = platform.rect
        
        assert rect.x == 0
        assert rect.y == 500
        assert rect.width == 200
        assert rect.height == 50
    
    def test_update_does_nothing(self, platform):
        """Test update on static platform does nothing."""
        original_x = platform.x
        original_y = platform.y
        
        platform.update()
        
        assert platform.x == original_x
        assert platform.y == original_y
    
    def test_get_render_rect_no_camera(self, platform):
        """Test render rect without camera offset."""
        render_rect = platform.get_render_rect(0)
        
        assert render_rect.x == platform.x
        assert render_rect.y == platform.y
    
    def test_get_render_rect_with_camera(self, platform):
        """Test render rect with camera offset."""
        camera_x = 50
        render_rect = platform.get_render_rect(camera_x)
        
        assert render_rect.x == platform.x - camera_x
        assert render_rect.y == platform.y


class TestMovingPlatform:
    """Tests for MovingPlatform class."""
    
    def test_initialization(self, config):
        """Test moving platform initialization."""
        platform = MovingPlatform(0, 300, 100, 25, end_x=200, end_y=300, speed=2.0, config=config)
        
        assert platform.x == 0
        assert platform.y == 300
        assert platform.start_x == 0
        assert platform.start_y == 300
        assert platform.end_x == 200
        assert platform.end_y == 300
        assert platform.speed == 2.0
        assert platform.progress == 0.0
        assert platform.direction == 1
    
    def test_update_moves_platform(self, moving_platform):
        """Test update moves platform toward end point."""
        initial_x = moving_platform.x
        
        moving_platform.update()
        
        assert moving_platform.x > initial_x
    
    def test_update_reverses_at_end(self, moving_platform):
        """Test platform reverses direction at end point."""
        # Move to end
        moving_platform.progress = 1.0
        moving_platform.update()
        
        assert moving_platform.direction == -1
    
    def test_update_reverses_at_start(self, moving_platform):
        """Test platform reverses direction at start point."""
        moving_platform.progress = 0.01
        moving_platform.direction = -1
        
        moving_platform.update()
        
        assert moving_platform.direction == 1
    
    def test_get_velocity(self, moving_platform):
        """Test get_velocity returns correct velocity."""
        dx, dy = moving_platform.get_velocity()
        
        # Moving horizontally, so dx should be non-zero
        assert dx != 0
        assert dy == 0  # Not moving vertically in this case
    
    def test_vertical_movement(self, config):
        """Test vertically moving platform."""
        platform = MovingPlatform(100, 100, 100, 25, end_x=100, end_y=300, speed=2.0, config=config)
        
        initial_y = platform.y
        platform.update()
        
        assert platform.y > initial_y
        assert platform.x == 100


class TestGravityPlatform:
    """Tests for GravityPlatform class."""
    
    def test_initialization(self, config):
        """Test gravity platform initialization."""
        platform = GravityPlatform(100, 200, 100, 25, config=config)
        
        assert platform.x == 100
        assert platform.y == 200
        assert platform.original_y == 200
        assert platform.dy == 0
        assert platform.gravity_direction == 1
        assert platform.is_falling is False
    
    def test_set_gravity_triggers_fall(self, gravity_platform):
        """Test setting gravity triggers falling."""
        gravity_platform.set_gravity(-1)
        
        assert gravity_platform.gravity_direction == -1
        assert gravity_platform.is_falling is True
    
    def test_set_gravity_same_direction(self, gravity_platform):
        """Test setting same gravity direction doesn't trigger fall."""
        gravity_platform.set_gravity(1)
        
        assert gravity_platform.is_falling is False
    
    def test_update_when_falling(self, gravity_platform):
        """Test update applies gravity when falling."""
        gravity_platform.is_falling = True
        initial_y = gravity_platform.y
        
        gravity_platform.update()
        
        assert gravity_platform.y != initial_y
        assert gravity_platform.dy != 0
    
    def test_update_when_not_falling(self, gravity_platform):
        """Test update does nothing when not falling."""
        initial_y = gravity_platform.y
        
        gravity_platform.update()
        
        assert gravity_platform.y == initial_y
    
    def test_reset(self, gravity_platform):
        """Test reset returns platform to original state."""
        gravity_platform.y = 500
        gravity_platform.dy = 10
        gravity_platform.is_falling = True
        gravity_platform.gravity_direction = -1
        
        gravity_platform.reset()
        
        assert gravity_platform.y == gravity_platform.original_y
        assert gravity_platform.dy == 0
        assert gravity_platform.is_falling is False
        assert gravity_platform.gravity_direction == 1
