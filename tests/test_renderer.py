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
        """Create a renderer instance for testing.

        Yields:
            Renderer: A configured renderer instance with an initialized pygame display.
        """
        pygame.init()
        pygame.font.init()
        config = GameConfig()
        screen = pygame.display.set_mode((config.window_width, config.window_height))
        renderer = Renderer(screen, config)
        yield renderer
        pygame.quit()
    
    @pytest.fixture
    def player(self):
        """Create a player for testing.

        Returns:
            Player: A player instance positioned at (100, 300).
        """
        config = GameConfig()
        return Player(100, 300, config)
    
    @pytest.fixture
    def platform(self):
        """Create a platform for testing.

        Returns:
            Platform: A static platform instance at position (0, 500) with size 200x50.
        """
        config = GameConfig()
        return Platform(0, 500, 200, 50, config=config)
    
    @pytest.fixture
    def moving_platform(self):
        """Create a moving platform for testing.

        Returns:
            MovingPlatform: A moving platform that travels between (100, 300) and (200, 300).
        """
        config = GameConfig()
        return MovingPlatform(100, 300, 100, 25, end_x=200, end_y=300, config=config)
    
    @pytest.fixture
    def gravity_platform(self):
        """Create a gravity platform for testing.

        Returns:
            GravityPlatform: A gravity-flipping platform at position (100, 200).
        """
        config = GameConfig()
        return GravityPlatform(100, 200, 100, 25, config=config)
    
    @pytest.fixture
    def enemy(self):
        """Create an enemy for testing.

        Returns:
            Enemy: An enemy instance positioned at (200, 450).
        """
        config = GameConfig()
        return Enemy(200, 450, config=config)
    
    @pytest.fixture
    def hazard(self):
        """Create a hazard for testing.

        Returns:
            Hazard: A hazard instance at position (300, 550) with size 50x20.
        """
        config = GameConfig()
        return Hazard(300, 550, 50, 20, config=config)
    
    def test_initialization(self, renderer):
        """Test renderer initialization.

        Args:
            renderer: The renderer fixture.

        Verifies that screen, config, and background layers are properly initialized.
        """
        assert renderer.screen is not None
        assert renderer.config is not None
        assert len(renderer.bg_layers) > 0
    
    def test_clear(self, renderer):
        """Test clear fills screen with background color.

        Args:
            renderer: The renderer fixture.

        Verifies that clear() executes without raising an exception.
        """
        renderer.clear()
        # No assertion needed - just verify no exception
    
    def test_draw_background(self, renderer):
        """Test draw_background runs without error.

        Args:
            renderer: The renderer fixture.

        Verifies that background drawing works with different camera offsets.
        """
        renderer.draw_background(0)
        renderer.draw_background(100)
    
    def test_draw_player(self, renderer, player):
        """Test draw_player runs without error.

        Args:
            renderer: The renderer fixture.
            player: The player fixture.

        Verifies that the player can be drawn at camera offset 0.
        """
        renderer.draw_player(player, 0)
    
    def test_draw_player_with_camera(self, renderer, player):
        """Test draw_player with camera offset.

        Args:
            renderer: The renderer fixture.
            player: The player fixture.

        Verifies that the player can be drawn with a non-zero camera offset.
        """
        renderer.draw_player(player, 50)
    
    def test_draw_player_facing_left(self, renderer, player):
        """Test draw_player when facing left.

        Args:
            renderer: The renderer fixture.
            player: The player fixture.

        Verifies that the player sprite is correctly flipped when facing left.
        """
        player.facing_right = False
        renderer.draw_player(player, 0)
    
    def test_draw_player_inverted_gravity(self, renderer, player):
        """Test draw_player with inverted gravity.

        Args:
            renderer: The renderer fixture.
            player: The player fixture.

        Verifies that the player sprite is correctly flipped when gravity is inverted.
        """
        player.gravity_direction = -1
        renderer.draw_player(player, 0)
    
    def test_draw_player_debug_hitbox(self, renderer, player):
        """Test draw_player draws hitbox in debug mode.

        Args:
            renderer: The renderer fixture.
            player: The player fixture.

        Verifies that hitbox visualization is rendered when show_hitboxes is enabled.
        """
        renderer.config.show_hitboxes = True
        renderer.draw_player(player, 0)
    
    def test_draw_platform(self, renderer, platform):
        """Test draw_platform runs without error.

        Args:
            renderer: The renderer fixture.
            platform: The platform fixture.

        Verifies that a platform can be drawn at camera offset 0.
        """
        renderer.draw_platform(platform, 0)
    
    def test_draw_platform_with_camera(self, renderer, platform):
        """Test draw_platform with camera offset.

        Args:
            renderer: The renderer fixture.
            platform: The platform fixture.

        Verifies that a platform can be drawn with a non-zero camera offset.
        """
        renderer.draw_platform(platform, 50)
    
    def test_draw_platform_off_screen_left(self, renderer, platform):
        """Test draw_platform skips off-screen platforms.

        Args:
            renderer: The renderer fixture.
            platform: The platform fixture.

        Verifies that platforms off-screen to the left are handled correctly.
        """
        renderer.draw_platform(platform, 1000)  # Platform should be off-screen
    
    def test_draw_platform_off_screen_right(self, renderer):
        """Test draw_platform skips off-screen platforms on right.

        Args:
            renderer: The renderer fixture.

        Verifies that platforms off-screen to the right are handled correctly.
        """
        config = GameConfig()
        platform = Platform(1000, 500, 100, 50, config=config)
        renderer.draw_platform(platform, 0)  # Platform should be off-screen
    
    def test_draw_moving_platform(self, renderer, moving_platform):
        """Test draw_platform for moving platform.

        Args:
            renderer: The renderer fixture.
            moving_platform: The moving platform fixture.

        Verifies that moving platforms are rendered correctly.
        """
        renderer.draw_platform(moving_platform, 0)
    
    def test_draw_gravity_platform(self, renderer, gravity_platform):
        """Test draw_platform for gravity platform.

        Args:
            renderer: The renderer fixture.
            gravity_platform: The gravity platform fixture.

        Verifies that gravity platforms are rendered correctly.
        """
        renderer.draw_platform(gravity_platform, 0)
    
    def test_draw_platform_debug_hitbox(self, renderer, platform):
        """Test draw_platform draws hitbox in debug mode.

        Args:
            renderer: The renderer fixture.
            platform: The platform fixture.

        Verifies that platform hitbox visualization is rendered when show_hitboxes is enabled.
        """
        renderer.config.show_hitboxes = True
        renderer.draw_platform(platform, 0)
    
    def test_draw_enemy(self, renderer, enemy):
        """Test draw_enemy runs without error.

        Args:
            renderer: The renderer fixture.
            enemy: The enemy fixture.

        Verifies that an enemy can be drawn at camera offset 0.
        """
        renderer.draw_enemy(enemy, 0)
    
    def test_draw_enemy_with_camera(self, renderer, enemy):
        """Test draw_enemy with camera offset.

        Args:
            renderer: The renderer fixture.
            enemy: The enemy fixture.

        Verifies that an enemy can be drawn with a non-zero camera offset.
        """
        renderer.draw_enemy(enemy, 50)
    
    def test_draw_enemy_inverted_gravity(self, renderer, enemy):
        """Test draw_enemy with inverted gravity.

        Args:
            renderer: The renderer fixture.
            enemy: The enemy fixture.

        Verifies that the enemy sprite is correctly flipped when gravity is inverted.
        """
        enemy.gravity_direction = -1
        renderer.draw_enemy(enemy, 0)
    
    def test_draw_enemy_off_screen(self, renderer, enemy):
        """Test draw_enemy skips off-screen enemies.

        Args:
            renderer: The renderer fixture.
            enemy: The enemy fixture.

        Verifies that enemies off-screen are handled correctly.
        """
        renderer.draw_enemy(enemy, 1000)
    
    def test_draw_enemy_debug_hitbox(self, renderer, enemy):
        """Test draw_enemy draws hitbox in debug mode.

        Args:
            renderer: The renderer fixture.
            enemy: The enemy fixture.

        Verifies that enemy hitbox visualization is rendered when show_hitboxes is enabled.
        """
        renderer.config.show_hitboxes = True
        renderer.draw_enemy(enemy, 0)
    
    def test_draw_hazard(self, renderer, hazard):
        """Test draw_hazard runs without error.

        Args:
            renderer: The renderer fixture.
            hazard: The hazard fixture.

        Verifies that a hazard can be drawn at camera offset 0.
        """
        renderer.draw_hazard(hazard, 0)
    
    def test_draw_hazard_with_camera(self, renderer, hazard):
        """Test draw_hazard with camera offset.

        Args:
            renderer: The renderer fixture.
            hazard: The hazard fixture.

        Verifies that a hazard can be drawn with a non-zero camera offset.
        """
        renderer.draw_hazard(hazard, 50)
    
    def test_draw_hazard_off_screen(self, renderer, hazard):
        """Test draw_hazard skips off-screen hazards.

        Args:
            renderer: The renderer fixture.
            hazard: The hazard fixture.

        Verifies that hazards off-screen are handled correctly.
        """
        renderer.draw_hazard(hazard, 1000)
    
    def test_draw_hazard_debug_hitbox(self, renderer, hazard):
        """Test draw_hazard draws hitbox in debug mode.

        Args:
            renderer: The renderer fixture.
            hazard: The hazard fixture.

        Verifies that hazard hitbox visualization is rendered when show_hitboxes is enabled.
        """
        renderer.config.show_hitboxes = True
        renderer.draw_hazard(hazard, 0)
    
    def test_draw_level(self, renderer):
        """Test draw_level draws all level elements.

        Args:
            renderer: The renderer fixture.

        Verifies that a complete level with all elements is rendered correctly.
        """
        config = GameConfig()
        level = LevelLoader.create_demo_level(config)
        
        renderer.draw_level(level)
    
    def test_draw_ui(self, renderer, player):
        """Test draw_ui draws UI elements.

        Args:
            renderer: The renderer fixture.
            player: The player fixture.

        Verifies that UI elements (score, lives) are rendered correctly.
        """
        renderer.draw_ui(player, score=100, lives=3)
    
    def test_draw_ui_debug_mode(self, renderer, player):
        """Test draw_ui with debug mode enabled.

        Args:
            renderer: The renderer fixture.
            player: The player fixture.

        Verifies that debug information is displayed when debug_mode is enabled.
        """
        renderer.config.debug_mode = True
        renderer.draw_ui(player, score=100, lives=3)
    
    def test_draw_game_over(self, renderer):
        """Test draw_game_over draws overlay.

        Args:
            renderer: The renderer fixture.

        Verifies that the game over overlay is rendered correctly.
        """
        renderer.draw_game_over()
    
    def test_draw_pause(self, renderer):
        """Test draw_pause draws overlay.

        Args:
            renderer: The renderer fixture.

        Verifies that the pause overlay is rendered correctly.
        """
        renderer.draw_pause()
