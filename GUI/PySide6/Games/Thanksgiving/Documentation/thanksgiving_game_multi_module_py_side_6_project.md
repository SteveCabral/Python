# ThanksgivingGame — Multi-module PySide6 Project

This canvas contains a multi-file PySide6 project (Option B) for your Wheel-of-Fortune–style Thanksgiving family game. Save each code block into a separate `.py` file (filenames shown). Run `python main.py` to start the app.

---

## Project structure

```
thanksgiving_game/
├─ main.py
├─ config.py
├─ phrase_manager.py
├─ leaderboard.py
├─ widgets/
│  ├─ phrase_grid.py
│  └─ letter_buttons.py
└─ game_window.py
```

---

### File: `config.py`
```python
# config.py
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "phrases": [
        {"phrase": "A FUN FAMILY GAME", "category": "EVENT"},
        {"phrase": "GIVE THANKS", "category": "HOLIDAY"}
    ],
    "points": {chr(c): 5 for c in range(ord('A'), ord('Z')+1)}
}

CONFIG_FILE = Path(__file__).parent / 'game_config.json'


def load_config(path: Path = CONFIG_FILE):
    if not path.exists():
        save_config(DEFAULT_CONFIG, path)
        return DEFAULT_CONFIG
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    # validate minimal structure
    data.setdefault('phrases', [])
    data.setdefault('points', {chr(c): 5 for c in range(ord('A'), ord('Z')+1)})
    return data


def save_config(data: dict, path: Path = CONFIG_FILE):
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
```

---

### File: `phrase_manager.py`
```python
# phrase_manager.py
from dataclasses import dataclass
from typing import List, Optional

MAX_LEN = 52

@dataclass
class Phrase:
    phrase: str
    category: str
    available: bool = True


class PhraseManager:
    def __init__(self, phrases_config: List[dict]):
        self._phrases = []
        for p in phrases_config:
            text = p.get('phrase', '').strip()
            cat = p.get('category', '').strip()
            if len(text) > MAX_LEN:
                raise ValueError(f"Phrase too long ({len(text)}): {text}")
            self._phrases.append(Phrase(text.upper(), cat.upper(), True))

    def all_phrases(self):
        return list(self._phrases)

    def next_available(self) -> Optional[Phrase]:
        for p in self._phrases:
            if p.available:
                return p
        return None

    def mark_unavailable(self, phrase: Phrase):
        for p in self._phrases:
            if p.phrase == phrase.phrase and p.category == phrase.category:
                p.available = False
                return
```

---

### File: `leaderboard.py`
```python
# leaderboard.py
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Slot
from operator import itemgetter

class LeaderboardModel(QAbstractTableModel):
    RANK, PLAYER, SCORE, PLAYED = range(4)
    HEADERS = ['Rank', 'Player', 'Score', 'Played']

    def __init__(self, players=None, parent=None):
        super().__init__(parent)
        self._players = players[:] if players else []
        self._recalculate()

    def rowCount(self, parent=QModelIndex()):
        return len(self._players)

    def columnCount(self, parent=QModelIndex()):
        return 4

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        r = index.row()
        c = index.column()
        p = self._players[r]
        if role == Qt.ItemDataRole.DisplayRole:
            if c == self.RANK:
                return p['rank']
            if c == self.PLAYER:
                return p['player']
            if c == self.SCORE:
                return p['score']
            if c == self.PLAYED:
                return 'Yes' if p.get('played', False) else 'No'
        if role == Qt.ItemDataRole.BackgroundRole and p.get('is_selected'):
            from PySide6.QtGui import QBrush, QColor
            return QBrush(QColor('#D6EAF8'))
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def _recalculate(self):
        # sort by score desc, name asc
        self._players = sorted(self._players, key=itemgetter('player'))
        self._players = sorted(self._players, key=itemgetter('score'), reverse=True)
        for i, p in enumerate(self._players):
            p['rank'] = i + 1

    @Slot(str)
    def add_player(self, name: str):
        if not name.strip():
            return
        if name.lower() in (p['player'].lower() for p in self._players):
            return
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._players.append({'player': name, 'score': 0, 'played': False, 'is_selected': False, 'rank': 0})
        self.endInsertRows()
        self._recalculate()
        self.layoutChanged.emit()

    @Slot(str, int)
    def update_score(self, player: str, points: int):
        for p in self._players:
            if p['player'] == player:
                p['score'] += points
                p['played'] = True
                break
        self._recalculate()
        if self.rowCount() > 0:
            self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount()-1, self.columnCount()-1))

    @Slot(str)
    def set_selected(self, player: str):
        changed = False
        for p in self._players:
            new = (p['player'] == player)
            if p.get('is_selected') != new:
                p['is_selected'] = new
                changed = True
        if changed:
            self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount()-1, self.columnCount()-1))

    def players(self):
        return list(self._players)
```

