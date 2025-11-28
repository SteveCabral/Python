import sys
import os
import json
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QProgressBar

class FileCopyApp(QWidget):
    config_source = ""
    config_target = ""

    def __init__(self):
        super().__init__()
        config_file_path = 'GUI 04.json'
        config = self.read_config(config_file_path)

        config_source = config['source directory']
        config_target = config['target directory']

        self.initUI()

    
    def initUI(self):
        layout = QVBoxLayout()

        self.source_label = QLabel("Source Directory:")
        self.source_dir = QLabel()
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_dir)

        self.target_label = QLabel("Target Directory:")
        self.target_dir = QLabel()
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_dir)

        self.pick_source_button = QPushButton("Pick Source Directory")
        self.pick_source_button.clicked.connect(self.pickSourceDirectory)
        layout.addWidget(self.pick_source_button)

        self.pick_target_button = QPushButton("Pick Target Directory")
        self.pick_target_button.clicked.connect(self.pickTargetDirectory)
        layout.addWidget(self.pick_target_button)

        self.copy_button = QPushButton("Copy Files")
        self.copy_button.clicked.connect(self.copyFiles)
        layout.addWidget(self.copy_button)
        
        self.progress_label = QLabel("Progress:")
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def pickSourceDirectory(self):
        source_options = QFileDialog.Option.ShowDirsOnly
        source_dir = QFileDialog.getExistingDirectory(self, "Select Source Directory", self.config_source, options=source_options)
        self.source_dir.setText(source_dir)

    def read_config(file_path):
        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
        return config

    def pickTargetDirectory(self):
        target_options = QFileDialog.Option.ShowDirsOnly
        target_dir = QFileDialog.getExistingDirectory(self, "Select Target Directory", self.config_target, options=target_options)
        self.target_dir.setText(target_dir)

    def copyFiles(self):
        source_dir = self.source_dir.text()
        target_dir = self.target_dir.text()

        if not source_dir or not target_dir:
            QMessageBox.critical(self, "Error", "Please select source and target directories.")
            return

        try:
            total_files = sum(len(files) for root, _, files in os.walk(source_dir))
            copied_files = 0
            
            for root, _, files in os.walk(source_dir):
                for file in files:
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_dir, file)
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                    with open(source_file, 'rb') as src, open(target_file, 'wb') as tgt:
                        tgt.write(src.read())
                    copied_files += 1
                    self.progress_bar.setValue(int((copied_files / total_files) * 100))

            QMessageBox.information(self, "Success", "Files copied successfully.")
        
        except Exception as e:
            #self.update_progress.emit(-1)  # Signal an error
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = FileCopyApp()
    window.setWindowTitle('File Copy Program')
    window.setGeometry(100, 100, 400, 250)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()