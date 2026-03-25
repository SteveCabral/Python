"""FileShrinker — entry point.

Run from the FileShrinker directory:
    python main.py
"""

import sys

from PySide6.QtWidgets import QApplication

from view.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("FileShrinker")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
