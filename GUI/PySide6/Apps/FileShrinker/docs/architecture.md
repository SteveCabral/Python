# Architecture

This document describes the internal structure of the FileShrinker application.

## Overview

FileShrinker follows a **Model / View / Configuration** separation pattern.  
Each layer has a distinct responsibility and may be understood or modified 
without touching the other layers.

```
FileShrinker/
├── main.py              ← entry point — bootstraps QApplication and MainWindow
├── README.md            ← root documentation (start here)
├── config/
│   ├── __init__.py
│   └── settings.py      ← application-wide constants (colours, version, byte value)
├── model/
│   ├── __init__.py
│   └── file_shrinker.py ← all file-system logic; no GUI dependencies
├── view/
│   ├── __init__.py
│   └── main_window.py   ← MainWindow widget; delegates work to the model
└── docs/
    ├── architecture.md  ← this file
    └── usage.md         ← step-by-step user guide
```

---

## Layer responsibilities

### `config/settings.py`

Constants only — no logic, no imports beyond the standard library.

| Symbol | Purpose |
|---|---|
| `APP_NAME` | Display name shown in the title bar |
| `APP_VERSION` | Semantic version string |
| `COLOR_SAFE` | Hex text colour for rows with no conflict (green-800) |
| `COLOR_CONFLICT` | Hex text colour for rows with a conflict (red-800) |
| `SHRINK_BYTE` | The single byte (`\x00`) written to every output file |

---

### `model/file_shrinker.py`

Pure business logic; contains no PySide6 imports and is independently testable.

#### `FileInfo`

An immutable `dataclass` representing a single file:

```python
@dataclass(frozen=True)
class FileInfo:
    name: str   # filename only (no directory component)
    path: Path  # full path on disk
    size: int   # size in bytes at scan time
```

#### `FileShrinker`

A stateless class whose three static methods represent the complete lifecycle:

| Method | Description |
|---|---|
| `scan_folder(folder)` | Returns a sorted `list[FileInfo]` of direct children of *folder* |
| `get_conflicts(source_files, target_folder)` | Returns the `set[str]` of filenames present in both places |
| `shrink_files(source_files, target_folder)` | Writes one-byte copies; creates the target folder if needed |

---

### `view/main_window.py`

Owns the entire UI layout. Key components:

| Widget | Role |
|---|---|
| `_source_edit` / `_target_edit` | Read-only line edits showing selected folder paths |
| `_table` (`QTableWidget`) | Five-column comparison grid (source name, source size, target name, target size, status) |
| `_shrink_btn` | Disabled until both folders are selected **and** there are zero conflicts |
| `statusBar()` | Running single-line summary of current state |

Row text colour coding is applied in `_populate_table()`:

- **Green text** (`COLOR_SAFE`) — source file does not yet exist in the target folder.
- **Red text** (`COLOR_CONFLICT`) — source file already exists in the target folder; the shrink operation is blocked.

The refresh cycle (`_refresh()` → `_populate_table()`) is triggered any time a folder selection changes or the ↺ button is pressed.

---

### `main.py`

Minimal entry point: creates `QApplication`, instantiates `MainWindow`, calls `show()` and `exec()`.

---

## Data flow

```
User selects folders
        │
        ▼
_browse_folder() ──► _refresh()
                          │
                          ├─► FileShrinker.scan_folder(source)   ──► _source_files
                          ├─► FileShrinker.get_conflicts(...)     ──► _conflicts
                          └─► _populate_table()
                                    │
                                    └─► Colours rows, enables/disables Shrink button

User clicks "Shrink Files"
        │
        ▼
_on_shrink()
        ├─► re-check conflicts (safety guard)
        ├─► QMessageBox.question() — confirm
        ├─► FileShrinker.shrink_files(source_files, target_folder)
        └─► _refresh()  ── updates table; conflicts now shown for the 1-byte files
```
