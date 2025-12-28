"""
Tests for the game module.
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
import pygame

from src.game import Game, GameState
from src.config import GameConfig


# Set dummy drivers before pygame init
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'


class TestGameState:
    """Tests for GameState enum."""
    
    def test_game_states_exist(self):
        """Test all game states are defined."""
        assert GameState.RUNNING
        assert GameState.PAUSED
        assert GameState.GAME_OVER


class TestGame:
    """Tests for Game class."""
    
    @pytest.fixture
    def game(self):
        """Create a game instance for testing."""
        config = GameConfig(
            window_width=800,
            window_height=600,
            fps=60
        )
        game = Game(config)
        yield game
        pygame.quit()
    
    def test_initialization(self, game):
        """Test game initialization."""
        assert game.config is not None
        assert game.screen is not None
        assert game.clock is not None
        assert game.state == GameState.RUNNING
        assert game.lives == 3
        assert game.score == 0
        assert game.running is True
    
    def test_player_initialized(self, game):
        """Test player is initialized."""
        assert game.player is not None
        assert game.player.x == game.level.player_spawn[0]
        assert game.player.y == game.level.player_spawn[1]
    
    def test_level_initialized(self, game):
        """Test level is initialized."""
        assert game.level is not None
        assert len(game.level.platforms) > 0
    
    def test_renderer_initialized(self, game):
        """Test renderer is initialized."""
        assert game.renderer is not None
    
    def test_input_handler_initialized(self, game):
        """Test input handler is initialized."""
        assert game.input_handler is not None
    
    def test_restart_resets_state(self, game):
        """Test restart resets game state."""
        game.lives = 1
        game.score = 500
        game.state = GameState.GAME_OVER
        
        game.restart()
        
        assert game.lives == 3
        assert game.score == 0
        assert game.state == GameState.RUNNING
    
    def test_player_hit_decreases_lives(self, game):
        """Test player hit decreases lives."""
        initial_lives = game.lives
        
        game._player_hit()
        
        assert game.lives == initial_lives - 1
    
    def test_player_hit_game_over(self, game):
        """Test player hit causes game over at 0 lives."""
        game.lives = 1
        
        game._player_hit()
        
        assert game.lives == 0
        assert game.state == GameState.GAME_OVER
    
    def test_player_hit_resets_player(self, game):
        """Test player hit resets player position."""
        game.player.x = 500
        game.player.y = 100
        
        game._player_hit()
        
        assert game.player.x == game.player.spawn_x
        assert game.player.y == game.player.spawn_y
    
    def test_update_paused_does_nothing(self, game):
        """Test update does nothing when paused."""
        game.state = GameState.PAUSED
        initial_score = game.score
        
        game.update()
        
        assert game.score == initial_score
    
    def test_update_game_over_does_nothing(self, game):
        """Test update does nothing when game over."""
        game.state = GameState.GAME_OVER
        initial_score = game.score
        
        game.update()
        
        assert game.score == initial_score
    
    def test_update_increases_score(self, game):
        """Test update increases score based on distance."""
        game.player.x = 500
        
        game.update()
        
        assert game.score >= 50  # 500 / 10
    
    def test_handle_player_input_paused(self, game):
        """Test player input does nothing when paused."""
        game.state = GameState.PAUSED
        game.input_handler.held_actions.add(
            __import__('src.input_handler', fromlist=['Action']).Action.MOVE_RIGHT
        )
        
        game.handle_player_input()
        
        assert game.player.dx == 0
    
    def test_handle_events_quit(self, game):
        """Test quit event stops game."""
        with patch('pygame.event.get') as mock_get:
            quit_event = MagicMock()
            quit_event.type = pygame.QUIT
            mock_get.return_value = [quit_event]
            
            game.handle_events()
            
            assert game.running is False
    
    def test_check_collisions_enemy(self, game):
        """Test enemy collision triggers player hit."""
        # Position player on enemy
        if game.level.enemies:
            enemy = game.level.enemies[0]
            game.player.x = enemy.x
            game.player.y = enemy.y
            initial_lives = game.lives
            
            game._check_collisions()
            
            assert game.lives == initial_lives - 1
    
    def test_check_collisions_hazard(self, game):
        """Test hazard collision triggers player hit."""
        # Position player on hazard
        if game.level.hazards:
            hazard = game.level.hazards[0]
            game.player.x = hazard.x
            game.player.y = hazard.y
            initial_lives = game.lives
            
            game._check_collisions()
            
            assert game.lives == initial_lives - 1
    
    def test_check_collisions_out_of_bounds(self, game):
        """Test out of bounds triggers player hit."""
        game.player.y = 1000  # Far below level
        initial_lives = game.lives
        
        game._check_collisions()
        
        assert game.lives == initial_lives - 1
    
    def test_render_calls_renderer_methods(self, game):
        """Test render calls appropriate renderer methods."""
        with patch.object(game.renderer, 'clear') as mock_clear, \
             patch.object(game.renderer, 'draw_level') as mock_level, \
             patch.object(game.renderer, 'draw_player') as mock_player, \
             patch.object(game.renderer, 'draw_ui') as mock_ui, \
             patch('pygame.display.flip'):
            
            game.render()
            
            mock_clear.assert_called_once()
            mock_level.assert_called_once()
            mock_player.assert_called_once()
            mock_ui.assert_called_once()
    
    def test_render_draws_pause_overlay(self, game):
        """Test render draws pause overlay when paused."""
        game.state = GameState.PAUSED
        
        with patch.object(game.renderer, 'clear'), \
             patch.object(game.renderer, 'draw_level'), \
             patch.object(game.renderer, 'draw_player'), \
             patch.object(game.renderer, 'draw_ui'), \
             patch.object(game.renderer, 'draw_pause') as mock_pause, \
             patch('pygame.display.flip'):
            
            game.render()
            
            mock_pause.assert_called_once()
    
    def test_render_draws_game_over_overlay(self, game):
        """Test render draws game over overlay."""
        game.state = GameState.GAME_OVER
        
        with patch.object(game.renderer, 'clear'), \
             patch.object(game.renderer, 'draw_level'), \
             patch.object(game.renderer, 'draw_player'), \
             patch.object(game.renderer, 'draw_ui'), \
             patch.object(game.renderer, 'draw_game_over') as mock_game_over, \
             patch('pygame.display.flip'):
            
            game.render()
            
            mock_game_over.assert_called_once()
