# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from game_window import GameWindow
from leaderboard import LeaderboardModel
from PySide6.QtWidgets import QTableView, QHeaderView, QVBoxLayout, QSizePolicy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Thanksgiving Family Game V1.2')
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
        self.player_input.setStyleSheet("""
            QLineEdit {
                border-style: none;
            }
            QLineEdit:focus { /* Style when the QLineEdit is in focus */
                border-style: solid;
                border-color: green;
            }
        """)
        self.add_player_btn = QPushButton('Add Player')
        self.add_player_btn.setEnabled(False)
        self.add_player_btn.setStyleSheet("""
            QPushButton {
                background-color: #d2b2f4; /* Dark gray background */
                color: black; /* Light gray text */
                border: 1px solid #555555; /* Slightly lighter border for subtle definition */
                padding: 4px 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #444444; /* Slightly lighter on hover */
            }
            QPushButton:pressed {
                background-color: #a88ec3; /* Slightly darker when pressed */
            }
        """)
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

        # Leaderboard title label (same width as player list area)
        from PySide6.QtGui import QFont
        self.leaderboard_label = QLabel('LeaderBoard')
        try:
            self.leaderboard_label.setFont(QFont('Sans Serif', 16))
        except Exception:
            pass
        self.leaderboard_label.setAlignment(Qt.AlignCenter)

        left_v.addWidget(self.leaderboard_label)
        # Make the table expand to fill the space between the leaderboard label and
        # the Add Player controls at the bottom.
        try:
            self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        except Exception:
            pass
        left_v.addWidget(self.table, 1)
        # place add-player controls at bottom in a single-row container with border
        add_container = QWidget()
        add_layout = QHBoxLayout()
        add_layout.setContentsMargins(6, 6, 6, 6)
        add_layout.setSpacing(8)
        add_container.setLayout(add_layout)
        try:
            add_container.setStyleSheet("""
                QWidget {
                    border-width: 1px;
                    border-style: solid;
                    border-color: #CCCCCC;
                    border-radius: 4px; /* Optional: for rounded corners */
                    padding: 4px;
                }
                QWidget:focus { /* Style when the QLineEdit is in focus */
                    border-color: green;
                }
            """)
        except Exception:
            pass
        add_layout.addWidget(self.player_input)
        add_layout.addWidget(self.add_player_btn)
        left_v.addWidget(add_container)

        # Current Player label (kept as attribute but not shown in leaderboard)
        # The visible current player is displayed in the Game Window above the phrase grid,
        # so keep the attribute for programmatic updates but do not add it to the leaderboard layout.
        self.current_player_label = QLabel("Current Player: None")

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