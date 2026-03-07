import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore 

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practice Window")  # Set the window title
        self.setGeometry(100, 100, 400, 300)    # Set window size and position
        
        self.layout = QtWidgets.QGridLayout()   # Create a grid layout
        
        self.label_FirstName = QtWidgets.QLabel("First Name:") # Add a label_FirstName
        self.line_edit_FirstName = QtWidgets.QLineEdit()       # Add a line edit for first name
        self.line_edit_FirstName.editingFinished.connect(self.on_button_click)  # Connect editing finished to handler
        self.layout.addWidget(self.label_FirstName, 0, 0)      # Add the label_FirstName to the layout at row 0, column 0
        self.layout.addWidget(self.line_edit_FirstName, 0, 1)  # Add the line edit to the layout at row 0, column 1

        self.label_LastName = QtWidgets.QLabel("Last Name:")    # Add a label_LastName
        self.line_edit_LastName = QtWidgets.QLineEdit()         # Add a line edit for last name
        self.line_edit_LastName.editingFinished.connect(self.on_button_click)  # Connect editing finished to handler
        self.layout.addWidget(self.label_LastName, 1, 0)        # Add the label_LastName to the layout at row 1, column 0
        self.layout.addWidget(self.line_edit_LastName, 1, 1)    # Add the line edit to the layout at row 1, column 1


        self.label_Status = QtWidgets.QLabel("Status:")     # Add a label_Status
        self.button = QtWidgets.QPushButton("Click Me")     # Add a button
        self.button.clicked.connect(self.on_button_click)   # Connect button click to handler
        self.layout.addWidget(self.label_Status, 2, 0, 1, 2)      # Add the label_Status to the layout at row 2, column 0
        self.layout.addWidget(self.button, 3, 1)            # Add the button to the layout at row 2, column 1
        
        self.setLayout(self.layout)             # Set the layout for the window index for centering
    
    @QtCore.Slot()                              # Slot decorator for button click handler
    def on_button_click(self):                  # Button click handler
        self.label_Status.setText(f"{self.line_edit_FirstName.text()} {self.line_edit_LastName.text()} ")  # Update label_Status text

if __name__ == "__main__": 
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    app.exec()