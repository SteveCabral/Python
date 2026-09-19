"""Application-wide configuration constants for PDF Page Size Finder."""

APP_NAME = "PDF Page Size Finder"
APP_VERSION = "1.0"
LAST_PDF_PATH_KEY = "last_pdf_path"

# ── Page size detection ─────────────────────────────────────────────────────
# Dimensions are compared in PDF points (1 inch = 72 points), using the
# longer/shorter edge of each page so rotated (landscape) pages still match.
# A small tolerance absorbs the sub-point rounding some PDF producers use.
POINTS_PER_INCH = 72.0
LETTER_SIZE_IN = (8.5, 11.0)
LEGAL_SIZE_IN = (8.5, 14.0)
SIZE_TOLERANCE_PT = 2.0

# ── Row labels ───────────────────────────────────────────────────────────────
LABEL_LETTER = "Letter (8½ × 11)"
LABEL_LEGAL = "Legal (8½ × 14)"
