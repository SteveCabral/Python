"""
Configuration Manager for Game Application

This module provides centralized configuration management using JSON.
It follows professional patterns used in production applications:
- Single source of truth for all settings
- Type validation and default values
- Easy to extend and modify without code changes
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class ConfigManager:
    """Singleton configuration manager for the application."""
    
    _instance: Optional['ConfigManager'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration if not already loaded."""
        if not self._config:
            self.load_config()
    
    def load_config(self, config_path: Optional[Path] = None) -> None:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to config file. If None, uses default location.
        """
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
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., 'app.window_width')
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
            
        Example:
            config.get('app.window_width', 800)
            config.get('games.game1.difficulty', 'medium')
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_app_config(self) -> Dict[str, Any]:
        """Get all application-level configuration."""
        return self._config.get('app', {})
    
    def get_game_config(self, game_module_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific game.
        
        Args:
            game_module_name: Name of the game module (e.g., 'game1')
            
        Returns:
            Dictionary of game-specific settings
        """
        return self._config.get('games', {}).get(game_module_name, {})
    
    def get_enabled_games(self) -> List[str]:
        """Get list of enabled game module names."""
        return self._config.get('games', {}).get('enabled', [])
    
    def is_game_enabled(self, game_module_name: str) -> bool:
        """Check if a game is enabled in configuration."""
        return game_module_name in self.get_enabled_games()
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self._config.get('logging', {})
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._config = {}
        self.load_config()
    
    def save_config(self, config_path: Optional[Path] = None) -> None:
        """
        Save current configuration to JSON file.
        
        Args:
            config_path: Path to save config file. If None, uses default location.
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)
    
    def update(self, key_path: str, value: Any) -> None:
        """
        Update a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., 'app.window_width')
            value: New value to set
        """
        keys = key_path.split('.')
        config = self._config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value


# Create singleton instance
config = ConfigManager()
