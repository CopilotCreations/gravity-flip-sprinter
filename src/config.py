"""
Configuration module for Gravity Flip Runner.
Contains all configurable game settings.
"""

import os
from dataclasses import dataclass


@dataclass
class GameConfig:
    """Configuration settings for the game."""
    
    # Window settings
    window_width: int = 800
    window_height: int = 600
    fps: int = 60
    title: str = "Gravity Flip Runner"
    
    # Player settings
    player_speed: float = 5.0
    player_jump_force: float = 15.0
    player_width: int = 32
    player_height: int = 48
    
    # Physics settings
    gravity_strength: float = 0.8
    max_fall_speed: float = 15.0
    
    # Debug settings
    debug_mode: bool = False
    show_hitboxes: bool = False
    
    # Colors (RGB)
    background_color: tuple = (30, 30, 50)
    player_color: tuple = (0, 200, 100)
    platform_color: tuple = (100, 100, 120)
    enemy_color: tuple = (200, 50, 50)
    hazard_color: tuple = (255, 100, 0)
    
    @classmethod
    def from_env(cls) -> "GameConfig":
        """Create configuration from environment variables.

        Reads game configuration values from environment variables, falling back
        to default values if not set.

        Supported environment variables:
            WINDOW_WIDTH: Window width in pixels (default: 800)
            WINDOW_HEIGHT: Window height in pixels (default: 600)
            FPS: Target frames per second (default: 60)
            PLAYER_SPEED: Player movement speed (default: 5.0)
            PLAYER_JUMP_FORCE: Player jump force (default: 15.0)
            GRAVITY_STRENGTH: Gravity strength (default: 0.8)
            DEBUG_MODE: Enable debug mode (default: false)
            SHOW_HITBOXES: Show collision hitboxes (default: false)

        Returns:
            GameConfig: A new GameConfig instance with values from environment.
        """
        return cls(
            window_width=int(os.getenv("WINDOW_WIDTH", 800)),
            window_height=int(os.getenv("WINDOW_HEIGHT", 600)),
            fps=int(os.getenv("FPS", 60)),
            player_speed=float(os.getenv("PLAYER_SPEED", 5.0)),
            player_jump_force=float(os.getenv("PLAYER_JUMP_FORCE", 15.0)),
            gravity_strength=float(os.getenv("GRAVITY_STRENGTH", 0.8)),
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
            show_hitboxes=os.getenv("SHOW_HITBOXES", "false").lower() == "true",
        )


# Default configuration instance
default_config = GameConfig()
