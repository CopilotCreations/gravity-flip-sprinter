#!/usr/bin/env python3
"""
Gravity Flip Runner - Entry Point

A 2D side-scrolling game with gravity flip mechanics.
Run this file to start the game.
"""

import sys
import argparse
import os

# Add the project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import GameConfig
from src.game import Game


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gravity Flip Runner - A 2D side-scrolling platformer with gravity mechanics"
    )
    
    parser.add_argument(
        "--width", "-W",
        type=int,
        default=800,
        help="Window width (default: 800)"
    )
    
    parser.add_argument(
        "--height", "-H",
        type=int,
        default=600,
        help="Window height (default: 600)"
    )
    
    parser.add_argument(
        "--fps",
        type=int,
        default=60,
        help="Target frames per second (default: 60)"
    )
    
    parser.add_argument(
        "--speed",
        type=float,
        default=5.0,
        help="Player movement speed (default: 5.0)"
    )
    
    parser.add_argument(
        "--gravity",
        type=float,
        default=0.8,
        help="Gravity strength (default: 0.8)"
    )
    
    parser.add_argument(
        "--jump",
        type=float,
        default=15.0,
        help="Jump force (default: 15.0)"
    )
    
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug mode (shows hitboxes and debug info)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the game."""
    args = parse_args()
    
    # Create configuration from command line args
    config = GameConfig(
        window_width=args.width,
        window_height=args.height,
        fps=args.fps,
        player_speed=args.speed,
        gravity_strength=args.gravity,
        player_jump_force=args.jump,
        debug_mode=args.debug,
        show_hitboxes=args.debug,
    )
    
    # Create and run game
    game = Game(config)
    game.run()


if __name__ == "__main__":
    main()
