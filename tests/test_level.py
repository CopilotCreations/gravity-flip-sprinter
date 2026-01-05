"""
Tests for the level module.
"""

import pytest
import json
import tempfile
import os
from src.level import Level, LevelLoader
from src.platforms import Platform, MovingPlatform, GravityPlatform
from src.enemies import Enemy, Hazard
from src.config import GameConfig


class TestLevel:
    """Tests for Level class."""
    
    def test_initialization(self, config):
        """Test level initialization.

        Args:
            config: GameConfig fixture providing game configuration.
        """
        level = Level(config)
        
        assert level.platforms == []
        assert level.enemies == []
        assert level.hazards == []
        assert level.camera_x == 0
    
    def test_default_spawn(self, level):
        """Test default spawn position.

        Args:
            level: Level fixture providing a level instance.
        """
        assert level.player_spawn == (100, 300)
    
    def test_default_bounds(self, level):
        """Test default level bounds.

        Args:
            level: Level fixture providing a level instance.
        """
        assert level.level_bounds == (0, 2000, 0, 600)
    
    def test_add_platform(self, level, platform):
        """Test adding a platform.

        Args:
            level: Level fixture providing a level instance.
            platform: Platform fixture providing a platform instance.
        """
        level.add_platform(platform)
        
        assert len(level.platforms) == 1
        assert platform in level.platforms
    
    def test_add_enemy(self, level, enemy):
        """Test adding an enemy.

        Args:
            level: Level fixture providing a level instance.
            enemy: Enemy fixture providing an enemy instance.
        """
        level.add_enemy(enemy)
        
        assert len(level.enemies) == 1
        assert enemy in level.enemies
    
    def test_add_hazard(self, level, hazard):
        """Test adding a hazard.

        Args:
            level: Level fixture providing a level instance.
            hazard: Hazard fixture providing a hazard instance.
        """
        level.add_hazard(hazard)
        
        assert len(level.hazards) == 1
        assert hazard in level.hazards
    
    def test_update_camera_follows_player(self, level, config):
        """Test camera follows player.

        Args:
            level: Level fixture providing a level instance.
            config: GameConfig fixture providing game configuration.
        """
        level.level_bounds = (0, 3000, 0, config.window_height)
        
        level.update(500)
        
        # Camera should have moved
        assert level.camera_x > 0
    
    def test_update_camera_clamped_left(self, level):
        """Test camera doesn't go past left bound.

        Args:
            level: Level fixture providing a level instance.
        """
        level.update(0)
        
        assert level.camera_x == level.level_bounds[0]
    
    def test_update_camera_clamped_right(self, level, config):
        """Test camera doesn't go past right bound.

        Args:
            level: Level fixture providing a level instance.
            config: GameConfig fixture providing game configuration.
        """
        level.level_bounds = (0, 1000, 0, config.window_height)
        
        level.update(2000)
        
        assert level.camera_x <= level.level_bounds[1] - config.window_width
    
    def test_update_updates_platforms(self, level, moving_platform):
        """Test update updates moving platforms.

        Args:
            level: Level fixture providing a level instance.
            moving_platform: MovingPlatform fixture providing a moving platform.
        """
        level.add_platform(moving_platform)
        initial_x = moving_platform.x
        
        level.update(0)
        
        assert moving_platform.x != initial_x
    
    def test_update_updates_enemies(self, level, enemy):
        """Test update updates enemies.

        Args:
            level: Level fixture providing a level instance.
            enemy: Enemy fixture providing an enemy instance.
        """
        level.add_enemy(enemy)
        initial_x = enemy.x
        
        level.update(0)
        
        # Enemy should have moved or had gravity applied
        assert enemy.x != initial_x or enemy.dy != 0
    
    def test_set_gravity_for_all_enemies(self, level, enemy):
        """Test setting gravity for all enemies.

        Args:
            level: Level fixture providing a level instance.
            enemy: Enemy fixture providing an enemy instance.
        """
        level.add_enemy(enemy)
        
        level.set_gravity_for_all(-1)
        
        assert enemy.gravity_direction == -1
    
    def test_set_gravity_for_gravity_platforms(self, level, gravity_platform):
        """Test setting gravity for gravity platforms.

        Args:
            level: Level fixture providing a level instance.
            gravity_platform: GravityPlatform fixture providing a gravity platform.
        """
        level.add_platform(gravity_platform)
        
        level.set_gravity_for_all(-1)
        
        assert gravity_platform.gravity_direction == -1
        assert gravity_platform.is_falling is True
    
    def test_reset_camera(self, level):
        """Test reset resets camera.

        Args:
            level: Level fixture providing a level instance.
        """
        level.camera_x = 500
        
        level.reset()
        
        assert level.camera_x == 0
    
    def test_reset_gravity_platforms(self, level, gravity_platform):
        """Test reset resets gravity platforms.

        Args:
            level: Level fixture providing a level instance.
            gravity_platform: GravityPlatform fixture providing a gravity platform.
        """
        level.add_platform(gravity_platform)
        gravity_platform.y = 500
        gravity_platform.is_falling = True
        
        level.reset()
        
        assert gravity_platform.y == gravity_platform.original_y
        assert gravity_platform.is_falling is False
    
    def test_player_out_of_bounds_bottom(self, level):
        """Test player out of bounds detection (bottom).

        Args:
            level: Level fixture providing a level instance.
        """
        level.level_bounds = (0, 2000, 0, 600)
        
        result = level.is_player_out_of_bounds(100, 700, 48)
        
        assert result is True
    
    def test_player_out_of_bounds_top(self, level):
        """Test player out of bounds detection (top).

        Args:
            level: Level fixture providing a level instance.
        """
        level.level_bounds = (0, 2000, 0, 600)
        
        result = level.is_player_out_of_bounds(100, -100, 48)
        
        assert result is True
    
    def test_player_in_bounds(self, level):
        """Test player in bounds.

        Args:
            level: Level fixture providing a level instance.
        """
        level.level_bounds = (0, 2000, 0, 600)
        
        result = level.is_player_out_of_bounds(100, 300, 48)
        
        assert result is False


