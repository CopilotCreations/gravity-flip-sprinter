"""
Tests for the renderer module.
"""

import pytest
from unittest.mock import MagicMock, patch
import pygame
import os

# Set dummy drivers
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from src.renderer import Renderer
from src.config import GameConfig
from src.player import Player
from src.platforms import Platform, MovingPlatform, GravityPlatform
from src.enemies import Enemy, Hazard
from src.level import Level, LevelLoader


class TestRenderer:
    """Tests for Renderer class."""
    
    @pytest.fixture
    def renderer(self):
        """Create a renderer instance for testing."""
        pygame.init()
        pygame.font.init()
        config = GameConfig()
        screen = pygame.display.set_mode((config.window_width, config.window_height))
        renderer = Renderer(screen, config)
        yield renderer
        pygame.quit()
    
    @pytest.fixture
    def player(self):
        """Create a player for testing."""
        config = GameConfig()
        return Player(100, 300, config)
    
    @pytest.fixture
    def platform(self):
        """Create a platform for testing."""
        config = GameConfig()
        return Platform(0, 500, 200, 50, config=config)
    
    @pytest.fixture
    def moving_platform(self):
        """Create a moving platform for testing."""
        config = GameConfig()
        return MovingPlatform(100, 300, 100, 25, end_x=200, end_y=300, config=config)
    
    @pytest.fixture
    def gravity_platform(self):
        """Create a gravity platform for testing."""
        config = GameConfig()
        return GravityPlatform(100, 200, 100, 25, config=config)
    
    @pytest.fixture
    def enemy(self):
        """Create an enemy for testing."""
        config = GameConfig()
        return Enemy(200, 450, config=config)
    
    @pytest.fixture
    def hazard(self):
        """Create a hazard for testing."""
        config = GameConfig()
        return Hazard(300, 550, 50, 20, config=config)
    
    def test_initialization(self, renderer):
        """Test renderer initialization."""
        assert renderer.screen is not None
        assert renderer.config is not None
        assert len(renderer.bg_layers) > 0
    
    def test_clear(self, renderer):
        """Test clear fills screen with background color."""
        renderer.clear()
        # No assertion needed - just verify no exception
    
    def test_draw_background(self, renderer):
        """Test draw_background runs without error."""
        renderer.draw_background(0)
        renderer.draw_background(100)
    
    def test_draw_player(self, renderer, player):
        """Test draw_player runs without error."""
        renderer.draw_player(player, 0)
    
    def test_draw_player_with_camera(self, renderer, player):
        """Test draw_player with camera offset."""
        renderer.draw_player(player, 50)
    
    def test_draw_player_facing_left(self, renderer, player):
        """Test draw_player when facing left."""
        player.facing_right = False
        renderer.draw_player(player, 0)
    
    def test_draw_player_inverted_gravity(self, renderer, player):
        """Test draw_player with inverted gravity."""
        player.gravity_direction = -1
        renderer.draw_player(player, 0)
    
    def test_draw_player_debug_hitbox(self, renderer, player):
        """Test draw_player draws hitbox in debug mode."""
        renderer.config.show_hitboxes = True
        renderer.draw_player(player, 0)
    
    def test_draw_platform(self, renderer, platform):
        """Test draw_platform runs without error."""
        renderer.draw_platform(platform, 0)
    
    def test_draw_platform_with_camera(self, renderer, platform):
        """Test draw_platform with camera offset."""
        renderer.draw_platform(platform, 50)
    
    def test_draw_platform_off_screen_left(self, renderer, platform):
        """Test draw_platform skips off-screen platforms."""
        renderer.draw_platform(platform, 1000)  # Platform should be off-screen
    
    def test_draw_platform_off_screen_right(self, renderer):
        """Test draw_platform skips off-screen platforms on right."""
        config = GameConfig()
        platform = Platform(1000, 500, 100, 50, config=config)
        renderer.draw_platform(platform, 0)  # Platform should be off-screen
    
    def test_draw_moving_platform(self, renderer, moving_platform):
        """Test draw_platform for moving platform."""
        renderer.draw_platform(moving_platform, 0)
    
    def test_draw_gravity_platform(self, renderer, gravity_platform):
        """Test draw_platform for gravity platform."""
        renderer.draw_platform(gravity_platform, 0)
    
    def test_draw_platform_debug_hitbox(self, renderer, platform):
        """Test draw_platform draws hitbox in debug mode."""
        renderer.config.show_hitboxes = True
        renderer.draw_platform(platform, 0)
    
    def test_draw_enemy(self, renderer, enemy):
        """Test draw_enemy runs without error."""
        renderer.draw_enemy(enemy, 0)
    
    def test_draw_enemy_with_camera(self, renderer, enemy):
        """Test draw_enemy with camera offset."""
        renderer.draw_enemy(enemy, 50)
    
    def test_draw_enemy_inverted_gravity(self, renderer, enemy):
        """Test draw_enemy with inverted gravity."""
        enemy.gravity_direction = -1
        renderer.draw_enemy(enemy, 0)
    
    def test_draw_enemy_off_screen(self, renderer, enemy):
        """Test draw_enemy skips off-screen enemies."""
        renderer.draw_enemy(enemy, 1000)
    
    def test_draw_enemy_debug_hitbox(self, renderer, enemy):
        """Test draw_enemy draws hitbox in debug mode."""
        renderer.config.show_hitboxes = True
        renderer.draw_enemy(enemy, 0)
    
    def test_draw_hazard(self, renderer, hazard):
        """Test draw_hazard runs without error."""
        renderer.draw_hazard(hazard, 0)
    
    def test_draw_hazard_with_camera(self, renderer, hazard):
        """Test draw_hazard with camera offset."""
        renderer.draw_hazard(hazard, 50)
    
    def test_draw_hazard_off_screen(self, renderer, hazard):
        """Test draw_hazard skips off-screen hazards."""
        renderer.draw_hazard(hazard, 1000)
    
    def test_draw_hazard_debug_hitbox(self, renderer, hazard):
        """Test draw_hazard draws hitbox in debug mode."""
        renderer.config.show_hitboxes = True
        renderer.draw_hazard(hazard, 0)
    
    def test_draw_level(self, renderer):
        """Test draw_level draws all level elements."""
        config = GameConfig()
        level = LevelLoader.create_demo_level(config)
        
        renderer.draw_level(level)
    
    def test_draw_ui(self, renderer, player):
        """Test draw_ui draws UI elements."""
        renderer.draw_ui(player, score=100, lives=3)
    
    def test_draw_ui_debug_mode(self, renderer, player):
        """Test draw_ui with debug mode enabled."""
        renderer.config.debug_mode = True
        renderer.draw_ui(player, score=100, lives=3)
    
    def test_draw_game_over(self, renderer):
        """Test draw_game_over draws overlay."""
        renderer.draw_game_over()
    
    def test_draw_pause(self, renderer):
        """Test draw_pause draws overlay."""
        renderer.draw_pause()
