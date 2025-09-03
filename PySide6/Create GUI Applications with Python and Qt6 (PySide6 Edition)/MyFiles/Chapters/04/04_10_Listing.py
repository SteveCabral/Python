from PySide6.QtWidgets import (
    QApplication,       # handle the main event loop
    QMainWindow,        # create the main application window
    QPushButton         # push button widget
)
import sys             # import the sys module for command line arguments

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True
        self.button_clicked_count = 0
        self.setWindowTitle("Listing 10")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked) # signal connected to slot
        
        self.setCentralWidget(self.button)  # set the button as the central widget

    def the_button_was_clicked(self):       # slot
        self.button_clicked_count += 1
        self.setWindowTitle(f"Clicked {self.button_clicked_count} (do not exceed 5 times).")
        if self.button_clicked_count >= 5:
            self.button.setEnabled(False)
            self.setWindowTitle("You have clicked 5 times. Button is disabled")
        self.button.setToolTip(f"Clicked {self.button_clicked_count} times")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
        