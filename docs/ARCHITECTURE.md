# Gravity Flip Runner - Architecture

## Overview

Gravity Flip Runner is a 2D side-scrolling platformer game built with Python and Pygame. The game features a unique gravity-flip mechanic where players can reverse gravity at any time, allowing them to navigate through levels by running on both floors and ceilings.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              run.py                                      │
│                         (Entry Point)                                    │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              Game                                        │
│                    (Main Game Loop & State)                              │
│  ┌─────────────┬──────────────┬──────────────┬───────────────────────┐  │
│  │  Player     │   Level      │   Renderer   │   InputHandler        │  │
│  │             │              │              │                        │  │
│  │ - Position  │ - Platforms  │ - Screen     │ - Key Bindings        │  │
│  │ - Velocity  │ - Enemies    │ - Drawing    │ - Action Mapping      │  │
│  │ - Gravity   │ - Hazards    │ - UI         │ - Callbacks           │  │
│  │ - Collisions│ - Camera     │ - Background │                        │  │
│  └─────────────┴──────────────┴──────────────┴───────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            GameConfig                                    │
│                    (Centralized Configuration)                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Module Descriptions

### 1. `run.py` - Entry Point

The main entry point for the game. Handles:
- Command-line argument parsing
- Configuration creation from CLI args
- Game instantiation and execution

**Key Features:**
- Configurable window size, FPS, player speed, gravity strength
- Debug mode flag for development
- Clean separation of concerns

### 2. `src/game.py` - Game Loop

The core game module managing the main game loop and state transitions.

**Classes:**
- `GameState` (Enum): RUNNING, PAUSED, GAME_OVER
- `Game`: Main game class

**Responsibilities:**
- Pygame initialization
- Frame rate control
- Event polling and distribution
- Game state management (running, paused, game over)
- Collision detection coordination
- Score tracking
- Life management

**Game Loop Flow:**
```
┌─────────────────┐
│  Handle Events  │◄────────────────────┐
└────────┬────────┘                     │
         ▼                              │
┌─────────────────┐                     │
│  Player Input   │                     │
└────────┬────────┘                     │
         ▼                              │
┌─────────────────┐                     │
│    Update       │                     │
│  - Physics      │                     │
│  - Collisions   │                     │
│  - Camera       │                     │
└────────┬────────┘                     │
         ▼                              │
┌─────────────────┐                     │
│    Render       │                     │
└────────┬────────┘                     │
         ▼                              │
┌─────────────────┐                     │
│  Frame Delay    │─────────────────────┘
└─────────────────┘
```

### 3. `src/player.py` - Player Character

Manages the player character state and physics.

**Class:** `Player`

**Attributes:**
- `x, y`: Position coordinates
- `dx, dy`: Velocity components
- `gravity_direction`: 1 (normal) or -1 (inverted)
- `on_ground`: Grounded state flag
- `spawn_x, spawn_y`: Respawn position

**Key Methods:**
- `move(direction)`: Horizontal movement
- `jump()`: Jump if grounded
- `flip_gravity()`: Toggle gravity direction
- `apply_gravity()`: Apply gravitational acceleration
- `update(platforms)`: Physics update with collision detection
- `reset()`: Return to spawn position

**Physics Model:**
```
                    ▲ -dy (inverted gravity)
                    │
        ◄───────────┼───────────►
       -dx          │           +dx
                    │
                    ▼ +dy (normal gravity)
```

### 4. `src/platforms.py` - Platform System

Defines various platform types for level construction.

**Classes:**

#### `Platform` (Base)
- Static platforms
- Basic collision rectangle
- Configurable color

#### `MovingPlatform` (extends Platform)
- Moves between two points
- Linear interpolation movement
- Reverses at endpoints
- Provides velocity for player riding

#### `GravityPlatform` (extends Platform)
- Affected by gravity flips
- Falls when gravity changes
- Can be reset to original position

**Platform Hierarchy:**
```
        Platform
           │
     ┌─────┴─────┐
     ▼           ▼
MovingPlatform  GravityPlatform
```

### 5. `src/enemies.py` - Enemies and Hazards

Contains enemy AI and hazard definitions.

**Classes:**

#### `Enemy`
- Patrols along platforms
- Responds to gravity changes
- Simple back-and-forth AI
- Configurable patrol distance and speed

**Enemy Behavior:**
```
Start ◄──────────────────────► End
        patrol_distance
```

#### `Hazard`
- Static damage zones
- Instant death on contact
- Typically placed at gaps or obstacles

### 6. `src/level.py` - Level Management

Handles level loading, object management, and camera control.

**Classes:**

