# Merge Videos

A PySide6 desktop application that merges a user-selected, ordered list of
video files (`.MPEG`, `.FLV`, `.AVI`, `.MP4`, and more) into a single output
file using the [FFmpeg](https://ffmpeg.org/) utility.

---

## Features

- **Add** multiple video files via a native file-picker dialog
- **Ordered list** — the top-to-bottom order in the list is the exact merge
  order passed to FFmpeg
- **Delete** a file from the list
- **Replace** any file in the list with a different file
- **Move Up / Move Down** to reorder files without re-adding them
- **Mixed-extension warning** — if the chosen files have different extensions,
  the app warns you and lets you decide whether to proceed
- **Smart Merge button** — enabled only when:
  1. At least two files are in the list
  2. An output filename has been chosen
  3. The output file's parent directory exists on disk
- Uses FFmpeg's **concat demuxer** with `-c copy` (stream-copy, no
  re-encoding) — fast and lossless for compatible source files

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.11 or later |
| PySide6 | 6.x |
| FFmpeg | Any recent build (must be on the system `PATH`) |

Install Python dependencies (activate your virtual environment first):

```bash
pip install PySide6
```

### Installing FFmpeg on Windows

1. Download the latest FFmpeg Windows build from <https://ffmpeg.org/download.html>
   (e.g. the *gpl* build from [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases)).
2. Extract the archive to a permanent location, e.g. `C:\ffmpeg\`.
3. Add `C:\ffmpeg\bin` to your system `PATH` environment variable.
4. Verify: open a new terminal and run `ffmpeg -version`.

The full path to the FFmpeg executable is already set in `config/settings.py`
(pointing to the WinGet-installed binary). If you ever upgrade FFmpeg or move
it, update the `FFMPEG_EXECUTABLE` constant in that file.

If FFmpeg is reliably on your `PATH` in every terminal you use, you can
simplify the setting to:

```python
FFMPEG_EXECUTABLE = "ffmpeg"
```

---

## Running the Application

```bash
cd GUI/PySide6/Apps/MergeVideos
python main.py
```

---

## Usage

1. **Add files** — click *Add Files…* to select one or more video files.
   Repeat as needed; new files are always appended to the bottom of the list.
2. **Reorder** — select a file in the list and use *Move Up* / *Move Down* to
   place it in the correct position.
3. **Remove or replace** — select a file and click *Delete* to remove it, or
   *Replace…* to substitute it with a different file while keeping its
   position in the list.
4. **Choose output** — click *Browse…* next to "Output File" and enter a
   destination filename (e.g. `D:\Videos\merged.mp4`).
5. **Merge** — once at least two files are listed and a valid output path is
   set, the *Merge* button becomes active. Click it to start the merge.
   A success or error dialog appears when FFmpeg finishes.

---

## How FFmpeg Is Invoked

The app writes a temporary text file (deleted after each run) in FFmpeg's
concat-demuxer format:

```
file '/C/Videos/part1.avi'
file '/C/Videos/part2.avi'
file '/C/Videos/part3.avi'
```

It then runs:

```
ffmpeg -f concat -safe 0 -i <tempfile.txt> -c copy <output_file> -y
```

- `-f concat` — use the concat demuxer (handles any container format)
- `-safe 0` — allow absolute paths in the filelist
- `-c copy` — stream-copy (no re-encoding); very fast, preserves quality
- `-y` — overwrite the output file without prompting if it already exists

> **Note:** `-c copy` requires that all input files use the same codec and,
> for most containers, the same resolution and frame rate. If your files were
> encoded differently, FFmpeg may silently drop frames or produce a corrupted
> output. In that case, remove `-c copy` from `merger.py` and let FFmpeg
> re-encode (slower but more robust).

---

## Project Structure

```
MergeVideos/
    main.py               Entry point
    README.md             Brief overview
    config/
        __init__.py
        settings.py       APP_NAME, FFMPEG_EXECUTABLE, VIDEO_EXTENSIONS
    model/
        __init__.py
        merger.py         VideoMerger — FFmpeg logic, no GUI imports
    view/
        __init__.py
        main_window.py    QMainWindow — all UI code
    docs/
        README.md         This file
```

---

## Known Limitations

- **No progress bar** — FFmpeg runs synchronously on the main thread; the UI
  will be unresponsive during a long merge. For very large files this may take
  several minutes. A future version could move the merge to a background thread
  with a progress indicator.
- **No format conversion** — the app always passes `-c copy`. If you need to
  convert between containers (e.g. `.flv` → `.mp4`) while merging, you must
  edit `model/merger.py` directly.
- **Single merge job** — only one merge at a time is supported.
