# Gemini AI
import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QFileDialog, QLineEdit, QLabel,
                               QRadioButton, QTableWidget, QTableWidgetItem,
                               QGroupBox, QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt

class FileComparatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.folder1_path = ""
        self.folder2_path = ""
        self.file_details_widget = None

    def init_ui(self):
        """Initializes the user interface."""
        self.setWindowTitle("File Comparator")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("font-size: 14px;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Folder selection widgets
        folder_selection_layout = QHBoxLayout()
        folder_selection_layout.setSpacing(10)

        # Folder 1
        folder1_layout = QVBoxLayout()
        self.folder1_label = QLabel("Folder 1:")
        self.folder1_lineedit = QLineEdit()
        self.folder1_lineedit.setPlaceholderText("Select Folder 1")
        self.folder1_lineedit.setReadOnly(True)
        self.folder1_button = QPushButton("Browse")
        self.folder1_button.clicked.connect(lambda: self.select_folder(self.folder1_lineedit))
        folder1_layout.addWidget(self.folder1_label)
        folder1_layout.addWidget(self.folder1_lineedit)
        folder1_layout.addWidget(self.folder1_button)
        folder_selection_layout.addLayout(folder1_layout)

        # Folder 2
        folder2_layout = QVBoxLayout()
        self.folder2_label = QLabel("Folder 2:")
        self.folder2_lineedit = QLineEdit()
        self.folder2_lineedit.setPlaceholderText("Select Folder 2")
        self.folder2_lineedit.setReadOnly(True)
        self.folder2_button = QPushButton("Browse")
        self.folder2_button.clicked.connect(lambda: self.select_folder(self.folder2_lineedit))
        folder2_layout.addWidget(self.folder2_label)
        folder2_layout.addWidget(self.folder2_lineedit)
        folder2_layout.addWidget(self.folder2_button)
        folder_selection_layout.addLayout(folder2_layout)

        main_layout.addLayout(folder_selection_layout)
        
        # Comparison options and button
        compare_options_layout = QHBoxLayout()
        compare_options_layout.setSpacing(15)
        
        # Radio buttons for comparison type
        radio_group = QGroupBox("Comparison Type")
        radio_group.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; margin-top: 1ex; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; }")
        radio_layout = QHBoxLayout()
        self.size_radio = QRadioButton("By Size")
        self.size_radio.setChecked(True)
        self.name_radio = QRadioButton("By Name")
        radio_layout.addWidget(self.size_radio)
        radio_layout.addWidget(self.name_radio)
        radio_layout.addStretch()
        radio_group.setLayout(radio_layout)
        
        compare_options_layout.addWidget(radio_group)
        
        # Compare button
        self.compare_button = QPushButton("Compare")
        self.compare_button.setFixedSize(150, 40)
        self.compare_button.clicked.connect(self.compare_files)
        compare_options_layout.addWidget(self.compare_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        main_layout.addLayout(compare_options_layout)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Folder 1", "Folder 2"])
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.itemSelectionChanged.connect(self.display_file_details)
        main_layout.addWidget(self.results_table)
        
        # File details display
        self.file_details_widget = QGroupBox("File Details")
        self.file_details_widget.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; margin-top: 1ex; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px; }")
        self.file_details_layout = QVBoxLayout()
        self.file_details_label = QLabel("Select a row in the table above to view details.")
        self.file_details_layout.addWidget(self.file_details_label)
        self.file_details_widget.setLayout(self.file_details_layout)
        main_layout.addWidget(self.file_details_widget)

        self.setLayout(main_layout)

    def select_folder(self, lineedit):
        """Opens a dialog to select a folder."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            lineedit.setText(folder_path)
            if lineedit == self.folder1_lineedit:
                self.folder1_path = folder_path
            else:
                self.folder2_path = folder_path
            
    def get_file_info(self, folder_path):
        """Returns a dictionary of file info (size and path) in a folder."""
        file_info = {}
        if not os.path.isdir(folder_path):
            return file_info
        for root, _, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    file_size = os.path.getsize(file_path)
                    file_info[filename] = {'size': file_size, 'path': file_path}
                except OSError:
                    continue
        return file_info
        
    def compare_files(self):
        """Compares files based on the selected method."""
        self.folder1_path = self.folder1_lineedit.text()
        self.folder2_path = self.folder2_lineedit.text()

        if not self.folder1_path or not self.folder2_path:
            self.results_table.setRowCount(0)
            self.results_table.insertRow(0)
            self.results_table.setItem(0, 0, QTableWidgetItem("Please select both folders."))
            self.results_table.setItem(0, 1, QTableWidgetItem(""))
            self.display_file_details_label("Select a row in the table above to view details.")
            return

        self.results_table.setRowCount(0)
        self.display_file_details_label("Select a row in the table above to view details.")
        
        files1 = self.get_file_info(self.folder1_path)
        files2 = self.get_file_info(self.folder2_path)
        
        # Create a set of (filename, size) for Folder 2 to quickly check for identical files
        identical_files_set = set()
        for filename, info in files2.items():
            identical_files_set.add((filename, info['size']))

        self.matching_files = []

        if self.size_radio.isChecked():
            self.compare_by_size(files1, files2, identical_files_set)
        elif self.name_radio.isChecked():
            #self.compare_by_name(files1, files2, identical_files_set)
            self.compare_by_name(files1, files2)
            
        if not self.matching_files:
            self.results_table.setRowCount(1)
            self.results_table.setItem(0, 0, QTableWidgetItem("No matching files found."))
            self.results_table.setItem(0, 1, QTableWidgetItem(""))
        else:
            self.update_results_table()

    def compare_by_size(self, files1, files2, identical_files_set):
        """Compares files by size, ignoring identical files."""
        size_to_names1 = {}
        for name, info in files1.items():
            size_to_names1.setdefault(info['size'], []).append(info)
            
        for name2, info2 in files2.items():
            # Check for identical files first and skip if found
            if (name2, info2['size']) in identical_files_set:
                continue

            if info2['size'] in size_to_names1:
                for info1 in size_to_names1[info2['size']]:
                    # Ensure the filename is not the same
                    if os.path.basename(info1['path']) != name2:
                        self.matching_files.append((info1, info2))

    def compare_by_name(self, files1, files2):
        """Compares files by name similarity, ignoring results where both filename and size are identical."""
        for name1, info1 in files1.items():
            for name2, info2 in files2.items():
                # Check if one filename is a substring of the other
                if name1 in name2 or name2 in name1:
                    # If filenames are identical, check if sizes are different.
                    # If sizes are also identical, it's a duplicate, so we skip it.
                    if name1 == name2 and info1['size'] == info2['size']:
                        continue  # Skip if both name and size are identical
                    self.matching_files.append((info1, info2))
    
    def update_results_table(self):
        """Populates the results table with matching files."""
        self.results_table.setRowCount(len(self.matching_files))
        for i, (info1, info2) in enumerate(self.matching_files):
            item1 = QTableWidgetItem(f"Folder 1: {os.path.basename(info1['path'])}")
            item2 = QTableWidgetItem(f"Folder 2: {os.path.basename(info2['path'])}")
            self.results_table.setItem(i, 0, item1)
            self.results_table.setItem(i, 1, item2)

    def display_file_details(self):
        """Displays details for the selected file row."""
        selected_rows = self.results_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        if row < 0 or row >= len(self.matching_files):
            return
            
        info1, info2 = self.matching_files[row]
        
        size1_formatted = f"{info1['size']:,}"
        size2_formatted = f"{info2['size']:,}"

        details_text = (
            f"<b>Folder 1</b><br>"
            f"File Name: {os.path.basename(info1['path'])}<br>"
            f"File Size: {size1_formatted} bytes<br>"
            f"<br>"
            f"<b>Folder 2</b><br>"
            f"File Name: {os.path.basename(info2['path'])}<br>"
            f"File Size: {size2_formatted} bytes"
        )
        self.display_file_details_label(details_text)

    def display_file_details_label(self, text):
        """Helper to update the details label."""
        self.file_details_label.setText(text)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileComparatorApp()
    window.show()
    sys.exit(app.exec())