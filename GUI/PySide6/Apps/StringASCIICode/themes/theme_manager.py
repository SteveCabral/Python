from typing import Optional
from PySide6.QtWidgets import QApplication


_DARK_QSS = """
/* ── Base ─────────────────────────────────────────────── */
QWidget {
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

/* ── Input field ──────────────────────────────────────── */
QTextEdit {
    background-color: #2d2d2d;
    color: #d4d4d4;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 4px 6px;
    selection-background-color: #264f78;
    selection-color: #ffffff;
}

QTextEdit:focus {
    border: 1px solid #007acc;
}

/* ── Table ────────────────────────────────────────────── */
QTableWidget {
    background-color: #252526;
    alternate-background-color: #2a2a2b;
    color: #d4d4d4;
    gridline-color: #3c3c3c;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
}

QTableWidget::item {
    padding: 4px 8px;
}

QTableWidget::item:selected {
    background-color: #094771;
    color: #ffffff;
}

/* ── Header ───────────────────────────────────────────── */
QHeaderView::section {
    background-color: #3c3c3c;
    color: #cccccc;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #4c4c4c;
    border-bottom: 1px solid #4c4c4c;
    font-weight: bold;
}

/* ── Labels ───────────────────────────────────────────── */
QLabel {
    color: #d4d4d4;
    background-color: transparent;
}

QLabel[heading="true"] {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
}

QLabel[secondary="true"] {
    color: #888888;
    font-size: 11px;
}

/* ── Scrollbars ───────────────────────────────────────── */
QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #4c4c4c;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #686868;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #1e1e1e;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #4c4c4c;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #686868;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""

# Orange accent used to highlight the selected character in the input field.
HIGHLIGHT_BG = "#ff8c00"
HIGHLIGHT_FG = "#000000"


class ThemeManager:
    """Singleton theme manager — applies the dark QSS stylesheet."""

    _instance: Optional['ThemeManager'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def apply_dark_theme(self, app: QApplication) -> None:
        app.setStyleSheet(_DARK_QSS)

    @staticmethod
    def highlight_colors() -> tuple[str, str]:
        """Return (background, foreground) hex strings for the char highlight."""
        return HIGHLIGHT_BG, HIGHLIGHT_FG


theme_manager = ThemeManager()
