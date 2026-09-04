# FileShrinker

A PySide6 desktop application that creates one-byte copies of every file in a
**Source** folder into a **Target** folder — useful for reproducing a large
directory tree structure without the storage cost of the real file content.

---

## Features

- Browse for source and target folders with native file dialogs
- Side-by-side file comparison table (source name, source size, target name, target size, status)
- Colour-coded rows — **green** for safe files, **red** for conflicts
- Conflict guard: the shrink operation is blocked if any target file already has the same name as a source file
- Live status bar with a summary of current state
- ↺ refresh button to re-scan both folders without reopening a dialog

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.11 or later |
| PySide6 | 6.x |

Install dependencies (activate your virtual environment first):

```bash
pip install PySide6
```

---

## Running the application

```bash
cd GUI/PySide6/Apps/FileShrinker
python main.py
```

---

## Quick start

1. Click **Browse…** next to **Source Folder** and select the folder containing the files you want to shrink.
2. Click **Browse…** next to **Target Folder** and select (or navigate to) an output directory.
3. Review the file comparison table.  Rows highlighted in **red** indicate a conflict — a file with that name already exists in the target folder.
4. Resolve any conflicts (remove or rename the conflicting files, then click ↺), or choose a different target folder.
5. Click **Shrink Files** and confirm.  Each source file is reproduced in the target folder as a single-byte (`0x00`) file with an identical filename.

---

## Project structure

```
FileShrinker/
├── main.py              # Application entry point
├── README.md            # This file
├── config/
│   ├── __init__.py
│   └── settings.py      # App-wide constants (colours, version, byte value)
├── model/
│   ├── __init__.py
│   └── file_shrinker.py # Business logic — no GUI dependencies
├── view/
│   ├── __init__.py
│   └── main_window.py   # PySide6 MainWindow
└── docs/
    ├── architecture.md  # Architecture and data-flow documentation
    └── usage.md         # Step-by-step user guide
```

---

## Documentation

- [Usage guide](docs/usage.md) — detailed walkthrough with FAQs
- [Architecture](docs/architecture.md) — module design, data flow, and extension points

---

## Conflict behaviour

If the target folder already contains **any** file sharing a name with a source
file, FileShrinker will:

1. Highlight those rows in **red** in the comparison table.
2. Disable the **Shrink Files** button.
3. Display a blocking error dialog if the button is somehow activated.

No files are ever created or overwritten until every conflict is resolved and the
user confirms the operation.

---

## Notes

- Only **direct** children of the source folder are processed; sub-folders are ignored.
- The target folder is created automatically (including missing parent directories) if it does not exist when the shrink operation runs.
- After a successful shrink, refreshing will show all rows as conflicts because the 1-byte copies now exist in the target folder.
