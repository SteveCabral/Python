from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor, QFont

from config.config_manager import config
from ascii_table_widget import AsciiTableWidget
from themes.theme_manager import theme_manager


class _BoundedTextEdit(QTextEdit):
    """Single-line QTextEdit that blocks Enter/Return and enforces a max length.

    Using QTextEdit (rather than QLineEdit) enables per-character colour
    formatting via QTextCharFormat, which is needed for the row-highlight feature.
    """

    def __init__(self, max_chars: int, parent=None):
        super().__init__(parent)
        self._max_chars = max_chars
        self.setFixedHeight(44)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFont(QFont("Consolas", 11))

    def keyPressEvent(self, event):
        # Always block newlines — this widget is intentionally single-line.
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            return

        ctrl_held = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
        is_nav_or_delete = event.key() in (
            Qt.Key.Key_Backspace, Qt.Key.Key_Delete,
            Qt.Key.Key_Left, Qt.Key.Key_Right,
            Qt.Key.Key_Home, Qt.Key.Key_End,
        )

        # Block regular character input once the limit is reached.
        if not ctrl_held and not is_nav_or_delete and len(self.toPlainText()) >= self._max_chars:
            return

        super().keyPressEvent(event)

    def insertFromMimeData(self, source):
        """Clip pasted text to the remaining capacity and strip newlines."""
        remaining = self._max_chars - len(self.toPlainText())
        if remaining <= 0:
            return
        # Collapse any embedded newlines so the widget stays single-line.
        text = source.text().replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        self.insertPlainText(text[:remaining])


class AppWindow(QWidget):
    """Main application window."""

    def __init__(self):
        super().__init__()
        app_cfg = config.get_app_config()
        self.setWindowTitle(app_cfg.get("title", "String ASCII Code Viewer"))
        self._max_chars: int = app_cfg.get("max_chars", 255)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # ── Heading ────────────────────────────────────────────────────
        heading = QLabel(app_cfg.get("title", "String ASCII Code Viewer"))
        heading.setProperty("heading", True)
        layout.addWidget(heading)

        # ── Input row ──────────────────────────────────────────────────
        input_row = QHBoxLayout()
        input_row.setSpacing(8)

        input_label = QLabel("Input:")
        input_label.setFixedWidth(46)

        self._input = _BoundedTextEdit(self._max_chars)

        self._char_count = QLabel(f"0 / {self._max_chars}")
        self._char_count.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._char_count.setFixedWidth(72)

        input_row.addWidget(input_label)
        input_row.addWidget(self._input, 1)
        input_row.addWidget(self._char_count)
        layout.addLayout(input_row)

        # ── Table ──────────────────────────────────────────────────────
        self._table = AsciiTableWidget()
        layout.addWidget(self._table, 1)

        # ── Hint ───────────────────────────────────────────────────────
        hint = QLabel("Click a row to highlight its character in the input field.")
        hint.setProperty("secondary", True)
        layout.addWidget(hint)

        # ── Signal wiring ──────────────────────────────────────────────
        self._input.textChanged.connect(self._on_text_changed)
        self._table.row_clicked.connect(self._on_row_clicked)

    # ------------------------------------------------------------------ #
    #  Slots                                                               #
    # ------------------------------------------------------------------ #

    def _on_text_changed(self) -> None:
        text = self._input.toPlainText()
        self._char_count.setText(f"{len(text)} / {self._max_chars}")

        # Clear any existing highlight without re-triggering this slot.
        self._input.blockSignals(True)
        try:
            cursor = self._input.textCursor()
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(QTextCharFormat())   # reset to default
            cursor.clearSelection()
            self._input.setTextCursor(cursor)
        finally:
            self._input.blockSignals(False)

        self._table.populate(text)

    def _on_row_clicked(self, index: int) -> None:
        """Highlight the character at position *index* inside the input field."""
        text = self._input.toPlainText()
        if index < 0 or index >= len(text):
            return

        hl_bg, hl_fg = theme_manager.highlight_colors()

        self._input.blockSignals(True)
        try:
            # 1. Clear all existing formatting
            cursor = self._input.textCursor()
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(QTextCharFormat())

            # 2. Apply accent highlight to the target character
            cursor.setPosition(index)
            cursor.movePosition(
                QTextCursor.MoveOperation.NextCharacter,
                QTextCursor.MoveMode.KeepAnchor,
            )
            fmt = QTextCharFormat()
            fmt.setBackground(QColor(hl_bg))
            fmt.setForeground(QColor(hl_fg))
            cursor.setCharFormat(fmt)

            # 3. Collapse selection so the caret sits after the highlight
            cursor.clearSelection()
            self._input.setTextCursor(cursor)
        finally:
            self._input.blockSignals(False)
