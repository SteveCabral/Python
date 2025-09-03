import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QCheckBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listing 5-15")
        self.resize(400, 300)

        widget = QCheckBox("This is a checkbox")
        widget.setCheckState(Qt.CheckState.Checked)    # set the check state to checked
        widget.stateChanged.connect(self.show_state)
        self.setCentralWidget(widget)   # set the widget as the central widget

    def show_state(self, s):
        print(s == Qt.CheckState.Checked)
        print(s)

app = QApplication(sys.argv)    # create the application
window = MainWindow()           # create the main window
window.show()                   # display the main window
app.exec()                      # run the event loop