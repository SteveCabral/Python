"""
User Preferences Manager (Optional Extension)

This module demonstrates how to extend the configuration system
to handle user-specific preferences (high scores, settings, etc.)
separate from application configuration.

Usage:
    from user_preferences import user_prefs
    
    # Save high score
    user_prefs.set_high_score("game1", 150)
    
    # Get last played game
    last_game = user_prefs.get("last_played_game", "game1")
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime


class UserPreferences:
    """Manage user-specific preferences and game progress."""
    
    _instance: Optional['UserPreferences'] = None
    _prefs: Dict[str, Any] = {}
    _prefs_file: Path = Path(__file__).parent.parent / "user_prefs.json"
    
    def __new__(cls):
        """Singleton pattern - only one instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Load preferences on first initialization."""
        if not self._prefs:
            self.load()
    
    def load(self) -> None:
        """Load user preferences from JSON file."""
        if self._prefs_file.exists():
            try:
                with open(self._prefs_file, 'r', encoding='utf-8') as f:
                    self._prefs = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._prefs = self._get_default_prefs()
        else:
            self._prefs = self._get_default_prefs()
    
    def save(self) -> None:
        """Save current preferences to JSON file."""
        with open(self._prefs_file, 'w', encoding='utf-8') as f:
            json.dump(self._prefs, f, indent=2, ensure_ascii=False)
    
    def _get_default_prefs(self) -> Dict[str, Any]:
        """Return default user preferences structure."""
        return {
            "last_played_game": None,
            "total_games_played": 0,
            "high_scores": {},
            "ui_preferences": {
                "show_timer": True,
                "sound_enabled": True,
                "music_volume": 0.7,
                "sfx_volume": 0.8
            },
            "game_statistics": {},
            "achievements": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get preference value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., 'ui_preferences.sound_enabled')
            default: Default value if key doesn't exist
            
        Returns:
            Preference value or default
        """
        keys = key_path.split('.')
        value = self._prefs
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any, auto_save: bool = True) -> None:
        """
        Set preference value using dot notation.
        
        Args:
            key_path: Dot-separated path
            value: Value to set
            auto_save: Automatically save to file after update
        """
        keys = key_path.split('.')
        prefs = self._prefs
        
        for key in keys[:-1]:
            if key not in prefs:
                prefs[key] = {}
            prefs = prefs[key]
        
        prefs[keys[-1]] = value
        self._prefs["last_updated"] = datetime.now().isoformat()
        
        if auto_save:
            self.save()
    
    # Convenience methods for common operations
    
    def get_high_score(self, game_name: str) -> int:
        """Get high score for a specific game."""
        return self._prefs.get("high_scores", {}).get(game_name, 0)
    
    def set_high_score(self, game_name: str, score: int, auto_save: bool = True) -> bool:
        """
        Set high score for a game if it's higher than current.
        
        Returns:
            True if new high score, False otherwise
        """
        current = self.get_high_score(game_name)
        if score > current:
            if "high_scores" not in self._prefs:
                self._prefs["high_scores"] = {}
            self._prefs["high_scores"][game_name] = score
            self._prefs["last_updated"] = datetime.now().isoformat()
            
            if auto_save:
                self.save()
            return True
        return False
    
    def record_game_played(self, game_name: str, score: int, 
                          duration_seconds: float, auto_save: bool = True) -> None:
        """Record statistics for a completed game."""
        # Update total games
        self._prefs["total_games_played"] = self._prefs.get("total_games_played", 0) + 1
        self._prefs["last_played_game"] = game_name
        
        # Update game-specific statistics
        if "game_statistics" not in self._prefs:
            self._prefs["game_statistics"] = {}
        
        if game_name not in self._prefs["game_statistics"]:
            self._prefs["game_statistics"][game_name] = {
                "times_played": 0,
                "total_score": 0,
                "total_time": 0,
                "average_score": 0,
                "average_time": 0
            }
        
        stats = self._prefs["game_statistics"][game_name]
        stats["times_played"] += 1
        stats["total_score"] += score
        stats["total_time"] += duration_seconds
        stats["average_score"] = stats["total_score"] / stats["times_played"]
        stats["average_time"] = stats["total_time"] / stats["times_played"]
        
        # Check for new high score
        self.set_high_score(game_name, score, auto_save=False)
        
        self._prefs["last_updated"] = datetime.now().isoformat()
        
        if auto_save:
            self.save()
    
    def unlock_achievement(self, achievement_id: str, auto_save: bool = True) -> bool:
        """
        Unlock an achievement.
        
        Returns:
            True if newly unlocked, False if already unlocked
        """
        if "achievements" not in self._prefs:
            self._prefs["achievements"] = []
        
        if achievement_id not in self._prefs["achievements"]:
            self._prefs["achievements"].append(achievement_id)
            self._prefs["last_updated"] = datetime.now().isoformat()
            
            if auto_save:
                self.save()
            return True
        return False
    
    def is_achievement_unlocked(self, achievement_id: str) -> bool:
        """Check if achievement is unlocked."""
        return achievement_id in self._prefs.get("achievements", [])
    
    def get_game_statistics(self, game_name: str) -> Dict[str, Any]:
        """Get all statistics for a specific game."""
        return self._prefs.get("game_statistics", {}).get(game_name, {
            "times_played": 0,
            "total_score": 0,
            "total_time": 0,
            "average_score": 0,
            "average_time": 0
        })
    
    def reset_all(self, auto_save: bool = True) -> None:
        """Reset all preferences to defaults."""
        self._prefs = self._get_default_prefs()
        if auto_save:
            self.save()
    
    def reset_game_data(self, game_name: str, auto_save: bool = True) -> None:
        """Reset all data for a specific game."""
        if "high_scores" in self._prefs and game_name in self._prefs["high_scores"]:
            del self._prefs["high_scores"][game_name]
        
        if "game_statistics" in self._prefs and game_name in self._prefs["game_statistics"]:
            del self._prefs["game_statistics"][game_name]
        
        self._prefs["last_updated"] = datetime.now().isoformat()
        
        if auto_save:
            self.save()


# Create singleton instance
user_prefs = UserPreferences()


# Example integration with a game
if __name__ == "__main__":
    print("User Preferences Demo")
    print("=" * 60)
    
    # Simulate playing a game
    game_name = "game1"
    score = 120
    duration = 45.5
    
    print(f"\n1. Recording game: {game_name}")
    print(f"   Score: {score}, Duration: {duration}s")
    user_prefs.record_game_played(game_name, score, duration)
    
    print(f"\n2. High score for {game_name}: {user_prefs.get_high_score(game_name)}")
    
    print(f"\n3. Game statistics:")
    stats = user_prefs.get_game_statistics(game_name)
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n4. UI Preferences:")
    print(f"   Sound enabled: {user_prefs.get('ui_preferences.sound_enabled')}")
    print(f"   Music volume: {user_prefs.get('ui_preferences.music_volume')}")
    
    print(f"\n5. Total games played: {user_prefs.get('total_games_played')}")
    print(f"   Last played: {user_prefs.get('last_played_game')}")
    
    print("\n" + "=" * 60)
    print(f"Preferences saved to: {user_prefs._prefs_file}")
