"""PDF Page Size Finder — entry point.

Run from the PDF directory:
    python main.py
"""

import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from config.settings import APP_NAME, CONTROL_FONT_FAMILIES
from view.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app_font = QFont()
    app_font.setFamilies(CONTROL_FONT_FAMILIES)
    app.setFont(app_font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
