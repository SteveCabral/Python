from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

from utils.ascii_utils import get_char_display, get_description, char_to_hex


class AsciiTableWidget(QTableWidget):
    """Read-only table that shows ASCII/Unicode info for each character."""

    row_clicked = Signal(int)  # emits the 0-based character index

    _HEADERS = ['Char', 'Dec', 'Hex', 'Description']
    CHAR_COL = 0
    DEC_COL  = 1
    HEX_COL  = 2
    DESC_COL = 3

    def __init__(self, parent=None):
        super().__init__(0, len(self._HEADERS), parent)

        self.setHorizontalHeaderLabels(self._HEADERS)

        # Column sizing
        header = self.horizontalHeader()
        header.setSectionResizeMode(self.CHAR_COL, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.DEC_COL,  QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.HEX_COL,  QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.DESC_COL,  QHeaderView.ResizeMode.Stretch)

        # Behaviour
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.verticalHeader().setVisible(False)

        # Fixed-width font for the Char column
        self._mono_font = QFont("Consolas", 11)

        self.cellClicked.connect(self._on_cell_clicked)

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def populate(self, text: str) -> None:
        """Rebuild the table — one row per character in *text*."""
        self.setRowCount(0)
        for i, ch in enumerate(text):
            self.insertRow(i)

            # Char
            char_item = QTableWidgetItem(get_char_display(ch))
            char_item.setFont(self._mono_font)
            char_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(i, self.CHAR_COL, char_item)

            # Dec
            dec_item = QTableWidgetItem(str(ord(ch)))
            dec_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(i, self.DEC_COL, dec_item)

            # Hex
            hex_item = QTableWidgetItem(char_to_hex(ch))
            hex_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(i, self.HEX_COL, hex_item)

            # Description
            self.setItem(i, self.DESC_COL, QTableWidgetItem(get_description(ch)))

    # ------------------------------------------------------------------ #
    #  Internal slots                                                      #
    # ------------------------------------------------------------------ #

    def _on_cell_clicked(self, row: int, _column: int) -> None:
        self.row_clicked.emit(row)
