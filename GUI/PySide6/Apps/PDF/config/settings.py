"""Application-wide configuration constants for PDF Page Size Finder."""

APP_NAME = "PDF Page Size Finder"
APP_VERSION = "3.6"
LAST_PDF_PATH_KEY = "last_pdf_path"
# Matches the Visual Studio Code UI/menu font on Windows (Segoe UI, 13 px).
CONTROL_FONT_FAMILIES = ["Segoe UI"]
CONTROL_FONT_SIZE_PX = 13

# Fixed-width font for the Page Range and Total Pages columns; matches the
# Visual Studio Code editor font on Windows (Consolas, 14 px).
MONO_FONT_FAMILIES = ["Consolas", "Courier New", "monospace"]
MONO_FONT_SIZE_PX = 14
MONO_FONT_BOLD = False
MONO_FONT_ITALIC = False

# ── Page size detection ─────────────────────────────────────────────────────
# Dimensions are compared in PDF points (1 inch = 72 points), using the
# longer/shorter edge of each page so rotated (landscape) pages still match.
# A small tolerance absorbs the sub-point rounding some PDF producers use.
POINTS_PER_INCH = 72.0
LETTER_SIZE_IN = (8.5, 11.0)
LEGAL_SIZE_IN = (8.5, 14.0)
SIZE_TOLERANCE_PT = 2.0

# ── Standard size labels ─────────────────────────────────────────────────────
LABEL_LETTER = "Letter (8½ × 11)"
LABEL_LEGAL = "Legal (8½ × 14)"

# Standard PDF page sizes. Values are (display label, (short edge, long edge)),
# in inches. Keep the display label here so all standard-size rows use one
# source of truth.
STANDARD_PAGE_SIZES = (
    (LABEL_LETTER, LETTER_SIZE_IN),
    (LABEL_LEGAL, LEGAL_SIZE_IN),
    ("A4 (8.27 × 11.69)", (8.27, 11.69)),
    ("A3 (11.69 × 16.54)", (11.69, 16.54)),
    ("A5 (5.83 × 8.27)", (5.83, 8.27)),
    ("B5 (6.93 × 9.84)", (6.93, 9.84)),
    ("Executive (7.25 × 10.5)", (7.25, 10.5)),
    ("Statement (5.5 × 8.5)", (5.5, 8.5)),
    ("Folio (8.5 × 13)", (8.5, 13.0)),
    ("Tabloid (11 × 17)", (11.0, 17.0)),
)

# ── Table text colors ────────────────────────────────────────────────────────
# Text color for the Page Range, Page Size, and Total Pages cells of Legal rows.
LEGAL_TEXT_COLOR = "#FF0000"
