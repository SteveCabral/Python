from PySide6.QtWidgets import (
    QApplication,   # handle the main event loop
    QMainWindow,    # create the main application window
    QPushButton     # push button widget
)

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True
        self.setWindowTitle("Listing 9")

        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.released.connect(self.the_button_was_released) # signal connected to slot
        self.button.setChecked(self.button_is_checked)   # set the button to checked

        self.setCentralWidget(self.button)   # set the button as the central widget

    def the_button_was_released(self):   # slot
        self.button_is_checked = self.button.isChecked()
        print("Released", self.button_is_checked)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()