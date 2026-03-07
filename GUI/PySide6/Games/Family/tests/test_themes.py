"""
Theme System Test Script

This script demonstrates all theme system features:
- Loading themes
- Switching between themes
- Accessing colors, fonts, spacing
- Generating stylesheets

Run this to verify the theme system works correctly.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from themes.theme_manager import theme_manager


def test_theme_system():
    """Test all theme system features."""
    
    print("=" * 70)
    print("Theme System Test")
    print("=" * 70)
    
    # Test 1: Available themes
    print("\n1. Available Themes:")
    themes = theme_manager.get_available_themes()
    for theme in themes:
        print(f"   - {theme}")
    
    # Test 2: Current theme
    print(f"\n2. Current Theme: {theme_manager.get_current_theme()}")
    
    # Test 3: Theme data
    print("\n3. Dark Theme Colors (sample):")
    dark_colors = theme_manager.get_theme_data("dark").get("colors", {})
    sample_colors = ["primary", "background", "text_primary", "success", "error"]
    for color_name in sample_colors:
        color_value = dark_colors.get(color_name, "N/A")
        print(f"   {color_name:20s} = {color_value}")
    
    print("\n4. Light Theme Colors (sample):")
    light_colors = theme_manager.get_theme_data("light").get("colors", {})
    for color_name in sample_colors:
        color_value = light_colors.get(color_name, "N/A")
        print(f"   {color_name:20s} = {color_value}")
    
    # Test 4: Get specific color
    print("\n5. Get Specific Colors:")
    print(f"   Dark primary: {theme_manager.get_color('primary', 'dark')}")
    print(f"   Light primary: {theme_manager.get_color('primary', 'light')}")
    
    # Test 5: Fonts
    print("\n6. Font Settings:")
    fonts = theme_manager.get_theme_data("dark").get("fonts", {})
    print(f"   Family: {fonts.get('family')}")
    print(f"   Normal size: {fonts.get('size_normal')}")
    print(f"   Title size: {fonts.get('size_title')}")
    print(f"   Bold weight: {fonts.get('weight_bold')}")
    
    # Test 6: Spacing
    print("\n7. Spacing Values:")
    spacing = theme_manager.get_theme_data("dark").get("spacing", {})
    for key, value in spacing.items():
        print(f"   {key:10s} = {value}")
    
    # Test 7: Borders
    print("\n8. Border Settings:")
    borders = theme_manager.get_theme_data("dark").get("borders", {})
    for key, value in borders.items():
        print(f"   {key:20s} = {value}")
    
    # Test 8: Theme switching
    print("\n9. Theme Switching Test:")
    original_theme = theme_manager.get_current_theme()
    print(f"   Current: {original_theme}")
    
    theme_manager.set_theme("light")
    print(f"   After switch: {theme_manager.get_current_theme()}")
    
    theme_manager.set_theme(original_theme)
    print(f"   Restored: {theme_manager.get_current_theme()}")
    
    # Test 9: Stylesheet generation
    print("\n10. Stylesheet Generation:")
    stylesheet = theme_manager.generate_stylesheet("dark")
    lines = stylesheet.strip().split('\n')
    print(f"   Generated {len(lines)} lines of QSS")
    print(f"   Preview (first 200 chars):")
    print(f"   {stylesheet[:200]}...")
    
    # Test 10: All colors defined
    print("\n11. Color Completeness Check:")
    dark_colors = theme_manager.get_theme_data("dark").get("colors", {})
    light_colors = theme_manager.get_theme_data("light").get("colors", {})
    print(f"   Dark theme: {len(dark_colors)} colors defined")
    print(f"   Light theme: {len(light_colors)} colors defined")
    
    # Check if both themes have same color keys
    dark_keys = set(dark_colors.keys())
    light_keys = set(light_colors.keys())
    
    if dark_keys == light_keys:
        print(f"   ✓ Both themes have matching color keys")
    else:
        missing_in_light = dark_keys - light_keys
        missing_in_dark = light_keys - dark_keys
        if missing_in_light:
            print(f"   ✗ Missing in light: {missing_in_light}")
        if missing_in_dark:
            print(f"   ✗ Missing in dark: {missing_in_dark}")
    
    print("\n" + "=" * 70)
    print("✓ All theme system tests completed!")
    print("=" * 70)


def show_color_palette():
    """Display all colors in both themes side by side."""
    print("\n" + "=" * 70)
    print("Complete Color Palette Comparison")
    print("=" * 70)
    
    dark_colors = theme_manager.get_theme_data("dark").get("colors", {})
    light_colors = theme_manager.get_theme_data("light").get("colors", {})
    
    print(f"\n{'Color Name':<30} {'Dark Theme':<15} {'Light Theme':<15}")
    print("-" * 70)
    
    for color_name in sorted(dark_colors.keys()):
        dark_value = dark_colors.get(color_name, "N/A")
        light_value = light_colors.get(color_name, "N/A")
        print(f"{color_name:<30} {dark_value:<15} {light_value:<15}")


if __name__ == "__main__":
    test_theme_system()
    
    print("\n")
    response = input("Show complete color palette? (y/n): ")
    if response.lower() == 'y':
        show_color_palette()
