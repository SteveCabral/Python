from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config.user_preferences import user_prefs
from scores.score_manager import ScoreManager


class PlayersWidget(QWidget):
    players_changed = Signal()
    players_locked_changed = Signal(bool)

    def __init__(self, score_manager: ScoreManager):
        super().__init__()
        self._score_manager = score_manager

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Players")
        title.setProperty("title", True)
        layout.addWidget(title)

        subtitle = QLabel("Add players for family play. When ready, press Done to lock the roster.")
        subtitle.setProperty("secondary", True)
        layout.addWidget(subtitle)

        # Add controls
        add_row = QWidget()
        add_layout = QHBoxLayout(add_row)
        add_layout.setContentsMargins(0, 0, 0, 0)
        add_layout.setSpacing(8)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter player name")
        self.name_input.returnPressed.connect(self._on_enter_pressed)
        add_layout.addWidget(self.name_input, 1)

        self.add_btn = QPushButton("Add")
        self.add_btn.setFixedWidth(90)
        self.add_btn.clicked.connect(self._add_player)
        add_layout.addWidget(self.add_btn)

        self.done_btn = QPushButton("Done")
        self.done_btn.setFixedWidth(90)
        self.done_btn.clicked.connect(self._lock_players)
        add_layout.addWidget(self.done_btn)

        layout.addWidget(add_row)

        self.lock_status = QLabel("")
        self.lock_status.setProperty("secondary", True)
        layout.addWidget(self.lock_status)

        self.current_player_status = QLabel("")
        self.current_player_status.setProperty("secondary", True)
        layout.addWidget(self.current_player_status)

        # Player list
        self.player_list = QListWidget()
        self.player_list.setSortingEnabled(True)
        self.player_list.currentItemChanged.connect(self._on_current_player_changed)
        layout.addWidget(self.player_list, 1)

        self.refresh()

    def is_locked(self) -> bool:
        return bool(user_prefs.get("players_locked", False))

    def refresh(self) -> None:
        self._refresh_list()
        self._apply_lock_state()
        self._restore_current_player_selection()
        self._update_current_player_status()

    def _refresh_list(self) -> None:
        self.player_list.clear()
        for player in self._score_manager.list_players():
            item = QListWidgetItem(player.name)
            item.setData(Qt.UserRole, player.player_id)
            self.player_list.addItem(item)
        # With sorting enabled, items will be displayed alphabetically.

    def _apply_lock_state(self) -> None:
        locked = self.is_locked()
        self.name_input.setEnabled(not locked)
        self.add_btn.setEnabled(not locked)
        self.done_btn.setEnabled(not locked)

        if locked:
            self.lock_status.setText("Players are locked. Adding new players is disabled.")
        else:
            self.lock_status.setText("Players are not locked. You can add more.")

    def _restore_current_player_selection(self) -> None:
        """Ensure there is a selected active player when players exist."""
        if self.player_list.count() == 0:
            user_prefs.set("current_player_id", None)
            return

        current_player_id = user_prefs.get("current_player_id", None)
        if current_player_id:
            for i in range(self.player_list.count()):
                item = self.player_list.item(i)
                if item and item.data(Qt.UserRole) == current_player_id:
                    self.player_list.setCurrentRow(i)
                    return

        # Fall back to first player.
        self.player_list.setCurrentRow(0)
        first = self.player_list.currentItem()
        if first:
            user_prefs.set("current_player_id", first.data(Qt.UserRole))

    def _on_current_player_changed(self, current: Optional[QListWidgetItem], previous: Optional[QListWidgetItem]) -> None:
        _ = previous
        if current is None:
            user_prefs.set("current_player_id", None)
        else:
            user_prefs.set("current_player_id", current.data(Qt.UserRole))
        self._update_current_player_status()

    def _update_current_player_status(self) -> None:
        item = self.player_list.currentItem()
        if item is None:
            self.current_player_status.setText("Current player: (none)")
            return
        self.current_player_status.setText(f"Current player: {item.text()}")

    def _on_enter_pressed(self) -> None:
        # Enter key should behave like clicking Add.
        if self.add_btn.isEnabled():
            self.add_btn.click()

    def _add_player(self) -> None:
        if self.is_locked():
            return

        name = self.name_input.text().strip()
        if not name:
            return

        try:
            self._score_manager.ensure_player(name)
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Player", str(e))
            return

        self.name_input.clear()
        self.name_input.setFocus(Qt.OtherFocusReason)

        self._refresh_list()
        self._restore_current_player_selection()
        self._update_current_player_status()
        self.players_changed.emit()

    def _lock_players(self) -> None:
        if self.is_locked():
            return

        # Confirm intent.
        resp = QMessageBox.question(
            self,
            "Lock Players",
            "Done will lock the player list and disable adding new players. Continue?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if resp != QMessageBox.Yes:
            return

        user_prefs.set("players_locked", True)
        self._apply_lock_state()
        self.players_locked_changed.emit(True)
