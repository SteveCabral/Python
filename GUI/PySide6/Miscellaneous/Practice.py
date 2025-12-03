import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore 

class PracticeWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practice Window")  # Set the window title
        self.setGeometry(100, 100, 400, 300)    # Set window size and position
        
        self.layout = QtWidgets.QVBoxLayout()   # Create a vertical box layout
        
        self.label = QtWidgets.QLabel("This is a practice window.") # Add a label
        self.layout.addWidget(self.label)       # Add the label to the layout
        
        self.button = QtWidgets.QPushButton("Click Me")     # Add a button
        self.button.clicked.connect(self.on_button_click)   # Connect button click to handler
        self.layout.addWidget(self.button)                  # Add the button to the layout
        
        self.setLayout(self.layout)             # Set the layout for the window index for centering
    
    @QtCore.Slot()                              # Slot decorator for button click handler
    def on_button_click(self):                  # Button click handler
        self.label.setText("Button Clicked!")   # Update label text on button click

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PracticeWindow()
    window.show()
    app.exec()