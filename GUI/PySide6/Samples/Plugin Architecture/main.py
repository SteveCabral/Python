from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QStackedWidget,
    QHBoxLayout, QListWidgetItem
)
from game_loader import load_games


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        # Left navigation list
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(200)

        # Right game window stack
        self.stack = QStackedWidget()

        layout.addWidget(self.nav_list)
        layout.addWidget(self.stack, 1)

        # Load games dynamically
        self.games = load_games()
        self.setup_games()

        # Hook list clicks to stack switching
        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)

    def setup_games(self):
        for game in self.games:

            # Add name to navigation list
            item = QListWidgetItem(game["name"])
            self.nav_list.addItem(item)

            # Instantiate and add game widget
            widget = game["widget_class"]()
            self.stack.addWidget(widget)


if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    win.resize(1000, 600)
    win.show()
    app.exec()
