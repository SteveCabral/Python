# Quick Reference: Configuration System

## File Structure
```
GUI/PySide6/Games/Family/
├── config/
│   ├── config.json          # App & game settings
│   ├── config_manager.py    # Configuration singleton
│   └── user_preferences.py  # User preferences manager
├── docs/
│   ├── ARCHITECTURE.md      # System architecture
│   ├── CONFIGURATION.md     # Detailed config guide
│   └── QUICKSTART.md        # This file
├── games/
│   └── game1.py             # Accesses game-specific config
├── players/                 # Players screen (select active player)
│   └── players_widget.py
├── scores/                  # Scoring + leaderboards
│   ├── score_manager.py
│   └── leaderboard_widget.py
├── tests/                   # Runnable test/demo scripts
│   ├── test_config.py
│   ├── test_themes.py
│   └── test_scores.py
├── user_prefs.json          # UI/user state (auto-generated)
├── scores.json              # Scores + players (auto-generated)
├── main.py                  # Entry point
└── game_loader.py           # Filters games by config
```

## Common Tasks

### 1. Change Window Size
Edit `config/config.json`:
```json
{
  "app": {
    "window_width": 1200,
    "window_height": 800
  }
}
```

### 2. Enable/Disable Games
Edit `config/config.json`:
```json
{
  "games": {
    "enabled": ["game1", "game3"]  // game2 won't load
  }
}
```

### 3. Configure a Game
Edit `config/config.json`:
```json
{
  "games": {
    "game1": {
      "display_name": "Super Word Game",
      "difficulty": "hard",
      "time_limit": 30
    }
  }
}
```

### 4. Access Config in Code
```python
from config.config_manager import config

# Get any setting with default
value = config.get("app.window_width", 1000)

# Get game-specific config
game_cfg = config.get_game_config("game1")
difficulty = game_cfg.get("difficulty", "easy")
```

### 5. User Preferences (Optional)
```python
from config.user_preferences import user_prefs

"""UserPreferences is optional.

The main app currently uses user_prefs primarily for lightweight UI/user state
(e.g., which player is currently selected on the Players screen).
"""

# Example: store/retrieve a simple preference
user_prefs.set("ui_preferences.sound_enabled", True)
enabled = user_prefs.get("ui_preferences.sound_enabled", True)
```

### 6. Update Config at Runtime
```python
from config.config_manager import config

# Change and save
config.update("app.theme", "dark")
config.save_config()
```

## Adding a New Game

### Step 1: Create game file
Create `games/my_game.py`:
```python
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from config.config_manager import config

GAME_NAME = "My Game"

class Game(QWidget):
    def __init__(self, game_config=None, score_reporter=None, game_id=None):
        super().__init__()

        # Access config (either injected by the loader, or fetched directly)
        cfg = game_config or config.get_game_config("my_game")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Welcome to {cfg.get('display_name')}!"))

        # Optional: report a score when a round finishes
        if score_reporter and game_id:
            score_reporter(game_id, 10, meta={"note": "example"})
```

### Step 2: Add to config/config.json
```json
{
  "games": {
    "enabled": ["game1", "game2", "game3", "my_game"],
    "my_game": {
      "display_name": "My Awesome Game",
      "description": "A fun new game",
      "difficulty": "medium",
      "max_score": 500,
      "time_limit": 120
    }
  }
}
```

### Step 3: Run
```powershell
& C:\PythonVenv\py311\Scripts\python.exe main.py
```
Your game appears in the list automatically!

## Configuration Files

### config/config.json (App Settings)
- Window dimensions and title
- Navigation settings
- Game configurations
- Feature flags
- Logging settings

**✓ Commit to git** - shared across all users

### user_prefs.json (User Data)
- UI/user state (e.g., current player selection)
- Optional extension patterns (if you choose to store more user-specific data)

**✗ Don't commit** - personal to each user

## Best Practices

1. **Always use defaults**: `config.get("key", default_value)`
2. **Validate user input**: Check types and ranges
3. **Document settings**: Add comments in JSON (or use schema)
4. **Version config**: Track changes in git
5. **Separate concerns**: App config vs. user preferences
6. **Test changes**: Run `python -m tests.test_config` after editing

  Prefer running tests as modules:
  - `python -m tests.test_config`

## Troubleshooting

### Config not loading?
```python
from config.config_manager import config
config.reload()  # Force reload
```

### Reset user preferences?
```python
from config.user_preferences import user_prefs
user_prefs.reset_all()  # Back to defaults
```

### Validate config structure?
```powershell
& C:\PythonVenv\py311\Scripts\python.exe -m json.tool config/config.json  # Check JSON syntax
```

## Advanced Features

See `config_examples.py` for:
- Environment-specific configs (dev/prod)
- Schema validation
- Hot-reload during development
- Feature flags
- Configuration inheritance

## Testing

```powershell
# Test configuration system
& C:\PythonVenv\py311\Scripts\python.exe -m tests.test_config

# Test user preferences
& C:\PythonVenv\py311\Scripts\python.exe config/user_preferences.py

# Test scoring system
& C:\PythonVenv\py311\Scripts\python.exe -m tests.test_scores
```

## Documentation

- Full guide: `CONFIGURATION.md`
- Usage examples: `../config_examples.py`
- Project README: `../README.md`
