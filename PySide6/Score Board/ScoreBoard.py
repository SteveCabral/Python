import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame
)

class ScoreBoardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Score Board")
        self.setGeometry(100, 100, 300, 600)
        self.users = {f"User {i+1}": 0 for i in range(20)}  # Up to 20 users with initial score of 0
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout(self)

        # Scroll area to contain the scoreboard for easier navigation if many users
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.score_layout = QVBoxLayout(scroll_content)
        
        # Create initial scoreboard
        self.update_scoreboard()
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
    def update_scoreboard(self):
        # Clear current layout
        for i in reversed(range(self.score_layout.count())):
            widget_to_remove = self.score_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()
                
        # Sort users by score (descending) and then by name (ascending)
        sorted_users = sorted(self.users.items(), key=lambda x: (-x[1], x[0]))

        # Add each user entry to the layout
        for name, score in sorted_users:
            user_layout = QHBoxLayout()
            user_label = QLabel(f"{name}: {score}")
            user_label.setAlignment(Qt.AlignLeft)

            # Increment and decrement buttons
            increment_btn = QPushButton("+")
            increment_btn.clicked.connect(lambda _, n=name: self.change_score(n, 1))
            decrement_btn = QPushButton("-")
            decrement_btn.clicked.connect(lambda _, n=name: self.change_score(n, -1))

            # Arrange widgets in user layout
            user_layout.addWidget(user_label)
            user_layout.addWidget(increment_btn)
            user_layout.addWidget(decrement_btn)

            # Create a frame to hold each user entry for better separation
            user_frame = QFrame()
            user_frame.setLayout(user_layout)
            user_frame.setFrameShape(QFrame.Box)

            # Add the user frame to the scoreboard layout
            self.score_layout.addWidget(user_frame)
        
    def change_score(self, name, delta):
        # Change the score and update the display
        self.users[name] += delta
        self.update_scoreboard()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScoreBoardApp()
    window.show()
    sys.exit(app.exec())
