import importlib
import pkgutil
from games import __path__ as games_path
from config.config_manager import config


def load_games():
    """Load all enabled games from the games directory.
    
    Only loads games that are:
    1. Present in the games/ directory
    2. Have GAME_NAME and Game attributes
    3. Are enabled in the configuration file
    """
    game_info = []
    enabled_games = config.get_enabled_games()

    # Iterate over modules in games/
    for module_info in pkgutil.iter_modules(games_path):
        module_name = f"games.{module_info.name}"
        
        # Check if game is enabled in config
        if module_info.name not in enabled_games:
            continue
        
        module = importlib.import_module(module_name)

        # Module must define GAME_NAME and Game
        if hasattr(module, "GAME_NAME") and hasattr(module, "Game"):
            # Get game-specific configuration
            game_config = config.get_game_config(module_info.name)
            
            game_info.append({
                "name": game_config.get("display_name", module.GAME_NAME),
                "widget_class": module.Game,
                "module_name": module_info.name,
                "config": game_config
            })

    return game_info
