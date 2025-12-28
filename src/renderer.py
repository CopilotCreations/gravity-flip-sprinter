"""
Renderer module for Gravity Flip Runner.
Handles all drawing operations.
"""

import pygame
from typing import Optional, List, Tuple
from .config import GameConfig, default_config
from .player import Player
from .platforms import Platform, MovingPlatform, GravityPlatform
from .enemies import Enemy, Hazard
from .level import Level


class Renderer:
    """
    Handles all rendering operations for the game.
    
    Attributes:
        screen: Pygame display surface
        config: Game configuration
    """
    
    def __init__(
        self,
        screen: pygame.Surface,
        config: Optional[GameConfig] = None
    ):
        """
        Initialize the renderer.
        
        Args:
            screen: Pygame display surface
            config: Game configuration
        """
        self.screen = screen
        self.config = config or default_config
        
        # Parallax background layers (color, scroll_factor)
        self.bg_layers: List[Tuple[Tuple[int, int, int], float]] = [
            ((20, 20, 35), 0.1),   # Far background
            ((25, 25, 45), 0.3),   # Mid background
            ((30, 30, 50), 0.5),   # Near background
        ]
        
    def clear(self) -> None:
        """Clear the screen with background color."""
        self.screen.fill(self.config.background_color)
    
    def draw_background(self, camera_x: float = 0) -> None:
        """
        Draw parallax background layers.
        
        Args:
            camera_x: Current camera x position
        """
        height = self.config.window_height
        layer_height = height // len(self.bg_layers)
        
        for i, (color, scroll_factor) in enumerate(self.bg_layers):
            # Create parallax offset
            offset = int(camera_x * scroll_factor) % self.config.window_width
            
            # Draw layer
            y = i * layer_height
            rect = pygame.Rect(0, y, self.config.window_width, layer_height)
            self.screen.fill(color, rect)
    
    def draw_player(
        self,
        player: Player,
        camera_x: float = 0
    ) -> None:
        """
        Draw the player.
        
        Args:
            player: Player object to draw
            camera_x: Camera x position for scrolling
        """
        # Calculate screen position
        screen_x = int(player.x - camera_x)
        screen_y = int(player.y)
        
        # Draw player body
        player_rect = pygame.Rect(
            screen_x, screen_y,
            player.width, player.height
        )
        pygame.draw.rect(self.screen, player.config.player_color, player_rect)
        
        # Draw direction indicator (eyes/facing)
        eye_size = 6
        eye_y = screen_y + 8 if player.gravity_direction > 0 else screen_y + player.height - 14
        
        if player.facing_right:
            eye_x = screen_x + player.width - 12
        else:
            eye_x = screen_x + 6
        
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (eye_x, eye_y),
            eye_size
        )
        pygame.draw.circle(
            self.screen,
            (0, 0, 0),
            (eye_x + (2 if player.facing_right else -2), eye_y),
            eye_size // 2
        )
        
        # Draw gravity indicator
        indicator_y = screen_y + player.height + 5 if player.gravity_direction > 0 else screen_y - 10
        arrow_dir = 1 if player.gravity_direction > 0 else -1
        
        pygame.draw.polygon(
            self.screen,
            (200, 200, 255),
            [
                (screen_x + player.width // 2, indicator_y + 5 * arrow_dir),
                (screen_x + player.width // 2 - 5, indicator_y - 5 * arrow_dir),
                (screen_x + player.width // 2 + 5, indicator_y - 5 * arrow_dir),
            ]
        )
        
        # Debug hitbox
        if self.config.show_hitboxes:
            pygame.draw.rect(self.screen, (255, 255, 0), player_rect, 1)
    
    def draw_platform(
        self,
        platform: Platform,
        camera_x: float = 0
    ) -> None:
        """
        Draw a platform.
        
        Args:
            platform: Platform object to draw
            camera_x: Camera x position
        """
        render_rect = platform.get_render_rect(camera_x)
        
        # Skip if off screen
        if render_rect.right < 0 or render_rect.left > self.config.window_width:
            return
        
        pygame.draw.rect(self.screen, platform.color, render_rect)
        
        # Add visual distinction for special platforms
        if isinstance(platform, MovingPlatform):
            # Draw movement indicators
            pygame.draw.rect(self.screen, (150, 150, 170), render_rect, 2)
        elif isinstance(platform, GravityPlatform):
            # Draw gravity icon
            pygame.draw.rect(self.screen, (100, 150, 200), render_rect, 2)
        
        # Debug hitbox
        if self.config.show_hitboxes:
            pygame.draw.rect(self.screen, (0, 255, 0), render_rect, 1)
    
    def draw_enemy(
        self,
        enemy: Enemy,
        camera_x: float = 0
    ) -> None:
        """
        Draw an enemy.
        
        Args:
            enemy: Enemy object to draw
            camera_x: Camera x position
        """
        render_rect = enemy.get_render_rect(camera_x)
        
        # Skip if off screen
        if render_rect.right < 0 or render_rect.left > self.config.window_width:
            return
        
        pygame.draw.rect(self.screen, enemy.color, render_rect)
        
        # Draw angry eyes
        eye_size = 4
        eye_y = render_rect.y + 8 if enemy.gravity_direction > 0 else render_rect.y + enemy.height - 12
        
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (render_rect.x + 8, eye_y),
            eye_size
        )
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (render_rect.x + enemy.width - 8, eye_y),
            eye_size
        )
        
        # Debug hitbox
        if self.config.show_hitboxes:
            pygame.draw.rect(self.screen, (255, 0, 0), render_rect, 1)
    
    def draw_hazard(
        self,
        hazard: Hazard,
        camera_x: float = 0
    ) -> None:
        """
        Draw a hazard.
        
        Args:
            hazard: Hazard object to draw
            camera_x: Camera x position
        """
        render_rect = hazard.get_render_rect(camera_x)
        
        # Skip if off screen
        if render_rect.right < 0 or render_rect.left > self.config.window_width:
            return
        
        # Draw spiky hazard
        pygame.draw.rect(self.screen, hazard.color, render_rect)
        
        # Draw spike triangles
        spike_count = render_rect.width // 10
        for i in range(spike_count):
            spike_x = render_rect.x + i * 10 + 5
            pygame.draw.polygon(
                self.screen,
                (255, 50, 0),
                [
                    (spike_x, render_rect.y),
                    (spike_x - 5, render_rect.y + render_rect.height),
                    (spike_x + 5, render_rect.y + render_rect.height),
                ]
            )
        
        # Debug hitbox
        if self.config.show_hitboxes:
            pygame.draw.rect(self.screen, (255, 128, 0), render_rect, 1)
    
    def draw_level(self, level: Level) -> None:
        """
        Draw all level elements.
        
        Args:
            level: Level object containing all game objects
        """
        camera_x = level.camera_x
        
        # Draw background
        self.draw_background(camera_x)
        
        # Draw platforms
        for platform in level.platforms:
            self.draw_platform(platform, camera_x)
        
        # Draw hazards
        for hazard in level.hazards:
            self.draw_hazard(hazard, camera_x)
        
        # Draw enemies
        for enemy in level.enemies:
            self.draw_enemy(enemy, camera_x)
    
    def draw_ui(
        self,
        player: Player,
        score: int = 0,
        lives: int = 3
    ) -> None:
        """
        Draw UI elements.
        
        Args:
            player: Player object for status info
            score: Current score
            lives: Remaining lives
        """
        font = pygame.font.Font(None, 36)
        
        # Lives
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 10))
        
        # Score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 45))
        
        # Gravity indicator
        gravity_str = "Normal" if player.gravity_direction > 0 else "Inverted"
        gravity_text = font.render(f"Gravity: {gravity_str}", True, (200, 200, 255))
        self.screen.blit(gravity_text, (self.config.window_width - 180, 10))
        
        # Debug info
        if self.config.debug_mode:
            debug_font = pygame.font.Font(None, 24)
            debug_lines = [
                f"Pos: ({player.x:.1f}, {player.y:.1f})",
                f"Vel: ({player.dx:.1f}, {player.dy:.1f})",
                f"On Ground: {player.on_ground}",
            ]
            for i, line in enumerate(debug_lines):
                text = debug_font.render(line, True, (200, 200, 200))
                self.screen.blit(text, (10, self.config.window_height - 80 + i * 20))
    
    def draw_game_over(self) -> None:
        """Draw game over screen."""
        # Dim overlay
        overlay = pygame.Surface((self.config.window_width, self.config.window_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, (255, 50, 50))
        text_rect = text.get_rect(center=(
            self.config.window_width // 2,
            self.config.window_height // 2 - 30
        ))
        self.screen.blit(text, text_rect)
        
        # Restart prompt
        small_font = pygame.font.Font(None, 36)
        restart_text = small_font.render("Press R to restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(
            self.config.window_width // 2,
            self.config.window_height // 2 + 30
        ))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause(self) -> None:
        """Draw pause overlay."""
        # Dim overlay
        overlay = pygame.Surface((self.config.window_width, self.config.window_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(100)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(
            self.config.window_width // 2,
            self.config.window_height // 2
        ))
        self.screen.blit(text, text_rect)
