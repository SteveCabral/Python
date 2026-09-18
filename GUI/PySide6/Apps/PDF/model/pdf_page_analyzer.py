"""Business logic for PDF Page Size Finder.

This module is intentionally free of any GUI imports so it can be tested
independently of PySide6.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from config.settings import (
    LABEL_LEGAL,
    LABEL_LETTER,
    LEGAL_SIZE_IN,
    LETTER_SIZE_IN,
    POINTS_PER_INCH,
    SIZE_TOLERANCE_PT,
)


@dataclass(frozen=True)
class PdfPageReport:
    """Result of scanning a single PDF file."""

    file_name: str
    file_path: Path
    page_count: int
    letter_pages: list[int]  # 1-based page numbers
    legal_pages: list[int]  # 1-based page numbers
    other_pages: list[int]  # 1-based page numbers that are neither size


class PdfPageAnalyzer:
    """Stateless helper that inspects a PDF's page sizes."""

    # ------------------------------------------------------------------
    # Scanning
    # ------------------------------------------------------------------

    @staticmethod
    def analyze(pdf_path: Path) -> PdfPageReport:
        """Read *pdf_path* and classify every page as Letter, Legal, or other.

        Raises:
            OSError: if the file cannot be read.
            pypdf.errors.PdfReadError: if the file is not a valid PDF.
        """
        reader = PdfReader(str(pdf_path))

        letter_pages: list[int] = []
        legal_pages: list[int] = []
        other_pages: list[int] = []

        for index, page in enumerate(reader.pages, start=1):
            width_pt = float(page.mediabox.width)
            height_pt = float(page.mediabox.height)
            size = _classify_page(width_pt, height_pt)
            if size == LABEL_LETTER:
                letter_pages.append(index)
            elif size == LABEL_LEGAL:
                legal_pages.append(index)
            else:
                other_pages.append(index)

        return PdfPageReport(
            file_name=pdf_path.name,
            file_path=pdf_path,
            page_count=len(reader.pages),
            letter_pages=letter_pages,
            legal_pages=legal_pages,
            other_pages=other_pages,
        )

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    @staticmethod
    def format_page_range(pages: list[int]) -> str:
        """Collapse a sorted list of 1-based page numbers into a range string.

        Example: ``[1, 2, 4]`` -> ``"1-2, 4"``.  Returns an empty string for
        an empty list.
        """
        if not pages:
            return ""

        ranges: list[str] = []
        start = prev = pages[0]

        for page in pages[1:]:
            if page == prev + 1:
                prev = page
                continue
            ranges.append(_format_span(start, prev))
            start = prev = page

        ranges.append(_format_span(start, prev))
        return ", ".join(ranges)


# ── Module-level helpers ──────────────────────────────────────────────────────

def _classify_page(width_pt: float, height_pt: float) -> str | None:
    """Return "Letter", "Legal", or None using the page's long/short edges.

    Comparing the sorted (short, long) edges makes the check orientation-
    independent, so landscape-rotated pages still match.
    """
    short_edge, long_edge = sorted((width_pt, height_pt))

    if _matches(short_edge, long_edge, LETTER_SIZE_IN):
        return LABEL_LETTER
    if _matches(short_edge, long_edge, LEGAL_SIZE_IN):
        return LABEL_LEGAL
    return None


def _matches(short_edge: float, long_edge: float, size_in: tuple[float, float]) -> bool:
    expected_short = size_in[0] * POINTS_PER_INCH
    expected_long = size_in[1] * POINTS_PER_INCH
    return (
        abs(short_edge - expected_short) <= SIZE_TOLERANCE_PT
        and abs(long_edge - expected_long) <= SIZE_TOLERANCE_PT
    )


def _format_span(start: int, end: int) -> str:
    return str(start) if start == end else f"{start}-{end}"
