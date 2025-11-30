from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QListWidgetItem,
    QStackedWidget, QHBoxLayout
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from game_loader import load_games


class NavList(QListWidget):
    def __init__(self):
        super().__init__()

        self.setIconSize(QSize(24, 24))
        self.setFixedWidth(220)

        self.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: white;
                border: none;
                padding-top: 10px;
            }
            QListWidget::item {
                height: 40px;
                padding-left: 12px;
            }
            QListWidget::item:selected {
                background-color: #444444;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
        """)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        # Custom stylized nav list
        self.nav = NavList()

        # Stack of games
        self.stack = QStackedWidget()

        layout.addWidget(self.nav)
        layout.addWidget(self.stack, 1)

        # Load plugins
        self.games = load_games()
        self.load_games_into_ui()

        # Switch depending on navigation click
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)

        # Default select first item
        if self.nav.count() > 0:
            self.nav.setCurrentRow(0)

    def load_games_into_ui(self):
        for game in self.games:
            item = QListWidgetItem(game["name"])

            # Optional: Add icons for each game
            # item.setIcon(QIcon("path/to/icon.png"))

            self.nav.addItem(item)

            widget = game["widget_class"]()
            self.stack.addWidget(widget)


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.resize(1100, 600)
    w.show()
    app.exec()
