# PDF Page Size Finder

A PySide6 desktop application that scans a PDF file and reports which pages
are **Letter** size (8.5 × 11 in) and which are **Legal** size (8.5 × 14 in) —
useful for printing mixed-size documents with the correct page range typed
into the Windows Print dialog box.

---

## Features

- Browse for a PDF file with a native file dialog
- Displays the selected file's name and full path
- Grid with one row for **Letter** pages and one row for **Legal** pages, each showing:
  - A compact page-range string (e.g. `1-2, 4`)
  - A **Copy** button that copies that range to the clipboard for pasting into Print → Pages
- Orientation-independent size detection — rotated (landscape) pages are still matched correctly

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.11 or later |
| PySide6 | 6.x |
| pypdf | latest |

Install dependencies (activate your virtual environment first):

```bash
pip install -r requirements.txt
```

---

## Running the application

```bash
cd GUI/PySide6/Apps/PDF
python main.py
```

---

## Quick start

1. Click **Browse for PDF…** and select the PDF file you want to inspect.
2. The **File Name** and **File Path** fields update to show the selected file.
3. The grid shows the page range for **Letter** pages and for **Legal** pages, e.g. a
   6-page PDF with Letter pages 1, 2, & 4 and Legal pages 3, 5, & 6 shows:

   | Size | Page Range | |
   |---|---|---|
   | Letter | 1-2, 4 | Copy |
   | Legal | 3, 5-6 | Copy |

4. Click **Copy** next to either row to copy that page range to the clipboard.
5. Paste the copied text into the **Pages** field of the Windows Print dialog box to print only that size's pages.

---

## Project structure

```
PDF/
├── main.py                    # Application entry point
├── README.md                  # This file
├── requirements.txt           # PySide6 + pypdf
├── config/
│   ├── __init__.py
│   └── settings.py            # App-wide constants (size thresholds, labels, version)
├── model/
│   ├── __init__.py
│   └── pdf_page_analyzer.py   # Business logic — no GUI dependencies
├── view/
│   ├── __init__.py
│   └── main_window.py         # PySide6 MainWindow
└── docs/
    ├── architecture.html      # Architecture and data-flow documentation
    └── usage.html             # Step-by-step user guide
```

---

## Documentation

- [Usage guide](docs/usage.html) — detailed walkthrough
- [Architecture](docs/architecture.html) — module design, data flow, and extension points

---

## Notes

- Page size is determined from each page's `mediabox` dimensions, compared in PDF points (1 in = 72 pt) with a small tolerance for rounding.
- Pages that are neither Letter nor Legal sized are counted in the status bar but not shown in the grid.
- Selecting a new PDF file replaces all previous results.
