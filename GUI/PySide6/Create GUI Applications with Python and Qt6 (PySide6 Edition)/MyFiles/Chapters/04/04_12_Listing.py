from PySide6.QtWidgets import (
    QApplication,       # handle the main event loop
    QMainWindow,        # create the main application window
    QWidget,            # base class for all UI objects
    QVBoxLayout,        # vertical layout
    QLabel,             # label widget
    QLineEdit           # single-line text widget
)

import sys                  # import the sys module for command line arguments

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 300)       # set the window size
        self.setWindowTitle("Listing 4-12")

        self.label = QLabel()       # create an instance of the QLabel object
        self.input = QLineEdit()    # create an instance of the QLineEdit object
        self.input.textChanged.connect(self.label.setText)  # connect the textChanged signal to the setText slot

        layout = QVBoxLayout()          # create a QVBoxLayout object
        layout.addWidget(self.input)    # add the input widget to the layout
        layout.addWidget(self.label)    # add the label widget to the layout
        
        container = QWidget()           # create a QWidget object
        container.setLayout(layout)     # set the layout of the container

        self.setCentralWidget(container)    # set the container as the central widget

app = QApplication(sys.argv)    # create the application
window = MainWindow()           # create the main window
window.show()                   # display the main window
app.exec()                      # run the event loop

   

        