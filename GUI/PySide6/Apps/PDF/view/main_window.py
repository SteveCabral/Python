"""Main application window for PDF Page Size Finder."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QButtonGroup,
    QFileDialog,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from config.settings import (
    APP_NAME,
    APP_VERSION,
    LABEL_LEGAL,
    LAST_PDF_PATH_KEY,
    LEGAL_TEXT_COLOR,
    MONO_FONT_BOLD,
    MONO_FONT_FAMILIES,
    MONO_FONT_ITALIC,
    MONO_FONT_SIZE_PX,
)
from model.pdf_page_analyzer import PdfPageAnalyzer, PdfPageReport


class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME}  Version {APP_VERSION}")
        self.setMinimumSize(620, 338)

        self._pdf_path: Path | None = None
        self._page_count = 0
        self._settings = QSettings(APP_NAME, APP_NAME)
        self._mono_font = _mono_font()

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
        root.addLayout(self._make_view_buttons())
        root.addWidget(self._make_tables(), stretch=1)
        root.addStretch()

        self.statusBar().setStyleSheet("QStatusBar { border-top: 1px solid #3A3A3A; }")
        self.statusBar().showMessage("Select a PDF file to begin.")

    def _make_browse_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        browse_btn = QPushButton("Open PDF")
        browse_btn.setFixedWidth(120)
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

    def _make_view_buttons(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        self._by_size_btn = QPushButton("By Page Size")
        self._by_page_btn = QPushButton("By Page Range")
        group = QButtonGroup(self)
        group.setExclusive(True)
        for index, button in enumerate((self._by_size_btn, self._by_page_btn)):
            button.setCheckable(True)
            button.setFixedWidth(120)
            group.addButton(button, index)
            row.addWidget(button)
        self._by_size_btn.setChecked(True)
        group.idClicked.connect(self._show_table)
        self._view_group = group
        row.addStretch()

        return row

    def _make_tables(self) -> QStackedWidget:
        self._stack = QStackedWidget()
        self._stack.addWidget(self._make_grid())
        self._stack.addWidget(self._make_page_grid())
        return self._stack

    def _show_table(self, index: int) -> None:
        self._stack.setCurrentIndex(index)

    def _make_page_grid(self) -> QTableWidget:
        table = self._make_table()
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # Roughly 30% of the By Page Size Page Range column (a 70% reduction).
        table.setColumnWidth(0, 100)
        self._page_grid = table
        return table

    def _make_grid(self) -> QTableWidget:
        table = self._make_table()
        self._grid = table
        return table

    def _make_table(self) -> QTableWidget:
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
        table.setHorizontalHeaderLabels(
            ["Page Range", "Page Size (H × W)", "Total Pages", ""]
        )
        for column in (0, 2):
            table.horizontalHeaderItem(column).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setShowGrid(False)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(True)
        table.verticalHeader().setDefaultSectionSize(28)
        table.verticalHeader().setMinimumSectionSize(28)
        table.horizontalHeader().setStretchLastSection(False)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(3, 70)
        return table

    def _add_size_row(self, label_text: str, pages: list[int] | None = None) -> None:
        page_range = PdfPageAnalyzer.format_page_range(pages or []) or "—"
        self._add_row(self._grid, page_range, label_text, len(pages) if pages else None)

    def _add_row(
        self, table: QTableWidget, page_range: str, label_text: str, total: int | None
    ) -> None:
        row = table.rowCount()
        table.insertRow(row)
        items = (
            QTableWidgetItem(page_range),
            QTableWidgetItem(label_text),
            QTableWidgetItem(str(total) if total else "—"),
        )
        for column, item in enumerate(items):
            if column != 1:
                item.setFont(self._mono_font)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if label_text == LABEL_LEGAL:
                item.setForeground(QColor(LEGAL_TEXT_COLOR))
            table.setItem(row, column, item)
        copy_button = QPushButton("Copy")
        copy_button.setEnabled(page_range != "—")
        copy_button.setFixedWidth(70)
        copy_button.clicked.connect(
            lambda checked=False, value=page_range: self._copy_range(value)
        )
        table.setCellWidget(row, 3, copy_button)

    def _clear_size_rows(self) -> None:
        self._grid.setRowCount(0)
        self._page_grid.setRowCount(0)

    def _populate_page_grid(self, size_groups: list[tuple[str, list[int]]]) -> None:
        entries: list[tuple[int, str, str, int]] = []
        for label, pages in size_groups:
            for page_range in PdfPageAnalyzer.split_page_ranges(pages):
                start, _, end = page_range.partition("-")
                total = int(end) - int(start) + 1 if end else 1
                entries.append((int(start), page_range, label, total))
        for _, page_range, label, total in sorted(entries):
            self._add_row(self._page_grid, page_range, label, total)

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
        self.statusBar().showMessage(
            f"{self._page_count} page(s) — Copied page range to clipboard: {range_text}"
        )

    # ------------------------------------------------------------------
    # Grid population
    # ------------------------------------------------------------------

    def _populate_grid(self, report: PdfPageReport) -> None:
        self._clear_size_rows()
        self._page_count = report.page_count
        size_groups = [
            *report.standard_size_pages,
            *report.other_size_pages,
        ]
        for label, pages in size_groups:
            self._add_size_row(label, pages)
        self._populate_page_grid(size_groups)

        message = (
            f"{report.page_count} page(s) — "
            f"{_count_pages(report.standard_size_pages, 'Letter')} Letter, "
            f"{_count_pages(report.standard_size_pages, 'Legal')} Legal"
        )
        if report.standard_size_pages:
            message += f", {len(report.standard_size_pages)} standard size(s)"
        if report.other_pages:
            message += f", {len(report.other_size_pages)} other size(s)"
        self.statusBar().showMessage(message)

    def _reset_grid(self) -> None:
        self._clear_size_rows()
        self._page_count = 0


# ── Module-level helpers ──────────────────────────────────────────────────────

def _mono_font() -> QFont:
    font = QFont()
    font.setFamilies(MONO_FONT_FAMILIES)
    font.setStyleHint(QFont.StyleHint.Monospace)
    font.setPixelSize(MONO_FONT_SIZE_PX)
    font.setBold(MONO_FONT_BOLD)
    font.setItalic(MONO_FONT_ITALIC)
    return font


def _count_pages(size_groups: list[tuple[str, list[int]]], size_name: str) -> int:
    prefix = f"{size_name} ("
    return sum(len(pages) for label, pages in size_groups if label.startswith(prefix))


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
