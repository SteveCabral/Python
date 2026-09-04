"""Main application window for FileShrinker."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from config.settings import APP_NAME, APP_VERSION, COLOR_CONFLICT, COLOR_SAFE
from model.file_shrinker import FileInfo, FileShrinker


class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME}  v{APP_VERSION}")
        self.setMinimumSize(860, 500)
        self.resize(1050, 680)

        self._source_folder: Path | None = None
        self._target_folder: Path | None = None
        self._source_files: list[FileInfo] = []
        self._conflicts: set[str] = set()

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setSpacing(8)
        root.setContentsMargins(14, 14, 14, 8)

        root.addLayout(self._make_folder_row("Source Folder:", "source"))
        root.addLayout(self._make_folder_row("Target Folder:", "target"))
        root.addWidget(_separator())
        root.addWidget(self._make_table())
        root.addWidget(_separator())
        root.addLayout(self._make_action_row())

        self.statusBar().showMessage(
            "Select a source folder and a target folder to begin."
        )

    def _make_folder_row(self, label_text: str, role: str) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        label = QLabel(label_text)
        label.setFixedWidth(115)

        edit = QLineEdit()
        edit.setReadOnly(True)
        edit.setPlaceholderText("No folder selected…")

        browse_btn = QPushButton("Browse…")
        browse_btn.setFixedWidth(90)
        browse_btn.clicked.connect(lambda _=False, r=role: self._browse_folder(r))

        refresh_btn = QPushButton("↺")
        refresh_btn.setFixedWidth(32)
        refresh_btn.setToolTip("Refresh folder contents")
        refresh_btn.clicked.connect(self._refresh)

        row.addWidget(label)
        row.addWidget(edit)
        row.addWidget(browse_btn)
        row.addWidget(refresh_btn)

        if role == "source":
            self._source_edit = edit
        else:
            self._target_edit = edit

        return row

    def _make_table(self) -> QTableWidget:
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            ["Source File", "Source Size", "Target File", "Target Size", "Status"]
        )

        hh = table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(False)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)

        self._table = table
        return table

    def _make_action_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(8)

        row.addLayout(self._make_legend())
        row.addStretch()

        self._shrink_btn = QPushButton("Shrink Files")
        self._shrink_btn.setFixedHeight(34)
        self._shrink_btn.setFixedWidth(130)
        self._shrink_btn.setEnabled(False)
        self._shrink_btn.clicked.connect(self._on_shrink)
        row.addWidget(self._shrink_btn)

        return row

    @staticmethod
    def _make_legend() -> QHBoxLayout:
        legend = QHBoxLayout()
        legend.setSpacing(4)

        entries = [
            (COLOR_SAFE, "Will be created"),
            (COLOR_CONFLICT, "Conflict — already exists in target"),
        ]
        for color, text in entries:
            swatch = QLabel()
            swatch.setFixedSize(14, 14)
            swatch.setStyleSheet(
                f"background-color: {color}; border: 1px solid #888;"
            )
            legend.addWidget(swatch)
            legend.addWidget(QLabel(text))
            legend.addSpacing(14)

        return legend

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _browse_folder(self, role: str) -> None:
        caption = "Select Source Folder" if role == "source" else "Select Target Folder"
        start = str(
            self._source_folder if role == "source" and self._source_folder
            else self._target_folder if role == "target" and self._target_folder
            else Path.home()
        )
        folder = QFileDialog.getExistingDirectory(self, caption, start)
        if not folder:
            return

        path = Path(folder)
        if role == "source":
            self._source_folder = path
            self._source_edit.setText(str(path))
        else:
            self._target_folder = path
            self._target_edit.setText(str(path))

        self._refresh()

    def _on_shrink(self) -> None:
        if not self._source_files or self._target_folder is None:
            return

        # Guard: re-check conflicts right before writing (state may have changed).
        self._conflicts = FileShrinker.get_conflicts(
            self._source_files, self._target_folder
        )
        if self._conflicts:
            names = "\n  • ".join(sorted(self._conflicts))
            QMessageBox.critical(
                self,
                "Conflicts Detected",
                f"The following file(s) already exist in the target folder:\n"
                f"  • {names}\n\n"
                f"No files were created. Resolve all conflicts before shrinking.",
            )
            self._populate_table()
            return

        count = len(self._source_files)
        reply = QMessageBox.question(
            self,
            "Confirm Shrink",
            f"Create {count} one-byte file(s) in:\n\n"
            f"  {self._target_folder}\n\nProceed?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            created = FileShrinker.shrink_files(self._source_files, self._target_folder)
        except OSError as exc:
            QMessageBox.critical(self, "Write Error", f"Failed to create files:\n\n{exc}")
            return

        self._refresh()
        self.statusBar().showMessage(
            f"Done — {len(created)} one-byte file(s) written to {self._target_folder}"
        )

    # ------------------------------------------------------------------
    # Refresh / table population
    # ------------------------------------------------------------------

    def _refresh(self) -> None:
        self._source_files = (
            FileShrinker.scan_folder(self._source_folder)
            if self._source_folder else []
        )
        self._conflicts = (
            FileShrinker.get_conflicts(self._source_files, self._target_folder)
            if self._source_files and self._target_folder is not None else set()
        )
        self._populate_table()

    def _populate_table(self) -> None:
        self._table.setRowCount(0)

        for fi in self._source_files:
            row = self._table.rowCount()
            self._table.insertRow(row)

            is_conflict = fi.name in self._conflicts
            brush = QBrush(QColor(COLOR_CONFLICT if is_conflict else COLOR_SAFE))

            # Resolve target-side metadata when a conflict exists.
            target_size_str = "—"
            if is_conflict and self._target_folder:
                target_path = self._target_folder / fi.name
                try:
                    target_size_str = _format_size(target_path.stat().st_size)
                except OSError:
                    target_size_str = "?"

            status_text = (
                "CONFLICT — already exists" if is_conflict else "Will be created"
            )

            items: list[QTableWidgetItem] = [
                QTableWidgetItem(fi.name),
                _right_aligned(QTableWidgetItem(_format_size(fi.size))),
                QTableWidgetItem(fi.name),
                _right_aligned(QTableWidgetItem(target_size_str)),
                QTableWidgetItem(status_text),
            ]
            for col, item in enumerate(items):
                item.setForeground(brush)
                self._table.setItem(row, col, item)

        # Enable the shrink button only when everything is ready.
        ready = (
            bool(self._source_files)
            and self._target_folder is not None
            and not self._conflicts
        )
        self._shrink_btn.setEnabled(ready)
        self.statusBar().showMessage(self._status_message())

    def _status_message(self) -> str:
        if not self._source_folder:
            return "Select a source folder and a target folder to begin."
        if not self._source_files:
            return "Source folder is empty — no files to shrink."
        if self._target_folder is None:
            return f"{len(self._source_files)} source file(s) found.  Select a target folder."
        if self._conflicts:
            return (
                f"{len(self._conflicts)} conflict(s) detected in "
                f"{len(self._source_files)} file(s) — resolve before shrinking."
            )
        return f"{len(self._source_files)} file(s) ready to shrink."


# ── Module-level helpers ──────────────────────────────────────────────────────

def _format_size(size: int) -> str:
    """Return a human-readable file size string."""
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024.0:
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{value:.1f} TB"


def _right_aligned(item: QTableWidgetItem) -> QTableWidgetItem:
    item.setTextAlignment(
        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    )
    return item


def _separator() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line
