"""
Input handler module for Gravity Flip Runner.
Maps keyboard input to player actions.
"""

import pygame
from typing import Dict, Set, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum, auto


class Action(Enum):
    """Enumeration of possible player actions."""
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    JUMP = auto()
    FLIP_GRAVITY = auto()
    PAUSE = auto()
    RESTART = auto()
    QUIT = auto()
    DEBUG_TOGGLE = auto()


@dataclass
class KeyBinding:
    """Represents a key binding for an action."""
    primary: int
    secondary: Optional[int] = None


class InputHandler:
    """
    Handles keyboard input and maps to game actions.
    
    Attributes:
        bindings: Dictionary mapping actions to key bindings
        held_actions: Set of currently held actions
    """
    
    DEFAULT_BINDINGS: Dict[Action, KeyBinding] = {
        Action.MOVE_LEFT: KeyBinding(pygame.K_LEFT, pygame.K_a),
        Action.MOVE_RIGHT: KeyBinding(pygame.K_RIGHT, pygame.K_d),
        Action.JUMP: KeyBinding(pygame.K_SPACE, pygame.K_w),
        Action.FLIP_GRAVITY: KeyBinding(pygame.K_UP, pygame.K_f),
        Action.PAUSE: KeyBinding(pygame.K_ESCAPE, pygame.K_p),
        Action.RESTART: KeyBinding(pygame.K_r, None),
        Action.QUIT: KeyBinding(pygame.K_q, None),
        Action.DEBUG_TOGGLE: KeyBinding(pygame.K_F3, None),
    }
    
    def __init__(self, bindings: Optional[Dict[Action, KeyBinding]] = None):
        """
        Initialize the input handler.
        
        Args:
            bindings: Custom key bindings (uses defaults if not provided)
        """
        self.bindings = bindings or self.DEFAULT_BINDINGS.copy()
        self.held_actions: Set[Action] = set()
        self._pressed_this_frame: Set[Action] = set()
        self._released_this_frame: Set[Action] = set()
        
        # Callbacks for actions
        self._callbacks: Dict[Action, Callable[[], Any]] = {}
    
    def register_callback(self, action: Action, callback: Callable[[], Any]) -> None:
        """
        Register a callback for when an action is triggered.
        
        Args:
            action: The action to register for
            callback: Function to call when action is triggered
        """
        self._callbacks[action] = callback
    
    def _get_action_for_key(self, key: int) -> Optional[Action]:
        """Get the action associated with a key."""
        for action, binding in self.bindings.items():
            if key == binding.primary or key == binding.secondary:
                return action
        return None
    
    def process_events(self, events: list) -> None:
        """
        Process pygame events for this frame.
        
        Args:
            events: List of pygame events
        """
        self._pressed_this_frame.clear()
        self._released_this_frame.clear()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                action = self._get_action_for_key(event.key)
                if action:
                    self.held_actions.add(action)
                    self._pressed_this_frame.add(action)
                    
                    # Trigger callback for press-triggered actions
                    if action in self._callbacks:
                        self._callbacks[action]()
                        
            elif event.type == pygame.KEYUP:
                action = self._get_action_for_key(event.key)
                if action and action in self.held_actions:
                    self.held_actions.discard(action)
                    self._released_this_frame.add(action)
    
    def is_action_held(self, action: Action) -> bool:
        """Check if an action key is currently held."""
        return action in self.held_actions
    
    def is_action_pressed(self, action: Action) -> bool:
        """Check if an action was just pressed this frame."""
        return action in self._pressed_this_frame
    
    def is_action_released(self, action: Action) -> bool:
        """Check if an action was just released this frame."""
        return action in self._released_this_frame
    
    def get_movement_direction(self) -> int:
        """
        Get the horizontal movement direction.
        
        Returns:
            -1 for left, 1 for right, 0 for no movement
        """
        direction = 0
        if self.is_action_held(Action.MOVE_LEFT):
            direction -= 1
        if self.is_action_held(Action.MOVE_RIGHT):
            direction += 1
        return direction
    
    def should_jump(self) -> bool:
        """Check if jump action was just pressed."""
        return self.is_action_pressed(Action.JUMP)
    
    def should_flip_gravity(self) -> bool:
        """Check if gravity flip action was just pressed."""
        return self.is_action_pressed(Action.FLIP_GRAVITY)
    
    def should_pause(self) -> bool:
        """Check if pause action was just pressed."""
        return self.is_action_pressed(Action.PAUSE)
    
    def should_restart(self) -> bool:
        """Check if restart action was just pressed."""
        return self.is_action_pressed(Action.RESTART)
    
    def should_quit(self) -> bool:
        """Check if quit action was just pressed."""
        return self.is_action_pressed(Action.QUIT)
    
    def should_toggle_debug(self) -> bool:
        """Check if debug toggle was just pressed."""
        return self.is_action_pressed(Action.DEBUG_TOGGLE)
    
    def reset(self) -> None:
        """Reset all input state."""
        self.held_actions.clear()
        self._pressed_this_frame.clear()
        self._released_this_frame.clear()
