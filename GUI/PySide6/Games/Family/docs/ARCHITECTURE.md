# Architecture Overview

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py (Entry Point)                   │
│  - Creates QApplication                                         │
│  - Instantiates MainWindow                                      │
│  - Uses config for window size/title                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MainWindow (QWidget)                      │
│  - QListWidget (navigation)   ┃   QStackedWidget (game area)   │
│  - Loads games via game_loader                                  │
│  - Switches between game widgets                                │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    game_loader.py (Dynamic Loading)             │
│  - Scans games/ directory                                       │
│  - Imports modules with GAME_NAME and Game class                │
│  - Filters by config.json enabled list                          │
│  - Returns game metadata + widget classes                       │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ├──────────────┬──────────────┬──────────────┐
                 ▼              ▼              ▼              ▼
         ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
         │  game1.py  │ │  game2.py  │ │  game3.py  │ │  gameN.py  │
         │            │ │            │ │            │ │            │
         │ GAME_NAME  │ │ GAME_NAME  │ │ GAME_NAME  │ │ GAME_NAME  │
         │ Game class │ │ Game class │ │ Game class │ │ Game class │
         └────────────┘ └────────────┘ └────────────┘ └────────────┘
                 │              │              │              │
                 └──────────────┴──────────────┴──────────────┘
                                │
                                ▼
                 ┌──────────────────────────────────────────┐
                 │  Each game accesses configuration:       │
                 │  config.get_game_config("game1")         │
                 └──────────────────────────────────────────┘
```

## Configuration System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Application Layer                        │
│  (main.py, game_loader.py, games/*.py)                         │
└────────────────┬───────────────────────────────┬────────────────┘
                 │                               │
                 ▼                               ▼
┌────────────────────────────────┐  ┌───────────────────────────┐
│   config_manager.py (Singleton)│  │ user_preferences.py       │
│                                │  │ (Singleton)               │
│  - get(key_path, default)      │  │ - High scores             │
│  - get_app_config()            │  │ - Game statistics         │
│  - get_game_config(name)       │  │ - UI preferences          │
│  - get_enabled_games()         │  │ - Achievements            │
│  - update(key, value)          │  │ - Play history            │
│  - save_config()               │  │                           │
│  - reload()                    │  │ Methods:                  │
└────────────────┬───────────────┘  │ - set_high_score()        │
                 │                  │ - record_game_played()    │
                 ▼                  │ - unlock_achievement()    │
┌────────────────────────────────┐  └───────────────┬───────────┘
│       config.json              │                  │
│                                │                  ▼
│  {                             │  ┌───────────────────────────┐
│    "app": {...},               │  │   user_prefs.json         │
│    "games": {                  │  │   (Auto-generated)        │
│      "enabled": [...],         │  │                           │
│      "game1": {...},           │  │  {                        │
│      "game2": {...}            │  │    "high_scores": {...},  │
│    },                          │  │    "game_statistics": ... │
│    "logging": {...}            │  │  }                        │
│  }                             │  │                           │
└────────────────────────────────┘  └───────────────────────────┘
```

## Data Flow: Loading a Game

```
1. User starts app
   └─> main.py creates QApplication
   
2. MainWindow.__init__()
   ├─> config_manager loads config/config.json
   ├─> game_loader.load_games() called
   │   ├─> Scans games/ directory
   │   ├─> For each .py file:
   │   │   ├─> Check if in config.get_enabled_games()
   │   │   ├─> Import module
   │   │   ├─> Get GAME_NAME and Game class
   │   │   └─> Fetch game config from config/config.json
   │   └─> Return list of game metadata
   │
   └─> For each game:
       ├─> Add to QListWidget (navigation)
       └─> Instantiate Game widget and add to QStackedWidget

3. User clicks game in list
   └─> QStackedWidget switches to selected game widget

4. Game widget displays
   ├─> Access config: config.get_game_config("game1")
   ├─> Access user data: user_prefs.get_high_score("game1")
   └─> Render UI with configuration
```

## Plugin Architecture Pattern

```
┌──────────────────────────────────────────────────────────────┐
│                    Core Application                          │
│  (Never needs to know about specific games)                  │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ Plugin Interface:
                         │ - GAME_NAME (str)
                         │ - Game (QWidget subclass)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    Plugin 1         Plugin 2         Plugin 3
    (game1.py)       (game2.py)       (game3.py)
    
    • Self-contained
    • Independently loadable
    • Config-driven
    • Zero coupling to core app
```

## Benefits of This Architecture

### 1. **Separation of Concerns**
- Config files hold settings
- Code files hold logic
- User files hold personal data

### 2. **Scalability**
- Add games without modifying core
- Add settings without changing code
- Users can customize independently

### 3. **Maintainability**
- Single source of truth (config.json)
- Clear boundaries between modules
- Easy to debug (isolated components)

### 4. **Flexibility**
- Enable/disable features via config
- Different configs for different environments
- Runtime configuration updates

### 5. **Professional Standards**
- Follows industry best practices
- Similar to Django/Flask patterns
- Singleton pattern for managers
- Plugin architecture for extensibility

## Comparison to Alternatives

### ❌ Hardcoded Values
```python
class MainWindow:
    def __init__(self):
        self.resize(1000, 600)  # Hard to change!
```

### ✅ Configuration-Driven
```python
class MainWindow:
    def __init__(self):
        width = config.get("app.window_width", 1000)
        height = config.get("app.window_height", 600)
        self.resize(width, height)  # Easy to customize!
```

### ❌ Manual Game Registration
```python
from games.game1 import Game1
from games.game2 import Game2

games = [Game1(), Game2()]  # Must edit when adding games
```

### ✅ Automatic Discovery
```python
games = load_games()  # Automatically finds all enabled games
```

## Extension Points

The architecture makes it easy to add:

1. **Themes**: Add theme engine reading from config
2. **Localization**: Load language strings from config
3. **Multiplayer**: Add network settings to config
4. **Analytics**: Track usage via user_preferences
5. **Achievements**: Already supported in user_preferences
6. **Cloud Sync**: Sync user_prefs.json to cloud storage
7. **Modding**: Load community-created games from mods/
8. **A/B Testing**: Use config to enable experimental features

## File Responsibilities

| File | Purpose | Modifiable |
|------|---------|------------|
| `main.py` | App entry point | Rarely |
| `game_loader.py` | Plugin discovery | Rarely |
| `config/config_manager.py` | Config API | Rarely |
| `config/user_preferences.py` | User data API | Rarely |
| `config/config.json` | App settings | **Often** |
| `user_prefs.json` | User data | Auto |
| `games/*.py` | Game plugins | **Per game** |
| `docs/*.md` | Documentation | As needed |

## Summary

This architecture provides:
- **Plugin system** for games
- **Configuration management** for settings
- **User preferences** for personal data
- **Clean separation** of concerns
- **Professional patterns** used in production apps

Perfect for:
- Educational projects
- Prototypes
- Small to medium applications
- Systems requiring frequent configuration changes
