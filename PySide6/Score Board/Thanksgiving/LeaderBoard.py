# LeaderBoard.py
import sys
from operator import itemgetter
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex, Slot, Signal
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QTableView, QLineEdit, QPushButton,
    QGridLayout, QSplitter, QLabel, QMessageBox,
    QHeaderView, QAbstractItemView
)
from PySide6.QtGui import QColor, QBrush, QFont, QKeySequence, QGuiApplication, QAction


class LeaderboardModel(QAbstractTableModel):
    """Model for the leaderboard: list of dicts with 'player','score','rank','is_selected'."""

    RANK, PLAYER, SCORE = 0, 1, 2
    HEADER_LABELS = ["Rank", "Player", "Score"]

    def __init__(self, players_data=None, parent=None):
        super().__init__(parent)
        self._players = players_data[:] if players_data else []
        # ensure ranks are computed
        self.sort_data()

    # Required model methods
    def rowCount(self, parent=QModelIndex()):
        return len(self._players)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADER_LABELS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if not (0 <= row < len(self._players)):
            return None
        item = self._players[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.RANK:
                return item.get('rank', '')
            elif col == self.PLAYER:
                return item.get('player', '')
            elif col == self.SCORE:
                return item.get('score', 0)

        if role == Qt.ItemDataRole.BackgroundRole:
            if item.get('is_selected', False):
                return QBrush(QColor("#D6EAF8"))

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADER_LABELS[section]
        return super().headerData(section, orientation, role)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        # Player name and rank and score are selectable, but not editable
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    # --- Data manipulation API ---
    def sort_data(self):
        """Sort by score (desc) then player name (asc). Recalculate ranks and notify view."""
        if not self._players:
            return

        # stable sort: secondary key first
        players = sorted(self._players, key=itemgetter('player'))
        players = sorted(players, key=itemgetter('score'), reverse=True)

        # assign ranks
        for i, p in enumerate(players):
            p['rank'] = i + 1

        # Replace model data (emit appropriate signals)
        self.beginResetModel()
        self._players = players
        self.endResetModel()
        # data changed for values (covers display role)
        if self.rowCount() > 0:
            top_left = self.index(0, 0)
            bottom_right = self.index(self.rowCount() - 1, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right)

    @Slot(str)
    def add_player(self, name):
        if not name:
            return
        # prevent duplicates (case-insensitive)
        if name.lower() in (p['player'].lower() for p in self._players):
            return
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._players.append({'player': name, 'score': 0, 'rank': 0, 'is_selected': False})
        self.endInsertRows()
        self.sort_data()

    @Slot(str, int)
    def update_score(self, player_name: str, points: int):
        for player in self._players:
            if player['player'] == player_name:
                player['score'] = player.get('score', 0) + points
                break
        # After modifying values, re-sort and refresh
        self.sort_data()

    @Slot(str)
    def set_selected_player(self, player_name: str):
        """Set is_selected flags so the view may highlight the row."""
        changed = False
        for p in self._players:
            new_val = (p['player'] == player_name)
            if p.get('is_selected', False) != new_val:
                p['is_selected'] = new_val
                changed = True
        if changed and self.rowCount() > 0:
            self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount() - 1, self.columnCount() - 1))

    @Slot()
    def reset_scores(self):
        """Reset all scores and selections."""
        if not self._players:
            return
        # Use beginResetModel because we are evolving many rows at once
        self.beginResetModel()
        for p in self._players:
            p['score'] = 0
            p['is_selected'] = False
            p['rank'] = 0
        self.endResetModel()
        # recalc ranks (they'll all be zero then recalculated to 1..n after sort_data)
        self.sort_data()


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thanksgiving Family Game 🦃")
        self.setGeometry(100, 100, 900, 600)

        # controller state
        self.clicked_numbers = set()
        self.current_player_name = "None"

        # central widget + main layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # left: leaderboard
        self.leaderboard_container = self._create_leaderboard_widget()
        splitter.addWidget(self.leaderboard_container)

        # right: game grid
        self.game_grid_widget = self._create_game_grid_widget()
        splitter.addWidget(self.game_grid_widget)

        splitter.setSizes([320, 600])

        # menu / actions
        self._create_actions()

    def _create_actions(self):
        reset_action = QAction("Reset Game", self)
        reset_action.setShortcut(QKeySequence("Ctrl+R"))
        reset_action.triggered.connect(self._reset_game)
        self.addAction(reset_action)

    def _create_leaderboard_widget(self):
        initial_players = [
            {'player': 'Leo', 'score': 15, 'rank': 0, 'is_selected': False},
            {'player': 'Amy', 'score': 20, 'rank': 0, 'is_selected': False},
            {'player': 'Chris', 'score': 15, 'rank': 0, 'is_selected': False},
        ]
        self.model = LeaderboardModel(initial_players)

        container = QWidget()
        vbox = QVBoxLayout(container)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Use currentChanged to track the active row more directly
        sel_model = self.table_view.selectionModel()
        sel_model.currentChanged.connect(self._on_table_current_changed)

        vbox.addWidget(self.table_view)

        # controls
        ctrl_widget = QWidget()
        ctrl_layout = QVBoxLayout(ctrl_widget)

        h = QHBoxLayout()
        self.player_name_input = QLineEdit()
        self.player_name_input.setPlaceholderText("Enter Player Name")
        add_btn = QPushButton("➕ Add Player")
        add_btn.clicked.connect(self._add_player)
        h.addWidget(self.player_name_input)
        h.addWidget(add_btn)
        ctrl_layout.addLayout(h)

        status_h = QHBoxLayout()
        status_h.addWidget(QLabel("Current Player:"))
        self.current_player_label = QLabel("None")
        self.current_player_label.setStyleSheet("font-weight: bold; color: blue;")
        status_h.addWidget(self.current_player_label)

        reset_btn = QPushButton("🔄 Reset Game")
        reset_btn.clicked.connect(self._reset_game)
        status_h.addWidget(reset_btn)

        ctrl_layout.addLayout(status_h)

        vbox.addWidget(ctrl_widget)
        return container

    def _create_game_grid_widget(self):
        container = QWidget()
        # top-level vertical layout
        vbox = QVBoxLayout(container)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(6)

        self.grid_buttons = {}
        # make buttons 1..36
        for i in range(6):
            for j in range(6):
                number = i * 6 + j + 1
                btn = QPushButton(str(number))
                btn.setFixedSize(70, 70)
                f = QFont()
                f.setBold(True)
                f.setPointSize(14)
                btn.setFont(f)
                # connect with default argument to capture number
                btn.clicked.connect(lambda checked, n=number: self._handle_grid_click(n))
                grid_layout.addWidget(btn, i, j)
                self.grid_buttons[number] = btn

        vbox.addLayout(grid_layout)
        # keep a reference to the whole container so we can call .update() on reset
        return container

    # ---------- UI / Controller Methods ----------
    @Slot()
    def _add_player(self):
        name = self.player_name_input.text().strip()
        if not name:
            return
        self.model.add_player(name)
        self.player_name_input.clear()
        # select the newly added player
        new_row = self.model.rowCount() - 1
        if new_row >= 0:
            idx = self.model.index(new_row, LeaderboardModel.PLAYER)
            # select the row in the view
            self.table_view.setCurrentIndex(idx)

    @Slot("QModelIndex", "QModelIndex")
    def _on_table_current_changed(self, current, previous):
        # find player string at current row, column PLAYER
        if not current.isValid():
            self._set_current_player("None")
            return
        player_idx = current.siblingAtColumn(LeaderboardModel.PLAYER)
        player_name = self.model.data(player_idx, Qt.ItemDataRole.DisplayRole)
        if player_name:
            self._set_current_player(player_name)
        else:
            self._set_current_player("None")

    def _set_current_player(self, player_name):
        self.current_player_name = player_name
        self.current_player_label.setText(player_name)
        self.model.set_selected_player(player_name)

    @Slot(int)
    def _handle_grid_click(self, points: int):
        if self.current_player_name == "None":
            QMessageBox.warning(self, "Player Not Selected", "Please select a player from the leaderboard first!")
            return

        if points in self.clicked_numbers:
            # already clicked — ignore
            return

        # apply score and mark button used
        self.model.update_score(self.current_player_name, points)

        self.clicked_numbers.add(points)
        btn = self.grid_buttons.get(points)
        if btn:
            btn.setEnabled(False)
            # visually indicate disabled
            btn.setStyleSheet("background-color: lightgray;")
            # force a repaint to ensure styles update
            btn.update()

    @Slot()
    def _reset_game(self):
        if QMessageBox.question(self, "Reset Game",
                                "Are you sure you want to reset all scores and clear the board?",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) != QMessageBox.Yes:
            return

        # 1) Reset model data (scores + selection)
        self.model.reset_scores()

        # 2) Clear clicked numbers and re-enable buttons
        self.clicked_numbers.clear()
        for btn in self.grid_buttons.values():
            btn.setEnabled(True)
            btn.setStyleSheet("")  # remove any custom styles
            btn.update()

        # 3) Clear selection in view and controller state
        self.table_view.clearSelection()
        self._set_current_player("None")

        # 4) Force the grid widget to repaint (helps theme engines)
        self.game_grid_widget.update()
        print("Game state reset successfully.")

if __name__ == '__main__':
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = GameWindow()
    win.show()
    sys.exit(app.exec())
