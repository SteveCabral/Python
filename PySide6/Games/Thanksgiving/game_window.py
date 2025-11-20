# game_window.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox, QLineEdit
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QShortcut, QFont
from PySide6.QtCore import QTimer

from leaderboard import LeaderboardModel
from phrase_manager import PhraseManager
from widgets.phrase_grid import PhraseGridWidget
from widgets.letter_buttons import LetterButtonsWidget
from config import load_config


class GameWindow(QWidget):
    def __init__(self, leaderboard_model=None, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.phrase_manager = PhraseManager(self.config.get('phrases', []))
        self.points_map = self.config.get('points', {})

        # use shared leaderboard model when provided so score updates reflect in the main UI
        self.model = leaderboard_model if leaderboard_model is not None else LeaderboardModel([])

        layout = QVBoxLayout(self)

        # allow the widget to receive keyboard events for letter input
        self.setFocusPolicy(Qt.StrongFocus)

        # top header: current player + countdown timer (two columns)
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        # local current player label (also updated by MainWindow)
        self.current_player_label = QLabel('Current Player: None')
        # reduce header height so phrase grid gets more visual space
        self.current_player_label.setFixedHeight(20)
        header_layout.addWidget(self.current_player_label, 1)

        # timer display: fixed two-digit, monospace, bright red
        self.time_limit = int(self.config.get('time_limit', 20))
        self._time_remaining = self.time_limit
        self.timer_label = QLabel(f"{self._time_remaining:02d}")
        self.timer_label.setFixedWidth(64)
        self.timer_label.setAlignment(Qt.AlignCenter)
        # use the same large font for both labels (36pt); timer stays red
        from PySide6.QtGui import QFont
        # make current player slightly smaller while keeping timer large
        player_font = QFont('Consolas', 24)
        timer_font = QFont('Consolas', 36)
        self.current_player_label.setFont(player_font)
        self.timer_label.setFont(timer_font)
        self.timer_label.setStyleSheet('color: red; font-family: "Consolas", "Courier New", monospace; font-weight: bold; font-size: 36px;')
        header_layout.addWidget(self.timer_label)
        layout.addWidget(header)
        # shrink header height to roughly 1/4 of its natural size to give grid more space
        try:
            h = max(32, int(header.sizeHint().height() * 0.25))
            # double the header height as requested
            h = h * 2
            header.setFixedHeight(h)
            # make the child labels match the header height and font
            try:
                self.current_player_label.setFixedHeight(h)
            except Exception:
                pass
            try:
                self.timer_label.setFixedHeight(h)
            except Exception:
                pass
        except Exception:
            pass

        # phrase grid
        self.phrase_grid = PhraseGridWidget()
        layout.addWidget(self.phrase_grid)

        # timer logic
        self._timer = QTimer(self)
        self._timer.setInterval(1000) # 1 second
        self._timer.timeout.connect(self._tick)

        # category label
        self.category_label = QLabel('')
        self.category_label.setStyleSheet('background-color: #3498DB; color: black; font-weight: bold;')
        # set category font to 16pt
        try:
            self.category_label.setFont(QFont('Sans Serif', 16))
        except Exception:
            pass
        self.category_label.setFixedHeight(32)
        self.category_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.category_label)

        # Letter Selected Information Grid: shows last letter selection result
        self.letter_info_label = QLabel('')
        self.letter_info_label.setStyleSheet('background-color: #FFFFFF; color: black;')
        # set info font to 16pt
        try:
            self.letter_info_label.setFont(QFont('Sans Serif', 16))
        except Exception:
            pass
        self.letter_info_label.setFixedHeight(28)
        self.letter_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.letter_info_label)

        # letter buttons
        self.letters = LetterButtonsWidget(self.points_map)
        self.letters.letter_clicked.connect(self.on_letter)
        layout.addWidget(self.letters)

        # Create application-level shortcuts for A-Z that map to letter buttons.
        # Shortcuts ignore input when typing into a QLineEdit (e.g., player input).
        self._shortcuts = []
        for code in range(ord('A'), ord('Z') + 1):
            ch = chr(code)
            seq = QKeySequence(ch)
            sc = QShortcut(seq, self)
            sc.setContext(Qt.ApplicationShortcut)
            sc.activated.connect(lambda ch=ch: self._on_shortcut_letter(ch))
            self._shortcuts.append(sc)

        # control buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton('Start Game')
        self.next_btn = QPushButton('Next Phrase')
        self.next_player_btn = QPushButton('Next Player')
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.next_player_btn)
        layout.addLayout(btn_layout)

        self.start_btn.clicked.connect(self.start_game)
        self.next_btn.clicked.connect(self.next_phrase)
        self.next_player_btn.clicked.connect(self.next_player)
        # Next phrase is only allowed after the current phrase has been solved
        self.next_btn.setEnabled(False)

        self.current_phrase = None
        self.current_player = None

    def next_player(self):
        players = self.model.players()
        if not players:
            QMessageBox.information(self, 'No players', 'No players available. Add players first.')
            return
        # find current index
        if not self.current_player:
            next_idx = 0
        else:
            names = [p['player'] for p in players]
            try:
                idx = names.index(self.current_player)
                next_idx = (idx + 1) % len(names)
            except ValueError:
                next_idx = 0
        next_player = players[next_idx]['player']
        # Prefer delegating to parent to update both UI and game state
        try:
            parent = self.parent()
            if parent is not None and hasattr(parent, 'set_current_player'):
                parent.set_current_player(next_player)
                # ensure per-player countdown resets when advancing players
                try:
                    self._reset_timer()
                except Exception:
                    pass
                return
        except Exception:
            pass

        # Fallback: set current player locally and update parent UI if possible
        self.set_current_player(next_player)
        # ensure timer is reset for the newly selected player
        try:
            self._reset_timer()
        except Exception:
            pass
        try:
            parent = self.parent()
            if parent is not None:
                if hasattr(parent, 'current_player_label'):
                    parent.current_player_label.setText(f"Current Player: {next_player}")
                if hasattr(parent, 'table'):
                    parent.table.selectRow(next_idx)
        except Exception:
            pass

    def set_current_player(self, player: str):
        # centralize current-player selection handling here so all callers
        # (MainWindow row click, Next Player button) use the same logic
        self.current_player = player
        # update local label and restart countdown
        try:
            if player:
                self.current_player_label.setText(f"Current Player: {player}")
                self._reset_timer()
            else:
                self.current_player_label.setText('Current Player: None')
                self._timer.stop()
                self._time_remaining = self.time_limit
                self.timer_label.setText(f"{self._time_remaining:02d}")
        except Exception:
            pass


    @Slot()
    def start_game(self):
        # Reset everything to initial state and load first phrase
        # Reset leaderboard scores but keep existing players if any
        try:
            if hasattr(self.model, 'reset_scores') and self.model.rowCount() > 0:
                self.model.reset_scores()
            elif hasattr(self.model, 'reset'):
                # fallback: clear players if no reset_scores available
                self.model.reset()
        except Exception:
            pass

        # Reset phrase manager to initial config
        self.phrase_manager = PhraseManager(self.config.get('phrases', []))

        # Clear UI state
        try:
            self.phrase_grid.clear()
        except Exception:
            pass
        self.category_label.setText('')
        self.current_phrase = None
        self.current_player = None
        # reset local current player UI and timer
        try:
            self.current_player_label.setText('Current Player: None')
            self._timer.stop()
            self._time_remaining = self.time_limit
            self.timer_label.setText(f"{self._time_remaining:02d}")
        except Exception:
            pass
        # reset letter buttons
        self.letters.reset()
        # disable Next until a phrase is solved
        self.next_btn.setEnabled(False)

        # Clear current player label in parent window if present
        try:
            parent = self.parent()
            if parent is not None and hasattr(parent, 'current_player_label'):
                parent.current_player_label.setText('Current Player: None')
        except Exception:
            pass

        # Load the first phrase
        self.next_phrase()
        # ensure GameWindow has focus so keyboard presses are captured
        self.setFocus()

    def _on_shortcut_letter(self, ch: str):
        # Ignore shortcuts while typing in text inputs
        fw = self.focusWidget()
        if isinstance(fw, QLineEdit):
            return
        # Only act if a phrase is currently loaded
        if not self.current_phrase:
            return
        btn = self.letters.buttons.get(ch)
        if btn and btn.isEnabled():
            btn.click()

    @Slot()
    def next_phrase(self):
        # Reset the per-player "played" flag when moving to a new phrase
        try:
            if hasattr(self.model, 'reset_played_flags'):
                self.model.reset_played_flags()
        except Exception:
            pass

        phrase = self.phrase_manager.next_available()
        if not phrase:
            # No more phrases — end the game and show top players
            players = self.model.players()
            if players:
                top = players[:3]
                lines = [f"{p.get('rank', i+1)}. {p.get('player')} — {p.get('score', 0)}" for i, p in enumerate(top)]
                msg = 'No more available phrases. Game over.\n\nTop players:\n' + '\n'.join(lines)
            else:
                msg = 'No more available phrases. Game over.\n\nNo players were added.'
            QMessageBox.information(self, 'Game Over', msg)
            self.current_phrase = None
            self.next_btn.setEnabled(False)
            # disable all letter buttons when game is over
            for b in self.letters.buttons.values():
                b.setEnabled(False)
            return
        self.current_phrase = phrase
        self.phrase_grid.display_phrase(phrase.phrase)
        self.category_label.setText(phrase.category)
        self.letters.reset()
        # disable Next until phrase is solved
        self.next_btn.setEnabled(False)
        # move keyboard focus to the letters grid so A-Z presses map to letters
        try:
            self.letters.setFocus()
            # focus the first enabled letter button for clear visual focus
            for btn in self.letters.buttons.values():
                if btn.isEnabled():
                    btn.setFocus()
                    break
        except Exception:
            pass

    @Slot(str)
    def on_letter(self, letter):
        # reset the per-player countdown whenever a letter is pressed
        try:
            self._reset_timer()
        except Exception:
            pass

        if not self.current_player:
            QMessageBox.warning(self, 'No player', 'Select a player first from the leaderboard!')
            return
        
        # reveal letters and compute scoring
        occurrences = self.current_phrase.phrase.count(letter)
        if occurrences > 0:
            letter_points = self.points_map.get(letter, 5)
            points = letter_points * occurrences
            self.model.update_score(self.current_player, points)
            self.phrase_grid.reveal_letter(letter)
            # update the Letter Selected Information Grid
            try:
                self.letter_info_label.setText(f"Letter {letter} ({letter_points} point{'s' if letter_points != 1 else ''}) appears {occurrences} times. {self.current_player} gets {points}.")
            except Exception:
                pass
            # if all letters now revealed, mark phrase solved/unavailable
            if self.phrase_grid.is_fully_revealed():
                self.phrase_manager.mark_unavailable(self.current_phrase)
                # if there are no more phrases, end the game now
                if not self.phrase_manager.next_available():
                    self.end_game()
                    return
                # otherwise enable Next so user can advance to the following phrase
                self.next_btn.setEnabled(True)
                # determine current leader (top-ranked player)
                players = self.model.players()
                if players:
                    leader = players[0].get('player')
                else:
                    leader = 'No leader'
                QMessageBox.information(
                    self,
                    'Solved',
                    f"All letters revealed.\nPhrase solved by {self.current_player}.\nThe current leader is {leader}.\nClick Next Phrase to continue."
                )
        else:
            # apply penalty equal to the configured points for the letter
            cost = self.points_map.get(letter, 5)
            # update the Letter Selected Information Grid for miss
            try:
                self.letter_info_label.setText(f"Letter {letter} is not in the phrase. {self.current_player} loses {cost}.")
            except Exception:
                pass
            self.model.update_score(self.current_player, -cost)
        self.letters.disable_letter(letter)

    @Slot()
    def solve(self):
        # show dialog for user solution (left as exercise to use QInputDialog or custom dialog)
        pass

    def end_game(self):
        # Show game over dialog with top 3 players and disable controls
        players = self.model.players()
        if players:
            top = players[:3]
            lines = [f"{p.get('rank', i+1)}. {p.get('player')} — {p.get('score', 0)}" for i, p in enumerate(top)]
            msg = 'No more available phrases. Game over.\n\nTop players:\n' + '\n'.join(lines)
        else:
            msg = 'No more available phrases. Game over.\n\nNo players were added.'
        QMessageBox.information(self, 'Game Over', msg)
        self.current_phrase = None
        self.next_btn.setEnabled(False)
        for b in self.letters.buttons.values():
            b.setEnabled(False)
        try:
            self._timer.stop()
        except Exception:
            pass

    def _reset_timer(self):
        try:
            self._timer.stop()
            self._time_remaining = self.time_limit
            self.timer_label.setText(f"{self._time_remaining:02d}")
            self._timer.start()
        except Exception:
            pass

    def _tick(self):
        try:
            if self._time_remaining > 0:
                self._time_remaining -= 1
                self.timer_label.setText(f"{self._time_remaining:02d}")
            if self._time_remaining <= 0:
                self._timer.stop()
        except Exception:
            pass