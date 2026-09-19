"""Main application window for PDF Page Size Finder."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from config.settings import (
    APP_NAME,
    APP_VERSION,
    LABEL_LEGAL,
    LABEL_LETTER,
    LAST_PDF_PATH_KEY,
)
from model.pdf_page_analyzer import PdfPageAnalyzer, PdfPageReport


class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME}  Version {APP_VERSION}")
        self.setMinimumSize(620, 338)

        self._pdf_path: Path | None = None
        self._settings = QSettings(APP_NAME, APP_NAME)

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setSpacing(10)
        root.setContentsMargins(14, 14, 14, 10)

        root.addLayout(self._make_browse_row())
        root.addLayout(self._make_info_rows())
        root.addWidget(_separator())
        root.addWidget(self._make_grid(), stretch=1)
        root.addStretch()

        self.statusBar().showMessage("Select a PDF file to begin.")

    def _make_browse_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        browse_btn = QPushButton("Open PDF")
        browse_btn.setFixedWidth(150)
        browse_btn.clicked.connect(self._browse_pdf)
        row.addWidget(browse_btn)
        row.addStretch()

        return row

    def _make_info_rows(self) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(4)

        name_row = QHBoxLayout()
        name_row.addWidget(_field_label("File Name:"))
        self._name_value = QLabel("—")
        name_row.addWidget(self._name_value)
        name_row.addStretch()
        col.addLayout(name_row)

        path_row = QHBoxLayout()
        path_row.addWidget(_field_label("File Path:"))
        self._path_value = QLabel("—")
        self._path_value.setWordWrap(True)
        path_row.addWidget(self._path_value, stretch=1)
        col.addLayout(path_row)

        return col

    def _make_grid(self) -> QWidget:
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(3)

        header = QGridLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setHorizontalSpacing(12)
        header.setVerticalSpacing(0)
        headers = ["Size", "Page Range", "Total", ""]
        for col, text in enumerate(headers):
            header_label = QLabel(text)
            header_label.setStyleSheet("font-weight: bold;")
            header.addWidget(header_label, 0, col)
        header.setColumnMinimumWidth(2, 40)
        header.setColumnMinimumWidth(3, 70)
        header.setColumnStretch(1, 1)
        container_layout.addLayout(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(4)

        self._grid = grid
        self._size_rows: list[tuple[QLabel, QLabel, QLabel, QPushButton]] = []
        self._add_size_row(LABEL_LETTER)
        self._add_size_row(LABEL_LEGAL)
        grid.setColumnMinimumWidth(2, 40)
        grid.setColumnMinimumWidth(3, 70)
        grid.setColumnStretch(1, 1)
        scroll_area.setWidget(grid_widget)
        container_layout.addWidget(scroll_area)
        return container

    def _add_size_row(self, label_text: str, pages: list[int] | None = None) -> None:
        row = len(self._size_rows) + 1
        page_range = PdfPageAnalyzer.format_page_range(pages or []) or "—"
        label = QLabel(label_text)
        range_value = QLabel(page_range)
        total_value = QLabel(str(len(pages)) if pages else "—")
        copy_button = QPushButton("Copy")
        copy_button.setEnabled(page_range != "—")
        copy_button.setFixedWidth(70)
        copy_button.clicked.connect(
            lambda checked=False, value=range_value: self._copy_range(value.text())
        )
        self._grid.addWidget(label, row, 0)
        self._grid.addWidget(range_value, row, 1)
        self._grid.addWidget(total_value, row, 2)
        self._grid.addWidget(copy_button, row, 3)
        self._size_rows.append((label, range_value, total_value, copy_button))

    def _clear_size_rows(self) -> None:
        for label, range_value, total_value, copy_button in self._size_rows:
            self._grid.removeWidget(label)
            self._grid.removeWidget(range_value)
            self._grid.removeWidget(total_value)
            self._grid.removeWidget(copy_button)
            label.deleteLater()
            range_value.deleteLater()
            total_value.deleteLater()
            copy_button.deleteLater()
        self._size_rows.clear()

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _browse_pdf(self) -> None:
        saved_value = self._settings.value(LAST_PDF_PATH_KEY, "")
        saved_path = Path(saved_value) if saved_value else None
        start_path = self._pdf_path or saved_path or Path.home()
        start = str(start_path.parent if start_path else Path.home())
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open PDF", start, "PDF Files (*.pdf)"
        )
        if not file_name:
            return

        path = Path(file_name)
        self._pdf_path = path
        self._settings.setValue(LAST_PDF_PATH_KEY, str(path))
        self._name_value.setText(path.name)
        self._path_value.setText(str(path))

        try:
            report = PdfPageAnalyzer.analyze(path)
        except Exception as exc:  # pypdf raises a range of format-specific errors
            QMessageBox.critical(self, "Unable to Read PDF", f"Failed to read PDF:\n\n{exc}")
            self._reset_grid()
            return

        self._populate_grid(report)

    def _copy_range(self, range_text: str) -> None:
        if not range_text or range_text == "—":
            return
        QApplication.clipboard().setText(range_text)
        self.statusBar().showMessage(f"Copied page range to clipboard: {range_text}")

    # ------------------------------------------------------------------
    # Grid population
    # ------------------------------------------------------------------

    def _populate_grid(self, report: PdfPageReport) -> None:
        self._clear_size_rows()
        size_groups = [
            (LABEL_LETTER, report.letter_pages),
            (LABEL_LEGAL, report.legal_pages),
            *report.other_size_pages,
        ]
        for label, pages in size_groups:
            self._add_size_row(label, pages)

        message = (
            f"{report.page_count} page(s) — "
            f"{len(report.letter_pages)} Letter, {len(report.legal_pages)} Legal"
        )
        if report.other_pages:
            message += f", {len(report.other_size_pages)} other size(s)"
        self.statusBar().showMessage(message)

    def _reset_grid(self) -> None:
        self._clear_size_rows()
        self._add_size_row(LABEL_LETTER)
        self._add_size_row(LABEL_LEGAL)


# ── Module-level helpers ──────────────────────────────────────────────────────

def _field_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setFixedWidth(80)
    label.setStyleSheet("font-weight: bold;")
    return label


def _separator() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line
