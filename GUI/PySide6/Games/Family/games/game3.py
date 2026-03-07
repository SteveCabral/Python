from __future__ import annotations

from typing import Any, Callable, Optional

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from config.config_manager import config

GAME_NAME = "Game Three"

class Game(QWidget):
    def __init__(
        self,
        game_config: dict | None = None,
        score_reporter: Optional[Callable[[str, int, Optional[dict[str, Any]]], None]] = None,
        game_id: str | None = None,
    ):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        game_config = game_config or config.get_game_config("game3")

        # Optional scoring callback (wired by main app)
        self._score_reporter = score_reporter
        self._game_id = game_id or "game3"

        title_label = QLabel("GAME 3")
        title_label.setProperty("title", True)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

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

        play_button = QPushButton("Start Game")
        play_button.setProperty("primary", True)
        play_button.setFixedSize(200, 50)

        button_layout = QVBoxLayout()
        button_layout.addWidget(play_button, alignment=Qt.AlignCenter)
        layout.addLayout(button_layout)

        layout.addStretch()
