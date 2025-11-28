from PySide6.QtWidgets import (
    QApplication,   # handle the main event loop
    QMainWindow,    # create the main application window
    QPushButton     # push button widget
)

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Listing 6")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked) # signal connected to slot
        button.clicked.connect(self.the_button_was_toggled) # signal connected to slot

        self.setCentralWidget(button)

    def the_button_was_clicked(self):   # slot
        print("Clicked")

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()