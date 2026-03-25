# Usage Guide

A step-by-step walkthrough of FileShrinker.

---

## Prerequisites

- Python 3.11 or later
- PySide6 installed in your active virtual environment:

```
pip install PySide6
```

---

## Starting the application

Run from the `FileShrinker` directory:

```
cd GUI/PySide6/Apps/FileShrinker
python main.py
```

The main window opens with an empty file table and both folder fields blank.

---

## Step 1 — Select the Source Folder

Click **Browse…** next to **Source Folder** and navigate to the directory whose
files you want to shrink.  Once confirmed, the table immediately populates with
every *direct* file in that folder (sub-folders are not included).

Each row's text is coloured **green** by default, indicating the file is safe to shrink
once a target folder is chosen.

> **Tip:** Clicking ↺ next to either folder field re-scans both folders without
> reopening the file dialog.  Use this if files are added or removed externally
> while the application is open.

---

## Step 2 — Select the Target Folder

Click **Browse…** next to **Target Folder** and select (or navigate to) the
output directory.

The table updates immediately:

| Condition | Row text colour | Status column text |
|---|---|---|
| File does **not** exist in target | Green | `Will be created` |
| File **already exists** in target | Red | `CONFLICT — already exists` |

The **Shrink Files** button is enabled only when **all** rows are green
(no conflicts) and both folders have been selected.

---

## Step 3 — Resolve conflicts (if any)

If one or more rows have red text, the shrink operation is blocked.

Options to resolve a conflict:

- Remove or rename the conflicting file(s) in the target folder, then press ↺ to refresh.
- Choose a different target folder that does not contain any of the source filenames.

---

## Step 4 — Shrink the files

Click **Shrink Files**.

A confirmation dialog displays the number of files to be created and the target
path.  Click **Yes** to proceed.

FileShrinker writes a single null byte (`0x00`) to each output file.  The target
folder is created automatically if it does not exist.

After completion:

- The status bar reports how many files were written.
- The table refreshes; all rows now show **red** (the 1-byte copies exist in the
  target folder).

---

## Understanding the output

Each file in the target folder:

- Has the **same filename** as its source counterpart.
- Contains exactly **1 byte** (`0x00`).
- Has a reported size of **1 B** in the Target Size column after a refresh.

This is useful for testing workflows that need to reference a large set of
filenames without the storage cost of the real content.

---

## Frequently asked questions

**Q: Are sub-folders included?**  
A: No. Only files directly inside the source folder are processed.

**Q: Can I run it again on the same pair of folders?**  
A: Not without first clearing the target folder.  Because the 1-byte copies now
exist there, every row will show as a conflict and the button will be disabled.

**Q: What happens if the target folder does not exist?**  
A: FileShrinker creates it (and any missing parent directories) automatically
when you click **Shrink Files**.

**Q: What byte value is written?**  
A: A single null byte (`\x00`).  This value is defined in
`config/settings.py` as `SHRINK_BYTE` and can be changed there if needed.
