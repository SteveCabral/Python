"""Application-wide configuration constants for PDF Page Size Finder."""

APP_NAME = "PDF Page Size Finder"
APP_VERSION = "3.4"
LAST_PDF_PATH_KEY = "last_pdf_path"
# Matches the Visual Studio Code UI/menu font on Windows (Segoe UI, 13 px).
CONTROL_FONT_FAMILIES = ["Segoe UI"]
CONTROL_FONT_SIZE_PX = 13

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

# ── Table text colors ────────────────────────────────────────────────────────
# Text color for the Page Range, Size, and Total cells of Legal rows.
LEGAL_TEXT_COLOR = "#FF0000"
