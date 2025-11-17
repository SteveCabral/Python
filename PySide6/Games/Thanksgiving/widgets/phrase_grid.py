# widgets/phrase_grid.py
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

CAPACITY = [12, 14, 14, 12]

def split_phrase_into_rows(phrase: str):
    words = phrase.split(' ')
    rows = [''] * 4
    idx = 0
    for w in words:
        candidate = (rows[idx] + ' ' + w) if rows[idx] else w
        if len(candidate) <= CAPACITY[idx]:
            rows[idx] = candidate
        else:
            idx += 1
            if idx >= 4:
                break
            rows[idx] = w
    rows = [r.ljust(CAPACITY[i]) for i, r in enumerate(rows)]
    return rows

class PhraseGridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.grid.setSpacing(4)
        self.cells = []
        font = QFont('Sans Serif', 12)
        for r, cap in enumerate(CAPACITY):
            row_cells = []
            for c in range(cap):
                lbl = QLabel(' ')
                lbl.setFixedSize(28, 28)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet('background-color: #A9DFBF; border: 1px solid #7DCEA0;')
                lbl.setFont(font)
                self.grid.addWidget(lbl, r, c)
                row_cells.append(lbl)
            self.cells.append(row_cells)

    def display_phrase(self, phrase: str):
        rows = split_phrase_into_rows(phrase)
        for r, text in enumerate(rows):
            for c, ch in enumerate(text):
                lbl = self.cells[r][c]
                if ch == ' ':
                    lbl.setText(' ')
                    lbl.setStyleSheet('background-color: #A9DFBF; border: 1px solid #7DCEA0;')
                else:
                    lbl.setText(ch.upper())
                    lbl.setStyleSheet('background-color: white; border: 1px solid #AAB7B8;')

    def reveal_letter(self, letter: str):
        letter = letter.upper()
        for row in self.cells:
            for lbl in row:
                if lbl.text().upper() == letter:
                    lbl.setStyleSheet('background-color: white; border: 1px solid #AAB7B8;')
