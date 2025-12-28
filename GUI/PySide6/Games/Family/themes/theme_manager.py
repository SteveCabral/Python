"""
Theme Manager for PySide6 Application

This module provides centralized theme management with support for:
- Multiple themes (dark, light, custom)
- Dynamic theme switching
- Qt Style Sheet (QSS) generation
- Semantic color naming
- Professional color palettes

Usage:
    from themes.theme_manager import theme_manager
    
    # Apply theme to app
    theme_manager.apply_theme(app)
    
    # Get color
    color = theme_manager.get_color("primary")
    
    # Switch theme
    theme_manager.set_theme("dark")
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor


class ThemeManager:
    """Singleton theme manager for the application."""
    
    _instance: Optional['ThemeManager'] = None
    _current_theme: str = "dark"
    _themes: Dict[str, Dict[str, Any]] = {}
    _theme_change_callbacks: list = []
    
    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize theme manager and load available themes."""
        if not self._themes:
            self._load_themes()
    
    def _load_themes(self) -> None:
        """Load all theme files from the themes directory."""
        themes_dir = Path(__file__).parent
        
        for theme_file in themes_dir.glob("*.json"):
            theme_name = theme_file.stem
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    self._themes[theme_name] = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load theme '{theme_name}': {e}")
    
    def get_available_themes(self) -> list[str]:
        """Get list of available theme names."""
        return list(self._themes.keys())
    
    def set_theme(self, theme_name: str) -> bool:
        """
        Set the current theme.
        
        Args:
            theme_name: Name of the theme to activate
            
        Returns:
            True if theme was set successfully, False otherwise
        """
        requested = (theme_name or "").strip().lower()

        # Backwards/Docs compatibility: accept "default" as an alias.
        if requested in {"default", "system", "auto", ""}:
            requested = "dark" if "dark" in self._themes else (next(iter(self._themes), ""))

        if requested not in self._themes:
            fallback = "dark" if "dark" in self._themes else (next(iter(self._themes), ""))
            print(f"Warning: Theme '{theme_name}' not found; falling back to '{fallback}'")
            if not fallback:
                return False
            requested = fallback
        
        self._current_theme = requested
        self._notify_theme_changed()
        return True
    
    def get_current_theme(self) -> str:
        """Get the name of the current theme."""
        return self._current_theme
    
    def get_theme_data(self, theme_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get theme data for a specific theme or current theme.
        
        Args:
            theme_name: Name of theme, or None for current theme
            
        Returns:
            Theme data dictionary
        """
        theme = theme_name or self._current_theme
        return self._themes.get(theme, {})
    
    def get_color(self, color_name: str, theme_name: Optional[str] = None) -> str:
        """
        Get a color value from the current or specified theme.
        
        Args:
            color_name: Name of the color (e.g., 'primary', 'background')
            theme_name: Optional theme name, defaults to current theme
            
        Returns:
            Hex color string (e.g., '#1976D2')
        """
        theme = self.get_theme_data(theme_name)
        return theme.get("colors", {}).get(color_name, "#000000")
    
    def get_font(self, font_property: str, theme_name: Optional[str] = None) -> str:
        """
        Get a font property from the current or specified theme.
        
        Args:
            font_property: Font property name (e.g., 'family', 'size_normal')
            theme_name: Optional theme name, defaults to current theme
            
        Returns:
            Font property value
        """
        theme = self.get_theme_data(theme_name)
        return theme.get("fonts", {}).get(font_property, "")
    
    def get_spacing(self, spacing_name: str, theme_name: Optional[str] = None) -> str:
        """Get spacing value from theme."""
        theme = self.get_theme_data(theme_name)
        return theme.get("spacing", {}).get(spacing_name, "8px")
    
    def get_border(self, border_property: str, theme_name: Optional[str] = None) -> str:
        """Get border property from theme."""
        theme = self.get_theme_data(theme_name)
        return theme.get("borders", {}).get(border_property, "1px")
    
    def generate_stylesheet(self, theme_name: Optional[str] = None) -> str:
        """
        Generate Qt Style Sheet (QSS) for the entire application.
        
        Args:
            theme_name: Optional theme name, defaults to current theme
            
        Returns:
            Complete QSS string
        """
        theme = theme_name or self._current_theme
        colors = self.get_theme_data(theme).get("colors", {})
        fonts = self.get_theme_data(theme).get("fonts", {})
        spacing = self.get_theme_data(theme).get("spacing", {})
        borders = self.get_theme_data(theme).get("borders", {})
        
        # Generate comprehensive stylesheet
        stylesheet = f"""
/* Global Application Styles */
QWidget {{
    background-color: {colors.get('background', '#FFFFFF')};
    color: {colors.get('text_primary', '#000000')};
    font-family: {fonts.get('family', 'Arial')};
    font-size: {fonts.get('size_normal', '11pt')};
    font-weight: {fonts.get('weight_normal', '400')};
}}

/* Main Window */
QMainWindow {{
    background-color: {colors.get('background', '#FFFFFF')};
}}

/* List Widget (Navigation) */
QListWidget {{
    background-color: {colors.get('navigation_background', '#F5F5F5')};
    border: {borders.get('width_thin', '1px')} solid {colors.get('border', '#E0E0E0')};
    border-radius: {borders.get('radius_small', '4px')};
    padding: {spacing.get('sm', '8px')};
    outline: none;
}}

QListWidget::item {{
    background-color: transparent;
    color: {colors.get('text_primary', '#000000')};
    padding: {spacing.get('md', '12px')};
    border-radius: {borders.get('radius_small', '4px')};
    margin-bottom: {spacing.get('xs', '4px')};
}}

QListWidget::item:hover {{
    background-color: {colors.get('navigation_item_hover', '#E8E8E8')};
}}

QListWidget::item:selected {{
    background-color: {colors.get('navigation_item_selected', '#1976D2')};
    color: {colors.get('selected_text', '#FFFFFF')};
}}

/* Push Button */
QPushButton {{
    background-color: {colors.get('button_background', '#F5F5F5')};
    color: {colors.get('text_primary', '#000000')};
    border: {borders.get('width_thin', '1px')} solid {colors.get('border', '#E0E0E0')};
    border-radius: {borders.get('radius_medium', '6px')};
    padding: {spacing.get('sm', '8px')} {spacing.get('lg', '16px')};
    font-weight: {fonts.get('weight_medium', '500')};
}}

QPushButton:hover {{
    background-color: {colors.get('button_hover', '#EEEEEE')};
    border-color: {colors.get('primary', '#1976D2')};
}}

QPushButton:pressed {{
    background-color: {colors.get('button_pressed', '#E0E0E0')};
}}

QPushButton:disabled {{
    background-color: {colors.get('disabled', '#E0E0E0')};
    color: {colors.get('text_disabled', '#BDBDBD')};
    border-color: {colors.get('border_light', '#EEEEEE')};
}}

/* Primary Button */
QPushButton[primary="true"] {{
    background-color: {colors.get('primary', '#1976D2')};
    color: {colors.get('text_inverse', '#FFFFFF')};
    border: none;
}}

QPushButton[primary="true"]:hover {{
    background-color: {colors.get('primary_light', '#42A5F5')};
}}

QPushButton[primary="true"]:pressed {{
    background-color: {colors.get('primary_dark', '#1565C0')};
}}

/* Line Edit (Text Input) */
QLineEdit {{
    background-color: {colors.get('input_background', '#FFFFFF')};
    color: {colors.get('text_primary', '#000000')};
    border: {borders.get('width_medium', '2px')} solid {colors.get('input_border', '#BDBDBD')};
    border-radius: {borders.get('radius_small', '4px')};
    padding: {spacing.get('sm', '8px')};
}}

QLineEdit:focus {{
    border-color: {colors.get('input_border_focus', '#1976D2')};
}}

QLineEdit:disabled {{
    background-color: {colors.get('disabled', '#E0E0E0')};
    color: {colors.get('text_disabled', '#BDBDBD')};
}}

/* Text Edit */
QTextEdit, QPlainTextEdit {{
    background-color: {colors.get('input_background', '#FFFFFF')};
    color: {colors.get('text_primary', '#000000')};
    border: {borders.get('width_thin', '1px')} solid {colors.get('input_border', '#BDBDBD')};
    border-radius: {borders.get('radius_small', '4px')};
    padding: {spacing.get('sm', '8px')};
}}

/* Label */
QLabel {{
    background-color: transparent;
    color: {colors.get('text_primary', '#000000')};
}}

QLabel[heading="true"] {{
    font-size: {fonts.get('size_large', '14pt')};
    font-weight: {fonts.get('weight_bold', '600')};
}}

QLabel[title="true"] {{
    font-size: {fonts.get('size_title', '18pt')};
    font-weight: {fonts.get('weight_bold', '600')};
}}

QLabel[secondary="true"] {{
    color: {colors.get('text_secondary', '#757575')};
}}

/* Scroll Bar */
QScrollBar:vertical {{
    background-color: {colors.get('scrollbar_background', '#F5F5F5')};
    width: 12px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background-color: {colors.get('scrollbar_handle', '#BDBDBD')};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {colors.get('scrollbar_handle_hover', '#9E9E9E')};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background-color: {colors.get('scrollbar_background', '#F5F5F5')};
    height: 12px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background-color: {colors.get('scrollbar_handle', '#BDBDBD')};
    border-radius: 6px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {colors.get('scrollbar_handle_hover', '#9E9E9E')};
}}

/* Combo Box */
QComboBox {{
    background-color: {colors.get('input_background', '#FFFFFF')};
    color: {colors.get('text_primary', '#000000')};
    border: {borders.get('width_medium', '2px')} solid {colors.get('input_border', '#BDBDBD')};
    border-radius: {borders.get('radius_small', '4px')};
    padding: {spacing.get('sm', '8px')};
}}

QComboBox:focus {{
    border-color: {colors.get('input_border_focus', '#1976D2')};
}}

/* Spin Box */
QSpinBox, QDoubleSpinBox {{
    background-color: {colors.get('input_background', '#FFFFFF')};
    color: {colors.get('text_primary', '#000000')};
    border: {borders.get('width_medium', '2px')} solid {colors.get('input_border', '#BDBDBD')};
    border-radius: {borders.get('radius_small', '4px')};
    padding: {spacing.get('sm', '8px')};
}}

/* Check Box */
QCheckBox {{
    color: {colors.get('text_primary', '#000000')};
    spacing: {spacing.get('sm', '8px')};
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: {borders.get('width_medium', '2px')} solid {colors.get('input_border', '#BDBDBD')};
    border-radius: {borders.get('radius_small', '4px')};
    background-color: {colors.get('input_background', '#FFFFFF')};
}}

QCheckBox::indicator:checked {{
    background-color: {colors.get('primary', '#1976D2')};
    border-color: {colors.get('primary', '#1976D2')};
}}

/* Radio Button */
QRadioButton {{
    color: {colors.get('text_primary', '#000000')};
    spacing: {spacing.get('sm', '8px')};
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: {borders.get('width_medium', '2px')} solid {colors.get('input_border', '#BDBDBD')};
    border-radius: 9px;
    background-color: {colors.get('input_background', '#FFFFFF')};
}}

QRadioButton::indicator:checked {{
    background-color: {colors.get('primary', '#1976D2')};
    border-color: {colors.get('primary', '#1976D2')};
}}

/* Tool Tip */
QToolTip {{
    background-color: {colors.get('tooltip_background', '#616161')};
    color: {colors.get('tooltip_text', '#FFFFFF')};
    border: none;
    padding: {spacing.get('sm', '8px')};
    border-radius: {borders.get('radius_small', '4px')};
}}

/* Menu Bar */
QMenuBar {{
    background-color: {colors.get('surface', '#FFFFFF')};
    color: {colors.get('text_primary', '#000000')};
    border-bottom: {borders.get('width_thin', '1px')} solid {colors.get('divider', '#E0E0E0')};
}}

QMenuBar::item:selected {{
    background-color: {colors.get('hover', '#F5F5F5')};
}}

/* Menu */
QMenu {{
    background-color: {colors.get('surface_elevated', '#FAFAFA')};
    color: {colors.get('text_primary', '#000000')};
    border: {borders.get('width_thin', '1px')} solid {colors.get('border', '#E0E0E0')};
    border-radius: {borders.get('radius_small', '4px')};
}}

QMenu::item {{
    padding: {spacing.get('sm', '8px')} {spacing.get('lg', '16px')};
}}

QMenu::item:selected {{
    background-color: {colors.get('hover', '#F5F5F5')};
}}

/* Tab Widget */
QTabWidget::pane {{
    border: {borders.get('width_thin', '1px')} solid {colors.get('border', '#E0E0E0')};
    border-radius: {borders.get('radius_small', '4px')};
    background-color: {colors.get('surface', '#FFFFFF')};
}}

QTabBar::tab {{
    background-color: {colors.get('background_light', '#FAFAFA')};
    color: {colors.get('text_secondary', '#757575')};
    border: {borders.get('width_thin', '1px')} solid {colors.get('border', '#E0E0E0')};
    padding: {spacing.get('sm', '8px')} {spacing.get('lg', '16px')};
    border-top-left-radius: {borders.get('radius_small', '4px')};
    border-top-right-radius: {borders.get('radius_small', '4px')};
}}

QTabBar::tab:selected {{
    background-color: {colors.get('surface', '#FFFFFF')};
    color: {colors.get('text_primary', '#000000')};
    border-bottom-color: {colors.get('surface', '#FFFFFF')};
}}

/* Progress Bar */
QProgressBar {{
    background-color: {colors.get('background_light', '#FAFAFA')};
    border: {borders.get('width_thin', '1px')} solid {colors.get('border', '#E0E0E0')};
    border-radius: {borders.get('radius_small', '4px')};
    text-align: center;
    color: {colors.get('text_primary', '#000000')};
}}

QProgressBar::chunk {{
    background-color: {colors.get('primary', '#1976D2')};
    border-radius: {borders.get('radius_small', '4px')};
}}
"""
        
        return stylesheet
    
    def apply_theme(self, app: QApplication, theme_name: Optional[str] = None) -> None:
        """
        Apply theme to the entire application.
        
        Args:
            app: QApplication instance
            theme_name: Optional theme name, defaults to current theme
        """
        if theme_name:
            self.set_theme(theme_name)
        
        stylesheet = self.generate_stylesheet()
        app.setStyleSheet(stylesheet)
        
        # Also set application palette for native widgets
        self._apply_palette(app)
    
    def _apply_palette(self, app: QApplication) -> None:
        """Apply color palette to application for native widgets."""
        palette = QPalette()
        theme = self.get_theme_data()
        colors = theme.get("colors", {})
        
        # Window colors
        palette.setColor(QPalette.Window, QColor(colors.get('background', '#FFFFFF')))
        palette.setColor(QPalette.WindowText, QColor(colors.get('text_primary', '#000000')))
        
        # Base colors
        palette.setColor(QPalette.Base, QColor(colors.get('input_background', '#FFFFFF')))
        palette.setColor(QPalette.AlternateBase, QColor(colors.get('background_light', '#FAFAFA')))
        
        # Text colors
        palette.setColor(QPalette.Text, QColor(colors.get('text_primary', '#000000')))
        palette.setColor(QPalette.BrightText, QColor(colors.get('text_inverse', '#FFFFFF')))
        
        # Button colors
        palette.setColor(QPalette.Button, QColor(colors.get('button_background', '#F5F5F5')))
        palette.setColor(QPalette.ButtonText, QColor(colors.get('text_primary', '#000000')))
        
        # Highlight colors
        palette.setColor(QPalette.Highlight, QColor(colors.get('selected', '#1976D2')))
        palette.setColor(QPalette.HighlightedText, QColor(colors.get('selected_text', '#FFFFFF')))
        
        # Link colors
        palette.setColor(QPalette.Link, QColor(colors.get('link', '#1976D2')))
        palette.setColor(QPalette.LinkVisited, QColor(colors.get('link_hover', '#1565C0')))
        
        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(colors.get('text_disabled', '#BDBDBD')))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(colors.get('text_disabled', '#BDBDBD')))
        
        app.setPalette(palette)
    
    def register_theme_change_callback(self, callback: callable) -> None:
        """Register a callback to be called when theme changes."""
        if callback not in self._theme_change_callbacks:
            self._theme_change_callbacks.append(callback)
    
    def unregister_theme_change_callback(self, callback: callable) -> None:
        """Unregister a theme change callback."""
        if callback in self._theme_change_callbacks:
            self._theme_change_callbacks.remove(callback)
    
    def _notify_theme_changed(self) -> None:
        """Notify all registered callbacks that theme has changed."""
        for callback in self._theme_change_callbacks:
            try:
                callback(self._current_theme)
            except Exception as e:
                print(f"Error in theme change callback: {e}")


# Create singleton instance
theme_manager = ThemeManager()
