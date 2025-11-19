# widgets/letter_buttons.py
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

class LetterButtonsWidget(QWidget):
    letter_clicked = Signal(str)

    def __init__(self, points_map: dict, parent=None):
        super().__init__(parent)
        self.points = points_map
        # allow the widget to accept keyboard focus so focus can move here
        self.setFocusPolicy(Qt.StrongFocus)
        self.grid = QGridLayout(self)
        # tighten spacing: keep horizontal tighter, allow a bit vertical space
        try:
            self.grid.setHorizontalSpacing(4)
            self.grid.setVerticalSpacing(6)
        except Exception:
            pass
        self.buttons = {}
        letters = [chr(c) for c in range(ord('A'), ord('Z')+1)]
        COLS = 13
        for i, L in enumerate(letters):
            btn = QPushButton(L)
            # increase font size for readability
            btn.setFont(QFont('Sans Serif', 18))
            # reduce width to roughly half of the natural size
            try:
                w = btn.sizeHint().width()
                btn.setFixedWidth(max(16, int(w * 0.5)))
            except Exception:
                pass
            btn.clicked.connect(lambda checked, ch=L: self._on_click(ch))
            self.buttons[L] = btn
            self.grid.addWidget(btn, i // COLS, i % COLS)

    def _on_click(self, ch):
        self.letter_clicked.emit(ch)

    def reset(self):
        for b in self.buttons.values():
            b.setEnabled(True)

    def disable_letter(self, ch):
        btn = self.buttons.get(ch)
        if btn:
            btn.setEnabled(False)