"""Main application window for PDF Page Size Finder."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
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

    def _make_grid(self) -> QTableWidget:
        table = QTableWidget(0, 4)
        table.setStyleSheet(
            """
            QTableWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
                gridline-color: #2A2A2A;
                selection-background-color: #3A3D41;
                selection-color: #FFFFFF;
            }
            QHeaderView::section:horizontal {
                background-color: #2A2D2E;
                color: #F0F0F0;
                border: 0px;
                border-bottom: 1px solid #3A3A3A;
                padding: 6px;
                font-weight: bold;
            }
            QHeaderView::section:vertical {
                background-color: #252525;
                color: #B0B0B0;
                border: 0px;
                border-right: 1px solid #333333;
            }
            QTableCornerButton::section {
                background-color: #252525;
                border: 0px;
            }
            QTableWidget::item:hover {
                background-color: #2E2E2E;
            }
            """
        )
        table.setHorizontalHeaderLabels(["Size", "Page Range", "Total", ""])
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setShowGrid(False)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(True)
        table.verticalHeader().setDefaultSectionSize(28)
        table.verticalHeader().setMinimumSectionSize(28)
        table.horizontalHeader().setStretchLastSection(False)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(3, 70)

        self._grid = table
        self._add_size_row(LABEL_LETTER)
        self._add_size_row(LABEL_LEGAL)
        return table

    def _add_size_row(self, label_text: str, pages: list[int] | None = None) -> None:
        row = self._grid.rowCount()
        page_range = PdfPageAnalyzer.format_page_range(pages or []) or "—"
        self._grid.insertRow(row)
        self._grid.setItem(row, 0, QTableWidgetItem(label_text))
        self._grid.setItem(row, 1, QTableWidgetItem(page_range))
        self._grid.setItem(row, 2, QTableWidgetItem(str(len(pages)) if pages else "—"))
        copy_button = QPushButton("Copy")
        copy_button.setEnabled(page_range != "—")
        copy_button.setFixedWidth(70)
        copy_button.clicked.connect(
            lambda checked=False, value=page_range: self._copy_range(value)
        )
        self._grid.setCellWidget(row, 3, copy_button)

    def _clear_size_rows(self) -> None:
        self._grid.setRowCount(0)

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
