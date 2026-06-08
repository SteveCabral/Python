import sys
from dataclasses import dataclass
from typing import Dict, List

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QStatusBar,
    QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem
)

@dataclass
class Player:
    name: str
    scores: Dict[str, int]
    final_score: int = 0
    rank: int = 0

    def calculate_final_score(self):
        self.final_score = sum(self.scores.values())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(640, 480)

        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        self.games = ["Card Game", "Water Bottle", "In The Bag", "Bingo Game", "Password"]
        self.headers = ["Player", "Rank"] + self.games + ["Final Score"]

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.tableWidget)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 640, 33))
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Score Tracker", None))
        QMetaObject.connectSlotsByName(self)

        self.players: List[Player] = [
            Player("Alice", {game: 80 + i*2 for i, game in enumerate(self.games)}),
            Player("Bob", {game: 70 + i*3 for i, game in enumerate(self.games)}),
            Player("Charlie", {game: 90 - i*4 for i, game in enumerate(self.games)}),
        ]
        self.update_scores()
        self.tableWidget.cellChanged.connect(self.on_cell_changed)  # Signal to connect cell changes slot to update scores

    def update_scores(self):
        # Calculate final scores for each player
        for player in self.players:
            player.calculate_final_score()
        
        # Sort players by final score in descending order
        self.players.sort(key=lambda p: p.final_score, reverse=True)
        
        # Assign ranks based on sorted order
        for i, player in enumerate(self.players):
            player.rank = i + 1

        self.tableWidget.blockSignals(True)             # Prevent signals while updating the table
        self.tableWidget.setRowCount(len(self.players)) # Set the number of rows based on players

        for row, player in enumerate(self.players):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(player.name))
            flags = self.tableWidget.item(row, 0).flags()
            flags &= ~Qt.ItemIsEditable
            self.tableWidget.item(row, 0).setFlags(flags)

            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(player.rank)))
            flags = self.tableWidget.item(row, 1).flags()
            flags &= ~Qt.ItemIsEditable
            self.tableWidget.item(row, 1).setFlags(flags)

            for col, game in enumerate(self.games, start=2):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(player.scores.get(game, 0))))

            self.tableWidget.setItem(row, len(self.headers)-1, QTableWidgetItem(str(player.final_score)))
            flags = self.tableWidget.item(row, len(self.headers)-1).flags()
            flags &= ~Qt.ItemIsEditable
            self.tableWidget.item(row, len(self.headers)-1).setFlags(flags)
        self.tableWidget.blockSignals(False)    # Allow signals after updating the table

    # Slot for handling cell changes to update player scores
    def on_cell_changed(self, row, column):
        if column < 2 or column >= len(self.headers) - 1:
            return
        game = self.headers[column]
        try:
            new_score = int(self.tableWidget.item(row, column).text())
        except ValueError:
            new_score = 0

        player = self.players[row]
        player.scores[game] = new_score

        self.update_scores()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
