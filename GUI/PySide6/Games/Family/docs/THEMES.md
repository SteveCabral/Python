# Theme System Documentation

## Overview

The Family Game Collection now includes a professional theming system that supports multiple color schemes with easy switching between light and dark themes. All UI controls use centralized theme definitions for consistent styling across the application.

## Folder Structure

```
themes/
├── __init__.py          # Package exports
├── theme_manager.py     # Theme management singleton
├── dark.json            # Dark theme definition
└── light.json           # Light theme definition
```

## Theme Files

Each theme is defined in a JSON file with the following structure:

### Color Definitions

All colors are defined with semantic names and hex codes:

```json
{
  "colors": {
    "primary": "#2196F3",           // Primary brand color
    "background": "#1E1E1E",        // Main background
    "text_primary": "#E0E0E0",      // Primary text color
    "success": "#4CAF50",           // Success state (green)
    "error": "#F44336",             // Error state (red)
    "warning": "#FFC107",           // Warning state (amber)
    // ... 40+ more semantic colors
  }
}
```

### Complete Color Palette

Both themes define these color categories:

**Brand Colors**
- `primary`, `primary_light`, `primary_dark`
- `secondary`, `secondary_light`, `secondary_dark`
- `accent`

**Background Colors**
- `background`, `background_light`, `background_dark`
- `surface`, `surface_elevated`

**Text Colors**
- `text_primary`, `text_secondary`, `text_disabled`, `text_inverse`

**UI State Colors**
- `hover`, `pressed`, `selected`, `disabled`
- `success`, `warning`, `error`, `info`

**Component-Specific Colors**
- `navigation_background`, `navigation_item_hover`, `navigation_item_selected`
- `button_background`, `button_hover`, `button_pressed`
- `input_background`, `input_border`, `input_border_focus`
- `scrollbar_background`, `scrollbar_handle`, `scrollbar_handle_hover`
- `tooltip_background`, `tooltip_text`
- `link`, `link_hover`

**Layout Colors**
- `border`, `border_light`, `divider`, `shadow`

### Font Definitions

```json
{
  "fonts": {
    "family": "Segoe UI, Arial, sans-serif",
    "size_small": "10pt",
    "size_normal": "11pt",
    "size_medium": "12pt",
    "size_large": "14pt",
    "size_title": "18pt",
    "weight_normal": "400",
    "weight_medium": "500",
    "weight_bold": "600"
  }
}
```

### Spacing System

```json
{
  "spacing": {
    "xs": "4px",   // Extra small
    "sm": "8px",   // Small
    "md": "12px",  // Medium
    "lg": "16px",  // Large
    "xl": "24px",  // Extra large
    "xxl": "32px"  // 2x extra large
  }
}
```

### Border Settings

```json
{
  "borders": {
    "radius_small": "4px",
    "radius_medium": "6px",
    "radius_large": "8px",
    "width_thin": "1px",
    "width_medium": "2px",
    "width_thick": "3px"
  }
}
```

## Using the Theme System

### Basic Usage

```python
from themes.theme_manager import theme_manager

# Apply theme to application
theme_manager.apply_theme(app, "dark")

# Get a color value
primary_color = theme_manager.get_color("primary")
background = theme_manager.get_color("background")

# Get font property
font_size = theme_manager.get_font("size_title")

# Get spacing
padding = theme_manager.get_spacing("md")
```

### Switching Themes

```python
# Switch to light theme
theme_manager.set_theme("light")
theme_manager.apply_theme(app)

# Switch to dark theme
theme_manager.set_theme("dark")
theme_manager.apply_theme(app)
```

### In Widgets

Use property selectors to apply theme-aware styles:

```python
from PySide6.QtWidgets import QLabel, QPushButton

# Title label - automatically styled by theme
title = QLabel("My Title")
title.setProperty("title", True)  # Uses theme's title styling

# Heading label
heading = QLabel("Section Heading")
heading.setProperty("heading", True)

# Secondary text
description = QLabel("This is secondary text")
description.setProperty("secondary", True)

# Primary button - uses theme primary color
button = QPushButton("Click Me")
button.setProperty("primary", True)
```

### Accessing Theme Values Programmatically

```python
from themes.theme_manager import theme_manager

# Get current theme name
current = theme_manager.get_current_theme()  # "dark" or "light"

# Get all available themes
themes = theme_manager.get_available_themes()  # ["dark", "light"]

# Get complete theme data
theme_data = theme_manager.get_theme_data("dark")
colors = theme_data["colors"]
fonts = theme_data["fonts"]
```

## Adding a New Theme

1. Create a new JSON file in `themes/` folder (e.g., `blue.json`)
2. Copy structure from `dark.json` or `light.json`
3. Customize colors while keeping the same color names
4. The theme will be automatically discovered

Example `themes/blue.json`:
```json
{
  "name": "Ocean Blue Theme",
  "colors": {
    "primary": "#0277BD",
    "background": "#E1F5FE",
    // ... other colors
  },
  "fonts": { /* same structure */ },
  "spacing": { /* same structure */ },
  "borders": { /* same structure */ }
}
```

