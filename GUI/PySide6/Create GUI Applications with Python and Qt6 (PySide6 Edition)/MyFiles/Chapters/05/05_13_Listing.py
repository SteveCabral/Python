import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listing 5-13")
        self.resize(400, 300)

        widget = QLabel("Hello")
        font = widget.font()    # get the font of the widget
        font.setPointSize(30)   # set the point size of the font
        widget.setFont(font)    # set the font of the widget
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)    # the book uses AlignHCenter and AlignVCenter but no intellisense in VS Code
        #widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)    # I noticed the AlignmentFlag enum is used in the PySide6 documentation
        #widget.setAlignment(Qt.AlignCenter)    # I also noticed the AlignCenter enum is used in the PySide6 documentation

        self.setCentralWidget(widget)   # set the widget as the central widget
    
app = QApplication(sys.argv)    # create the application
window = MainWindow()           # create the main window
window.show()                   # display the main window
app.exec()                      # run the event loop
