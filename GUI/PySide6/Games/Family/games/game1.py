from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from config.config_manager import config
from themes.theme_manager import theme_manager

GAME_NAME = "Game One"

class Game(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Access game-specific configuration
        game_config = config.get_game_config("game1")
        
        # Title with theme-aware styling
        title_label = QLabel("GAME 1")
        title_label.setProperty("title", True)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Display game configuration
        desc_label = QLabel(
            f"Description: {game_config.get('description', 'N/A')}\n"
            f"Difficulty: {game_config.get('difficulty', 'N/A')}\n"
            f"Max Score: {game_config.get('max_score', 'N/A')}\n"
            f"Time Limit: {game_config.get('time_limit', 'N/A')} seconds"
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setProperty("secondary", True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # Sample button with primary styling
        play_button = QPushButton("Start Game")
        play_button.setProperty("primary", True)
        play_button.setFixedSize(200, 50)
        
        # Center the button
        button_layout = QVBoxLayout()
        button_layout.addWidget(play_button, alignment=Qt.AlignCenter)
        layout.addLayout(button_layout)
        
        layout.addStretch()
