# Plugin-Like Architecture for Game Modules (Professional / Scalable)

This design lets you:

- Add new games simply by adding new Python files
- Automatically load all game modules at runtime
- Keep each game isolated (like plugins)
- Avoid modifying the main app when adding Game 11, Game 12, etc.

This is the same structure used in modular Qt applications and game engines.

```
word_games/
    main.py
    game_loader.py
    games/
        __init__.py
        game1.py
        game2.py
        game3.py
```
