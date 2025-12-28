from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QStackedWidget,
    QHBoxLayout, QListWidgetItem, QPushButton, QVBoxLayout, QLabel
)
from game_loader import load_games
from config.config_manager import config
from themes.theme_manager import theme_manager


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set window title from config
        app_config = config.get_app_config()
        self.app_title = app_config.get("title", "Game Collection")
        self.setWindowTitle(self.app_title)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top bar with theme switcher
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        # Content area
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(8, 8, 8, 8)
        
        # Left navigation list
        self.nav_list = QListWidget()
        nav_width = config.get("app.nav_list_width", 200)
        self.nav_list.setFixedWidth(nav_width)

        # Right game window stack
        self.stack = QStackedWidget()

        content_layout.addWidget(self.nav_list)
        content_layout.addWidget(self.stack, 1)
        
        main_layout.addLayout(content_layout)

        # Load games dynamically
        self.games = load_games()
        self.setup_games()

        # Hook list clicks to stack switching
        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)
    
    def create_top_bar(self):
        """Create top bar with theme switcher."""
        top_bar = QWidget()
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Title
        title = QLabel(self.app_title)
        title.setProperty("heading", True)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Theme buttons
        theme_label = QLabel("Theme:")
        theme_label.setProperty("secondary", True)
        layout.addWidget(theme_label)
        
        self.light_btn = QPushButton("Light")
        self.light_btn.setFixedWidth(80)
        self.light_btn.clicked.connect(lambda: self.switch_theme("light"))
        layout.addWidget(self.light_btn)
        
        self.dark_btn = QPushButton("Dark")
        self.dark_btn.setFixedWidth(80)
        self.dark_btn.clicked.connect(lambda: self.switch_theme("dark"))
        layout.addWidget(self.dark_btn)
        
        # Highlight current theme button
        self.update_theme_buttons()
        
        return top_bar
    
    def switch_theme(self, theme_name: str):
        """Switch application theme."""
        theme_manager.set_theme(theme_name)
        app = QApplication.instance()
        theme_manager.apply_theme(app, theme_name)
        
        # Update config
        config.update("app.theme", theme_name)
        config.save_config()
        
        # Update button states
        self.update_theme_buttons()
    
    def update_theme_buttons(self):
        """Update theme button states to show active theme."""
        current_theme = theme_manager.get_current_theme()
        
        # Set primary property for active button
        self.light_btn.setProperty("primary", current_theme == "light")
        self.dark_btn.setProperty("primary", current_theme == "dark")
        
        # Force style update
        self.light_btn.style().unpolish(self.light_btn)
        self.light_btn.style().polish(self.light_btn)
        self.dark_btn.style().unpolish(self.dark_btn)
        self.dark_btn.style().polish(self.dark_btn)

    def setup_games(self):
        for game in self.games:

            # Add name to navigation list
            item = QListWidgetItem(game["name"])
            self.nav_list.addItem(item)

            # Instantiate and add game widget
            try:
                widget = game["widget_class"](game_config=game.get("config"))
            except TypeError:
                widget = game["widget_class"]()
            self.stack.addWidget(widget)


if __name__ == "__main__":
    app = QApplication([])
    
    # Apply theme before showing window
    theme_name = config.get("app.theme", "dark")
    theme_manager.set_theme(theme_name)
    theme_manager.apply_theme(app)
    
    win = MainWindow()
    
    # Get window size from config
    width = config.get("app.window_width", 1000)
    height = config.get("app.window_height", 600)
    win.resize(width, height)
    
    win.show()
    app.exec()
