"""
Tests for the player module.
"""

import pytest
from unittest.mock import MagicMock, patch
from src.player import Player
from src.config import GameConfig
from src.platforms import Platform


class TestPlayer:
    """Tests for Player class."""
    
    def test_initialization(self, config):
        """Test player initialization with default values.

        Args:
            config: Game configuration fixture providing player settings.
        """
        player = Player(100, 200, config)
        
        assert player.x == 100
        assert player.y == 200
        assert player.dx == 0
        assert player.dy == 0
        assert player.gravity_direction == 1
        assert player.on_ground is False
        assert player.width == config.player_width
        assert player.height == config.player_height
    
    def test_spawn_position(self, player):
        """Test spawn position is recorded.

        Args:
            player: Player fixture initialized at spawn position.
        """
        assert player.spawn_x == 100
        assert player.spawn_y == 300
    
    def test_rect_property(self, player):
        """Test rect property returns correct pygame.Rect.

        Args:
            player: Player fixture to get rect from.
        """
        rect = player.rect
        
        assert rect.x == 100
        assert rect.y == 300
        assert rect.width == player.width
        assert rect.height == player.height
    
    def test_move_right(self, player):
        """Test moving right sets correct velocity.

        Args:
            player: Player fixture to test movement on.
        """
        player.move(1)
        
        assert player.dx == player.config.player_speed
        assert player.is_moving is True
        assert player.facing_right is True
    
    def test_move_left(self, player):
        """Test moving left sets correct velocity.

        Args:
            player: Player fixture to test movement on.
        """
        player.move(-1)
        
        assert player.dx == -player.config.player_speed
        assert player.is_moving is True
        assert player.facing_right is False
    
    def test_move_stop(self, player):
        """Test stopping movement.

        Args:
            player: Player fixture to test movement on.
        """
        player.move(1)
        player.move(0)
        
        assert player.dx == 0
        assert player.is_moving is False
    
    def test_jump_on_ground(self, player):
        """Test jumping when on ground.

        Args:
            player: Player fixture to test jumping on.
        """
        player.on_ground = True
        result = player.jump()
        
        assert result is True
        assert player.dy == -player.config.player_jump_force
        assert player.on_ground is False
    
    def test_jump_in_air(self, player):
        """Test jumping when in air (should fail).

        Args:
            player: Player fixture to test jumping on.
        """
        player.on_ground = False
        result = player.jump()
        
        assert result is False
        assert player.dy == 0
    
    def test_jump_inverted_gravity(self, player):
        """Test jumping with inverted gravity.

        Args:
            player: Player fixture to test jumping on.
        """
        player.gravity_direction = -1
        player.on_ground = True
        player.jump()
        
        # Jump should be in opposite direction
        assert player.dy == player.config.player_jump_force
    
    def test_flip_gravity(self, player):
        """Test gravity flip.

        Args:
            player: Player fixture to test gravity flip on.
        """
        original_direction = player.gravity_direction
        player.flip_gravity()
        
        assert player.gravity_direction == -original_direction
        assert player.on_ground is False
    
    def test_flip_gravity_twice(self, player):
        """Test flipping gravity twice returns to original.

        Args:
            player: Player fixture to test gravity flip on.
        """
        original_direction = player.gravity_direction
        player.flip_gravity()
        player.flip_gravity()
        
        assert player.gravity_direction == original_direction
    
    def test_apply_gravity_normal(self, player):
        """Test gravity application in normal direction.

        Args:
            player: Player fixture to test gravity on.
        """
        player.dy = 0
        player.apply_gravity()
        
        assert player.dy == player.config.gravity_strength
    
    def test_apply_gravity_inverted(self, player):
        """Test gravity application in inverted direction.

        Args:
            player: Player fixture to test gravity on.
        """
        player.gravity_direction = -1
        player.dy = 0
        player.apply_gravity()
        
        assert player.dy == -player.config.gravity_strength
    
    def test_apply_gravity_clamped(self, player):
        """Test gravity clamps at max fall speed.

        Args:
            player: Player fixture to test gravity clamping on.
        """
        player.dy = player.config.max_fall_speed
        player.apply_gravity()
        
        assert player.dy == player.config.max_fall_speed
    
    def test_apply_gravity_inverted_clamped(self, player):
        """Test inverted gravity clamps at max fall speed.

        Args:
            player: Player fixture to test gravity clamping on.
        """
        player.gravity_direction = -1
        player.dy = -player.config.max_fall_speed
        player.apply_gravity()
        
        assert player.dy == -player.config.max_fall_speed
    
    def test_reset(self, player):
        """Test player reset to spawn position.

        Args:
            player: Player fixture to test reset on.
        """
        player.x = 500
        player.y = 100
        player.dx = 5
        player.dy = 10
        player.gravity_direction = -1
        player.on_ground = True
        
        player.reset()
        
        assert player.x == player.spawn_x
        assert player.y == player.spawn_y
        assert player.dx == 0
        assert player.dy == 0
        assert player.gravity_direction == 1
        assert player.on_ground is False
    
    def test_set_spawn(self, player):
        """Test setting new spawn position.

        Args:
            player: Player fixture to test spawn setting on.
        """
        player.set_spawn(200, 400)
        
        assert player.spawn_x == 200
        assert player.spawn_y == 400
    
    def test_update_applies_gravity(self, player):
        """Test update applies gravity.

        Args:
            player: Player fixture to test update on.
        """
        initial_dy = player.dy
        player.update([])
        
        assert player.dy != initial_dy
    
    def test_update_moves_player(self, player):
        """Test update moves player by velocity.

        Args:
            player: Player fixture to test update on.
        """
        player.dx = 5
        player.dy = 0
        initial_x = player.x
        
        player.update([])
        
        assert player.x == initial_x + 5
    
    def test_horizontal_collision_right(self, player, config):
        """Test horizontal collision when moving right.

        Args:
            player: Player fixture to test collision on.
            config: Game configuration fixture for platform creation.
        """
        platform = Platform(140, 280, 100, 100, config=config)
        player.x = 100
        player.dx = 10
        player.dy = 0
        
        player.update([platform])
        
        # Player should stop at platform edge
        assert player.x == platform.rect.left - player.width
    
    def test_horizontal_collision_left(self, player, config):
        """Test horizontal collision when moving left.

        Args:
            player: Player fixture to test collision on.
            config: Game configuration fixture for platform creation.
        """
        platform = Platform(50, 280, 40, 100, config=config)
        player.x = 100
        player.dx = -10
        player.dy = 0
        
        player.update([platform])
        
        # Player should stop at platform edge
        assert player.x == platform.rect.right
    
    def test_vertical_collision_falling(self, player, config):
        """Test vertical collision when falling.

        Args:
            player: Player fixture to test collision on.
            config: Game configuration fixture for platform creation.
        """
        platform = Platform(80, 360, 100, 50, config=config)
        player.x = 100
        player.y = 300
        player.dy = 20
        
        player.update([platform])
        
        assert player.y == platform.rect.top - player.height
        assert player.dy == 0
        assert player.on_ground is True
    
    def test_vertical_collision_ceiling(self, player, config):
        """Test vertical collision with ceiling.

        Args:
            player: Player fixture to test collision on.
            config: Game configuration fixture for platform creation.
        """
        platform = Platform(80, 200, 100, 50, config=config)
        player.x = 100
        player.y = 260
        player.dy = -20
        
        player.update([platform])
        
        assert player.y == platform.rect.bottom
        assert player.dy == 0
    
    def test_check_enemy_collision_hit(self, player, enemy):
        """Test enemy collision detection when hit.

        Args:
            player: Player fixture to test collision on.
            enemy: Enemy fixture to collide with.
        """
        # Position player on enemy
        player.x = enemy.x
        player.y = enemy.y
        
        result = player.check_enemy_collision([enemy])
        
        assert result is True
    
    def test_check_enemy_collision_miss(self, player, enemy):
        """Test enemy collision detection when not hit.

        Args:
            player: Player fixture to test collision on.
            enemy: Enemy fixture to check against.
        """
        player.x = 0
        player.y = 0
        
        result = player.check_enemy_collision([enemy])
        
        assert result is False
    
    def test_check_hazard_collision_hit(self, player, hazard):
        """Test hazard collision detection when hit.

        Args:
            player: Player fixture to test collision on.
            hazard: Hazard fixture to collide with.
        """
        player.x = hazard.x
        player.y = hazard.y
        
        result = player.check_hazard_collision([hazard])
        
        assert result is True
    
    def test_check_hazard_collision_miss(self, player, hazard):
        """Test hazard collision detection when not hit.

        Args:
            player: Player fixture to test collision on.
            hazard: Hazard fixture to check against.
        """
        player.x = 0
        player.y = 0
        
        result = player.check_hazard_collision([hazard])
        
        assert result is False
    
    def test_inverted_gravity_landing(self, player, config):
        """Test landing on ceiling with inverted gravity.

        Args:
            player: Player fixture to test landing on.
            config: Game configuration fixture for platform creation.
        """
        platform = Platform(80, 200, 100, 50, config=config)
        player.gravity_direction = -1
        player.x = 100
        player.y = 260
        player.dy = -20  # Moving up (falling with inverted gravity)
        
        player.update([platform])
        
        assert player.y == platform.rect.bottom
        assert player.dy == 0
        assert player.on_ground is True
