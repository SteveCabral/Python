from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget
)

from game1 import Game1
from game2 import Game2


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Layout: LEFT = menu buttons, RIGHT = game window
        main_layout = QHBoxLayout(self)

        #
        # LEFT PANEL (menu)
        #
        menu_layout = QVBoxLayout()
        btn_game1 = QPushButton("Game 1")
        btn_game2 = QPushButton("Game 2")

        menu_layout.addWidget(btn_game1)
        menu_layout.addWidget(btn_game2)
        menu_layout.addStretch()

        #
        # RIGHT PANEL (stacked container)
        #
        self.stacked = QStackedWidget()
        self.stacked.addWidget(Game1())  # index 0
        self.stacked.addWidget(Game2())  # index 1

        #
        # Wiring buttons
        #
        btn_game1.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        btn_game2.clicked.connect(lambda: self.stacked.setCurrentIndex(1))

        #
        # Add everything to main layout
        #
        main_layout.addLayout(menu_layout, 1)      # 1/4 width
        main_layout.addWidget(self.stacked, 3)     # 3/4 width


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(900, 500)
    window.show()
    app.exec()

