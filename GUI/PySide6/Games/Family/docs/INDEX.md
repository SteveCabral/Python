# Documentation Index

Welcome to the Family Game Collection documentation!

## Quick Start

New to the project? Start here:
- **[../README.md](../README.md)** - Project overview and basic usage
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference for common tasks

## In-Depth Guides

- **[CONFIGURATION.md](CONFIGURATION.md)** - Comprehensive configuration system guide
  - Understanding config.json structure
  - Configuration manager API
  - User preferences system
  - Usage examples and patterns
  
- **[THEMES.md](THEMES.md)** - Theme system guide
  - Dark and light theme support
  - Color palette definitions
  - Applying themes to widgets
  - Creating custom themes
  
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design patterns
  - Component diagrams
  - Plugin architecture
  - Data flow visualization
  - Professional patterns and best practices

- **[SCORING.md](SCORING.md)** - Scoring & leaderboards
  - Per-game best scores
  - Overall leaderboard (sum of best-per-game)

- **[MIGRATION.md](MIGRATION.md)** - Folder reorganization notes
  - What moved and why
  - Pointers to updated imports and docs

## File Structure

```
Family/
├── config/                  # Configuration files
│   ├── __init__.py          # Package exports
│   ├── config.json         # App and game settings
│   ├── config_manager.py   # Configuration API
│   └── user_preferences.py # User data manager
├── themes/                  # Theme system
│   ├── __init__.py          # Package exports
│   ├── theme_manager.py    # Theme API
│   ├── dark.json           # Dark theme
│   └── light.json          # Light theme
├── docs/                    # Documentation (you are here)
│   ├── INDEX.md            # This file
│   ├── QUICKSTART.md       # Quick reference
│   ├── CONFIGURATION.md    # Config guide
│   ├── THEMES.md           # Theme guide
│   ├── ARCHITECTURE.md     # Architecture guide
│   └── MIGRATION.md        # Folder reorganization notes
├── games/                   # Game plugins
│   ├── __init__.py
│   ├── game1.py
│   ├── game2.py
│   └── game3.py
├── players/                 # Players screen (select active player)
│   ├── __init__.py
│   └── players_widget.py
├── scores/                  # Scoring & leaderboards
│   ├── __init__.py
│   ├── score_manager.py
│   └── leaderboard_widget.py
├── tests/                   # Runnable test/demo scripts
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_themes.py
│   └── test_scores.py
├── main.py                  # Application entry point
├── game_loader.py           # Dynamic game loader
├── config_examples.py       # Advanced config examples
├── user_prefs.json          # Auto-generated UI/user state
└── scores.json              # Auto-generated scores + players
```

## Development Guides

### Adding a New Game

See the [README.md](../README.md#adding-a-new-game) section for step-by-step instructions.

Quick summary:
1. Create `games/your_game.py` with `GAME_NAME` and `Game` class
2. Add configuration to `config/config.json`
3. Run - the game appears automatically!

### Modifying Configuration

See [QUICKSTART.md](QUICKSTART.md#common-tasks) for common configuration tasks:
- Changing window size
- Enabling/disabling games
- Configuring game settings
- Accessing config in code

### Understanding the System

See [ARCHITECTURE.md](ARCHITECTURE.md) for:
- How components work together
- Plugin loading mechanism
- Configuration system design
- Extension points

## Testing

```powershell
# Test configuration system
& C:\PythonVenv\py311\Scripts\python.exe -m tests.test_config

# Test theme system
& C:\PythonVenv\py311\Scripts\python.exe -m tests.test_themes

# Test scoring system
& C:\PythonVenv\py311\Scripts\python.exe -m tests.test_scores

# Test user preferences
& C:\PythonVenv\py311\Scripts\python.exe -c "from config.user_preferences import user_prefs; print(user_prefs.get('total_games_played', 0))"
```

## Additional Resources

- **config_examples.py** - Advanced configuration patterns
- **.gitignore** - Recommended ignore patterns
- **user_prefs.json** - Auto-generated UI/user state (don't edit manually)
- **scores.json** - Auto-generated scores + players (don't edit manually)

## Support

For questions or issues:
1. Check the relevant documentation file above
2. Review code examples in `config_examples.py`
3. Run `python -m tests.test_config` to verify your setup

## Contributing

When adding new features or games:
1. Update relevant documentation files
2. Add examples to README or QUICKSTART
3. Test thoroughly with `python -m tests.test_config`
4. Update this index if adding new docs
