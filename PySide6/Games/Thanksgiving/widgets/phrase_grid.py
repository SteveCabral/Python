# widgets/phrase_grid.py
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Helper to split phrase without breaking words into 4 rows (12,14,14,12 capacity)
CAPACITY = [12, 14, 14, 12]


def split_phrase_into_rows(phrase: str):
    words = phrase.split(' ')
    rows = [''] * 4
    idx = 0
    for w in words:
        if rows[idx]:
            candidate = rows[idx] + ' ' + w
        else:
            candidate = w
        if len(candidate) <= CAPACITY[idx]:
            rows[idx] = candidate
        else:
            idx += 1
            if idx >= 4:
                # shouldn't happen if phrase validated earlier
                break
            rows[idx] = w
    # pad with spaces for display consistent cells
    rows = [r.ljust(CAPACITY[i]) for i, r in enumerate(rows)]
    return rows


class PhraseGridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        # keep horizontal tight but increase vertical spacing between rows
        self.grid.setHorizontalSpacing(1)
        self.grid.setVerticalSpacing(6)
        self.cells = []
        # store underlying characters for each cell (None for empty/space)
        self._grid_chars = []
        # make boxes larger and font bigger to improve readability
        BOX_SIZE = 48
        FONT_SIZE = 18
        size = BOX_SIZE
        font = QFont('Sans Serif', FONT_SIZE)
        for r, cap in enumerate(CAPACITY):
            row_cells = []
            for c in range(cap):
                lbl = QLabel(' ')
                lbl.setFixedSize(size, size)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet('background-color: #A9DFBF; border: 1px solid #7DCEA0;')
                lbl.setFont(font)
                self.grid.addWidget(lbl, r, c)
                row_cells.append(lbl)
            self.cells.append(row_cells)
            self._grid_chars.append([None] * cap)

    def clear(self):
        """Clear the visible grid and underlying char storage."""
        for r, row in enumerate(self.cells):
            for c, lbl in enumerate(row):
                lbl.setText(' ')
                lbl.setStyleSheet('background-color: #A9DFBF; border: 1px solid #7DCEA0; color: black;')
                self._grid_chars[r][c] = None

    def display_phrase(self, phrase: str):
        rows = split_phrase_into_rows(phrase)
        # store underlying chars and show placeholders for unrevealed letters
        for r, text in enumerate(rows):
            for c, ch in enumerate(text):
                lbl = self.cells[r][c]
                if ch == ' ':
                    lbl.setText(' ')
                    lbl.setStyleSheet('background-color: #A9DFBF; border: 1px solid #7DCEA0; color: black;')
                    self._grid_chars[r][c] = None
                else:
                    # keep the real character in grid_chars, but display a placeholder
                    real = ch.upper()
                    self._grid_chars[r][c] = real
                    lbl.setText('_')
                    # show placeholder boxes with white background to indicate a letter slot
                    lbl.setStyleSheet('background-color: white; border: 1px solid #AAB7B8; color: black;')

    def reveal_letter(self, letter: str):
        letter = letter.upper()
        # replace any matching letters in cells with white background
        for r, row in enumerate(self.cells):
            for c, lbl in enumerate(row):
                real = self._grid_chars[r][c]
                if real is not None and real == letter:
                    lbl.setText(letter)
                    lbl.setStyleSheet('background-color: white; border: 1px solid #AAB7B8; color: black;')

    def is_fully_revealed(self) -> bool:
        """Return True if all underlying letters have been revealed in the grid."""
        for r, row in enumerate(self.cells):
            for c, lbl in enumerate(row):
                real = self._grid_chars[r][c]
                if real is not None:
                    if lbl.text().upper() != real:
                        return False
        return True