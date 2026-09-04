"""Main application window for Merge Videos."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config.settings import APP_NAME, APP_VERSION, VIDEO_EXTENSIONS
from model.merger import VideoMerger


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _separator() -> QFrame:
    """Return a sunken horizontal-line separator frame."""
    sep = QFrame()
    sep.setFrameShape(QFrame.Shape.HLine)
    sep.setFrameShadow(QFrame.Shadow.Sunken)
    return sep


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME}  v{APP_VERSION}")
        self.setMinimumSize(760, 480)
        self.resize(960, 600)
        self._last_add_dir: Path = Path.home()  # remembered across Add-Files calls
        self._build_ui()
        self._update_merge_btn_state()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setSpacing(8)
        root.setContentsMargins(14, 14, 14, 8)

        list_label = QLabel("Video Files to Merge  (top → bottom = merge order):")
        root.addWidget(list_label)

        list_row = QHBoxLayout()
        list_row.setSpacing(10)
        list_row.addWidget(self._make_list(), 1)
        list_row.addLayout(self._make_file_buttons())
        root.addLayout(list_row, 1)

        root.addWidget(_separator())
        root.addLayout(self._make_output_row())
        root.addWidget(_separator())
        root.addLayout(self._make_action_row())

        self.statusBar().showMessage(
            "Add two or more video files and choose an output filename to begin."
        )

    def _make_list(self) -> QListWidget:
        self._list = QListWidget()
        self._list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._list.setAlternatingRowColors(True)
        self._list.itemSelectionChanged.connect(self._update_file_btn_states)
        return self._list

    def _make_file_buttons(self) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(6)
        col.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._add_btn = QPushButton("Add Files…")
        self._add_btn.setFixedWidth(110)
        self._add_btn.clicked.connect(self._on_add)
        col.addWidget(self._add_btn)

        col.addWidget(_separator())

        self._delete_btn = QPushButton("Delete")
        self._delete_btn.setFixedWidth(110)
        self._delete_btn.setEnabled(False)
        self._delete_btn.clicked.connect(self._on_delete)
        col.addWidget(self._delete_btn)

        self._replace_btn = QPushButton("Replace…")
        self._replace_btn.setFixedWidth(110)
        self._replace_btn.setEnabled(False)
        self._replace_btn.clicked.connect(self._on_replace)
        col.addWidget(self._replace_btn)

        col.addWidget(_separator())

        self._up_btn = QPushButton("Move Up")
        self._up_btn.setFixedWidth(110)
        self._up_btn.setEnabled(False)
        self._up_btn.clicked.connect(self._on_move_up)
        col.addWidget(self._up_btn)

        self._down_btn = QPushButton("Move Down")
        self._down_btn.setFixedWidth(110)
        self._down_btn.setEnabled(False)
        self._down_btn.clicked.connect(self._on_move_down)
        col.addWidget(self._down_btn)

        col.addWidget(_separator())

        self._clear_btn = QPushButton("Clear List")
        self._clear_btn.setFixedWidth(110)
        self._clear_btn.setEnabled(False)
        self._clear_btn.clicked.connect(self._on_clear)
        col.addWidget(self._clear_btn)

        col.addStretch()
        return col

    def _make_output_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        label = QLabel("Output File:")
        label.setFixedWidth(88)

        self._output_edit = QLineEdit()
        self._output_edit.setPlaceholderText("Type a path or use Browse…")
        # Re-evaluate Merge button whenever the output path changes.
        self._output_edit.textChanged.connect(self._update_merge_btn_state)

        browse_btn = QPushButton("Browse…")
        browse_btn.setFixedWidth(90)
        browse_btn.clicked.connect(self._on_browse_output)

        row.addWidget(label)
        row.addWidget(self._output_edit)
        row.addWidget(browse_btn)
        return row

    def _make_action_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addStretch()

        self._merge_btn = QPushButton("Merge")
        self._merge_btn.setFixedHeight(34)
        self._merge_btn.setFixedWidth(110)
        self._merge_btn.setEnabled(False)
        self._merge_btn.clicked.connect(self._on_merge)
        row.addWidget(self._merge_btn)
        return row

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def _update_merge_btn_state(self) -> None:
        """Enable Merge only when ALL three conditions are satisfied:

        1. The file list contains at least two entries.
        2. The output filename field is non-empty.
        3. The parent directory of the chosen output path exists on disk.
        """
        has_enough_files = self._list.count() >= 2
        output_text = self._output_edit.text().strip()
        output_valid = (
            bool(output_text)
            and Path(output_text).parent.is_dir()
        )
        self._merge_btn.setEnabled(has_enough_files and output_valid)

    def _update_file_btn_states(self) -> None:
        """Enable/disable Delete, Replace, Move Up, Move Down, Clear based on selection/count."""
        row = self._list.currentRow()
        count = self._list.count()
        has_sel = row >= 0

        self._delete_btn.setEnabled(has_sel)
        self._replace_btn.setEnabled(has_sel)
        self._up_btn.setEnabled(has_sel and row > 0)
        self._down_btn.setEnabled(has_sel and row < count - 1)
        self._clear_btn.setEnabled(count > 0)

    # ------------------------------------------------------------------
    # File-list slots
    # ------------------------------------------------------------------

    def _on_add(self) -> None:
        filter_str = (
            "Video Files (" + " ".join(VIDEO_EXTENSIONS) + ")"
            ";;All Files (*)"
        )
        # Use an explicit dialog object with ExistingFiles mode so that
        # Ctrl+Click / Shift+Click multi-selection is always honoured,
        # regardless of the native file-picker platform quirks.
        dialog = QFileDialog(self, "Select Video Files to Merge")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter(filter_str)
        dialog.setDirectory(str(self._last_add_dir))

        if not dialog.exec():
            return

        paths = dialog.selectedFiles()
        if not paths:
            return

        for p in paths:
            self._list.addItem(p)

        # Remember this directory so the next Add-Files call opens here.
        self._last_add_dir = Path(paths[0]).parent

        # Auto-populate the output filename from the first file in the list.
        first = Path(self._list.item(0).text())
        suggested = first.parent / (first.stem + "_target" + first.suffix)
        self._output_edit.setText(str(suggested))

        self._update_merge_btn_state()
        self._update_file_btn_states()
        self.statusBar().showMessage(f"{self._list.count()} file(s) in list.")

    def _on_clear(self) -> None:
        if self._list.count() == 0:
            return
        answer = QMessageBox.question(
            self,
            "Clear List",
            "Remove all files from the list?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self._list.clear()
        self._update_merge_btn_state()
        self._update_file_btn_states()
        self.statusBar().showMessage("File list cleared.")

    def _on_delete(self) -> None:
        row = self._list.currentRow()
        if row < 0:
            return
        self._list.takeItem(row)
        new_count = self._list.count()
        if new_count > 0:
            self._list.setCurrentRow(min(row, new_count - 1))
        self._update_merge_btn_state()
        self._update_file_btn_states()
        self.statusBar().showMessage(f"{self._list.count()} file(s) in list.")

    def _on_replace(self) -> None:
        row = self._list.currentRow()
        if row < 0:
            return
        filter_str = (
            "Video Files (" + " ".join(VIDEO_EXTENSIONS) + ")"
            ";;All Files (*)"
        )
        path, _ = QFileDialog.getOpenFileName(
            self, "Replace With…", str(Path.home()), filter_str
        )
        if not path:
            return
        self._list.item(row).setText(path)
        self._update_merge_btn_state()
        self.statusBar().showMessage(f"Row {row + 1} replaced.")

    def _on_move_up(self) -> None:
        row = self._list.currentRow()
        if row <= 0:
            return
        item = self._list.takeItem(row)
        self._list.insertItem(row - 1, item)
        self._list.setCurrentRow(row - 1)
        self._update_file_btn_states()

    def _on_move_down(self) -> None:
        row = self._list.currentRow()
        if row < 0 or row >= self._list.count() - 1:
            return
        item = self._list.takeItem(row)
        self._list.insertItem(row + 1, item)
        self._list.setCurrentRow(row + 1)
        self._update_file_btn_states()

    # ------------------------------------------------------------------
    # Output slot
    # ------------------------------------------------------------------

    def _on_browse_output(self) -> None:
        # Default start directory: same folder as the first file in the list.
        start_dir = str(Path.home())
        suggested_name = "merged_output"
        if self._list.count() > 0:
            first = Path(self._list.item(0).text())
            if first.parent.is_dir():
                start_dir = str(first.parent)
            suggested_name = "merged_output" + first.suffix

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Choose Output File",
            str(Path(start_dir) / suggested_name),
            "Video Files (*.mp4 *.mpeg *.mpg *.avi *.flv *.mkv *.mov *.wmv *.m4v *.ts *.webm)"
            ";;All Files (*)",
        )
        if path:
            self._output_edit.setText(path)

    # ------------------------------------------------------------------
    # Merge slot
    # ------------------------------------------------------------------

    def _warn_mixed_extensions(self, files: list[Path]) -> bool:
        """Warn the user if the files span more than one extension.

        Returns ``True`` to proceed, ``False`` to cancel.
        """
        exts = VideoMerger.get_extensions(files)
        if len(exts) <= 1:
            return True

        ext_list = "  " + "\n  ".join(sorted(exts))
        answer = QMessageBox.warning(
            self,
            "Mixed File Extensions",
            f"The selected files have different extensions:\n{ext_list}\n\n"
            "FFmpeg may still merge them if the codec streams are compatible, "
            "but results are not guaranteed.\n\n"
            "Do you want to proceed anyway?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return answer == QMessageBox.StandardButton.Yes

    def _on_merge(self) -> None:
        files = [Path(self._list.item(i).text()) for i in range(self._list.count())]
        output_path = Path(self._output_edit.text().strip())

        if not self._warn_mixed_extensions(files):
            return

        self._merge_btn.setEnabled(False)
        self.statusBar().showMessage("Merging… please wait.")

        success, message = VideoMerger.merge(files, output_path)

        # Always re-evaluate button state after the operation.
        self._update_merge_btn_state()

        if success:
            QMessageBox.information(self, "Merge Complete", message)
            self.statusBar().showMessage(f"Done — {message}")
        else:
            QMessageBox.critical(
                self,
                "Merge Failed",
                f"FFmpeg reported an error:\n\n{message}",
            )
            self.statusBar().showMessage("Merge failed — see error dialog for details.")
