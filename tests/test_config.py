"""
Tests for the config module.
"""

import pytest
import os
from src.config import GameConfig, default_config


class TestGameConfig:
    """Tests for GameConfig class."""
    
    def test_default_values(self):
        """Test that default configuration has expected values."""
        config = GameConfig()
        
        assert config.window_width == 800
        assert config.window_height == 600
        assert config.fps == 60
        assert config.player_speed == 5.0
        assert config.player_jump_force == 15.0
        assert config.gravity_strength == 0.8
        assert config.debug_mode is False
        assert config.show_hitboxes is False
    
    def test_custom_values(self):
        """Test configuration with custom values."""
        config = GameConfig(
            window_width=1024,
            window_height=768,
            fps=30,
            player_speed=10.0,
            debug_mode=True,
        )
        
        assert config.window_width == 1024
        assert config.window_height == 768
        assert config.fps == 30
        assert config.player_speed == 10.0
        assert config.debug_mode is True
    
    def test_from_env_defaults(self, monkeypatch):
        """Test configuration from environment with default values."""
        # Clear relevant env vars
        for var in ['WINDOW_WIDTH', 'WINDOW_HEIGHT', 'FPS', 'PLAYER_SPEED', 
                    'PLAYER_JUMP_FORCE', 'GRAVITY_STRENGTH', 'DEBUG_MODE', 'SHOW_HITBOXES']:
            monkeypatch.delenv(var, raising=False)
        
        config = GameConfig.from_env()
        
        assert config.window_width == 800
        assert config.window_height == 600
        assert config.fps == 60
    
    def test_from_env_custom(self, monkeypatch):
        """Test configuration from environment with custom values."""
        monkeypatch.setenv('WINDOW_WIDTH', '1920')
        monkeypatch.setenv('WINDOW_HEIGHT', '1080')
        monkeypatch.setenv('FPS', '120')
        monkeypatch.setenv('PLAYER_SPEED', '8.0')
        monkeypatch.setenv('DEBUG_MODE', 'true')
        monkeypatch.setenv('SHOW_HITBOXES', 'TRUE')
        
        config = GameConfig.from_env()
        
        assert config.window_width == 1920
        assert config.window_height == 1080
        assert config.fps == 120
        assert config.player_speed == 8.0
        assert config.debug_mode is True
        assert config.show_hitboxes is True
    
    def test_default_config_instance(self):
        """Test the default_config singleton."""
        assert default_config is not None
        assert isinstance(default_config, GameConfig)
        assert default_config.window_width == 800
    
    def test_colors_are_tuples(self):
        """Test that color values are proper RGB tuples."""
        config = GameConfig()
        
        assert isinstance(config.background_color, tuple)
        assert len(config.background_color) == 3
        assert all(0 <= c <= 255 for c in config.background_color)
        
        assert isinstance(config.player_color, tuple)
        assert isinstance(config.platform_color, tuple)
        assert isinstance(config.enemy_color, tuple)
        assert isinstance(config.hazard_color, tuple)
    
    def test_player_dimensions(self):
        """Test player dimension defaults."""
        config = GameConfig()
        
        assert config.player_width == 32
        assert config.player_height == 48
        assert config.player_width > 0
        assert config.player_height > 0
    
    def test_physics_values(self):
        """Test physics configuration values."""
        config = GameConfig()
        
        assert config.gravity_strength > 0
        assert config.max_fall_speed > 0
        assert config.player_jump_force > 0
