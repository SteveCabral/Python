import sys
from operator import itemgetter
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex, Signal, Slot, QItemSelection
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, 
    QVBoxLayout, QTableView, QLineEdit, QPushButton, 
    QGridLayout, QSplitter, QLabel, QMessageBox,
    QHeaderView, QAbstractItemView
)
from PySide6.QtGui import QColor, QBrush, QFont, QGuiApplication

# --- 1. Leaderboard Data Model (QAbstractTableModel) ---
class LeaderboardModel(QAbstractTableModel):
    """A custom model to handle the game's player data and sorting logic."""
    
    RANK, PLAYER, SCORE = 0, 1, 2
    HEADER_LABELS = ["Rank", "Player", "Score"]

    def __init__(self, players_data, parent=None):
        super().__init__(parent)
        self._players = players_data
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

        item = self._players[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.RANK:
                return item['rank']
            elif col == self.PLAYER:
                return item['player']
            elif col == self.SCORE:
                return item['score']
        
        # --- VISUAL FEEDBACK (Highlighting Selected Player) ---
        if role == Qt.ItemDataRole.BackgroundRole and item.get('is_selected', False):
            return QBrush(QColor("#D6EAF8")) 
        
        if role == Qt.ItemDataRole.FlagsRole and col == self.PLAYER:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADER_LABELS[section]
        return None

    def sort_data(self):
        """Sorts the data based on score (descending) then player name (ascending, as tie-breaker)."""
        
        # 1. Stable sort by the secondary key (Player Name) in ascending order.
        sorted_players = sorted(
            self._players, 
            key=itemgetter('player'), 
            reverse=False 
        )
        
        # 2. Stable sort by the primary key (Score) in descending order.
        sorted_players = sorted(
            sorted_players, 
            key=itemgetter('score'), 
            reverse=True 
        )

        # 3. Assign Rank (starting at 1)
        for i, player in enumerate(sorted_players):
            player['rank'] = i + 1
        
        self._players = sorted_players
        
        self.layoutChanged.emit()

    @Slot(str)
    def add_player(self, name):
        """Adds a new player to the list and re-sorts."""
        if name.lower() in [p['player'].lower() for p in self._players]:
            return 
        
        self.beginInsertRows(QModelIndex(), len(self._players), len(self._players))
        self._players.append({'player': name, 'score': 0, 'rank': 0, 'is_selected': False}) 
        self.endInsertRows()
        
        self.sort_data()

    @Slot(str, int)
    def update_score(self, player_name, points):
        """Updates the score of a player and re-sorts."""
        player_found = False
        for player in self._players:
            if player['player'] == player_name:
                player['score'] += points
                player_found = True
                break
        
        if player_found:
            self.sort_data()

    @Slot(str)
    def set_selected_player(self, player_name):
        """Sets the 'is_selected' flag for the current player."""
        
        # Reset the selection flag for all players
        for player in self._players:
            player['is_selected'] = (player['player'] == player_name)
            
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount() - 1, self.columnCount() - 1))

    # --- FIX 1: Ensure sort_data is called to update the view after reset ---
    @Slot()
    def reset_scores(self):
        """Resets all player scores to 0."""
        for player in self._players:
            player['score'] = 0
            player['is_selected'] = False
        self.sort_data()

        # Force the view to repaint all score cells
        if self.rowCount() > 0:
            top_left = self.index(0, 0)
            bottom_right = self.index(self.rowCount() - 1, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right)


# --- 2. Main Application Window ---
class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thanksgiving Family Game 🦃")
        self.clicked_numbers = set()
        self.current_player_name = "None"
        
        self.setGeometry(100, 100, 900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.leaderboard_widget = self._create_leaderboard_widget()
        main_splitter.addWidget(self.leaderboard_widget)
        
        self.game_grid_widget = self._create_game_grid_widget()
        main_splitter.addWidget(self.game_grid_widget)
        
        main_splitter.setSizes([300, 600]) 

        layout = QHBoxLayout(central_widget)
        layout.addWidget(main_splitter)
        
        # Initial set for the label
        self.current_player_label.setText(self.current_player_name) 

    # (Other methods like _create_leaderboard_widget, _create_player_controls, 
    # and _create_game_grid_widget remain the same)
    def _create_leaderboard_widget(self):
        initial_players = [
            {'player': 'Leo', 'score': 15, 'rank': 0, 'is_selected': False},
            {'player': 'Amy', 'score': 20, 'rank': 0, 'is_selected': False},
            {'player': 'Chris', 'score': 15, 'rank': 0, 'is_selected': False},
        ]
        
        self.model = LeaderboardModel(initial_players)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table_view.selectionModel().selectionChanged.connect(self._select_player_from_table)
        
        self.player_controls = self._create_player_controls()
        
        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.table_view)
        left_vbox.addWidget(self.player_controls)

        leaderboard_container = QWidget()
        leaderboard_container.setLayout(left_vbox)
        return leaderboard_container

    def _create_player_controls(self):
        container = QWidget()
        vbox = QVBoxLayout(container)
        
        add_player_hbox = QHBoxLayout()
        self.player_name_input = QLineEdit()
        self.player_name_input.setPlaceholderText("Enter Player Name")
        
        add_button = QPushButton("➕ Add Player")
        add_button.clicked.connect(self._add_player)
        
        add_player_hbox.addWidget(self.player_name_input)
        add_player_hbox.addWidget(add_button)
        vbox.addLayout(add_player_hbox)

        status_hbox = QHBoxLayout()
        status_hbox.addWidget(QLabel("Current Player:"))
        
        self.current_player_label = QLabel("None") 
        self.current_player_label.setStyleSheet("font-weight: bold; color: blue;")
        status_hbox.addWidget(self.current_player_label)
        
        reset_button = QPushButton("🔄 Reset Game")
        reset_button.clicked.connect(self._reset_game)
        status_hbox.addWidget(reset_button)

        vbox.addLayout(status_hbox)

        return container
        
    def _create_game_grid_widget(self):
        container = QWidget()
        grid_layout = QGridLayout(container)
        
        self.grid_buttons = {} 

        for i in range(6):
            for j in range(6):
                number = (i * 6) + j + 1
                button = QPushButton(str(number))
                button.setFixedSize(70, 70) 
                
                font = QFont()
                font.setBold(True)
                font.setPointSize(14)
                button.setFont(font)

                self.grid_buttons[number] = button
                
                button.clicked.connect(lambda checked, val=number: self._handle_grid_click(val))
                
                grid_layout.addWidget(button, i, j)
        
        vbox = QVBoxLayout(container)
        vbox.addLayout(grid_layout)
        vbox.setAlignment(grid_layout, Qt.AlignmentFlag.AlignCenter)

        container.repaint()

        return container

    @Slot()
    def _add_player(self):
        player_name = self.player_name_input.text().strip()
        if player_name:
            self.model.add_player(player_name)
            self.player_name_input.clear()
            
            new_row = self.model.rowCount() - 1
            idx = self.model.index(new_row, 0)
            self.table_view.setCurrentIndex(idx)
            
    @Slot(QItemSelection, QItemSelection)
    def _select_player_from_table(self, selected, deselected): 
        indexes = selected.indexes()
        
        if indexes:
            player_index = indexes[0].siblingAtColumn(self.model.PLAYER)
            player_name = self.model.data(player_index)
            self._set_current_player(player_name)
        else:
            self._set_current_player("None")

    def _set_current_player(self, player_name):
        self.current_player_name = player_name
        self.current_player_label.setText(player_name)
        self.model.set_selected_player(player_name)

    @Slot(int)
    def _handle_grid_click(self, points):
        if self.current_player_name == "None":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Player Not Selected")
            msg.setText("Please select a player from the leaderboard first!")
            msg.exec()
            return
            
        if points in self.clicked_numbers:
            return

        print(f"Player '{self.current_player_name}' scores {points} points!")
        
        self.model.update_score(self.current_player_name, points)
        
        self.clicked_numbers.add(points)
        self.grid_buttons[points].setDisabled(True)
        self.grid_buttons[points].setStyleSheet("background-color: lightgray;") 

    # --- FIX 2: Ensure buttons are re-enabled and selection is cleared ---
    @Slot()
    def _reset_game(self):
        """Handles the Reset Game button click."""
        reply = QMessageBox.question(self, 'Reset Game',
            "Are you sure you want to reset all scores and clear the board?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 1. Reset Model Scores (This resets scores and 'is_selected' flags in the data)
            self.model.reset_scores()
            
            # 2. Reset Grid Buttons (Visual and functional reset)
            self.clicked_numbers.clear()
            for button in self.grid_buttons.values():
                button.setDisabled(False)
                # Reset style to default/empty string
                button.setStyleSheet("") 
            
            # 3. Clear Table Selection in the View (Crucial for clearing the highlight)
            # This ensures no row remains visually selected in the QTableView itself.
            self.table_view.clearSelection() 
            
            # 4. Clear Current Player State
            # This updates the label and tells the model to clear any old selection logic (though the model reset already did this, redundancy here is safer).
            self._set_current_player("None")

            print("Game state reset successfully.")


if __name__ == '__main__':
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling) 
    
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())