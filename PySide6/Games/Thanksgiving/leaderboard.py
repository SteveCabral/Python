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

    def reset(self):
        """Clear all players and reset the model state."""
        from PySide6.QtCore import QModelIndex
        self.beginResetModel()
        self._players = []
        self.endResetModel()
        self.layoutChanged.emit()