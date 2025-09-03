import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# subclass QMainWindow to customize the application main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Chapter 1, Listing 5")

        button = QPushButton("Press Me!")

        self.setFixedSize(QSize(400, 300))
        
        # set the central widget of the window
        self.setCentralWidget(button)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()