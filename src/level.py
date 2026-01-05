"""
Level module for Gravity Flip Runner.
Handles level loading, management, and scrolling.
"""

import json
from typing import List, Optional, Dict, Any, Tuple
from .platforms import Platform, MovingPlatform, GravityPlatform
from .enemies import Enemy, Hazard
from .config import GameConfig, default_config


class Level:
    """
    Level container and manager.
    
    Attributes:
        platforms: List of all platforms in the level
        enemies: List of all enemies
        hazards: List of all hazards
        player_spawn: Starting position for the player
        level_bounds: Tuple of (min_x, max_x, min_y, max_y)
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        """Initialize an empty level.
        
        Args:
            config: Game configuration settings. Uses default_config if None.
        """
        self.config = config or default_config
        
        self.platforms: List[Platform] = []
        self.enemies: List[Enemy] = []
        self.hazards: List[Hazard] = []
        
        self.player_spawn: Tuple[float, float] = (100, 300)
        self.level_bounds: Tuple[float, float, float, float] = (0, 2000, 0, 600)
        
        # Camera
        self.camera_x = 0.0
        
    def add_platform(self, platform: Platform) -> None:
        """Add a platform to the level.
        
        Args:
            platform: The platform object to add.
        """
        self.platforms.append(platform)
        
    def add_enemy(self, enemy: Enemy) -> None:
        """Add an enemy to the level.
        
        Args:
            enemy: The enemy object to add.
        """
        self.enemies.append(enemy)
        
    def add_hazard(self, hazard: Hazard) -> None:
        """Add a hazard to the level.
        
        Args:
            hazard: The hazard object to add.
        """
        self.hazards.append(hazard)
    
    def update(self, player_x: float) -> None:
        """
        Update all level objects.
        
        Args:
            player_x: Player x position for camera following
        """
        # Update camera to follow player
        target_camera = player_x - self.config.window_width // 3
        self.camera_x = max(
            self.level_bounds[0],
            min(target_camera, self.level_bounds[1] - self.config.window_width)
        )
        
        # Update platforms
        for platform in self.platforms:
            platform.update()
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.platforms)
    
    def set_gravity_for_all(self, direction: int) -> None:
        """
        Set gravity direction for all gravity-affected objects.
        
        Args:
            direction: 1 for normal, -1 for inverted
        """
        for enemy in self.enemies:
            enemy.set_gravity(direction)
        
        for platform in self.platforms:
            if isinstance(platform, GravityPlatform):
                platform.set_gravity(direction)
    
    def reset(self) -> None:
        """Reset all level objects to initial state.
        
        Resets camera position to 0 and resets all gravity platforms.
        Note: Enemies would need spawn position tracking for full reset.
        """
        self.camera_x = 0
        
        for platform in self.platforms:
            if isinstance(platform, GravityPlatform):
                platform.reset()
        
        # Enemies would need spawn position tracking for full reset
    
    def is_player_out_of_bounds(
        self,
        player_x: float,
        player_y: float,
        player_height: int
    ) -> bool:
        """Check if player has fallen out of level bounds.
        
        Args:
            player_x: Player's current x position.
            player_y: Player's current y position.
            player_height: Height of the player sprite.
            
        Returns:
            True if player is outside vertical bounds, False otherwise.
        """
        min_x, max_x, min_y, max_y = self.level_bounds
        return (
            player_y > max_y + player_height or
            player_y < min_y - player_height
        )


class LevelLoader:
    """Utility class for loading levels from various sources."""
    
    @staticmethod
    def create_demo_level(config: Optional[GameConfig] = None) -> Level:
        """Create a demo level for testing.
        
        Creates a sample level with ground platforms, ceiling platforms,
        floating platforms, moving platforms, enemies, and hazards.
        
        Args:
            config: Game configuration settings. Uses default_config if None.
            
        Returns:
            A Level object with sample content.
        """
        config = config or default_config
        level = Level(config)
        
        # Set level bounds
        level.level_bounds = (0, 3000, 0, config.window_height)
        level.player_spawn = (100, 400)
        
        # Ground platforms
        level.add_platform(Platform(0, 550, 500, 50, config=config))
        level.add_platform(Platform(600, 550, 400, 50, config=config))
        level.add_platform(Platform(1100, 550, 600, 50, config=config))
        level.add_platform(Platform(1800, 550, 500, 50, config=config))
        level.add_platform(Platform(2400, 550, 600, 50, config=config))
        
        # Ceiling platforms (for inverted gravity)
        level.add_platform(Platform(0, 0, 500, 50, config=config))
        level.add_platform(Platform(600, 0, 400, 50, config=config))
        level.add_platform(Platform(1100, 0, 600, 50, config=config))
        level.add_platform(Platform(1800, 0, 500, 50, config=config))
        level.add_platform(Platform(2400, 0, 600, 50, config=config))
        
        # Floating platforms
        level.add_platform(Platform(300, 400, 150, 25, config=config))
        level.add_platform(Platform(550, 300, 150, 25, config=config))
        level.add_platform(Platform(800, 350, 150, 25, config=config))
        level.add_platform(Platform(1300, 300, 200, 25, config=config))
        level.add_platform(Platform(1600, 400, 150, 25, config=config))
        level.add_platform(Platform(2000, 350, 200, 25, config=config))
        level.add_platform(Platform(2500, 300, 150, 25, config=config))
        
        # Moving platform
        level.add_platform(MovingPlatform(
            1000, 450, 100, 25,
            end_x=1000, end_y=150,
            speed=1.5,
            config=config
        ))
        
        # Enemies
        level.add_enemy(Enemy(400, 500, patrol_distance=80, config=config))
        level.add_enemy(Enemy(1200, 500, patrol_distance=100, config=config))
        level.add_enemy(Enemy(2000, 500, patrol_distance=120, config=config))
        
        # Hazards (spikes at gaps)
        level.add_hazard(Hazard(510, 570, 80, 30, config=config))
        level.add_hazard(Hazard(1010, 570, 80, 30, config=config))
        level.add_hazard(Hazard(1710, 570, 80, 30, config=config))
        level.add_hazard(Hazard(2310, 570, 80, 30, config=config))
        
        return level
    
    @staticmethod
    def load_from_json(filepath: str, config: Optional[GameConfig] = None) -> Level:
        """Load a level from a JSON file.
        
        Parses a JSON file containing level data including bounds, spawn point,
        platforms (static, moving, gravity), enemies, and hazards.
        
        Args:
            filepath: Path to the JSON level file.
            config: Game configuration settings. Uses default_config if None.
            
        Returns:
            A Level object loaded from the file.
            
        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        config = config or default_config
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        level = Level(config)
        
        # Level metadata
        if 'bounds' in data:
            level.level_bounds = tuple(data['bounds'])
        if 'spawn' in data:
            level.player_spawn = tuple(data['spawn'])
        
        # Load platforms
        for p in data.get('platforms', []):
            platform_type = p.get('type', 'static')
            
            if platform_type == 'moving':
                level.add_platform(MovingPlatform(
                    p['x'], p['y'], p['width'], p['height'],
                    p.get('end_x', p['x']),
                    p.get('end_y', p['y']),
                    p.get('speed', 2.0),
                    config=config
                ))
            elif platform_type == 'gravity':
                level.add_platform(GravityPlatform(
                    p['x'], p['y'], p['width'], p['height'],
                    config=config
                ))
            else:
                level.add_platform(Platform(
                    p['x'], p['y'], p['width'], p['height'],
                    config=config
                ))
        
        # Load enemies
        for e in data.get('enemies', []):
            level.add_enemy(Enemy(
                e['x'], e['y'],
                e.get('width', 32),
                e.get('height', 32),
                e.get('patrol_distance', 100),
                e.get('speed', 2.0),
                config=config
            ))
        
        # Load hazards
        for h in data.get('hazards', []):
            level.add_hazard(Hazard(
                h['x'], h['y'], h['width'], h['height'],
                config=config
            ))
        
        return level
    
    @staticmethod
    def save_to_json(level: Level, filepath: str) -> None:
        """Save a level to a JSON file.
        
        Serializes the level data including bounds, spawn point, platforms,
        enemies, and hazards to a JSON file with pretty-printed formatting.
        
        Args:
            level: The Level object to save.
            filepath: Output file path for the JSON file.
            
        Raises:
            IOError: If the file cannot be written.
        """
        data: Dict[str, Any] = {
            'bounds': list(level.level_bounds),
            'spawn': list(level.player_spawn),
            'platforms': [],
            'enemies': [],
            'hazards': []
        }
        
        for platform in level.platforms:
            p_data = {
                'x': platform.x,
                'y': platform.y,
                'width': platform.width,
                'height': platform.height
            }
            
            if isinstance(platform, MovingPlatform):
                p_data['type'] = 'moving'
                p_data['end_x'] = platform.end_x
                p_data['end_y'] = platform.end_y
                p_data['speed'] = platform.speed
            elif isinstance(platform, GravityPlatform):
                p_data['type'] = 'gravity'
            else:
                p_data['type'] = 'static'
            
            data['platforms'].append(p_data)
        
        for enemy in level.enemies:
            data['enemies'].append({
                'x': enemy.start_x,
                'y': enemy.y,
                'width': enemy.width,
                'height': enemy.height,
                'patrol_distance': enemy.patrol_distance,
                'speed': enemy.speed
            })
        
        for hazard in level.hazards:
            data['hazards'].append({
                'x': hazard.x,
                'y': hazard.y,
                'width': hazard.width,
                'height': hazard.height
            })
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
