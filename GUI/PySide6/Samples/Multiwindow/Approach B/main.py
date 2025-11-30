from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton
)

from game1 import Game1
from game2 import Game2


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)
        menu_layout = QVBoxLayout()

        # Buttons
        btn_game1 = QPushButton("Game 1")
        btn_game2 = QPushButton("Game 2")
        menu_layout.addWidget(btn_game1)
        menu_layout.addWidget(btn_game2)
        menu_layout.addStretch()

        # Placeholder for game
        self.game_container = QWidget()
        self.game_layout = QVBoxLayout(self.game_container)

        # Add to main layout
        main_layout.addLayout(menu_layout, 1)
        main_layout.addWidget(self.game_container, 3)

        # Wire up button clicks
        btn_game1.clicked.connect(lambda: self.show_game(Game1))
        btn_game2.clicked.connect(lambda: self.show_game(Game2))

    def show_game(self, game_class):
        # Clear current game screen
        while self.game_layout.count():
            widget = self.game_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # Add new game screen
        new_game = game_class()
        self.game_layout.addWidget(new_game)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(900, 500)
    window.show()
    app.exec()
