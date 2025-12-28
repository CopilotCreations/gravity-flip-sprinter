"""
Game module for Gravity Flip Runner.
Main game loop and state management.
"""

import pygame
from typing import Optional
from enum import Enum, auto

from .config import GameConfig, default_config
from .player import Player
from .level import Level, LevelLoader
from .renderer import Renderer
from .input_handler import InputHandler


class GameState(Enum):
    """Possible game states."""
    RUNNING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Game:
    """
    Main game class handling the game loop and state.
    
    Attributes:
        config: Game configuration
        screen: Pygame display surface
        clock: Pygame clock for frame rate control
        state: Current game state
        player: Player object
        level: Current level
        renderer: Renderer instance
        input_handler: Input handler instance
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        """
        Initialize the game.
        
        Args:
            config: Game configuration (uses default if not provided)
        """
        self.config = config or default_config
        
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        
        # Create display
        self.screen = pygame.display.set_mode((
            self.config.window_width,
            self.config.window_height
        ))
        pygame.display.set_caption(self.config.title)
        
        # Clock for frame rate
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.RUNNING
        self.lives = 3
        self.score = 0
        self.running = True
        
        # Initialize game objects
        self._init_game_objects()
    
    def _init_game_objects(self) -> None:
        """Initialize or reset game objects."""
        # Load level
        self.level = LevelLoader.create_demo_level(self.config)
        
        # Create player at spawn point
        spawn_x, spawn_y = self.level.player_spawn
        self.player = Player(spawn_x, spawn_y, self.config)
        
        # Create renderer
        self.renderer = Renderer(self.screen, self.config)
        
        # Create input handler
        self.input_handler = InputHandler()
    
    def handle_events(self) -> None:
        """Process pygame events."""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
        
        # Process input
        self.input_handler.process_events(events)
        
        # Handle global actions
        if self.input_handler.should_quit():
            self.running = False
            return
        
        if self.input_handler.should_toggle_debug():
            self.config.debug_mode = not self.config.debug_mode
            self.config.show_hitboxes = self.config.debug_mode
        
        if self.input_handler.should_pause():
            if self.state == GameState.RUNNING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.RUNNING
        
        if self.input_handler.should_restart():
            self.restart()
    
    def handle_player_input(self) -> None:
        """Process player-specific input."""
        if self.state != GameState.RUNNING:
            return
        
        # Movement
        direction = self.input_handler.get_movement_direction()
        self.player.move(direction)
        
        # Jump
        if self.input_handler.should_jump():
            self.player.jump()
        
        # Gravity flip
        if self.input_handler.should_flip_gravity():
            self.player.flip_gravity()
            self.level.set_gravity_for_all(self.player.gravity_direction)
    
    def update(self) -> None:
        """Update game state."""
        if self.state != GameState.RUNNING:
            return
        
        # Update player
        self.player.update(self.level.platforms)
        
        # Update level (camera, platforms, enemies)
        self.level.update(self.player.x)
        
        # Check collisions
        self._check_collisions()
        
        # Update score based on distance
        self.score = max(self.score, int(self.player.x / 10))
    
    def _check_collisions(self) -> None:
        """Check for player collisions with hazards and enemies."""
        # Check enemy collision
        if self.player.check_enemy_collision(self.level.enemies):
            self._player_hit()
        
        # Check hazard collision
        if self.player.check_hazard_collision(self.level.hazards):
            self._player_hit()
        
        # Check out of bounds
        if self.level.is_player_out_of_bounds(
            self.player.x,
            self.player.y,
            self.player.height
        ):
            self._player_hit()
    
    def _player_hit(self) -> None:
        """Handle player getting hit."""
        self.lives -= 1
        
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
        else:
            self.player.reset()
            self.level.reset()
    
    def render(self) -> None:
        """Render the game."""
        # Clear screen
        self.renderer.clear()
        
        # Draw level
        self.renderer.draw_level(self.level)
        
        # Draw player
        self.renderer.draw_player(self.player, self.level.camera_x)
        
        # Draw UI
        self.renderer.draw_ui(self.player, self.score, self.lives)
        
        # Draw state-specific overlays
        if self.state == GameState.PAUSED:
            self.renderer.draw_pause()
        elif self.state == GameState.GAME_OVER:
            self.renderer.draw_game_over()
        
        # Update display
        pygame.display.flip()
    
    def restart(self) -> None:
        """Restart the game."""
        self.lives = 3
        self.score = 0
        self.state = GameState.RUNNING
        self._init_game_objects()
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            # Handle events
            self.handle_events()
            
            if not self.running:
                break
            
            # Handle player input
            self.handle_player_input()
            
            # Update game state
            self.update()
            
            # Render
            self.render()
            
            # Maintain frame rate
            self.clock.tick(self.config.fps)
        
        # Cleanup
        pygame.quit()


def main():
    """Entry point for the game."""
    config = GameConfig.from_env()
    game = Game(config)
    game.run()


if __name__ == "__main__":
    main()
