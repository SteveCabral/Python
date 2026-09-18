"""Main application window for PDF Page Size Finder."""

from __future__ import annotations

from pathlib import Path

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
    QVBoxLayout,
    QWidget,
)

from config.settings import APP_NAME, APP_VERSION, LABEL_LEGAL, LABEL_LETTER
from model.pdf_page_analyzer import PdfPageAnalyzer, PdfPageReport


class MainWindow(QMainWindow):
    """Primary application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME}  v{APP_VERSION}")
        self.setMinimumSize(620, 260)

        self._pdf_path: Path | None = None

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
        root.addLayout(self._make_grid())
        root.addStretch()

        self.statusBar().showMessage("Select a PDF file to begin.")

    def _make_browse_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        browse_btn = QPushButton("Browse for PDF…")
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

    def _make_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)

        headers = ["Size", "Page Range", ""]
        for col, text in enumerate(headers):
            header = QLabel(text)
            header.setStyleSheet("font-weight: bold;")
            grid.addWidget(header, 0, col)

        self._letter_range_value = QLabel("—")
        self._legal_range_value = QLabel("—")

        self._letter_copy_btn = QPushButton("Copy")
        self._legal_copy_btn = QPushButton("Copy")
        self._letter_copy_btn.setEnabled(False)
        self._legal_copy_btn.setEnabled(False)
        self._letter_copy_btn.setFixedWidth(70)
        self._legal_copy_btn.setFixedWidth(70)
        self._letter_copy_btn.clicked.connect(
            lambda: self._copy_range(self._letter_range_value.text())
        )
        self._legal_copy_btn.clicked.connect(
            lambda: self._copy_range(self._legal_range_value.text())
        )

        grid.addWidget(QLabel(LABEL_LETTER), 1, 0)
        grid.addWidget(self._letter_range_value, 1, 1)
        grid.addWidget(self._letter_copy_btn, 1, 2)

        grid.addWidget(QLabel(LABEL_LEGAL), 2, 0)
        grid.addWidget(self._legal_range_value, 2, 1)
        grid.addWidget(self._legal_copy_btn, 2, 2)

        grid.setColumnStretch(1, 1)
        return grid

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _browse_pdf(self) -> None:
        start = str(self._pdf_path.parent if self._pdf_path else Path.home())
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", start, "PDF Files (*.pdf)"
        )
        if not file_name:
            return

        path = Path(file_name)
        self._pdf_path = path
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
        letter_range = PdfPageAnalyzer.format_page_range(report.letter_pages)
        legal_range = PdfPageAnalyzer.format_page_range(report.legal_pages)

        self._letter_range_value.setText(letter_range or "—")
        self._legal_range_value.setText(legal_range or "—")
        self._letter_copy_btn.setEnabled(bool(letter_range))
        self._legal_copy_btn.setEnabled(bool(legal_range))

        message = (
            f"{report.page_count} page(s) — "
            f"{len(report.letter_pages)} Letter, {len(report.legal_pages)} Legal"
        )
        if report.other_pages:
            message += f", {len(report.other_pages)} other size"
        self.statusBar().showMessage(message)

    def _reset_grid(self) -> None:
        self._letter_range_value.setText("—")
        self._legal_range_value.setText("—")
        self._letter_copy_btn.setEnabled(False)
        self._legal_copy_btn.setEnabled(False)


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
