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
        self.player_input.textChanged.connect(lambda text: self.add_player_btn.setEnabled(bool(text.strip())))
        self.add_player_btn.clicked.connect(lambda: (self.leaderboard_model.add_player(self.player_input.text().strip()), self.player_input.clear()))
        left_v.addWidget(self.player_input)
        left_v.addWidget(self.add_player_btn)
        left_v.addWidget(self.table)

        # Add Current Player label
        self.current_player_label = QLabel("Current Player: None")
        left_v.addWidget(self.current_player_label)

        left_widget = QWidget()
        left_widget.setLayout(left_v)

        # right: game
        self.game = GameWindow()

        h.addWidget(left_widget, 3)
        h.addWidget(self.game, 7)

        # Connect row selection → GameWindow
        self.table.selectionModel().selectionChanged.connect(self.on_player_selected)

    def on_player_selected(self, selected, deselected):
        if selected.indexes():
            row = selected.indexes()[0].row()
            player = self.leaderboard_model.players()[row]['player']
            self.game.set_current_player(player)
            self.current_player_label.setText(f"Current Player: {player}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())