## Styled Components

The theme system automatically styles these Qt widgets:

### Navigation
- **QListWidget** - Navigation panel with hover and selection states

### Buttons
- **QPushButton** - Regular and primary buttons
- Property `primary="true"` for primary button style

### Inputs
- **QLineEdit** - Text input with focus states
- **QTextEdit** / **QPlainTextEdit** - Multi-line text
- **QComboBox** - Dropdown selection
- **QSpinBox** / **QDoubleSpinBox** - Number input

### Selection
- **QCheckBox** - Checkbox with custom indicator
- **QRadioButton** - Radio button with custom indicator

### Display
- **QLabel** - Text labels
  - Property `title="true"` for title styling
  - Property `heading="true"` for heading styling
  - Property `secondary="true"` for secondary text

### Layout
- **QScrollBar** - Horizontal and vertical scrollbars
- **QMenuBar** / **QMenu** - Menu items
- **QTabWidget** / **QTabBar** - Tabbed interface
- **QProgressBar** - Progress indicator
- **QToolTip** - Tooltips

## Integration with Config System

Theme preference is stored in `config/config.json`:

```json
{
  "app": {
    "theme": "dark"  // or "light"
  }
}
```

The theme is:
- Loaded on application startup
- Saved when changed via UI
- Persisted across sessions

## Theme Manager API

### Methods

```python
# Theme selection
set_theme(theme_name: str) -> bool
get_current_theme() -> str
get_available_themes() -> list[str]

# Theme data access
get_theme_data(theme_name: str = None) -> dict
get_color(color_name: str, theme_name: str = None) -> str
get_font(font_property: str, theme_name: str = None) -> str
get_spacing(spacing_name: str, theme_name: str = None) -> str
get_border(border_property: str, theme_name: str = None) -> str

# Application
apply_theme(app: QApplication, theme_name: str = None) -> None
generate_stylesheet(theme_name: str = None) -> str

# Callbacks
register_theme_change_callback(callback: callable) -> None
unregister_theme_change_callback(callback: callable) -> None
```

## Custom Widget Styling

To apply theme colors to custom widgets:

```python
from themes.theme_manager import theme_manager

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Get theme colors
        bg_color = theme_manager.get_color("surface")
        text_color = theme_manager.get_color("text_primary")
        border_color = theme_manager.get_color("border")
        
        # Apply custom styling
        self.setStyleSheet(f"""
            MyWidget {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
            }}
        """)
```

## React to Theme Changes

```python
def on_theme_changed(theme_name: str):
    """Called when theme changes."""
    print(f"Theme changed to: {theme_name}")
    # Update custom widgets, refresh UI, etc.

# Register callback
theme_manager.register_theme_change_callback(on_theme_changed)

# Unregister when done
theme_manager.unregister_theme_change_callback(on_theme_changed)
```

## Best Practices

1. **Use Semantic Color Names** - Always use named colors like `primary`, `text_primary` instead of hardcoded hex values
2. **Leverage Properties** - Use Qt properties (`title`, `primary`, `secondary`) for automatic theming
3. **Avoid Hardcoded Styles** - Let the theme system handle colors and fonts
4. **Test Both Themes** - Ensure UI looks good in both light and dark themes
5. **Use Consistent Spacing** - Reference theme spacing values (`xs`, `sm`, `md`, etc.)
6. **Follow the Palette** - Stick to the defined color palette for consistency

## Example: Complete Game Widget

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class ThemedGame(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Title - automatically themed
        title = QLabel("Game Title")
        title.setProperty("title", True)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description - secondary text
        desc = QLabel("Game description text")
        desc.setProperty("secondary", True)
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Primary action button
        play_btn = QPushButton("Play Game")
        play_btn.setProperty("primary", True)
        layout.addWidget(play_btn)
        
        # Secondary button (default styling)
        settings_btn = QPushButton("Settings")
        layout.addWidget(settings_btn)
```

## Troubleshooting

### Theme not applying
```python
# Ensure theme is applied to app
app = QApplication.instance()
theme_manager.apply_theme(app)
```

### Custom properties not working
```python
# Force style refresh after setting property
widget.setProperty("primary", True)
widget.style().unpolish(widget)
widget.style().polish(widget)
```

### Colors not updating on theme switch
```python
# Reapply theme to entire application
theme_manager.apply_theme(QApplication.instance())
```

## Testing

Run the theme test script:
```powershell
& C:\PythonVenv\py311\Scripts\python.exe test_themes.py
```

This validates:
- Theme loading
- Color definitions
- Theme switching
- Stylesheet generation
- Completeness of both themes

## Future Enhancements

Possible additions:
- User-created custom themes
- Theme editor UI
- System theme detection (auto light/dark)
- Per-game theme overrides
- Accent color customization
- High contrast mode
- Color blindness accommodations
