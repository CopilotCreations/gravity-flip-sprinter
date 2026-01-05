"""
Tests for the config module.
"""

import pytest
import os
from src.config import GameConfig, default_config


class TestGameConfig:
    """Tests for GameConfig class."""
    
    def test_default_values(self):
        """Test that default configuration has expected values.

        Creates a default GameConfig instance and verifies all default
        values are set correctly for window dimensions, FPS, player
        physics, and debug settings.
        """
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
        """Test configuration with custom values.

        Verifies that GameConfig accepts and stores custom values
        for window dimensions, FPS, player speed, and debug mode.
        """
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
        """Test configuration from environment with default values.

        Clears all configuration-related environment variables and
        verifies that from_env() returns default values when no
        environment variables are set.

        Args:
            monkeypatch: Pytest fixture for modifying environment variables.
        """
        # Clear relevant env vars
        for var in ['WINDOW_WIDTH', 'WINDOW_HEIGHT', 'FPS', 'PLAYER_SPEED', 
                    'PLAYER_JUMP_FORCE', 'GRAVITY_STRENGTH', 'DEBUG_MODE', 'SHOW_HITBOXES']:
            monkeypatch.delenv(var, raising=False)
        
        config = GameConfig.from_env()
        
        assert config.window_width == 800
        assert config.window_height == 600
        assert config.fps == 60
    
    def test_from_env_custom(self, monkeypatch):
        """Test configuration from environment with custom values.

        Sets custom environment variables and verifies that from_env()
        correctly parses and applies them to the configuration, including
        boolean values with different case formats.

        Args:
            monkeypatch: Pytest fixture for modifying environment variables.
        """
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
        """Test the default_config singleton.

        Verifies that the default_config module-level instance exists,
        is of the correct type, and has the expected default values.
        """
        assert default_config is not None
        assert isinstance(default_config, GameConfig)
        assert default_config.window_width == 800
    
    def test_colors_are_tuples(self):
        """Test that color values are proper RGB tuples.

        Verifies that all color configuration values are tuples with
        exactly 3 elements, and that background_color values are valid
        RGB values (0-255 range).
        """
        config = GameConfig()
        
        assert isinstance(config.background_color, tuple)
        assert len(config.background_color) == 3
        assert all(0 <= c <= 255 for c in config.background_color)
        
        assert isinstance(config.player_color, tuple)
        assert isinstance(config.platform_color, tuple)
        assert isinstance(config.enemy_color, tuple)
        assert isinstance(config.hazard_color, tuple)
    
    def test_player_dimensions(self):
        """Test player dimension defaults.

        Verifies that player width and height have the expected default
        values and are positive integers.
        """
        config = GameConfig()
        
        assert config.player_width == 32
        assert config.player_height == 48
        assert config.player_width > 0
        assert config.player_height > 0
    
    def test_physics_values(self):
        """Test physics configuration values.

        Verifies that physics-related configuration values (gravity,
        max fall speed, jump force) are all positive numbers.
        """
        config = GameConfig()
        
        assert config.gravity_strength > 0
        assert config.max_fall_speed > 0
        assert config.player_jump_force > 0
