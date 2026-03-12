import json
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Singleton configuration manager for the application."""

    _instance: Optional['ConfigManager'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self.load_config()

    def load_config(self, config_path: Optional[Path] = None) -> None:
        if config_path is None:
            config_path = Path(__file__).parent / "config.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a config value using dot-notation (e.g. 'app.window_width')."""
        keys = key_path.split('.')
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def get_app_config(self) -> Dict[str, Any]:
        return self._config.get('app', {})


config = ConfigManager()
