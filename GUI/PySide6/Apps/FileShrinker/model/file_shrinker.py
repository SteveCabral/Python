"""Business logic for FileShrinker.

This module is intentionally free of any GUI imports so it can be tested
independently of PySide6.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config.settings import SHRINK_BYTE


@dataclass(frozen=True)
class FileInfo:
    """Lightweight, immutable snapshot of a single file on disk."""

    name: str
    path: Path
    size: int


class FileShrinker:
    """Stateless helper that performs all file-system operations."""

    # ------------------------------------------------------------------
    # Scanning
    # ------------------------------------------------------------------

    @staticmethod
    def scan_folder(folder: Path) -> list[FileInfo]:
        """Return a sorted list of *direct* (non-recursive) files in *folder*.

        Returns an empty list if *folder* does not exist or contains no files.
        """
        if not folder.is_dir():
            return []
        return [
            FileInfo(name=f.name, path=f, size=f.stat().st_size)
            for f in sorted(folder.iterdir())
            if f.is_file()
        ]

    @staticmethod
    def get_conflicts(
        source_files: list[FileInfo],
        target_folder: Path,
    ) -> set[str]:
        """Return the set of filenames present in both *source_files* and *target_folder*.

        Returns an empty set when *target_folder* does not yet exist.
        """
        if not target_folder.is_dir():
            return set()
        target_names: set[str] = {
            f.name for f in target_folder.iterdir() if f.is_file()
        }
        return {fi.name for fi in source_files if fi.name in target_names}

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    @staticmethod
    def shrink_files(
        source_files: list[FileInfo],
        target_folder: Path,
    ) -> list[Path]:
        """Create a one-byte copy of each file in *source_files* inside *target_folder*.

        The target folder is created (including any missing parents) if it does
        not already exist.  Each output file contains exactly ``SHRINK_BYTE``.

        Returns the list of :class:`~pathlib.Path` objects that were written.

        Raises:
            OSError: if any file cannot be written.
        """
        target_folder.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        for fi in source_files:
            out = target_folder / fi.name
            out.write_bytes(SHRINK_BYTE)
            created.append(out)
        return created
