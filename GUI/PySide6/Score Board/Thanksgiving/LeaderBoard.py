# LeaderBoard.py
import sys
import json
from pathlib import Path
from operator import itemgetter

from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex, Slot,
    QSortFilterProxyModel, QSize
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QTableView, QLineEdit, QPushButton,
    QGridLayout, QSplitter, QLabel, QMessageBox,
    QHeaderView, QAbstractItemView, QHBoxLayout as QHLayout
)
from PySide6.QtGui import (
    QColor, QBrush, QFont, QGuiApplication,
    QAction, QKeySequence, QIcon, QPixmap, QPainter, QPen
)


SCORES_FILE = Path(__file__).parent / "scores.json"
BUTTON_SIZE = 70  # px (kept in sync with pixmap size)


class LeaderboardModel(QAbstractTableModel):
    """Model for the leaderboard: list of dicts with 'player','score','rank','is_selected'."""

    RANK, PLAYER, SCORE = 0, 1, 2
    HEADER_LABELS = ["Rank", "Player", "Score"]

    def __init__(self, players_data=None, parent=None):
        super().__init__(parent)
        self._players = players_data[:] if players_data else []
        self.sort_data()

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
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def sort_data(self):
        """Sort by score (desc) then player name (asc). Recalculate ranks and notify view."""
        # stable sort: secondary key first
        players = sorted(self._players, key=itemgetter('player'))
        players = sorted(players, key=itemgetter('score'), reverse=True)

        for i, p in enumerate(players):
            p['rank'] = i + 1

        self.beginResetModel()
        self._players = players
        self.endResetModel()

        if self.rowCount() > 0:
            self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount() - 1, self.columnCount() - 1))

    @Slot(str)
    def add_player(self, name):
        if not name:
            return
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
        self.sort_data()

    @Slot(str)
    def set_selected_player(self, player_name: str):
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
        if not self._players:
            return
        self.beginResetModel()
        for p in self._players:
            p['score'] = 0
            p['is_selected'] = False
            p['rank'] = 0
        self.endResetModel()
        self.sort_data()


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thanksgiving Family Game 🦃")
        self.setGeometry(100, 100, 1000, 640)

        # controller state
        self.clicked_numbers = set()
        self.current_player_name = "None"
        self._last_action = None  # dict holding undo info: {'player','points','number'}

        # UI setup
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # create/load players and state from disk if available
        players_from_file, clicked_from_file = self._load_state()

        initial_players = players_from_file if players_from_file is not None else [
            {'player': 'Leo', 'score': 15, 'rank': 0, 'is_selected': False},
            {'player': 'Amy', 'score': 20, 'rank': 0, 'is_selected': False},
            {'player': 'Chris', 'score': 15, 'rank': 0, 'is_selected': False},
        ]

        self.model = LeaderboardModel(initial_players)

        # left: leaderboard + controls
        self.leaderboard_widget = self._create_leaderboard_widget()
        splitter.addWidget(self.leaderboard_widget)

        # right: game grid
        self.game_grid_widget = self._create_game_grid_widget()
        splitter.addWidget(self.game_grid_widget)

        splitter.setSizes([360, 640])

        # menu actions
        self._create_actions()

        # apply loaded board state (if any)
        if clicked_from_file:
            self.clicked_numbers = set(clicked_from_file)
            for n in self.clicked_numbers:
                btn = self.grid_buttons.get(n)
                if btn:
                    btn.setEnabled(False)
                    btn.setIcon(self._make_icon(n, used=True))
                    btn.setIconSize(QSize(BUTTON_SIZE, BUTTON_SIZE))

    # ---------- persistence ----------
    def _load_state(self):
        """Return (players_list_or_None, clicked_numbers_or_None)."""
        if not SCORES_FILE.exists():
            return None, None
        try:
            with SCORES_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            players = data.get("players")
            clicked = data.get("clicked_numbers", [])
            # Ensure structure is correct
            if players and isinstance(players, list):
                # normalize dicts to include required keys
                players_norm = []
                for p in players:
                    players_norm.append({
                        'player': p.get('player', ''),
                        'score': p.get('score', 0),
                        'rank': p.get('rank', 0),
                        'is_selected': p.get('is_selected', False)
                    })
                return players_norm, clicked
            return None, clicked
        except Exception:
            return None, None

    def _save_state(self):
        """Save players and clicked numbers to JSON file."""
        try:
            players_to_save = [
                {
                    'player': p.get('player', ''),
                    'score': p.get('score', 0),
                    'rank': p.get('rank', 0),
                    'is_selected': p.get('is_selected', False)
                } for p in self.model._players
            ]
            data = {
                'players': players_to_save,
                'clicked_numbers': list(self.clicked_numbers)
            }
            with SCORES_FILE.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("Failed to save state:", e)

    # ---------- actions & UI ----------
    def _create_actions(self):
        reset_action = QAction("Reset Game", self)
        reset_action.setShortcut(QKeySequence("Ctrl+R"))
        reset_action.triggered.connect(self._reset_game)
        self.addAction(reset_action)

        undo_action = QAction("Undo Last", self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(self._undo_last)
        self.addAction(undo_action)

    def _create_leaderboard_widget(self):
        container = QWidget()
        vbox = QVBoxLayout(container)

        # Search box and proxy model
        search_h = QWidget()
        sh_layout = QHLayout()
        search_h.setLayout(sh_layout)
        sh_layout.addWidget(QLabel("Search:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Filter by player name...")
        sh_layout.addWidget(self.search_box)
        vbox.addWidget(search_h)

        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setFilterKeyColumn(LeaderboardModel.PLAYER)

        self.table_view = QTableView()
        self.table_view.setModel(self.proxy)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSortingEnabled(True)  # allow clicking headers to sort
        vbox.addWidget(self.table_view)

        # Connect search -> proxy
        self.search_box.textChanged.connect(self.proxy.setFilterFixedString)

        # when selection changes on proxy view, map to source index
        sel_model = self.table_view.selectionModel()
        sel_model.currentChanged.connect(self._on_table_current_changed)

        # Controls area
        ctrl = QWidget()
        ctrl_layout = QVBoxLayout(ctrl)

        add_h = QWidget()
        add_h_layout = QHLayout()
        add_h.setLayout(add_h_layout)

        self.player_name_input = QLineEdit()
        self.player_name_input.setPlaceholderText("Enter Player Name")
        self.add_player_btn = QPushButton("➕ Add Player")
        self.add_player_btn.setEnabled(False)
        self.add_player_btn.clicked.connect(self._add_player)

        add_h_layout.addWidget(self.player_name_input)
        add_h_layout.addWidget(self.add_player_btn)
        ctrl_layout.addWidget(add_h)

        # Enable add button only when text present
        self.player_name_input.textChanged.connect(lambda text: self.add_player_btn.setEnabled(bool(text.strip())))

        status_h = QWidget()
        status_layout = QHLayout()
        status_h.setLayout(status_layout)
        status_layout.addWidget(QLabel("Current Player:"))
        self.current_player_label = QLabel("None")
        self.current_player_label.setStyleSheet("font-weight: bold; color: blue;")
        status_layout.addWidget(self.current_player_label)

        # reset + undo buttons
        btns = QWidget()
        btns_layout = QHLayout()
        btns.setLayout(btns_layout)
        self.reset_btn = QPushButton("🔄 Reset Game")
        self.reset_btn.clicked.connect(self._reset_game)
        self.undo_btn = QPushButton("↩ Undo")
        self.undo_btn.clicked.connect(self._undo_last)
        self.undo_btn.setEnabled(False)

        btns_layout.addWidget(self.reset_btn)
        btns_layout.addWidget(self.undo_btn)
        status_layout.addWidget(btns)

        ctrl_layout.addWidget(status_h)
        vbox.addWidget(ctrl)

        return container

    def _create_game_grid_widget(self):
        container = QWidget()
        vbox = QVBoxLayout(container)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(6)

        self.grid_buttons = {}
        for i in range(6):
            for j in range(6):
                number = i * 6 + j + 1
                btn = QPushButton()
                btn.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                btn.setIcon(self._make_icon(number, used=False))
                btn.setIconSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
                font = QFont()
                font.setBold(True)
                font.setPointSize(10)
                btn.setFont(font)
                btn.clicked.connect(lambda checked, n=number: self._handle_grid_click(n))
                grid_layout.addWidget(btn, i, j)
                self.grid_buttons[number] = btn

        vbox.addLayout(grid_layout)
        return container

    # ---------- drawing icons ----------
    def _make_icon(self, number: int, used: bool = False) -> QIcon:
        """Create a QIcon with the number drawn. If used=True draw an 'X' overlay."""
        size = BUTTON_SIZE
        pix = QPixmap(size, size)
        pix.fill(QColor("transparent"))
        p = QPainter(pix)

        # background circle
        radius = size // 2 - 2
        center = (size // 2, size // 2)
        bg_color = QColor("#FFFFFF") if not used else QColor("#E0E0E0")
        pen = QPen(QColor("#2C3E50"))
        pen.setWidth(2)
        p.setPen(pen)
        p.setBrush(bg_color)
        p.drawEllipse(center[0] - radius, center[1] - radius, radius * 2, radius * 2)

        # number text
        p.setPen(QPen(QColor("#2C3E50")))
        f = QFont()
        f.setBold(True)
        f.setPointSize(18)
        p.setFont(f)
        txt = str(number)
        rect = pix.rect()
        p.drawText(rect, Qt.AlignCenter, txt)

        if used:
            # draw an X overlay
            pen_x = QPen(QColor("#8B0000"))
            pen_x.setWidth(4)
            p.setPen(pen_x)
            offset = size * 0.22
            p.drawLine(int(offset), int(offset), int(size - offset), int(size - offset))
            p.drawLine(int(size - offset), int(offset), int(offset), int(size - offset))

        p.end()
        return QIcon(pix)

    # ---------- model/view interactions ----------
    @Slot()
    def _add_player(self):
        name = self.player_name_input.text().strip()
        if not name:
            return
        self.model.add_player(name)
        self.player_name_input.clear()
        self.add_player_btn.setEnabled(False)
        # select the newly added player in proxy view
        # find the source row
        for src_row, p in enumerate(self.model._players):
            if p['player'] == name:
                src_idx = self.model.index(src_row, LeaderboardModel.PLAYER)
                proxy_idx = self.proxy.mapFromSource(src_idx)
                self.table_view.setCurrentIndex(proxy_idx)
                break
        self._save_state()

    @Slot("QModelIndex", "QModelIndex")
    def _on_table_current_changed(self, current, previous):
        # 'current' is proxy index; map to source to get player
        if not current.isValid():
            self._set_current_player("None")
            return
        src_idx = self.proxy.mapToSource(current)
        player_name = self.model.data(src_idx, Qt.ItemDataRole.DisplayRole)
        if player_name:
            self._set_current_player(player_name)
        else:
            self._set_current_player("None")

    def _set_current_player(self, player_name: str):
        self.current_player_name = player_name
        self.current_player_label.setText(player_name)
        self.model.set_selected_player(player_name)

    @Slot(int)
    def _handle_grid_click(self, points: int):
        if self.current_player_name == "None":
            QMessageBox.warning(self, "Player Not Selected", "Please select a player from the leaderboard first!")
            return
        if points in self.clicked_numbers:
            return

        # update model (score)
        # record previous state for undo
        prev_score = None
        for p in self.model._players:
            if p['player'] == self.current_player_name:
                prev_score = p.get('score', 0)
                break

        self.model.update_score(self.current_player_name, points)

        # update UI button
        btn = self.grid_buttons.get(points)
        if btn:
            btn.setEnabled(False)
            btn.setIcon(self._make_icon(points, used=True))
            btn.setIconSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
            btn.update()

        # record last action for undo
        self._last_action = {
            'player': self.current_player_name,
            'points': points,
            'number': points,
            'prev_score': prev_score
        }
        self.undo_btn.setEnabled(True)

        # mark clicked and save
        self.clicked_numbers.add(points)
        self._save_state()

    @Slot()
    def _undo_last(self):
        if not self._last_action:
            return
        act = self._last_action
        player = act['player']
        pts = act['points']
        num = act['number']
        prev = act.get('prev_score')

        # restore player score (set to prev_score if available, otherwise subtract)
        found = False
        for p in self.model._players:
            if p['player'] == player:
                if prev is not None:
                    p['score'] = prev
                else:
                    p['score'] = p.get('score', 0) - pts
                found = True
                break
        if found:
            # notify model/view
            self.model.sort_data()

        # re-enable button
        btn = self.grid_buttons.get(num)
        if btn:
            btn.setEnabled(True)
            btn.setIcon(self._make_icon(num, used=False))
            btn.setIconSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
            btn.update()

        # remove from clicked set and save
        if num in self.clicked_numbers:
            self.clicked_numbers.remove(num)
        self._last_action = None
        self.undo_btn.setEnabled(False)
        self._save_state()

    @Slot()
    def _reset_game(self):
        if QMessageBox.question(self, "Reset Game",
                                "Are you sure you want to reset all scores and clear the board?",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) != QMessageBox.Yes:
            return

        # reset model scores
        self.model.reset_scores()
        # clear clicked numbers and re-enable buttons
        self.clicked_numbers.clear()
        for n, btn in self.grid_buttons.items():
            btn.setEnabled(True)
            btn.setIcon(self._make_icon(n, used=False))
            btn.setIconSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
            btn.update()

        # clear current selection and controller state
        self.table_view.clearSelection()
        self._set_current_player("None")

        # clear undo
        self._last_action = None
        self.undo_btn.setEnabled(False)

        # repaint grid widget to satisfy style engines
        self.game_grid_widget.update()

        # save
        self._save_state()
        print("Game state reset successfully.")

if __name__ == '__main__':
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = GameWindow()
    w.show()
    sys.exit(app.exec())
