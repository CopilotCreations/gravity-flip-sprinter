# Gravity Flip Runner - User Guide

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Controls](#controls)
5. [Game Mechanics](#game-mechanics)
6. [Command-Line Options](#command-line-options)
7. [Configuration](#configuration)
8. [Creating Custom Levels](#creating-custom-levels)
9. [Troubleshooting](#troubleshooting)

## Overview

Gravity Flip Runner is a 2D side-scrolling platformer where you control a character who can flip gravity at will. Navigate through challenging levels filled with platforms, enemies, and hazards by running on both the floor and ceiling!

### Key Features

- **Gravity Flip Mechanic**: Press a button to instantly reverse gravity
- **Smooth Physics**: Responsive controls and natural movement
- **Enemies and Hazards**: Patrol enemies and static hazards that respond to gravity
- **Moving Platforms**: Dynamic level elements for added challenge
- **Modular Design**: Easy to extend with new features and levels

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Steps

1. **Clone or download the project**:
   ```bash
   cd gravity-flip-sprinter
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

Run the game with default settings:

```bash
python run.py
```

Or with Python 3 explicitly:

```bash
python3 run.py
```

## Controls

### Default Key Bindings

| Action | Primary Key | Alternative Key |
|--------|-------------|-----------------|
| Move Left | ← (Left Arrow) | A |
| Move Right | → (Right Arrow) | D |
| Jump | Space | W |
| Flip Gravity | ↑ (Up Arrow) | F |
| Pause | Escape | P |
| Restart | R | - |
| Quit | Q | - |
| Toggle Debug | F3 | - |

### Control Tips

- **Movement**: Hold left or right to move continuously
- **Jumping**: Press jump while on the ground (floor or ceiling)
- **Gravity Flip**: Can be performed at any time, even mid-air
- **Combining Moves**: Jump and flip gravity together for maximum height

## Game Mechanics

### Gravity System

The core mechanic of Gravity Flip Runner is the ability to flip gravity:

```
Normal Gravity (↓)          Inverted Gravity (↑)
                           
    ▄▄▄▄                        ▀▀▀▀  
   █    █  ←Player              █    █  ←Player
   ▀▀▀▀                        ▄▄▄▄
                           
═══════════════            ═══════════════
    Ground                      Ceiling
```

When you flip gravity:
- Your character immediately starts falling in the opposite direction
- Enemies are also affected and will fall accordingly
- Special "gravity platforms" will fall in the new gravity direction
- You can flip gravity again at any time

### Jumping

- You can only jump when standing on a surface
- Jump direction is opposite to current gravity direction
- Jump height is affected by gravity strength

### Enemies

Enemies patrol back and forth on platforms:
- They damage you on contact
- They respond to gravity flips (they'll fall too!)
- Use gravity flips strategically to move enemies away

### Hazards

Hazards are static obstacles (like spikes):
- Instant damage on contact
- Often placed at gaps or dangerous areas
- Cannot be destroyed or moved

### Lives and Score

- You start with 3 lives
- Lose a life by:
  - Touching an enemy
  - Touching a hazard
  - Falling out of bounds
- Score increases based on distance traveled
- Game Over when all lives are lost

## Command-Line Options

```bash
python run.py [OPTIONS]
```

### Available Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--width` | `-W` | int | 800 | Window width in pixels |
| `--height` | `-H` | int | 600 | Window height in pixels |
| `--fps` | - | int | 60 | Target frames per second |
| `--speed` | - | float | 5.0 | Player movement speed |
| `--gravity` | - | float | 0.8 | Gravity strength |
| `--jump` | - | float | 15.0 | Jump force |
| `--debug` | `-d` | flag | false | Enable debug mode |

### Examples

**Fullscreen-ish (1920x1080)**:
```bash
python run.py --width 1920 --height 1080
```

**Slower, easier gameplay**:
```bash
python run.py --speed 3.0 --gravity 0.5 --jump 12.0
```

**Debug mode** (shows hitboxes and debug info):
```bash
python run.py --debug
```

**Fast and challenging**:
```bash
python run.py --speed 8.0 --gravity 1.2 --jump 18.0
```

## Configuration

### Environment Variables

You can configure the game using environment variables. Copy `.env.example` to `.env` and modify:

```bash
# Window settings
WINDOW_WIDTH=800
WINDOW_HEIGHT=600
FPS=60

# Player settings
PLAYER_SPEED=5.0
PLAYER_JUMP_FORCE=15.0

# Physics settings
GRAVITY_STRENGTH=0.8

# Debug settings
DEBUG_MODE=false
SHOW_HITBOXES=false
```

### Priority Order

Configuration is applied in this order (later overrides earlier):
1. Default values
2. Environment variables
3. Command-line arguments

## Creating Custom Levels

### Level JSON Format

Levels are stored as JSON files with the following structure:

```json
{
  "bounds": [0, 2000, 0, 600],
  "spawn": [100, 400],
  "platforms": [
    {
      "type": "static",
      "x": 0,
      "y": 550,
      "width": 500,
      "height": 50
    },
    {
      "type": "moving",
      "x": 600,
      "y": 400,
      "width": 100,
      "height": 25,
      "end_x": 800,
      "end_y": 400,
      "speed": 2.0
    },
    {
      "type": "gravity",
      "x": 1000,
      "y": 300,
      "width": 150,
      "height": 25
    }
  ],
  "enemies": [
    {
      "x": 300,
      "y": 500,
      "width": 32,
      "height": 32,
      "patrol_distance": 100,
      "speed": 2.0
    }
  ],
  "hazards": [
    {
      "x": 500,
      "y": 570,
      "width": 80,
      "height": 30
    }
  ]
}
```

### Level Properties

#### Bounds
- `[min_x, max_x, min_y, max_y]`
- Defines the level boundaries
- Player dies if they fall outside

#### Spawn
- `[x, y]`
- Player starting position
- Also used for respawning after death

#### Platform Types

| Type | Description | Additional Properties |
|------|-------------|----------------------|
| `static` | Fixed platform | None |
| `moving` | Moving platform | `end_x`, `end_y`, `speed` |
| `gravity` | Falls on gravity flip | None |

### Level Design Tips

1. **Always include ceiling platforms** - Players need somewhere to land with inverted gravity
2. **Balance normal and inverted sections** - Make both directions viable
3. **Use moving platforms for timing challenges** - They add dynamic gameplay
4. **Place hazards at gaps** - Creates risk/reward decisions
5. **Test with different gravity timings** - Ensure all paths are possible

## Troubleshooting

### Common Issues

#### "pygame not found" or import errors
```bash
pip install pygame
```
Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

#### Black screen or no display
Try running with SDL dummy driver for diagnosis:
```bash
SDL_VIDEODRIVER=dummy python run.py
```

#### Game runs too slow
- Lower the resolution: `python run.py -W 640 -H 480`
- Reduce FPS target: `python run.py --fps 30`

#### Game is too hard
- Reduce player speed: `python run.py --speed 3.0`
- Lower gravity: `python run.py --gravity 0.5`
- Increase jump power: `python run.py --jump 18.0`

#### Game is too easy
- Increase speed: `python run.py --speed 8.0`
- Increase gravity: `python run.py --gravity 1.2`

### Debug Mode

Enable debug mode to see:
- Player position and velocity
- Collision hitboxes
- Ground state indicator

```bash
python run.py --debug
```

Or press F3 during gameplay to toggle.

### Getting Help

1. Check the [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
2. Review the [SUGGESTIONS.md](SUGGESTIONS.md) for known limitations
3. Run tests to verify installation: `pytest tests/ -v`

## Tips and Tricks

1. **Master the double-flip**: Flip gravity twice quickly to fake out enemies
2. **Use ceiling as escape**: Flip to the ceiling to avoid ground hazards
3. **Timing is everything**: Learn enemy patrol patterns
4. **Momentum matters**: You keep horizontal speed during gravity flips
5. **Watch the gravity indicator**: Small arrow shows current gravity direction
