"""
Platforms module for Gravity Flip Runner.
Contains platform classes for level construction.
"""

import pygame
from typing import Optional, Tuple
from .config import GameConfig, default_config


class Platform:
    """
    Basic static platform.
    
    Attributes:
        x: Horizontal position
        y: Vertical position
        width: Platform width
        height: Platform height
    """
    
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: Optional[Tuple[int, int, int]] = None,
        config: Optional[GameConfig] = None
    ):
        """
        Initialize a platform.
        
        Args:
            x: X position
            y: Y position
            width: Platform width
            height: Platform height
            color: RGB color tuple (uses config default if not provided)
            config: Game configuration
        """
        self.config = config or default_config
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color or self.config.platform_color
        
    @property
    def rect(self) -> pygame.Rect:
        """Get the platform's collision rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def update(self) -> None:
        """Update platform state (no-op for static platforms)."""
        pass
    
    def get_render_rect(self, camera_x: float = 0) -> pygame.Rect:
        """Get rectangle adjusted for camera position."""
        return pygame.Rect(
            int(self.x - camera_x),
            int(self.y),
            self.width,
            self.height
        )


class MovingPlatform(Platform):
    """
    Platform that moves between two points.
    
    Attributes:
        start_x, start_y: Starting position
        end_x, end_y: Ending position
        speed: Movement speed
        direction: Current movement direction (1 or -1)
    """
    
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        end_x: float,
        end_y: float,
        speed: float = 2.0,
        color: Optional[Tuple[int, int, int]] = None,
        config: Optional[GameConfig] = None
    ):
        """
        Initialize a moving platform.
        
        Args:
            x: Starting X position
            y: Starting Y position
            width: Platform width
            height: Platform height
            end_x: End X position
            end_y: End Y position
            speed: Movement speed
            color: RGB color tuple
            config: Game configuration
        """
        super().__init__(x, y, width, height, color, config)
        
        self.start_x = x
        self.start_y = y
        self.end_x = end_x
        self.end_y = end_y
        self.speed = speed
        self.progress = 0.0  # 0 to 1, position between start and end
        self.direction = 1  # 1 = toward end, -1 = toward start
        
    def update(self) -> None:
        """Update platform position."""
        self.progress += self.speed * self.direction * 0.01
        
        # Reverse direction at endpoints
        if self.progress >= 1.0:
            self.progress = 1.0
            self.direction = -1
        elif self.progress <= 0.0:
            self.progress = 0.0
            self.direction = 1
        
        # Interpolate position
        self.x = self.start_x + (self.end_x - self.start_x) * self.progress
        self.y = self.start_y + (self.end_y - self.start_y) * self.progress
    
    def get_velocity(self) -> Tuple[float, float]:
        """Get current velocity for player riding."""
        dx = (self.end_x - self.start_x) * self.speed * self.direction * 0.01
        dy = (self.end_y - self.start_y) * self.speed * self.direction * 0.01
        return dx, dy


class GravityPlatform(Platform):
    """
    Platform affected by gravity flips.
    Falls in the direction of gravity when activated.
    """
    
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: Optional[Tuple[int, int, int]] = None,
        config: Optional[GameConfig] = None
    ):
        """Initialize a gravity-affected platform."""
        super().__init__(x, y, width, height, color, config)
        self.dy = 0.0
        self.gravity_direction = 1
        self.is_falling = False
        self.original_y = y
        
    def set_gravity(self, direction: int) -> None:
        """Set gravity direction."""
        if direction != self.gravity_direction:
            self.gravity_direction = direction
            self.is_falling = True
    
    def update(self) -> None:
        """Update platform if falling."""
        if self.is_falling:
            self.dy += self.config.gravity_strength * self.gravity_direction * 0.5
            self.y += self.dy
    
    def reset(self) -> None:
        """Reset platform to original position."""
        self.y = self.original_y
        self.dy = 0
        self.is_falling = False
        self.gravity_direction = 1
