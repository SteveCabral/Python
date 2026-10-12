"""Business logic for PDF Page Size Finder.

This module is intentionally free of any GUI imports so it can be tested
independently of PySide6.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from config.settings import (
    POINTS_PER_INCH,
    SIZE_TOLERANCE_PT,
    STANDARD_PAGE_SIZES,
)


@dataclass(frozen=True)
class PdfPageReport:
    """Result of scanning a single PDF file."""

    file_name: str
    file_path: Path
    page_count: int
    other_pages: list[int]  # 1-based page numbers that are neither size
    standard_size_pages: list[tuple[str, list[int]]]
    other_size_pages: list[tuple[str, list[int]]]


class PdfPageAnalyzer:
    """Stateless helper that inspects a PDF's page sizes."""

    # ------------------------------------------------------------------
    # Scanning
    # ------------------------------------------------------------------

    @staticmethod
    def analyze(pdf_path: Path) -> PdfPageReport:
        """Read *pdf_path* and classify every page by configured standard size.

        Raises:
            OSError: if the file cannot be read.
            pypdf.errors.PdfReadError: if the file is not a valid PDF.
        """
        reader = PdfReader(str(pdf_path))

        standard_size_pages: dict[str, list[int]] = {
            label: [] for label, _ in STANDARD_PAGE_SIZES
        }
        other_pages: list[int] = []
        other_size_pages: dict[tuple[float, float], list[int]] = {}

        for index, page in enumerate(reader.pages, start=1):
            width_pt = float(page.mediabox.width)
            height_pt = float(page.mediabox.height)
            size = _classify_page(width_pt, height_pt)
            if size in standard_size_pages:
                standard_size_pages[size].append(index)
            else:
                other_pages.append(index)
                dimensions = (
                    _rounded_inches(width_pt),
                    _rounded_inches(height_pt),
                )
                other_size_pages.setdefault(dimensions, []).append(index)

        return PdfPageReport(
            file_name=pdf_path.name,
            file_path=pdf_path,
            page_count=len(reader.pages),
            other_pages=other_pages,
            standard_size_pages=[
                (label, standard_size_pages[label])
                for label, _ in STANDARD_PAGE_SIZES
                if standard_size_pages[label]
            ],
            other_size_pages=[
                (_format_size_label(width, height), pages)
                for (width, height), pages in other_size_pages.items()
            ],
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
        return ", ".join(PdfPageAnalyzer.split_page_ranges(pages))

    @staticmethod
    def split_page_ranges(pages: list[int]) -> list[str]:
        """Split a sorted list of page numbers into individual range strings.

        Example: ``[1, 4, 5]`` -> ``["1", "4-5"]``.
        """
        if not pages:
            return []

        ranges: list[str] = []
        start = prev = pages[0]

        for page in pages[1:]:
            if page == prev + 1:
                prev = page
                continue
            ranges.append(_format_span(start, prev))
            start = prev = page

        ranges.append(_format_span(start, prev))
        return ranges


# ── Module-level helpers ──────────────────────────────────────────────────────

def _classify_page(width_pt: float, height_pt: float) -> str | None:
    """Return a standard size name or label using the page's long/short edges.

    Comparing the sorted (short, long) edges makes the check orientation-
    independent, so landscape-rotated pages still match.
    """
    short_edge, long_edge = sorted((width_pt, height_pt))

    for label, size in STANDARD_PAGE_SIZES:
        if _matches(short_edge, long_edge, size):
            return label
    return None


def _matches(short_edge: float, long_edge: float, size_in: tuple[float, float]) -> bool:
    expected_short = size_in[0] * POINTS_PER_INCH
    expected_long = size_in[1] * POINTS_PER_INCH
    return (
        abs(short_edge - expected_short) <= SIZE_TOLERANCE_PT
        and abs(long_edge - expected_long) <= SIZE_TOLERANCE_PT
    )


def _rounded_inches(points: float) -> float:
    return round(points / POINTS_PER_INCH, 2)


def _format_size_label(width: float, height: float) -> str:
    return f"{width:g} × {height:g}"


def _format_span(start: int, end: int) -> str:
    return str(start) if start == end else f"{start}-{end}"