class TestLevelLoader:
    """Tests for LevelLoader class."""
    
    def test_create_demo_level(self, config):
        """Test demo level creation.

        Args:
            config: GameConfig fixture providing game configuration.
        """
        level = LevelLoader.create_demo_level(config)
        
        assert len(level.platforms) > 0
        assert len(level.enemies) > 0
        assert len(level.hazards) > 0
        assert level.player_spawn != (0, 0)
    
    def test_demo_level_has_ground(self, demo_level):
        """Test demo level has ground platforms.

        Args:
            demo_level: Level fixture providing a demo level instance.
        """
        ground_platforms = [p for p in demo_level.platforms if p.y >= 500]
        
        assert len(ground_platforms) > 0
    
    def test_demo_level_has_ceiling(self, demo_level):
        """Test demo level has ceiling platforms for inverted gravity.

        Args:
            demo_level: Level fixture providing a demo level instance.
        """
        ceiling_platforms = [p for p in demo_level.platforms if p.y == 0]
        
        assert len(ceiling_platforms) > 0
    
    def test_demo_level_has_moving_platform(self, demo_level):
        """Test demo level has a moving platform.

        Args:
            demo_level: Level fixture providing a demo level instance.
        """
        moving_platforms = [p for p in demo_level.platforms if isinstance(p, MovingPlatform)]
        
        assert len(moving_platforms) > 0
    
    def test_save_and_load_json(self, level, platform, enemy, hazard, config):
        """Test saving and loading level from JSON.

        Args:
            level: Level fixture providing a level instance.
            platform: Platform fixture providing a platform instance.
            enemy: Enemy fixture providing an enemy instance.
            hazard: Hazard fixture providing a hazard instance.
            config: GameConfig fixture providing game configuration.
        """
        level.add_platform(platform)
        level.add_enemy(enemy)
        level.add_hazard(hazard)
        level.player_spawn = (150, 400)
        level.level_bounds = (0, 2500, 0, 700)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            LevelLoader.save_to_json(level, filepath)
            loaded_level = LevelLoader.load_from_json(filepath, config)
            
            assert len(loaded_level.platforms) == 1
            assert len(loaded_level.enemies) == 1
            assert len(loaded_level.hazards) == 1
            assert loaded_level.player_spawn == (150, 400)
            assert loaded_level.level_bounds == (0, 2500, 0, 700)
        finally:
            os.unlink(filepath)
    
    def test_load_moving_platform_from_json(self, config):
        """Test loading moving platform from JSON.

        Args:
            config: GameConfig fixture providing game configuration.
        """
        level_data = {
            'bounds': [0, 1000, 0, 600],
            'spawn': [100, 300],
            'platforms': [{
                'type': 'moving',
                'x': 0,
                'y': 200,
                'width': 100,
                'height': 25,
                'end_x': 200,
                'end_y': 200,
                'speed': 3.0
            }],
            'enemies': [],
            'hazards': []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(level_data, f)
            filepath = f.name
        
        try:
            loaded_level = LevelLoader.load_from_json(filepath, config)
            
            assert len(loaded_level.platforms) == 1
            assert isinstance(loaded_level.platforms[0], MovingPlatform)
            assert loaded_level.platforms[0].end_x == 200
            assert loaded_level.platforms[0].speed == 3.0
        finally:
            os.unlink(filepath)
    
    def test_load_gravity_platform_from_json(self, config):
        """Test loading gravity platform from JSON.

        Args:
            config: GameConfig fixture providing game configuration.
        """
        level_data = {
            'bounds': [0, 1000, 0, 600],
            'spawn': [100, 300],
            'platforms': [{
                'type': 'gravity',
                'x': 100,
                'y': 200,
                'width': 100,
                'height': 25
            }],
            'enemies': [],
            'hazards': []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(level_data, f)
            filepath = f.name
        
        try:
            loaded_level = LevelLoader.load_from_json(filepath, config)
            
            assert len(loaded_level.platforms) == 1
            assert isinstance(loaded_level.platforms[0], GravityPlatform)
        finally:
            os.unlink(filepath)
    
    def test_save_moving_platform_type(self, level, config):
        """Test saving moving platform preserves type.

        Args:
            level: Level fixture providing a level instance.
            config: GameConfig fixture providing game configuration.
        """
        moving = MovingPlatform(0, 100, 100, 25, end_x=200, end_y=100, speed=2.0, config=config)
        level.add_platform(moving)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            LevelLoader.save_to_json(level, filepath)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert data['platforms'][0]['type'] == 'moving'
            assert data['platforms'][0]['end_x'] == 200
            assert data['platforms'][0]['speed'] == 2.0
        finally:
            os.unlink(filepath)
    
    def test_save_gravity_platform_type(self, level, gravity_platform):
        """Test saving gravity platform preserves type.

        Args:
            level: Level fixture providing a level instance.
            gravity_platform: GravityPlatform fixture providing a gravity platform.
        """
        level.add_platform(gravity_platform)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            LevelLoader.save_to_json(level, filepath)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert data['platforms'][0]['type'] == 'gravity'
        finally:
            os.unlink(filepath)
