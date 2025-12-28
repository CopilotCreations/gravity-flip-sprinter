"""
Enemies module for Gravity Flip Runner.
Contains enemy classes with AI behavior.
"""

import pygame
from typing import List, Optional, Tuple
from .config import GameConfig, default_config


class Enemy:
    """
    Basic enemy that patrols along platforms.
    
    Attributes:
        x, y: Position
        width, height: Dimensions
        speed: Movement speed
        gravity_direction: Current gravity state
    """
    
    def __init__(
        self,
        x: float,
        y: float,
        width: int = 32,
        height: int = 32,
        patrol_distance: float = 100.0,
        speed: float = 2.0,
        color: Optional[Tuple[int, int, int]] = None,
        config: Optional[GameConfig] = None
    ):
        """
        Initialize an enemy.
        
        Args:
            x: X position
            y: Y position
            width: Enemy width
            height: Enemy height
            patrol_distance: Distance to patrol from start
            speed: Movement speed
            color: RGB color tuple
            config: Game configuration
        """
        self.config = config or default_config
        
        self.x = x
        self.y = y
        self.start_x = x
        self.width = width
        self.height = height
        self.patrol_distance = patrol_distance
        self.speed = speed
        self.color = color or self.config.enemy_color
        
        # Movement state
        self.dx = speed
        self.dy = 0.0
        self.direction = 1  # 1 = right, -1 = left
        
        # Physics
        self.gravity_direction = 1
        self.on_ground = False
        
    @property
    def rect(self) -> pygame.Rect:
        """Get the enemy's collision rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def set_gravity(self, direction: int) -> None:
        """Set the gravity direction for this enemy."""
        self.gravity_direction = direction
        self.on_ground = False
    
    def apply_gravity(self) -> None:
        """Apply gravity to vertical velocity."""
        gravity = self.config.gravity_strength * self.gravity_direction
        self.dy += gravity
        
        # Clamp fall speed
        max_speed = self.config.max_fall_speed
        if self.gravity_direction > 0:
            self.dy = min(self.dy, max_speed)
        else:
            self.dy = max(self.dy, -max_speed)
    
    def update(self, platforms: List["Platform"]) -> None:
        """
        Update enemy position and behavior.
        
        Args:
            platforms: List of platforms for collision detection
        """
        self.apply_gravity()
        
        # Patrol movement
        self._patrol()
        
        # Update position
        self.x += self.dx * self.direction
        self.y += self.dy
        
        # Check collisions
        self._check_collisions(platforms)
    
    def _patrol(self) -> None:
        """Handle patrol behavior."""
        distance_from_start = self.x - self.start_x
        
        if distance_from_start >= self.patrol_distance:
            self.direction = -1
        elif distance_from_start <= -self.patrol_distance:
            self.direction = 1
    
    def _check_collisions(self, platforms: List["Platform"]) -> None:
        """Check and resolve platform collisions."""
        enemy_rect = self.rect
        self.on_ground = False
        
        for platform in platforms:
            if enemy_rect.colliderect(platform.rect):
                if self.gravity_direction > 0:  # Normal gravity
                    if self.dy > 0:  # Falling down
                        self.y = platform.rect.top - self.height
                        self.dy = 0
                        self.on_ground = True
                    elif self.dy < 0:  # Moving up
                        self.y = platform.rect.bottom
                        self.dy = 0
                else:  # Inverted gravity
                    if self.dy < 0:  # Falling up
                        self.y = platform.rect.bottom
                        self.dy = 0
                        self.on_ground = True
                    elif self.dy > 0:  # Moving down
                        self.y = platform.rect.top - self.height
                        self.dy = 0
    
    def get_render_rect(self, camera_x: float = 0) -> pygame.Rect:
        """Get rectangle adjusted for camera position."""
        return pygame.Rect(
            int(self.x - camera_x),
            int(self.y),
            self.width,
            self.height
        )


class Hazard:
    """
    Static hazard that damages the player on contact.
    Examples: spikes, lava, electric barriers.
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
        Initialize a hazard.
        
        Args:
            x: X position
            y: Y position
            width: Hazard width
            height: Hazard height
            color: RGB color tuple
            config: Game configuration
        """
        self.config = config or default_config
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color or self.config.hazard_color
        
    @property
    def rect(self) -> pygame.Rect:
        """Get the hazard's collision rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def get_render_rect(self, camera_x: float = 0) -> pygame.Rect:
        """Get rectangle adjusted for camera position."""
        return pygame.Rect(
            int(self.x - camera_x),
            int(self.y),
            self.width,
            self.height
        )
