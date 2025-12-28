"""
Tests for the enemies module.
"""

import pytest
from src.enemies import Enemy, Hazard
from src.platforms import Platform
from src.config import GameConfig


class TestEnemy:
    """Tests for Enemy class."""
    
    def test_initialization(self, config):
        """Test enemy initialization."""
        enemy = Enemy(100, 200, patrol_distance=80, speed=3.0, config=config)
        
        assert enemy.x == 100
        assert enemy.y == 200
        assert enemy.start_x == 100
        assert enemy.patrol_distance == 80
        assert enemy.speed == 3.0
        assert enemy.direction == 1
        assert enemy.gravity_direction == 1
    
    def test_default_dimensions(self, enemy):
        """Test enemy has default dimensions."""
        assert enemy.width == 32
        assert enemy.height == 32
    
    def test_custom_dimensions(self, config):
        """Test enemy with custom dimensions."""
        enemy = Enemy(0, 0, width=64, height=48, config=config)
        
        assert enemy.width == 64
        assert enemy.height == 48
    
    def test_default_color(self, enemy):
        """Test enemy uses default color from config."""
        assert enemy.color == enemy.config.enemy_color
    
    def test_custom_color(self, config):
        """Test enemy with custom color."""
        custom_color = (0, 255, 0)
        enemy = Enemy(0, 0, color=custom_color, config=config)
        
        assert enemy.color == custom_color
    
    def test_rect_property(self, enemy):
        """Test rect property returns correct pygame.Rect."""
        rect = enemy.rect
        
        assert rect.x == 200
        assert rect.y == 450
        assert rect.width == 32
        assert rect.height == 32
    
    def test_set_gravity(self, enemy):
        """Test setting gravity direction."""
        enemy.set_gravity(-1)
        
        assert enemy.gravity_direction == -1
        assert enemy.on_ground is False
    
    def test_apply_gravity(self, enemy):
        """Test gravity application."""
        enemy.dy = 0
        enemy.apply_gravity()
        
        assert enemy.dy > 0
    
    def test_apply_gravity_inverted(self, enemy):
        """Test inverted gravity application."""
        enemy.gravity_direction = -1
        enemy.dy = 0
        enemy.apply_gravity()
        
        assert enemy.dy < 0
    
    def test_apply_gravity_clamped(self, enemy):
        """Test gravity clamps at max fall speed."""
        enemy.dy = enemy.config.max_fall_speed
        enemy.apply_gravity()
        
        assert enemy.dy == enemy.config.max_fall_speed
    
    def test_patrol_right(self, enemy):
        """Test patrol movement to the right."""
        initial_x = enemy.x
        enemy.update([])
        
        assert enemy.x > initial_x
    
    def test_patrol_reverses_at_end(self, enemy):
        """Test patrol reverses at patrol distance."""
        enemy.x = enemy.start_x + enemy.patrol_distance + 1
        enemy._patrol()
        
        assert enemy.direction == -1
    
    def test_patrol_reverses_at_start(self, enemy):
        """Test patrol reverses at negative patrol distance."""
        enemy.x = enemy.start_x - enemy.patrol_distance - 1
        enemy._patrol()
        
        assert enemy.direction == 1
    
    def test_collision_with_platform(self, enemy, config):
        """Test enemy lands on platform."""
        platform = Platform(150, 500, 200, 50, config=config)
        enemy.y = 460
        enemy.dy = 10
        
        enemy.update([platform])
        
        assert enemy.y == platform.rect.top - enemy.height
        assert enemy.dy == 0
        assert enemy.on_ground is True
    
    def test_get_render_rect_no_camera(self, enemy):
        """Test render rect without camera offset."""
        render_rect = enemy.get_render_rect(0)
        
        assert render_rect.x == enemy.x
        assert render_rect.y == enemy.y
    
    def test_get_render_rect_with_camera(self, enemy):
        """Test render rect with camera offset."""
        camera_x = 100
        render_rect = enemy.get_render_rect(camera_x)
        
        assert render_rect.x == enemy.x - camera_x
        assert render_rect.y == enemy.y


class TestHazard:
    """Tests for Hazard class."""
    
    def test_initialization(self, config):
        """Test hazard initialization."""
        hazard = Hazard(100, 200, 50, 30, config=config)
        
        assert hazard.x == 100
        assert hazard.y == 200
        assert hazard.width == 50
        assert hazard.height == 30
    
    def test_default_color(self, hazard):
        """Test hazard uses default color from config."""
        assert hazard.color == hazard.config.hazard_color
    
    def test_custom_color(self, config):
        """Test hazard with custom color."""
        custom_color = (128, 0, 128)
        hazard = Hazard(0, 0, 50, 30, color=custom_color, config=config)
        
        assert hazard.color == custom_color
    
    def test_rect_property(self, hazard):
        """Test rect property returns correct pygame.Rect."""
        rect = hazard.rect
        
        assert rect.x == 300
        assert rect.y == 550
        assert rect.width == 50
        assert rect.height == 20
    
    def test_get_render_rect_no_camera(self, hazard):
        """Test render rect without camera offset."""
        render_rect = hazard.get_render_rect(0)
        
        assert render_rect.x == hazard.x
        assert render_rect.y == hazard.y
    
    def test_get_render_rect_with_camera(self, hazard):
        """Test render rect with camera offset."""
        camera_x = 150
        render_rect = hazard.get_render_rect(camera_x)
        
        assert render_rect.x == hazard.x - camera_x
        assert render_rect.y == hazard.y
