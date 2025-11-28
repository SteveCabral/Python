from PySide6.QtWidgets import (
    QApplication,       # handle the main event loop
    QMainWindow,        # create the main application window
    QPushButton         # push button widget
)

import sys                  # import the sys module for command line arguments
from random import choice   # import the choice function from the random module

window_titles = [
    "My App",
    "My App",
    "Still My App",
    "Still My App",
    "What on earth",
    "What on earth",
    "This is surprising",
    "This is surprising",
    "Something went wrong",
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window size using resize method
        self.resize(400, 300)
        
        # Alternatively, you can use setGeometry method
        # self.setGeometry(100, 100, 800, 600)

        self.n_times_clicked = 0
        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)        # signal connect the button to the function
        self.windowTitleChanged.connect(self.the_window_title_changed)  # signal connect the window title to the function

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):                   # slot function to change the window title
        print("Clicked")
        new_window_title = choice(window_titles)        # pick a random title
        print("Setting title: %s" % new_window_title)   # print the new title
        self.setWindowTitle(new_window_title)           # set the new title

    def the_window_title_changed(self, window_title):   # slot function to disable the button
        print("Window title changed: %s" % window_title)
        if window_title == "Something went wrong":
            self.button.setDisabled(True)

app = QApplication(sys.argv)    # create the application
window = MainWindow()           # create the main window
window.show()                   # display the main window
app.exec()                      # run the event loop

