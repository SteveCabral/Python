# game_window.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Slot, Qt

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

    def set_current_player(self, player: str):
        self.current_player = player
        self.model.set_selected(player)


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