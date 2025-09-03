import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel
 )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listing 5-14")
        self.resize(400, 300)

        widget = QLabel()
        pixmap = QPixmap("C:\\Users\\Steve\\OneDrive\\Books\\Computers\\Python\\No Starch - Samples\\3rd Edition\\pcc_3e-main\\solution_files\\chapter_13\\ex_13_5_sideways_shooter_2\\images\\rocket_small.png")
        widget.setPixmap(pixmap)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()