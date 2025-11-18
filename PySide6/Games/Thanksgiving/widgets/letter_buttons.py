# widgets/letter_buttons.py
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtCore import Signal

class LetterButtonsWidget(QWidget):
    letter_clicked = Signal(str)

    def __init__(self, points_map: dict, parent=None):
        super().__init__(parent)
        self.points = points_map
        self.grid = QGridLayout(self)
        self.buttons = {}
        letters = [chr(c) for c in range(ord('A'), ord('Z')+1)]
        for i, L in enumerate(letters):
            btn = QPushButton(L)
            btn.clicked.connect(lambda checked, ch=L: self._on_click(ch))
            self.buttons[L] = btn
            self.grid.addWidget(btn, i // 7, i % 7)

    def _on_click(self, ch):
        self.letter_clicked.emit(ch)

    def reset(self):
        for b in self.buttons.values():
            b.setEnabled(True)

    def disable_letter(self, ch):
        btn = self.buttons.get(ch)
        if btn:
            btn.setEnabled(False)