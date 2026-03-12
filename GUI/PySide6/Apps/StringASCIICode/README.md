# String ASCII Code Viewer

A PySide6 desktop application that displays the ASCII / Unicode properties of every character in a string — one row per character, updated live as you type.

## Features

- **Live update** — the table rebuilds with every keystroke
- **1–255 character input** enforced; paste is automatically clipped to fit
- **Non-printable characters** (space, tab, CR, LF, NUL, ESC, …) shown using `<TOKEN>` notation in the Char column
- **Click a table row** to highlight the corresponding character in the input field
- **Dark theme** consistent with the rest of the PySide6 app collection

## Table Columns

| Column      | Description |
|-------------|-------------|
| **Char**    | The character rendered in a fixed-width (Consolas) font. Non-printable characters are shown as `<SP>`, `<TAB>`, `<CR>`, `<LF>`, `<NUL>`, `<ESC>`, `<DEL>`, etc. |
| **Dec**     | Decimal code point (ASCII/Unicode) |
| **Hex**     | Hexadecimal code point (e.g. `0x41`) |
| **Description** | Unicode character name (e.g. `LATIN CAPITAL LETTER A`) |

## Requirements

- Python 3.11+
- PySide6

```
pip install PySide6
```

## Usage

```
cd "GUI/PySide6/Apps/StringASCIICode"
python main.py
```

## File Structure

```
StringASCIICode/
├── README.md
├── main.py                  ← QApplication entry point
├── app_window.py            ← Main window and single-line input widget
├── ascii_table_widget.py    ← 4-column read-only table widget
├── config/
│   ├── config_manager.py    ← Singleton JSON config loader
│   └── config.json          ← App settings (title, window size, max_chars)
├── themes/
│   └── theme_manager.py     ← Dark QSS stylesheet
└── utils/
    └── ascii_utils.py       ← Character display helpers (get_char_display, get_description, char_to_hex)
```
