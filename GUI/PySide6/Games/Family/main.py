from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QStackedWidget,
    QHBoxLayout, QListWidgetItem, QPushButton, QVBoxLayout, QLabel,
    QMessageBox
)
import inspect
from typing import Any, Callable, Optional
from game_loader import load_games
from config.config_manager import config
from config.user_preferences import user_prefs
from players.players_widget import PlayersWidget
from scores.score_manager import score_manager
from scores.leaderboard_widget import LeaderboardWidget
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

        # Built-in screens (must be added before games so indices match nav)
        self._add_leaderboard_screen()
        self._add_players_screen()

        # Load games dynamically
        self.games = load_games()
        self.setup_games()

        # Hook list clicks to stack switching
        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)

        # First-run UX: if there are no players yet, jump to Players setup.
        if score_manager.list_players() == []:
            self._show_players_screen()
    
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

        players_btn = QPushButton("Players")
        players_btn.setFixedWidth(90)
        players_btn.clicked.connect(self._show_players_screen)
        layout.addWidget(players_btn)

        leaderboard_btn = QPushButton("Leaderboard")
        leaderboard_btn.setFixedWidth(110)
        leaderboard_btn.clicked.connect(self._show_leaderboard_screen)
        layout.addWidget(leaderboard_btn)
        
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

    # -------------------------
    # Players + scoring
    # -------------------------

    def _get_current_player_id(self) -> Optional[str]:
        player_id = user_prefs.get("current_player_id", None)
        return str(player_id) if player_id else None

    def report_score(self, game_id: str, score: int, meta: Optional[dict[str, Any]] = None) -> None:
        """Callback for games to submit a completed round score."""
        player_id = self._get_current_player_id()
        if not player_id:
            QMessageBox.information(
                self,
                "Select a Player",
                "Add/select a player before recording scores. Use the Players screen to create players.",
            )
            return

        try:
            score_manager.record_score(player_id=player_id, game_id=game_id, score=int(score), meta=meta or {})
        except Exception as e:
            QMessageBox.warning(self, "Score Not Recorded", str(e))
            return

        if hasattr(self, "leaderboard_widget"):
            self.leaderboard_widget.refresh()

    def _add_leaderboard_screen(self) -> None:
        item = QListWidgetItem("Leaderboard")
        self.nav_list.addItem(item)

        self.leaderboard_widget = LeaderboardWidget(score_manager)
        self.stack.addWidget(self.leaderboard_widget)
        self._leaderboard_index = self.stack.count() - 1

    def _add_players_screen(self) -> None:
        item = QListWidgetItem("Players")
        self.nav_list.addItem(item)

        self.players_widget = PlayersWidget(score_manager)
        self.players_widget.players_changed.connect(self._on_players_changed)
        self.players_widget.players_locked_changed.connect(self._on_players_locked_changed)
        self.stack.addWidget(self.players_widget)
        self._players_index = self.stack.count() - 1

    def _show_players_screen(self) -> None:
        if hasattr(self, "players_widget"):
            self.players_widget.refresh()
        self.nav_list.setCurrentRow(getattr(self, "_players_index", 1))

    def _on_players_changed(self) -> None:
        # Selection is handled by PlayersWidget; nothing else needed here.
        return

    def _on_players_locked_changed(self, locked: bool) -> None:
        # Nothing to toggle in the top-bar anymore, but keep hook for future.
        _ = locked

    def _show_leaderboard_screen(self) -> None:
        if hasattr(self, "leaderboard_widget"):
            self.leaderboard_widget.refresh()
        self.nav_list.setCurrentRow(getattr(self, "_leaderboard_index", 0))
    
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
            widget = self._instantiate_game_widget(game)
            self.stack.addWidget(widget)

    def _instantiate_game_widget(self, game: dict) -> QWidget:
        """Instantiate a game widget, passing optional kwargs if supported.

        Supported optional kwargs for game widgets:
        - game_config: dict
        - score_reporter: callable(game_id: str, score: int, meta: dict | None)
        - game_id: str
        """
        widget_class = game["widget_class"]
        game_id = game.get("module_name")

        kwargs: dict[str, Any] = {}

        try:
            sig = inspect.signature(widget_class.__init__)
            params = sig.parameters
            accepts_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values())

            if accepts_kwargs or "game_config" in params:
                kwargs["game_config"] = game.get("config")
            if accepts_kwargs or "score_reporter" in params:
                kwargs["score_reporter"] = self.report_score
            if accepts_kwargs or "game_id" in params:
                kwargs["game_id"] = game_id
        except (TypeError, ValueError):
            # Builtins or unexpected signatures; fall back to try/except below.
            kwargs = {
                "game_config": game.get("config"),
                "score_reporter": self.report_score,
                "game_id": game_id,
            }

        # Attempt instantiation with decreasing kwargs.
        for attempt in (
            kwargs,
            {k: v for k, v in kwargs.items() if k in {"game_config"}},
            {},
        ):
            try:
                return widget_class(**attempt)
            except TypeError:
                continue

        # Last-resort: no kwargs
        return widget_class()


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