#### `Level`
- Container for all level objects
- Camera following logic
- Gravity propagation to objects
- Bounds checking

#### `LevelLoader`
- Static methods for level creation
- Demo level generator
- JSON save/load functionality

**Level Structure:**
```json
{
  "bounds": [min_x, max_x, min_y, max_y],
  "spawn": [x, y],
  "platforms": [...],
  "enemies": [...],
  "hazards": [...]
}
```

### 7. `src/renderer.py` - Rendering System

Handles all visual output.

**Class:** `Renderer`

**Features:**
- Parallax background layers
- Player rendering with direction indicator
- Platform rendering with type-specific styling
- Enemy rendering with animated eyes
- Hazard rendering with spike patterns
- UI overlay (lives, score, gravity indicator)
- Debug hitbox visualization
- Game state overlays (pause, game over)

**Rendering Order:**
1. Background (parallax layers)
2. Platforms
3. Hazards
4. Enemies
5. Player
6. UI
7. State overlays

### 8. `src/input_handler.py` - Input System

Maps keyboard input to game actions.

**Classes:**

#### `Action` (Enum)
Defines all possible player actions:
- MOVE_LEFT, MOVE_RIGHT
- JUMP
- FLIP_GRAVITY
- PAUSE, RESTART, QUIT
- DEBUG_TOGGLE

#### `KeyBinding`
Associates primary and secondary keys to actions.

#### `InputHandler`
- Processes pygame events
- Tracks held, pressed, and released states
- Supports action callbacks
- Provides query methods for game logic

**Default Key Bindings:**
| Action | Primary | Secondary |
|--------|---------|-----------|
| Move Left | ← | A |
| Move Right | → | D |
| Jump | Space | W |
| Flip Gravity | ↑ | F |
| Pause | Escape | P |
| Restart | R | - |
| Quit | Q | - |
| Debug | F3 | - |

### 9. `src/config.py` - Configuration

Centralized game settings.

**Class:** `GameConfig` (dataclass)

**Categories:**
- Window settings (size, FPS, title)
- Player settings (speed, jump force, dimensions)
- Physics settings (gravity, max fall speed)
- Debug settings
- Color definitions

**Configuration Sources:**
1. Default values
2. Environment variables
3. Command-line arguments

## Data Flow

### Game Loop Data Flow
```
InputHandler ──► Player ──► Level ──► Renderer
     │              │          │
     │              │          │
     ▼              ▼          ▼
  Actions      Position    Camera
              Velocity    Objects
```

### Collision System
```
Player.update()
     │
     ├──► Horizontal Movement
     │         │
     │         ▼
     │    Check Platform Collisions
     │         │
     │         ▼
     │    Resolve (push back)
     │
     ├──► Vertical Movement
     │         │
     │         ▼
     │    Check Platform Collisions
     │         │
     │         ▼
     │    Resolve + Set on_ground
     │
     └──► Game._check_collisions()
               │
               ├──► Enemy collisions
               ├──► Hazard collisions
               └──► Bounds checking
```

## Design Patterns Used

### 1. Dataclass Pattern
Used for `GameConfig` to provide clean, immutable configuration objects.

### 2. Factory Pattern
`LevelLoader` provides factory methods for creating levels from various sources.

### 3. Component Pattern
Game entities (Player, Enemy, Platform) are composed of position, physics, and rendering properties.

### 4. Observer Pattern (Callback System)
`InputHandler` supports registering callbacks for action events.

### 5. State Machine
`GameState` enum with state-specific behavior in `Game` class.

## Extension Points

### Adding New Platform Types
1. Create a new class extending `Platform`
2. Override `update()` for custom behavior
3. Add rendering logic in `Renderer.draw_platform()`
4. Add JSON loading support in `LevelLoader`

### Adding New Enemy Types
1. Create a new class extending `Enemy`
2. Override AI methods
3. Add rendering logic in `Renderer.draw_enemy()`

### Adding New Game Modes
1. Add new state to `GameState` enum
2. Handle state transitions in `Game.handle_events()`
3. Add state-specific update logic
4. Add state-specific rendering overlays

## Performance Considerations

1. **Off-screen culling**: Renderer skips objects outside viewport
2. **Pygame clock**: Maintains consistent frame rate
3. **Efficient collision detection**: Simple AABB (Axis-Aligned Bounding Box) checks
4. **Camera-relative rendering**: Only visible objects are drawn

## Testing Strategy

- **Unit tests**: Individual module testing with mocks
- **Fixtures**: Shared test data in `conftest.py`
- **Coverage target**: 75%+ code coverage
- **Headless testing**: SDL dummy driver for CI/CD
