"""
Player module for Gravity Flip Runner.
Handles player movement, gravity, and collisions.
"""

import pygame
from typing import List, Optional
from .config import GameConfig, default_config


class Player:
    """
    Player class representing the main character.
    
    Attributes:
        x: Horizontal position
        y: Vertical position
        dx: Horizontal velocity
        dy: Vertical velocity
        gravity_direction: 1 for normal gravity, -1 for inverted
        on_ground: Whether player is standing on a surface
    """
    
    def __init__(
        self,
        x: float,
        y: float,
        config: Optional[GameConfig] = None
    ):
        """
        Initialize the player.
        
        Args:
            x: Initial x position
            y: Initial y position
            config: Game configuration (uses default if not provided)
        """
        self.config = config or default_config
        
        # Position
        self.x = x
        self.y = y
        self.spawn_x = x
        self.spawn_y = y
        
        # Velocity
        self.dx = 0.0
        self.dy = 0.0
        
        # Physics state
        self.gravity_direction = 1  # 1 = down, -1 = up
        self.on_ground = False
        
        # Dimensions
        self.width = self.config.player_width
        self.height = self.config.player_height
        
        # Animation state
        self.facing_right = True
        self.is_moving = False
        
    @property
    def rect(self) -> pygame.Rect:
        """Get the player's collision rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def move(self, direction: int) -> None:
        """
        Handle horizontal movement.
        
        Args:
            direction: -1 for left, 1 for right, 0 for no movement
        """
        self.dx = direction * self.config.player_speed
        self.is_moving = direction != 0
        
        if direction > 0:
            self.facing_right = True
        elif direction < 0:
            self.facing_right = False
    
    def jump(self) -> bool:
        """
        Attempt to jump if on ground.
        
        Returns:
            True if jump was successful, False otherwise
        """
        if self.on_ground:
            # Jump direction is opposite to gravity
            self.dy = -self.config.player_jump_force * self.gravity_direction
            self.on_ground = False
            return True
        return False
    
    def flip_gravity(self) -> None:
        """Reverse the gravity direction."""
        self.gravity_direction *= -1
        self.on_ground = False
    
    def apply_gravity(self) -> None:
        """Apply gravity to vertical velocity."""
        self.dy += self.config.gravity_strength * self.gravity_direction
        
        # Clamp fall speed
        max_speed = self.config.max_fall_speed
        if self.gravity_direction > 0:
            self.dy = min(self.dy, max_speed)
        else:
            self.dy = max(self.dy, -max_speed)
    
    def update(self, platforms: List["Platform"]) -> None:
        """
        Update player position and check collisions.
        
        Args:
            platforms: List of platforms to check collisions against
        """
        self.apply_gravity()
        
        # Update horizontal position
        self.x += self.dx
        self._check_horizontal_collisions(platforms)
        
        # Update vertical position
        self.y += self.dy
        self._check_vertical_collisions(platforms)
    
    def _check_horizontal_collisions(self, platforms: List["Platform"]) -> None:
        """Check and resolve horizontal collisions with platforms."""
        player_rect = self.rect
        
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if self.dx > 0:  # Moving right
                    self.x = platform.rect.left - self.width
                elif self.dx < 0:  # Moving left
                    self.x = platform.rect.right
    
    def _check_vertical_collisions(self, platforms: List["Platform"]) -> None:
        """Check and resolve vertical collisions with platforms."""
        player_rect = self.rect
        self.on_ground = False
        
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
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
    
    def check_enemy_collision(self, enemies: List["Enemy"]) -> bool:
        """
        Check collision with enemies.
        
        Args:
            enemies: List of enemies to check
            
        Returns:
            True if colliding with any enemy, False otherwise
        """
        player_rect = self.rect
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                return True
        return False
    
    def check_hazard_collision(self, hazards: List["Hazard"]) -> bool:
        """
        Check collision with hazards.
        
        Args:
            hazards: List of hazards to check
            
        Returns:
            True if colliding with any hazard, False otherwise
        """
        player_rect = self.rect
        for hazard in hazards:
            if player_rect.colliderect(hazard.rect):
                return True
        return False
    
    def reset(self) -> None:
        """Reset player to spawn position."""
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.dx = 0
        self.dy = 0
        self.gravity_direction = 1
        self.on_ground = False
    
    def set_spawn(self, x: float, y: float) -> None:
        """Set a new spawn point."""
        self.spawn_x = x
        self.spawn_y = y
