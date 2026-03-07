import importlib
import pkgutil
from pathlib import Path
from games import __path__ as games_path


def load_games():
    game_info = []

    # Iterate over modules in games/
    for module_info in pkgutil.iter_modules(games_path):
        module_name = f"games.{module_info.name}"
        module = importlib.import_module(module_name)

        # Module must define GAME_NAME and Game
        if hasattr(module, "GAME_NAME") and hasattr(module, "Game"):
            game_info.append({
                "name": module.GAME_NAME,
                "widget_class": module.Game
            })

    return game_info
