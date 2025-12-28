"""
Example: Advanced Configuration Usage Patterns

This file demonstrates professional patterns for using the configuration system
in your game modules and main application.
"""

from config.config_manager import config


# Pattern 1: Configuration-driven feature flags
def example_feature_flags():
    """Use config to enable/disable features without code changes."""
    
    if config.get("logging.enabled", False):
        print("Logging is enabled")
        # Set up logging system
    
    if config.get("app.theme") == "dark":
        # Apply dark theme
        pass


# Pattern 2: Environment-specific configuration
def example_environment_config():
    """Different settings for dev/test/prod environments.
    
    You can maintain separate config files:
    - config.json (default)
    - config.dev.json (development)
    - config.prod.json (production)
    
    Then load based on environment variable.
    """
    import os
    from pathlib import Path
    
    env = os.getenv("APP_ENV", "default")
    config_file = Path(__file__).parent / "config" / f"config.{env}.json"
    
    if config_file.exists():
        config.load_config(config_file)


# Pattern 3: Runtime configuration updates
def example_runtime_updates():
    """Update configuration at runtime and persist changes."""
    
    # Update a single value
    config.update("app.theme", "dark")
    
    # Save to file
    config.save_config()
    
    # Reload from file
    config.reload()


# Pattern 4: Validation and type safety
def example_validation():
    """Validate configuration values with defaults and type checking."""
    
    # Get with type-safe defaults
    width = config.get("app.window_width", 1000)
    if not isinstance(width, int) or width < 100:
        width = 1000
    
    # Validate enum values
    theme = config.get("app.theme", "dark")
    valid_themes = ["dark", "light"]
    if theme not in valid_themes:
        theme = "dark"


# Pattern 5: Game-specific configuration with inheritance
def example_game_inheritance():
    """Games can have default values that are overridden by config."""
    
    class BaseGame:
        def __init__(self, module_name):
            # Load config with fallback defaults
            game_cfg = config.get_game_config(module_name)
            
            self.difficulty = game_cfg.get("difficulty", "medium")
            self.max_score = game_cfg.get("max_score", 100)
            self.time_limit = game_cfg.get("time_limit", 60)
            self.description = game_cfg.get("description", "A fun game")


# Pattern 6: User preferences (extend configuration)
def example_user_preferences():
    """Store user-specific settings separate from app config.
    
    Common pattern: config.json for app defaults, user_prefs.json for user settings.
    """
    
    # You could create a separate UserPreferences class similar to ConfigManager
    # that manages user-specific settings like:
    # - Last played game
    # - High scores
    # - UI preferences
    # - Custom keybindings


# Pattern 7: Configuration schema validation
def example_schema_validation():
    """Validate configuration against a schema (using jsonschema package).
    
    This ensures config.json has all required fields with correct types.
    """
    
    # Example schema (requires: pip install jsonschema)
    schema = {
        "type": "object",
        "properties": {
            "app": {
                "type": "object",
                "required": ["title", "window_width", "window_height"],
                "properties": {
                    "title": {"type": "string"},
                    "window_width": {"type": "integer", "minimum": 100},
                    "window_height": {"type": "integer", "minimum": 100}
                }
            }
        },
        "required": ["app", "games"]
    }
    
    # In config_manager.py, you could add:
    # from jsonschema import validate
    # validate(instance=self._config, schema=schema)


# Pattern 8: Configuration hot-reload
def example_hot_reload():
    """Watch config file and reload when it changes (useful for development).
    
    Requires: pip install watchdog
    """
    
    from pathlib import Path
    # from watchdog.observers import Observer
    # from watchdog.events import FileSystemEventHandler
    
    # class ConfigReloader(FileSystemEventHandler):
    #     def on_modified(self, event):
    #         if event.src_path.endswith("config.json"):
    #             config.reload()
    #             print("Configuration reloaded!")
    
    # observer = Observer()
    # observer.schedule(ConfigReloader(), path=str(Path(__file__).parent))
    # observer.start()


if __name__ == "__main__":
    print("Configuration Usage Examples")
    print("=" * 60)
    print("\nSee source code for professional configuration patterns:")
    print("1. Feature flags")
    print("2. Environment-specific configs")
    print("3. Runtime updates")
    print("4. Validation and type safety")
    print("5. Game configuration inheritance")
    print("6. User preferences")
    print("7. Schema validation")
    print("8. Hot-reload")
