"""
Tests for the input_handler module.
"""

import pytest
from unittest.mock import MagicMock, patch
import pygame

from src.input_handler import InputHandler, Action, KeyBinding


# Initialize pygame for event constants
pygame.init()


class TestKeyBinding:
    """Tests for KeyBinding dataclass."""
    
    def test_initialization_with_primary(self):
        """Test key binding with primary key only.

        Creates a KeyBinding with only a primary key and verifies
        that the primary is set correctly and secondary is None.
        """
        binding = KeyBinding(pygame.K_SPACE)
        
        assert binding.primary == pygame.K_SPACE
        assert binding.secondary is None
    
    def test_initialization_with_secondary(self):
        """Test key binding with both keys.

        Creates a KeyBinding with both primary and secondary keys
        and verifies both are set correctly.
        """
        binding = KeyBinding(pygame.K_LEFT, pygame.K_a)
        
        assert binding.primary == pygame.K_LEFT
        assert binding.secondary == pygame.K_a


class TestInputHandler:
    """Tests for InputHandler class."""
    
    def test_initialization(self):
        """Test input handler initialization.

        Verifies that a new InputHandler has bindings configured
        and starts with no held actions.
        """
        handler = InputHandler()
        
        assert handler.bindings is not None
        assert len(handler.held_actions) == 0
    
    def test_default_bindings(self, input_handler):
        """Test default key bindings are set.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that all expected default action bindings are present.
        """
        assert Action.MOVE_LEFT in input_handler.bindings
        assert Action.MOVE_RIGHT in input_handler.bindings
        assert Action.JUMP in input_handler.bindings
        assert Action.FLIP_GRAVITY in input_handler.bindings
        assert Action.PAUSE in input_handler.bindings
    
    def test_custom_bindings(self):
        """Test custom key bindings.

        Verifies that custom key bindings override the defaults
        when passed to the InputHandler constructor.
        """
        custom = {
            Action.JUMP: KeyBinding(pygame.K_UP, None)
        }
        handler = InputHandler(custom)
        
        assert handler.bindings[Action.JUMP].primary == pygame.K_UP
    
    def test_get_action_for_key_primary(self, input_handler):
        """Test getting action for primary key.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that the correct action is returned for a primary key.
        """
        action = input_handler._get_action_for_key(pygame.K_SPACE)
        
        assert action == Action.JUMP
    
    def test_get_action_for_key_secondary(self, input_handler):
        """Test getting action for secondary key.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that the correct action is returned for a secondary key.
        """
        action = input_handler._get_action_for_key(pygame.K_a)
        
        assert action == Action.MOVE_LEFT
    
    def test_get_action_for_unknown_key(self, input_handler):
        """Test getting action for unknown key returns None.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that None is returned for keys not bound to any action.
        """
        action = input_handler._get_action_for_key(pygame.K_z)
        
        assert action is None
    
    def test_process_keydown_event(self, input_handler):
        """Test processing keydown event.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that a keydown event adds the action to held_actions
        and marks it as pressed this frame.
        """
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE
        
        input_handler.process_events([event])
        
        assert Action.JUMP in input_handler.held_actions
        assert input_handler.is_action_pressed(Action.JUMP)
    
    def test_process_keyup_event(self, input_handler):
        """Test processing keyup event.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that a keyup event removes the action from held_actions
        and marks it as released this frame.
        """
        # First press the key
        down_event = MagicMock()
        down_event.type = pygame.KEYDOWN
        down_event.key = pygame.K_SPACE
        input_handler.process_events([down_event])
        
        # Then release it
        up_event = MagicMock()
        up_event.type = pygame.KEYUP
        up_event.key = pygame.K_SPACE
        input_handler.process_events([up_event])
        
        assert Action.JUMP not in input_handler.held_actions
        assert input_handler.is_action_released(Action.JUMP)
    
    def test_is_action_held(self, input_handler):
        """Test is_action_held method.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that is_action_held returns True only for actions
        currently in the held_actions set.
        """
        input_handler.held_actions.add(Action.MOVE_RIGHT)
        
        assert input_handler.is_action_held(Action.MOVE_RIGHT) is True
        assert input_handler.is_action_held(Action.MOVE_LEFT) is False
    
    def test_is_action_pressed_clears_next_frame(self, input_handler):
        """Test is_action_pressed clears on next frame.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that pressed state is only valid for one frame
        and clears when process_events is called again.
        """
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE
        
        input_handler.process_events([event])
        assert input_handler.is_action_pressed(Action.JUMP) is True
        
        # Next frame with no events
        input_handler.process_events([])
        assert input_handler.is_action_pressed(Action.JUMP) is False
    
    def test_get_movement_direction_right(self, input_handler):
        """Test movement direction when holding right.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that holding right returns a positive direction value.
        """
        input_handler.held_actions.add(Action.MOVE_RIGHT)
        
        assert input_handler.get_movement_direction() == 1
    
    def test_get_movement_direction_left(self, input_handler):
        """Test movement direction when holding left.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that holding left returns a negative direction value.
        """
        input_handler.held_actions.add(Action.MOVE_LEFT)
        
        assert input_handler.get_movement_direction() == -1
    
    def test_get_movement_direction_both(self, input_handler):
        """Test movement direction when holding both (cancel out).

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that holding both left and right cancels out to zero.
        """
        input_handler.held_actions.add(Action.MOVE_LEFT)
        input_handler.held_actions.add(Action.MOVE_RIGHT)
        
        assert input_handler.get_movement_direction() == 0
    
    def test_get_movement_direction_none(self, input_handler):
        """Test movement direction when holding neither.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that no movement keys results in zero direction.
        """
        assert input_handler.get_movement_direction() == 0
    
    def test_should_jump(self, input_handler):
        """Test should_jump method.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that should_jump returns True when JUMP was pressed this frame.
        """
        input_handler._pressed_this_frame.add(Action.JUMP)
        
        assert input_handler.should_jump() is True
    
    def test_should_flip_gravity(self, input_handler):
        """Test should_flip_gravity method.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that should_flip_gravity returns True when FLIP_GRAVITY
        was pressed this frame.
        """
        input_handler._pressed_this_frame.add(Action.FLIP_GRAVITY)
        
        assert input_handler.should_flip_gravity() is True
    
    def test_should_pause(self, input_handler):
        """Test should_pause method.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that should_pause returns True when PAUSE was pressed this frame.
        """
        input_handler._pressed_this_frame.add(Action.PAUSE)
        
        assert input_handler.should_pause() is True
    
    def test_should_restart(self, input_handler):
        """Test should_restart method.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that should_restart returns True when RESTART was pressed this frame.
        """
        input_handler._pressed_this_frame.add(Action.RESTART)
        
        assert input_handler.should_restart() is True
    
    def test_should_quit(self, input_handler):
        """Test should_quit method.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that should_quit returns True when QUIT was pressed this frame.
        """
        input_handler._pressed_this_frame.add(Action.QUIT)
        
        assert input_handler.should_quit() is True
    
    def test_should_toggle_debug(self, input_handler):
        """Test should_toggle_debug method.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that should_toggle_debug returns True when DEBUG_TOGGLE
        was pressed this frame.
        """
        input_handler._pressed_this_frame.add(Action.DEBUG_TOGGLE)
        
        assert input_handler.should_toggle_debug() is True
    
    def test_reset(self, input_handler):
        """Test reset clears all state.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that reset clears held_actions, pressed_this_frame,
        and released_this_frame sets.
        """
        input_handler.held_actions.add(Action.JUMP)
        input_handler._pressed_this_frame.add(Action.MOVE_LEFT)
        input_handler._released_this_frame.add(Action.MOVE_RIGHT)
        
        input_handler.reset()
        
        assert len(input_handler.held_actions) == 0
        assert len(input_handler._pressed_this_frame) == 0
        assert len(input_handler._released_this_frame) == 0
    
    def test_register_callback(self, input_handler):
        """Test registering a callback.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that a registered callback is invoked when its
        associated action is triggered by a key press.
        """
        callback = MagicMock()
        input_handler.register_callback(Action.JUMP, callback)
        
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE
        
        input_handler.process_events([event])
        
        callback.assert_called_once()
    
    def test_callback_not_called_on_release(self, input_handler):
        """Test callback is not called on key release.

        Args:
            input_handler: Pytest fixture providing an InputHandler instance.

        Verifies that callbacks are only triggered on key press events,
        not on key release events.
        """
        callback = MagicMock()
        input_handler.register_callback(Action.JUMP, callback)
        
        # Press and release
        down = MagicMock()
        down.type = pygame.KEYDOWN
        down.key = pygame.K_SPACE
        input_handler.process_events([down])
        
        callback.reset_mock()
        
        up = MagicMock()
        up.type = pygame.KEYUP
        up.key = pygame.K_SPACE
        input_handler.process_events([up])
        
        callback.assert_not_called()