---

### File: `widgets/phrase_grid.py`
```python
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
        # replace any matching letters in cells with white background
        for r, row in enumerate(self.cells):
            for c, lbl in enumerate(row):
                if lbl.text().upper() == letter:
                    lbl.setStyleSheet('background-color: white; border: 1px solid #AAB7B8;')
```

---

### File: `widgets/letter_buttons.py`
```python
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
```

---

### File: `game_window.py`
```python
# game_window.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Slot

from leaderboard import LeaderboardModel
from phrase_manager import PhraseManager
from widgets.phrase_grid import PhraseGridWidget
from widgets.letter_buttons import LetterButtonsWidget
from config import load_config


class GameWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.phrase_manager = PhraseManager(self.config.get('phrases', []))
        self.points_map = self.config.get('points', {})

        self.model = LeaderboardModel([])

        layout = QVBoxLayout(self)

        # phrase grid
        self.phrase_grid = PhraseGridWidget()
        layout.addWidget(self.phrase_grid)

        # category label
        self.category_label = QLabel('')
        self.category_label.setStyleSheet('background-color: #3498DB; color: black; font-weight: bold;')
        self.category_label.setFixedHeight(32)
        self.category_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.category_label)

        # letter buttons
        self.letters = LetterButtonsWidget(self.points_map)
        self.letters.letter_clicked.connect(self.on_letter)
        layout.addWidget(self.letters)

        # control buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton('Start Game')
        self.next_btn = QPushButton('Next Phrase')
        self.solve_btn = QPushButton('Solve')
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.solve_btn)
        layout.addLayout(btn_layout)

        self.start_btn.clicked.connect(self.start_game)
        self.next_btn.clicked.connect(self.next_phrase)
        self.solve_btn.clicked.connect(self.solve)

        self.current_phrase = None
        self.current_player = None

    @Slot()
    def start_game(self):
        # mark all available
        QMessageBox.information(self, 'Start', 'Game started. Click Next Phrase to load first phrase.')
        self.letters.reset()

    @Slot()
    def next_phrase(self):
        phrase = self.phrase_manager.next_available()
        if not phrase:
            QMessageBox.information(self, 'Info', 'No more available phrases.')
            return
        self.current_phrase = phrase
        self.phrase_grid.display_phrase(phrase.phrase)
        self.category_label.setText(phrase.category)
        self.letters.reset()
        QMessageBox.information(self, 'Pick Player', 'Please select the first player from the leaderboard.')

    @Slot(str)
    def on_letter(self, letter):
        if not self.current_player:
            QMessageBox.warning(self, 'No player', 'Select a player first from the leaderboard!')
            return
        # reveal letters and compute scoring
        occurrences = self.current_phrase.phrase.count(letter)
        if occurrences > 0:
            points = self.points_map.get(letter, 5) * occurrences
            self.model.update_score(self.current_player, points)
            self.phrase_grid.reveal_letter(letter)
        else:
            cost = self.points_map.get(letter, 5) * 0
            QMessageBox.information(self, 'Not found', f"Letter {letter} is not in phrase. Cost {cost}.")
            self.model.update_score(self.current_player, -cost)
        self.letters.disable_letter(letter)

    @Slot()
    def solve(self):
        # show dialog for user solution (left as exercise to use QInputDialog or custom dialog)
        pass
```

---

### File: `main.py`
```python
# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from game_window import GameWindow
from leaderboard import LeaderboardModel
from PySide6.QtWidgets import QTableView, QHeaderView, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Thanksgiving Family Game')
        self.resize(1200, 720)

        central = QWidget()
        self.setCentralWidget(central)
        h = QHBoxLayout(central)

        # left: leaderboard
        self.leaderboard_model = LeaderboardModel([])
        self.table = QTableView()
        self.table.setModel(self.leaderboard_model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_v = QVBoxLayout()
        left_v.addWidget(self.table)

        left_widget = QWidget()
        left_widget.setLayout(left_v)

        # right: game
        self.game = GameWindow()

        h.addWidget(left_widget, 3)
        h.addWidget(self.game, 7)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
```

---

# How to proceed

1. Copy each code block into its own `.py` file using the filenames indicated above. Create the `widgets/` folder and save the two widget files there.
2. Run `python main.py` from the project root.
3. I intentionally left the `solve` dialog stub so you can pick how you want the UX to work (QInputDialog vs custom dialog). If you'd like, I will implement it and wire the full flow (including awarding remaining unrevealed letter points).

Would you like me to now:

- (A) Generate the full implementation for `solve()` and polish UI interactions (player selection UI wired to leaderboard view)?
- (B) Create the file contents on disk here (I can prepare a downloadable zip)?
- (C) Implement multi-step undo and auto-save game state between sessions?

Pick one and I will continue and produce the next deliverable.

