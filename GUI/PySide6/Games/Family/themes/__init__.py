"""
Themes package for PySide6 application.

This package provides:
- Theme definitions (dark.json, light.json)
- Theme manager for applying and switching themes
- Color, font, spacing, and border definitions

Usage:
    from themes import theme_manager
    
    # Apply theme
    theme_manager.apply_theme(app, "dark")
    
    # Get colors
    primary_color = theme_manager.get_color("primary")
"""

from .theme_manager import theme_manager, ThemeManager

__all__ = ['theme_manager', 'ThemeManager']
