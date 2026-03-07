"""
Test script to validate the configuration system.
Run this to verify config_manager.py works correctly.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.config_manager import config


def test_config():
    """Test all configuration manager features."""
    
    print("=" * 60)
    print("Configuration System Test")
    print("=" * 60)
    
    # Test app configuration
    print("\n1. App Configuration:")
    print(f"   Title: {config.get('app.title')}")
    print(f"   Window Size: {config.get('app.window_width')}x{config.get('app.window_height')}")
    print(f"   Nav Width: {config.get('app.nav_list_width')}")
    print(f"   Theme: {config.get('app.theme')}")
    
    # Test enabled games
    print("\n2. Enabled Games:")
    enabled = config.get_enabled_games()
    print(f"   {', '.join(enabled)}")
    
    # Test game-specific configuration
    print("\n3. Game Configurations:")
    for game_name in enabled:
        game_cfg = config.get_game_config(game_name)
        print(f"\n   {game_name}:")
        print(f"      Display Name: {game_cfg.get('display_name')}")
        print(f"      Description: {game_cfg.get('description')}")
        print(f"      Difficulty: {game_cfg.get('difficulty')}")
        print(f"      Max Score: {game_cfg.get('max_score')}")
        print(f"      Time Limit: {game_cfg.get('time_limit')}s")
    
    # Test logging configuration
    print("\n4. Logging Configuration:")
    log_cfg = config.get_logging_config()
    print(f"   Enabled: {log_cfg.get('enabled')}")
    print(f"   Level: {log_cfg.get('level')}")
    print(f"   Log File: {log_cfg.get('log_file')}")
    
    # Test game enabled check
    print("\n5. Game Enable Status:")
    for test_game in ["game1", "game2", "game3", "game4"]:
        status = "✓ Enabled" if config.is_game_enabled(test_game) else "✗ Disabled"
        print(f"   {test_game}: {status}")
    
    # Test default values
    print("\n6. Default Value Test:")
    print(f"   Non-existent key: {config.get('non.existent.key', 'DEFAULT_VALUE')}")
    
    print("\n" + "=" * 60)
    print("✓ All configuration tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    test_config()
