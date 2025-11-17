# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTableView, QHeaderView
from game_window import GameWindow
from leaderboard import LeaderboardModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Thanksgiving Family Game')
        self.resize(1200, 720)

        central = QWidget()
        self.setCentralWidget(central)
        h = QHBoxLayout(central)

        self.leaderboard_model = LeaderboardModel([])
        self.table = QTableView()
        self.table.setModel(self.leaderboard_model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_v = QVBoxLayout()
        left_v.addWidget(self.table)

        left_widget = QWidget()
        left_widget.setLayout(left_v)

        self.game = GameWindow()

        h.addWidget(left_widget, 3)
        h.addWidget(self.game, 7)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
