# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel
from game_window import GameWindow
from leaderboard import LeaderboardModel
from PySide6.QtWidgets import QTableView, QHeaderView, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Thanksgiving Family Game')
        self.resize(1200, 720)

        central = QWidget()
        self.setCentralWidget(central)
        h = QHBoxLayout(central)

        # left: leaderboard
        self.leaderboard_model = LeaderboardModel([])
        self.table = QTableView()
        self.table.setModel(self.leaderboard_model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Highlight the whole row when clicked
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)

        left_v = QVBoxLayout()

        # Add Player input
        from PySide6.QtWidgets import QLineEdit, QPushButton
        self.player_input = QLineEdit()
        self.player_input.setPlaceholderText('Enter player name')
        self.add_player_btn = QPushButton('Add Player')
        self.add_player_btn.setEnabled(False)
        # enable button when there's text
        self.player_input.textChanged.connect(lambda text: self.add_player_btn.setEnabled(bool(text.strip())))

        # centralize add-player behavior so it can be triggered by button or Enter key
        def do_add_player():
            name = self.player_input.text().strip()
            if not name:
                return
            self.leaderboard_model.add_player(name)
            self.player_input.clear()
            self.player_input.setFocus()

        self.add_player_btn.clicked.connect(do_add_player)
        # allow pressing Enter in the input to add the player
        self.player_input.returnPressed.connect(do_add_player)
        left_v.addWidget(self.player_input)
        left_v.addWidget(self.add_player_btn)
        left_v.addWidget(self.table)

        # Add Current Player label
        self.current_player_label = QLabel("Current Player: None")
        left_v.addWidget(self.current_player_label)

        left_widget = QWidget()
        left_widget.setLayout(left_v)

        # right: game (pass shared leaderboard model so scores update in the table)
        self.game = GameWindow(self.leaderboard_model, self)

        h.addWidget(left_widget, 3)
        h.addWidget(self.game, 7)

        # Connect row selection → GameWindow
        self.table.selectionModel().selectionChanged.connect(self.on_player_selected)

        # Keep reference to left widget for potential future use
        self.left_widget = left_widget

    def on_player_selected(self, selected, deselected):
        if selected.indexes():
            row = selected.indexes()[0].row()
            player = self.leaderboard_model.players()[row]['player']
            # centralize setting current player so other code can call this
            self.set_current_player(player)
            # move keyboard focus to the letters grid when a player is chosen
            try:
                self.game.letters.setFocus()
            except Exception:
                pass

    def set_current_player(self, player: str):
        """Set the current player in the UI and model selection."""
        self.current_player_label.setText(f"Current Player: {player}")
        # ensure leaderboard model selection matches — block selection signals
        try:
            players = self.leaderboard_model.players()
            for i, p in enumerate(players):
                if p.get('player') == player:
                    sm = self.table.selectionModel()
                    if sm is not None:
                        sm.blockSignals(True)
                    self.table.selectRow(i)
                    if sm is not None:
                        sm.blockSignals(False)
                    break
        except Exception:
            pass
        # inform GameWindow of current player (no recursion from selection change)
        try:
            if hasattr(self, 'game') and self.game is not None:
                self.game.set_current_player(player)
        except Exception:
            pass

    def on_focus_changed(self, old, new):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec())