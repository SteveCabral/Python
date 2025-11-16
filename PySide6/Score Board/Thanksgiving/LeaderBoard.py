import sys
from operator import itemgetter
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex, Signal, Slot, QItemSelection
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, 
    QVBoxLayout, QTableView, QLineEdit, QPushButton, 
    QGridLayout, QSplitter, QLabel # <-- You added this after the last error, but I need to point it out here
)

# --- 1. Leaderboard Data Model (QAbstractTableModel) ---
# This class handles the data storage, sorting, and display roles for the QTableView.
class LeaderboardModel(QAbstractTableModel):
    """A custom model to handle the game's player data and sorting logic."""
    
    # Define column indices for clarity
    RANK, PLAYER, SCORE = 0, 1, 2
    HEADER_LABELS = ["Rank", "Player", "Score"]

    def __init__(self, players_data, parent=None):
        super().__init__(parent)
        # Data structure: List of dicts: 
        # [{'player': 'Alice', 'score': 15, 'rank': 1}]
        self._players = players_data
        self.sort_data() # Initial sort

    def rowCount(self, parent=QModelIndex()):
        return len(self._players)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADER_LABELS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            item = self._players[row]
            if col == self.RANK:
                return item['rank']
            elif col == self.PLAYER:
                return item['player']
            elif col == self.SCORE:
                return item['score']
        
        # Make the Player column selectable for setting the current player
        if role == Qt.ItemDataRole.FlagsRole and col == self.PLAYER:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADER_LABELS[section]
        return None

    def sort_data(self):
        """Sorts the data based on score (descending) then player name (ascending, as tie-breaker)."""
        
        # 1. Sort by the secondary key (Player Name) in ascending order.
        # This is the tie-breaker sort. Python's sort is stable, so this order will be preserved.
        sorted_players = sorted(
            self._players, 
            key=itemgetter('player'), 
            reverse=False # Ascending order for tie-breaker
        )
        
        # 2. Sort by the primary key (Score) in descending order.
        # Since Python's sort is stable, items with the same score maintain the order established in step 1.
        sorted_players = sorted(
            sorted_players, 
            key=itemgetter('score'), 
            reverse=True # Descending order for score
        )

        # 3. Assign Rank (starting at 1)
        for i, player in enumerate(sorted_players):
            player['rank'] = i + 1
        
        self._players = sorted_players
        
        # Notify the view that the underlying data has changed for a full redraw
        self.layoutChanged.emit()

        # 2. Assign Rank (starting at 1)
        for i, player in enumerate(sorted_players):
            player['rank'] = i + 1
        
        self._players = sorted_players
        
        # Notify the view that the underlying data has changed for a full redraw
        self.layoutChanged.emit()

    @Slot(str)
    def add_player(self, name):
        """Adds a new player to the list and re-sorts."""
        # Prevent adding duplicate names (case-insensitive check)
        if name.lower() in [p['player'].lower() for p in self._players]:
            return 
        
        # Notify the view before and after adding to a list for efficiency
        self.beginInsertRows(QModelIndex(), len(self._players), len(self._players))
        self._players.append({'player': name, 'score': 0, 'rank': 0})
        self.endInsertRows()
        
        self.sort_data()

    @Slot(str, int)
    def update_score(self, player_name, points):
        """Updates the score of a player and re-sorts."""
        player_found = False
        # Find the player and update their score
        for player in self._players:
            if player['player'] == player_name:
                player['score'] += points
                player_found = True
                break
        
        if player_found:
            self.sort_data()
            
# --- 2. Main Application Window ---
class GameWindow(QMainWindow):
    # Signal to notify the PlayerControl panel that a new player is selected
    player_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thanksgiving Family Game 🦃")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Call to _create_leaderboard_widget which calls _create_player_controls
        self.leaderboard_widget = self._create_leaderboard_widget() 
        main_splitter.addWidget(self.leaderboard_widget)
        
        # --- Right Side: Game Grid ---
        self.game_grid_widget = self._create_game_grid_widget()
        main_splitter.addWidget(self.game_grid_widget)
        
        # Set the initial ratio for the split (e.g., 30% for leaderboard, 70% for game)
        main_splitter.setSizes([250, 550]) 

        # Set the main layout of the central widget to the splitter
        layout = QHBoxLayout(central_widget)
        layout.addWidget(main_splitter)
        
        # Initial selected player
        self.current_player_name = "None"

    def _create_leaderboard_widget(self):
        """Creates the widget containing the QTableView and player controls."""
        
        # Initial dummy data
        initial_players = [
            {'player': 'Leo', 'score': 15, 'rank': 0},
            {'player': 'Amy', 'score': 20, 'rank': 0},
            {'player': 'Chris', 'score': 15, 'rank': 0},
        ]
        
        # Model-View setup
        self.model = LeaderboardModel(initial_players)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        # Connect selection change to a slot to set the current player
        self.table_view.selectionModel().selectionChanged.connect(self._select_player_from_table)
        
        # Player Controls Widget (Add Player, Current Player)
        self.player_controls = self._create_player_controls()
        
        # Layout for the left side
        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.table_view)
        left_vbox.addWidget(self.player_controls)

        leaderboard_container = QWidget()
        leaderboard_container.setLayout(left_vbox)
        return leaderboard_container

    def _create_player_controls(self):
        """Creates the widget for adding a player and displaying the current player."""
        
        container = QWidget()
        vbox = QVBoxLayout(container)
        
        # 1. Add Player Controls
        add_player_hbox = QHBoxLayout()
        self.player_name_input = QLineEdit()
        self.player_name_input.setPlaceholderText("Enter Player Name")
        
        add_button = QPushButton("➕ Add Player")
        add_button.clicked.connect(self._add_player)
        
        add_player_hbox.addWidget(self.player_name_input)
        add_player_hbox.addWidget(add_button)
        vbox.addLayout(add_player_hbox)

        # 2. Current Player Display
        current_player_hbox = QHBoxLayout()
        current_player_hbox.addWidget(QLabel("Current Player:"))
        
        # *** SELF.CURRENT_PLAYER_LABEL IS CREATED AND ASSIGNED HERE ***
        self.current_player_label = QLabel("None") 
        self.current_player_label.setStyleSheet("font-weight: bold; color: blue;")
        current_player_hbox.addWidget(self.current_player_label)

        vbox.addLayout(current_player_hbox)

        return container
        
    def _create_game_grid_widget(self):
        """Creates the 6x6 grid of buttons for the game interface."""
        
        container = QWidget()
        grid_layout = QGridLayout(container)
        
        # Create 6x6 grid buttons with numbers 1 to 36
        for i in range(6):
            for j in range(6):
                number = (i * 6) + j + 1
                button = QPushButton(str(number))
                # Set a fixed size for a clean grid look
                button.setFixedSize(50, 50) 
                
                # Connect the button click to the score update logic
                button.clicked.connect(lambda checked, val=number: self._handle_grid_click(val))
                
                grid_layout.addWidget(button, i, j)
        
        # Center the grid within its container
        vbox = QVBoxLayout(container)
        vbox.addLayout(grid_layout)
        vbox.setAlignment(grid_layout, Qt.AlignmentFlag.AlignCenter)

        return container

    @Slot()
    def _add_player(self):
        """Slot to handle the 'Add Player' button click."""
        player_name = self.player_name_input.text().strip()
        if player_name:
            self.model.add_player(player_name)
            self.player_name_input.clear()
            
            # Auto-select the newly added player
            self._set_current_player(player_name)
            
    @Slot(QItemSelection, QItemSelection)
    def _select_player_from_table(self, selected, deselected):
        """Slot to handle selection changes in the QTableView."""
        indexes = selected.indexes()
        if indexes:
            # The player name is in column 1 (index 1)
            player_index = indexes[0].siblingAtColumn(self.model.PLAYER)
            player_name = self.model.data(player_index)
            self._set_current_player(player_name)
        else:
            self._set_current_player("None")

    def _set_current_player(self, player_name):
        """Internal method to update the current player state."""
        self.current_player_name = player_name
        self.current_player_label.setText(player_name)
        # Optional: Emit signal if other widgets need to react
        self.player_selected.emit(player_name)


    @Slot(int)
    def _handle_grid_click(self, points):
        """Slot to handle a button click in the game grid."""
        if self.current_player_name == "None":
            print("Please select a player first!")
            # Optional: Show a QMessageBox to the user
            return
            
        print(f"Player '{self.current_player_name}' scores {points} points!")
        
        # Update the model with the new score
        self.model.update_score(self.current_player_name, points)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())