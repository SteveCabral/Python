"""Business logic for MergeVideos.

This module is intentionally free of any GUI imports so it can be tested
independently of PySide6.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

from config.settings import FFMPEG_EXECUTABLE


class VideoMerger:
    """Stateless helper that drives all FFmpeg operations."""

    # ------------------------------------------------------------------
    # Inspection helpers
    # ------------------------------------------------------------------

    @staticmethod
    def get_extensions(files: list[Path]) -> set[str]:
        """Return the set of lowercase suffixes present in *files*.

        An empty list returns an empty set.
        """
        return {f.suffix.lower() for f in files if f.suffix}

    # ------------------------------------------------------------------
    # Merge
    # ------------------------------------------------------------------

    @staticmethod
    def merge(input_files: list[Path], output_path: Path) -> tuple[bool, str]:
        """Merge *input_files* into *output_path* using FFmpeg's concat demuxer.

        The files are concatenated in the order given; no re-encoding is
        performed (``-c copy``), so the operation is fast and lossless as long
        as all inputs share the same codec and container.

        Returns:
            ``(True, success_message)`` on success.
            ``(False, error_summary)`` on failure; *error_summary* contains the
            last few lines of FFmpeg's stderr output.

        Raises:
            Nothing — all exceptions are caught and returned as error strings.
        """
        fd, tmp_path = tempfile.mkstemp(suffix=".txt")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                for p in input_files:
                    # FFmpeg filelist format: forward-slash paths, single-quoted.
                    # Escape any embedded single quotes in the path.
                    safe = str(p).replace("\\", "/").replace("'", "\\'")
                    fh.write(f"file '{safe}'\n")

            cmd = [
                FFMPEG_EXECUTABLE,
                "-f", "concat",
                "-safe", "0",
                "-i", tmp_path,
                "-c", "copy",
                str(output_path),
                "-y",           # overwrite output if it already exists
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                return True, f"Merged successfully → {output_path.name}"

            # Provide a concise summary from the end of stderr.
            stderr = result.stderr.strip()
            lines = [ln for ln in stderr.splitlines() if ln.strip()]
            summary = "\n".join(lines[-8:]) if lines else "FFmpeg returned a non-zero exit code."
            return False, summary

        except FileNotFoundError:
            return (
                False,
                f"FFmpeg executable not found: '{FFMPEG_EXECUTABLE}'.\n"
                "Make sure FFmpeg is installed and on your system PATH.",
            )
        except Exception as exc:  # pragma: no cover
            return False, str(exc)
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
