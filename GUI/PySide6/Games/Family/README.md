# Plugin-Like Architecture for Game Modules (Professional / Scalable)

This design lets you:

- Add new games simply by adding new Python files
- Automatically load all game modules at runtime
- Keep each game isolated (like plugins)
- Avoid modifying the main app when adding Game 11, Game 12, etc.
- Configure app and game settings through a centralized JSON configuration file
- Switch between professional light and dark themes instantly

This is the same structure used in modular Qt applications and game engines.

## Project Structure

```
word_games/
    main.py                 # Entry point
    game_loader.py          # Dynamic game module loader
    config/
        config.json         # Configuration file (app & game settings)
        config_manager.py   # Configuration management singleton
        user_preferences.py # User data and preferences
    themes/
        theme_manager.py    # Theme management system
        dark.json           # Dark theme colors and styles
        light.json          # Light theme colors and styles
    games/
        __init__.py
        game1.py
        game2.py
        game3.py
    docs/
        ARCHITECTURE.md     # System architecture documentation
        CONFIGURATION.md    # Detailed configuration guide
        THEMES.md           # Theme system guide
        QUICKSTART.md       # Quick reference guide
```

## Configuration System

The application uses a professional JSON-based configuration system that separates settings from code.

### config.json Structure

```json
{
  "app": {
    "title": "Family Game Collection",
    "window_width": 1000,
    "window_height": 600,
    "nav_list_width": 200,
    "theme": "dark"
  },
  "games": {
    "enabled": ["game1", "game2", "game3"],
    "game1": {
      "display_name": "Word Scramble",
      "description": "Unscramble the letters to form words",
      "difficulty": "easy",
      "max_score": 100,
      "time_limit": 60
    }
  },
  "logging": {
    "enabled": true,
    "level": "INFO",
    "log_file": "game_app.log"
  }
}
```

### Using Configuration in Code

```python
from config.config_manager import config

# Get app-level settings
window_width = config.get("app.window_width", 1000)

# Get game-specific settings
game_config = config.get_game_config("game1")
difficulty = game_config.get("difficulty", "easy")

# Check if game is enabled
if config.is_game_enabled("game1"):
    # Load game
    pass
```

### Benefits

- **Centralized Settings**: All configuration in one place
- **No Code Changes**: Modify behavior without editing Python files
- **Easy Deployment**: Different configs for dev/prod environments
- **Runtime Flexibility**: Enable/disable games without recompiling
- **Type Safety**: ConfigManager provides type hints and defaults

## Theme System

The application supports professional light and dark themes with instant switching.

### Switching Themes

Use the theme buttons in the top bar to switch between light and dark modes. The theme preference is automatically saved.

### Theme Features

- **40+ Semantic Colors**: Named colors like `primary`, `background`, `text_primary`
- **Consistent Styling**: All controls automatically themed
- **Professional Palettes**: Carefully chosen color combinations
- **Font System**: Consistent typography across the app
- **Spacing System**: Standardized spacing values

### Using Themes in Code

```python
from themes.theme_manager import theme_manager

# Get a color
color = theme_manager.get_color("primary")

# Apply property-based styling
label = QLabel("Title")
label.setProperty("title", True)  # Uses theme's title styling

button = QPushButton("Action")
button.setProperty("primary", True)  # Primary button styling
```

For complete theme documentation, see [docs/THEMES.md](docs/THEMES.md).

## Adding a New Game

1. Create `games/game4.py`:
```python
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from config.config_manager import config

GAME_NAME = "Game Four"

class Game(QWidget):
  def __init__(self, game_config=None):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Access game config
    game_config = game_config or config.get_game_config("game4")
        layout.addWidget(QLabel(game_config.get("description", "Game 4")))
```

2. Add to `config/config.json`:
```json
{
  "games": {
    "enabled": ["game1", "game2", "game3", "game4"],
    "game4": {
      "display_name": "New Game",
      "description": "A brand new game",
      "difficulty": "medium"
    }
  }
}
```

3. Run `main.py` — the new game appears automatically!

## Documentation

For detailed information, see:
- **[docs/INDEX.md](docs/INDEX.md)** - Documentation index and navigation
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Quick reference for common tasks
- **[docs/CONFIGURATION.md](docs/CONFIGURATION.md)** - Comprehensive configuration guide
- **[docs/THEMES.md](docs/THEMES.md)** - Complete theme system documentation
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design patterns

## Getting Started

Run the application:
```powershell
& C:\PythonVenv\py311\Scripts\python.exe main.py
```

Test the configuration system:
```powershell
& C:\PythonVenv\py311\Scripts\python.exe test_config.py
```

Test the theme system:
```powershell
& C:\PythonVenv\py311\Scripts\python.exe test_themes.py
```

See advanced examples:
```powershell
& C:\PythonVenv\py311\Scripts\python.exe config_examples.py
```
