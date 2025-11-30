# ChatGPT
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QFileDialog, QLineEdit, QRadioButton, QLabel, QTableWidget, 
    QTableWidgetItem, QGroupBox, QHeaderView, QTextEdit
)
from PySide6.QtCore import Qt


class FileCompareApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder File Compare")
        self.resize(800, 600)

        # Layout
        main_layout = QVBoxLayout(self)

        # Folder selection
        folder_layout = QHBoxLayout()
        self.folder1_edit = QLineEdit()
        self.folder2_edit = QLineEdit()
        browse1_btn = QPushButton("Browse Folder 1")
        browse2_btn = QPushButton("Browse Folder 2")
        browse1_btn.clicked.connect(lambda: self.select_folder(self.folder1_edit))
        browse2_btn.clicked.connect(lambda: self.select_folder(self.folder2_edit))

        folder_layout.addWidget(QLabel("Folder 1:"))
        folder_layout.addWidget(self.folder1_edit)
        folder_layout.addWidget(browse1_btn)
        folder_layout.addWidget(QLabel("Folder 2:"))
        folder_layout.addWidget(self.folder2_edit)
        folder_layout.addWidget(browse2_btn)

        main_layout.addLayout(folder_layout)

        # Compare controls
        controls_layout = QHBoxLayout()
        self.size_radio = QRadioButton("By Size")
        self.name_radio = QRadioButton("By Name")
        self.size_radio.setChecked(True)

        compare_btn = QPushButton("Compare")
        compare_btn.clicked.connect(self.compare_folders)

        controls_layout.addWidget(self.size_radio)
        controls_layout.addWidget(self.name_radio)
        controls_layout.addStretch()
        controls_layout.addWidget(compare_btn)
        main_layout.addLayout(controls_layout)

        # Results table
        self.results_table = QTableWidget(0, 2)
        self.results_table.setHorizontalHeaderLabels(["Folder 1 File", "Folder 2 File"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.cellClicked.connect(self.show_details)
        main_layout.addWidget(self.results_table)

        # Details area
        details_group = QGroupBox("Details")
        details_layout = QVBoxLayout()
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        details_layout.addWidget(self.details_text)
        details_group.setLayout(details_layout)
        main_layout.addWidget(details_group)

        self.setLayout(main_layout)

    def select_folder(self, edit_box):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            edit_box.setText(folder)

    def get_files(self, folder):
        """Return dict: filename -> (path, size)"""
        files = {}
        if folder and os.path.isdir(folder):
            for f in os.listdir(folder):
                full_path = os.path.join(folder, f)
                if os.path.isfile(full_path):
                    files[f] = (full_path, os.path.getsize(full_path))
        return files

    def compare_folders(self):
        self.results_table.setRowCount(0)
        self.details_text.clear()

        folder1 = self.folder1_edit.text()
        folder2 = self.folder2_edit.text()

        files1 = self.get_files(folder1)
        files2 = self.get_files(folder2)

        matches = []

        if self.size_radio.isChecked():
            # Compare by file size
            size_map = {}
            for f, (_, size) in files1.items():
                size_map.setdefault(size, []).append(f)
            for f2, (_, size2) in files2.items():
                if size2 in size_map:
                    for f1 in size_map[size2]:
                        # Skip if both filename and size are identical
                        if f1 == f2 and files1[f1][1] == size2:
                            continue
                        matches.append((f1, f2))
        else:
            # Compare by filename inclusion
            for f1, (path1, size1) in files1.items():
                for f2, (path2, size2) in files2.items():
                    if f1 in f2 or f2 in f1:
                        # Skip if both filename and size are identical
                        if f1 == f2 and size1 == size2:
                            continue
                        matches.append((f1, f2))

        # Populate table
        for f1, f2 in matches:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            self.results_table.setItem(row, 0, QTableWidgetItem(f1))
            self.results_table.setItem(row, 1, QTableWidgetItem(f2))

        # Store file info for details
        self.matches = matches
        self.files1 = files1
        self.files2 = files2


    def show_details(self, row, col):
        if row < 0 or row >= len(self.matches):
            return

        f1, f2 = self.matches[row]
        f1_path, f1_size = self.files1.get(f1, ("", 0))
        f2_path, f2_size = self.files2.get(f2, ("", 0))

        details = (
            f"Folder 1\n"
            f"File Name: {f1}\n"
            f"File Size: {f1_size:,}\n\n"
            f"Folder 2\n"
            f"File Name: {f2}\n"
            f"File Size: {f2_size:,}\n"
        )

        self.details_text.setText(details)


if __name__ == "__main__":
    app = QApplication([])
    window = FileCompareApp()
    window.show()
    app.exec()
