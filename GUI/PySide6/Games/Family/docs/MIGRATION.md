# Folder Reorganization Notes

**Date**: December 27, 2025

This project was reorganized to keep the root folder focused on “things you run” and to group supporting code and documentation into dedicated folders.

If you’re looking for how to *use* configuration or themes, prefer the living docs:

- [INDEX.md](INDEX.md) (start here)
- [CONFIGURATION.md](CONFIGURATION.md)
- [THEMES.md](THEMES.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)

## What Changed

- Configuration code and JSON moved into the `config/` package.
- Documentation consolidated under `docs/`.
- Theme support is organized under `themes/` (no functional change implied by this note).

## Follow-on Changes (After the Reorg)

- A **Players** screen and **Leaderboard** screen were added to the main UI.
- A dedicated scoring system now lives under `scores/` and persists to `scores.json`.
- `user_prefs.json` is still used for lightweight UI/user state (e.g., selected player).

## If You Had the Old Layout

Most breakage from the reorg will be import paths.

Use the package paths:

```python
from config.config_manager import config
from config.user_preferences import user_prefs
```

Config JSON now lives at:

- `config/config.json`

For a more detailed migration guide for existing games/config usage, see the “Migration Guide” section in [CONFIGURATION.md](CONFIGURATION.md).

## Sanity Checks

From the `Family/` folder:

```powershell
& C:\PythonVenv\py311\Scripts\python.exe main.py
& C:\PythonVenv\py311\Scripts\python.exe -m tests.test_config
& C:\PythonVenv\py311\Scripts\python.exe -m tests.test_themes
& C:\PythonVenv\py311\Scripts\python.exe -m tests.test_scores
```
