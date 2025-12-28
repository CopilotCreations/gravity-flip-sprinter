# Gravity Flip Runner

A 2D side-scrolling platformer with gravity flip mechanics built with Python and Pygame.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Tests](https://img.shields.io/badge/tests-179%20passed-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)

## Overview

Gravity Flip Runner is a unique platformer where players can flip gravity at will, allowing them to run on both floors and ceilings. Navigate through challenging levels filled with platforms, enemies, and hazards!

### Key Features

- 🔄 **Gravity Flip Mechanic**: Instantly reverse gravity at any time
- 🏃 **Smooth Physics**: Responsive controls with natural movement feel
- 👾 **Dynamic Enemies**: Patrol enemies that respond to gravity changes
- 🔧 **Modular Design**: Easy to extend with new features and levels
- 🎮 **Configurable**: Adjust speed, gravity, window size, and more

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd gravity-flip-sprinter

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Game

```bash
python run.py
```

### Controls

| Action | Key |
|--------|-----|
| Move Left/Right | Arrow Keys or A/D |
| Jump | Space or W |
| Flip Gravity | Up Arrow or F |
| Pause | Escape or P |
| Restart | R |
| Quit | Q |
| Toggle Debug | F3 |

## Project Structure

```
gravity-flip-sprinter/
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment configuration
├── .gitignore             # Git ignore patterns
│
├── .github/workflows/     # CI/CD pipeline
│   └── ci.yml             # GitHub Actions workflow
│
├── src/                   # Source code
│   ├── __init__.py
│   ├── config.py          # Game configuration
│   ├── game.py            # Main game loop
│   ├── player.py          # Player mechanics
│   ├── platforms.py       # Platform types
│   ├── enemies.py         # Enemies and hazards
│   ├── level.py           # Level loading/management
│   ├── renderer.py        # Rendering system
│   └── input_handler.py   # Input management
│
├── tests/                 # Test suite
│   ├── conftest.py        # Shared fixtures
│   ├── test_config.py
│   ├── test_player.py
│   ├── test_platforms.py
│   ├── test_enemies.py
│   ├── test_level.py
│   ├── test_input_handler.py
│   ├── test_game.py
│   └── test_renderer.py
│
└── docs/                  # Documentation
    ├── ARCHITECTURE.md    # System architecture
    ├── USAGE.md           # User guide
    └── SUGGESTIONS.md     # Future improvements
```

## Configuration

### Command-Line Options

```bash
python run.py --help

Options:
  --width, -W     Window width (default: 800)
  --height, -H    Window height (default: 600)
  --fps           Target FPS (default: 60)
  --speed         Player speed (default: 5.0)
  --gravity       Gravity strength (default: 0.8)
  --jump          Jump force (default: 15.0)
  --debug, -d     Enable debug mode
```

### Examples

```bash
# Full HD window
python run.py --width 1920 --height 1080

# Easier gameplay
python run.py --speed 3.0 --gravity 0.5

# Debug mode with hitboxes
python run.py --debug
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_player.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/ run.py

# Sort imports
isort src/ tests/ run.py

# Lint
flake8 src/ tests/ run.py
```

## Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)**: System design and module descriptions
- **[User Guide](docs/USAGE.md)**: Complete usage instructions and tips
- **[Suggestions](docs/SUGGESTIONS.md)**: Ideas for future improvements

## Game Mechanics

### Gravity System

When you flip gravity:
- Your character falls in the opposite direction
- Enemies are affected and will fall accordingly
- Special platforms may fall in the new gravity direction
- You can flip gravity again at any time (even mid-air!)

### Tips

1. **Master the double-flip**: Flip gravity twice quickly to fake out enemies
2. **Use ceiling as escape**: Flip to the ceiling to avoid ground hazards
3. **Timing is everything**: Learn enemy patrol patterns
4. **Momentum matters**: You keep horizontal speed during gravity flips

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest tests/ -v`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request
