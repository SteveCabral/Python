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
        self.setWindowTitle("Listing 8")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked) # signal connected to slot
        button.clicked.connect(self.the_button_was_toggled) # signal connected to slot
        button.setChecked(self.button_is_checked)   # set the button to checked

        self.setCentralWidget(button)   # set the button as the central widget

    def the_button_was_clicked(self):   # slot
        print("Clicked")

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print("Checked?", self.button_is_checked)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()