from __future__ import annotations

from typing import List, Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from config.config_manager import config
from scores.score_manager import ScoreManager


class LeaderboardWidget(QWidget):
    def __init__(self, score_manager: ScoreManager):
        super().__init__()
        self._score_manager = score_manager

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Leaderboards")
        title.setProperty("title", True)
        layout.addWidget(title)

        subtitle = QLabel("Overall = sum of best-per-game. Per-game = best score per player.")
        subtitle.setProperty("secondary", True)
        layout.addWidget(subtitle)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, 1)

        self._build_overall_tab()
        self._build_game_tab()

        self.refresh()

    # -------------------------
    # Tabs
    # -------------------------

    def _build_overall_tab(self) -> None:
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(8)

        self.overall_table = QTableWidget(0, 2)
        self.overall_table.setHorizontalHeaderLabels(["Player", "Total"])
        self.overall_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.overall_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.overall_table.setSelectionMode(QTableWidget.SingleSelection)
        self.overall_table.setAlternatingRowColors(True)
        self.overall_table.verticalHeader().setVisible(False)
        self.overall_table.horizontalHeader().setStretchLastSection(True)
        page_layout.addWidget(self.overall_table, 1)

        self.tabs.addTab(page, "Overall")

    def _build_game_tab(self) -> None:
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(8)

        top = QWidget()
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(8)

        label = QLabel("Game:")
        label.setProperty("secondary", True)
        top_layout.addWidget(label)

        self.game_combo = QComboBox()
        self.game_combo.setMinimumWidth(240)
        self.game_combo.currentIndexChanged.connect(lambda: self.refresh())
        top_layout.addWidget(self.game_combo)

        top_layout.addStretch()
        page_layout.addWidget(top)

        self.game_table = QTableWidget(0, 2)
        self.game_table.setHorizontalHeaderLabels(["Player", "Best Score"])
        self.game_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.game_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.game_table.setSelectionMode(QTableWidget.SingleSelection)
        self.game_table.setAlternatingRowColors(True)
        self.game_table.verticalHeader().setVisible(False)
        self.game_table.horizontalHeader().setStretchLastSection(True)
        page_layout.addWidget(self.game_table, 1)

        self.tabs.addTab(page, "Per-Game")

    # -------------------------
    # Public API
    # -------------------------

    def refresh(self) -> None:
        self._refresh_game_combo_if_needed()
        self._refresh_overall_table()
        self._refresh_game_table()

    # -------------------------
    # Internal refresh helpers
    # -------------------------

    def _refresh_game_combo_if_needed(self) -> None:
        enabled = config.get_enabled_games()
        existing_ids = [self.game_combo.itemData(i) for i in range(self.game_combo.count())]

        if existing_ids == enabled:
            return

        current = self.game_combo.currentData()

        self.game_combo.blockSignals(True)
        self.game_combo.clear()
        for game_id in enabled:
            game_cfg = config.get_game_config(game_id)
            display = game_cfg.get("display_name", game_id)
            self.game_combo.addItem(str(display), game_id)

        if current:
            idx = self.game_combo.findData(current)
            if idx >= 0:
                self.game_combo.setCurrentIndex(idx)

        self.game_combo.blockSignals(False)

    def _refresh_overall_table(self) -> None:
        rows = self._score_manager.get_overall_leaderboard(limit=None)
        self.overall_table.setRowCount(len(rows))

        for r, (player, total) in enumerate(rows):
            name_item = QTableWidgetItem(player.name)
            total_item = QTableWidgetItem(str(total))
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.overall_table.setItem(r, 0, name_item)
            self.overall_table.setItem(r, 1, total_item)

        self.overall_table.resizeColumnsToContents()

    def _refresh_game_table(self) -> None:
        game_id = self.game_combo.currentData()
        if not game_id:
            self.game_table.setRowCount(0)
            return

        rows = self._score_manager.get_game_leaderboard(str(game_id), limit=None)
        self.game_table.setRowCount(len(rows))

        for r, (player, best) in enumerate(rows):
            name_item = QTableWidgetItem(player.name)
            best_item = QTableWidgetItem(str(best))
            best_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.game_table.setItem(r, 0, name_item)
            self.game_table.setItem(r, 1, best_item)

        self.game_table.resizeColumnsToContents()
