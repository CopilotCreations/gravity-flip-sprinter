"""
Pytest configuration and shared fixtures.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'


@pytest.fixture
def config():
    """Provide a default GameConfig for tests."""
    from src.config import GameConfig
    return GameConfig()


@pytest.fixture
def custom_config():
    """Provide a custom GameConfig for tests."""
    from src.config import GameConfig
    return GameConfig(
        window_width=1024,
        window_height=768,
        fps=30,
        player_speed=10.0,
        gravity_strength=1.0,
        debug_mode=True,
        show_hitboxes=True,
    )


@pytest.fixture
def player(config):
    """Provide a Player instance for tests."""
    from src.player import Player
    return Player(100, 300, config)


@pytest.fixture
def platform(config):
    """Provide a Platform instance for tests."""
    from src.platforms import Platform
    return Platform(0, 500, 200, 50, config=config)


@pytest.fixture
def moving_platform(config):
    """Provide a MovingPlatform instance for tests."""
    from src.platforms import MovingPlatform
    return MovingPlatform(0, 300, 100, 25, end_x=200, end_y=300, speed=2.0, config=config)


@pytest.fixture
def gravity_platform(config):
    """Provide a GravityPlatform instance for tests."""
    from src.platforms import GravityPlatform
    return GravityPlatform(100, 200, 100, 25, config=config)


@pytest.fixture
def enemy(config):
    """Provide an Enemy instance for tests."""
    from src.enemies import Enemy
    return Enemy(200, 450, patrol_distance=100, config=config)


@pytest.fixture
def hazard(config):
    """Provide a Hazard instance for tests."""
    from src.enemies import Hazard
    return Hazard(300, 550, 50, 20, config=config)


@pytest.fixture
def level(config):
    """Provide a Level instance for tests."""
    from src.level import Level
    return Level(config)


@pytest.fixture
def demo_level(config):
    """Provide a demo Level with content for tests."""
    from src.level import LevelLoader
    return LevelLoader.create_demo_level(config)


@pytest.fixture
def input_handler():
    """Provide an InputHandler instance for tests."""
    from src.input_handler import InputHandler
    return InputHandler()
