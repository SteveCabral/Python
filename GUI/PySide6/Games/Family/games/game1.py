from __future__ import annotations

import random
from typing import Any, Callable, Optional

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from config.config_manager import config

GAME_NAME = "Game One"

class Game(QWidget):
    def __init__(
        self,
        game_config: dict | None = None,
        score_reporter: Optional[Callable[[str, int, Optional[dict[str, Any]]], None]] = None,
        game_id: str | None = None,
    ):
        super().__init__()
        self._score_reporter = score_reporter
        self._game_id = game_id or "game1"

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Access game-specific configuration
        game_config = game_config or config.get_game_config("game1")
        self._max_score = int(game_config.get("max_score", 100) or 100)
        
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

        self._status_label = QLabel("Ready")
        self._status_label.setAlignment(Qt.AlignCenter)
        self._status_label.setProperty("secondary", True)
        layout.addWidget(self._status_label)
        
        layout.addStretch()
        
        # Sample button with primary styling
        play_button = QPushButton("Start Game")
        play_button.setProperty("primary", True)
        play_button.setFixedSize(200, 50)
        play_button.clicked.connect(self._on_start)
        
        # Center the button
        button_layout = QVBoxLayout()
        button_layout.addWidget(play_button, alignment=Qt.AlignCenter)
        layout.addLayout(button_layout)
        
        layout.addStretch()

    def _on_start(self) -> None:
        """Demo scoring hook: generate a random score and report it."""
        score = random.randint(0, max(self._max_score, 0))
        self._status_label.setText(f"Round complete. Score: {score}")

        if self._score_reporter:
            self._score_reporter(
                self._game_id,
                score,
                {
                    "mode": "demo",
                    "max_score": self._max_score,
                },
            )
