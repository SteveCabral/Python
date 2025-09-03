import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QListWidget, QListWidgetItem, QSizePolicy
)
from PySide6.QtCore import Qt

class FileComparatorApp(QWidget):
    """
    A GUI application for comparing files in two folders.

    It finds files with the same size and extension but different names.
    """
    def __init__(self):
        super().__init__()
        self.folder1_path = ""
        self.folder2_path = ""
        self.init_ui()

    def init_ui(self):
        """Initializes the user interface layout and widgets."""
        self.setWindowTitle("File Comparator")
        self.setMinimumSize(600, 400)

        # Main layout for the entire window
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # --- Folder 1 Selection ---
        self.folder1_label = QLabel("Folder 1: Not selected")
        main_layout.addWidget(self.folder1_label)

        self.select_folder1_btn = QPushButton("Select Folder 1")
        self.select_folder1_btn.clicked.connect(self.select_folder1)
        main_layout.addWidget(self.select_folder1_btn)

        # --- Folder 2 Selection ---
        self.folder2_label = QLabel("Folder 2: Not selected")
        main_layout.addWidget(self.folder2_label)

        self.select_folder2_btn = QPushButton("Select Folder 2")
        self.select_folder2_btn.clicked.connect(self.select_folder2)
        main_layout.addWidget(self.select_folder2_btn)

        # --- Comparison Button ---
        self.compare_btn = QPushButton("Compare Files")
        self.compare_btn.clicked.connect(self.compare_files)
        self.compare_btn.setEnabled(False)  # Disabled until both folders are selected
        main_layout.addWidget(self.compare_btn)

        # --- Results Display ---
        self.results_list = QListWidget()
        self.results_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.results_list)

        self.setLayout(main_layout)

    def select_folder1(self):
        """Opens a dialog to select the first folder."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder 1")
        if folder_path:
            self.folder1_path = folder_path
            self.folder1_label.setText(f"Folder 1: {self.folder1_path}")
            self.check_enable_compare()

    def select_folder2(self):
        """Opens a dialog to select the second folder."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder 2")
        if folder_path:
            self.folder2_path = folder_path
            self.folder2_label.setText(f"Folder 2: {self.folder2_path}")
            self.check_enable_compare()

    def check_enable_compare(self):
        """Enables the compare button if both folders are selected."""
        if self.folder1_path and self.folder2_path:
            self.compare_btn.setEnabled(True)
        else:
            self.compare_btn.setEnabled(False)

    def compare_files(self):
        """
        Compares files in the two selected folders based on size and extension.
        
        The method uses a dictionary to group files by their (size, extension) tuple
        for efficient comparison, rather than a nested loop.
        """
        self.results_list.clear()

        # Group files from folder 1 by (size, extension)
        files1_by_size_ext = {}
        for filename in os.listdir(self.folder1_path):
            full_path = os.path.join(self.folder1_path, filename)
            if os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                _, ext = os.path.splitext(filename)
                key = (size, ext.lower())
                
                if key not in files1_by_size_ext:
                    files1_by_size_ext[key] = []
                files1_by_size_ext[key].append(filename)

        # Iterate through files in folder 2 and check for matches
        for filename2 in os.listdir(self.folder2_path):
            full_path2 = os.path.join(self.folder2_path, filename2)
            if os.path.isfile(full_path2):
                size2 = os.path.getsize(full_path2)
                _, ext2 = os.path.splitext(filename2)
                key2 = (size2, ext2.lower())

                # Check if this file's key exists in the first folder's dictionary
                if key2 in files1_by_size_ext:
                    for filename1 in files1_by_size_ext[key2]:
                        # The core comparison: same size, same extension, but different name
                        if filename1 != filename2:
                            item_text = f"Folder 1: {filename1}\nFolder 2: {filename2}"
                            list_item = QListWidgetItem(item_text)
                            self.results_list.addItem(list_item)
                            
        if self.results_list.count() == 0:
            self.results_list.addItem("No matching files found.")
            
        self.results_list.sortItems()

if __name__ == '__main__':
    app = QApplication([])
    window = FileComparatorApp()
    window.show()
    app.exec()