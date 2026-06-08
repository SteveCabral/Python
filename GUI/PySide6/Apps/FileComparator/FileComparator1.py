import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QTableWidget, QTableWidgetItem, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt

class FileComparatorApp(QWidget):
    """
    A GUI application for comparing files in two folders.

    It finds files with the same size and extension but different names.
    This version adds functionality to delete either file from a duplicate pair.
    """
    def __init__(self):
        super().__init__()
        self.folder1_path = ""
        self.folder2_path = ""
        self.init_ui()

    def init_ui(self):
        """Initializes the user interface layout and widgets."""
        self.setWindowTitle("File Comparator")
        self.setMinimumSize(700, 500)

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
        self.results_table = QTableWidget()
        self.results_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Folder 1 File", "Delete Folder 1 File?", "Folder 2 File", "Delete Folder 2 File?"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setColumnWidth(1, 150)
        self.results_table.setColumnWidth(3, 150)
        
        # Connect the itemChanged signal to our new method for managing the exclusive checkboxes
        self.results_table.itemChanged.connect(self.handle_exclusive_check)
        main_layout.addWidget(self.results_table)

        # --- Deletion Button ---
        self.delete_btn = QPushButton("Delete Checked Files")
        self.delete_btn.clicked.connect(self.delete_checked_files)
        self.delete_btn.setEnabled(False) # Initially disabled
        main_layout.addWidget(self.delete_btn)

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

    def handle_exclusive_check(self, item):
        """Ensures only one checkbox is checked per row."""
        if item.column() not in [1, 3]:
            return

        if item.checkState() == Qt.Checked:
            self.results_table.blockSignals(True)
            if item.column() == 1:
                # Uncheck the Folder 2 checkbox in the same row
                other_item = self.results_table.item(item.row(), 3)
                if other_item:
                    other_item.setCheckState(Qt.Unchecked)
            else: # item.column() == 3
                # Uncheck the Folder 1 checkbox in the same row
                other_item = self.results_table.item(item.row(), 1)
                if other_item:
                    other_item.setCheckState(Qt.Unchecked)
            self.results_table.blockSignals(False)

        self.check_enable_delete()

    def check_enable_delete(self):
        """Enables/disables the delete button based on checked items."""
        has_checked_item = False
        for i in range(self.results_table.rowCount()):
            if self.results_table.item(i, 1).checkState() == Qt.Checked or \
               self.results_table.item(i, 3).checkState() == Qt.Checked:
                has_checked_item = True
                break
        self.delete_btn.setEnabled(has_checked_item)

    def compare_files(self):
        """
        Compares files in the two selected folders based on size and extension.
        
        The method uses a dictionary to group files by their (size, extension) tuple
        for efficient comparison, rather than a nested loop.
        """
        self.results_table.setRowCount(0)

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
                            row_position = self.results_table.rowCount()
                            self.results_table.insertRow(row_position)

                            # Folder 1 File Name
                            item1 = QTableWidgetItem(filename1)
                            item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                            self.results_table.setItem(row_position, 0, item1)

                            # Folder 1 Checkbox
                            check1 = QTableWidgetItem()
                            check1.setFlags(check1.flags() | Qt.ItemIsUserCheckable)
                            check1.setCheckState(Qt.Unchecked)
                            self.results_table.setItem(row_position, 1, check1)
                            
                            # Folder 2 File Name
                            item2 = QTableWidgetItem(filename2)
                            item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                            self.results_table.setItem(row_position, 2, item2)
                            
                            # Folder 2 Checkbox
                            check2 = QTableWidgetItem()
                            check2.setFlags(check2.flags() | Qt.ItemIsUserCheckable)
                            check2.setCheckState(Qt.Unchecked)
                            self.results_table.setItem(row_position, 3, check2)

        if self.results_table.rowCount() == 0:
            self.results_table.setRowCount(1)
            item = QTableWidgetItem("No matching files found.")
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)
            self.results_table.setItem(0, 0, item)
            self.results_table.setSpan(0, 0, 1, 4)
            
    def delete_checked_files(self):
        """Deletes the files that are checked in the results table."""
        reply = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete the selected files?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            return

        deleted_count = 0
        # We need to iterate from the end to avoid index issues when removing items
        for i in range(self.results_table.rowCount() - 1, -1, -1):
            file1_checked = self.results_table.item(i, 1).checkState() == Qt.Checked
            file2_checked = self.results_table.item(i, 3).checkState() == Qt.Checked
            
            if file1_checked or file2_checked:
                # We need to get the file names before we remove the row
                file1_name = self.results_table.item(i, 0).text()
                file2_name = self.results_table.item(i, 2).text()
                
                success = False
                try:
                    if file1_checked:
                        path = os.path.join(self.folder1_path, file1_name)
                        if os.path.exists(path):
                            os.remove(path)
                            print(f"Deleted: {path}")
                            success = True
                    if file2_checked:
                        path = os.path.join(self.folder2_path, file2_name)
                        if os.path.exists(path):
                            os.remove(path)
                            print(f"Deleted: {path}")
                            success = True
                except OSError as e:
                    QMessageBox.critical(self, "Deletion Error", f"Error deleting file(s): {e}")

                if success:
                    self.results_table.removeRow(i)
                    deleted_count += 1
        
        if deleted_count > 0:
            QMessageBox.information(self, "Deletion Complete", f"Successfully deleted {deleted_count} file(s).")
            self.check_enable_delete()
        
if __name__ == '__main__':
    app = QApplication([])
    window = FileComparatorApp()
    window.show()
    app.exec()
