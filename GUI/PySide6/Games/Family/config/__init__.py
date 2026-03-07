"""
Configuration package for Family Game Collection.

This package contains:
- config_manager: Central configuration management
- user_preferences: User-specific data and preferences
- config.json: Application and game settings
"""

from .config_manager import config, ConfigManager
from .user_preferences import user_prefs, UserPreferences

__all__ = ['config', 'ConfigManager', 'user_prefs', 'UserPreferences']
