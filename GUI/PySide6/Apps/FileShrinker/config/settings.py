"""Application-wide configuration constants for FileShrinker."""

APP_NAME = "FileShrinker"
APP_VERSION = "1.0.0"

# ── Table row colour coding ────────────────────────────────────────────────
# Material Design 800-level values – used as foreground (text) colour.
COLOR_SAFE = "#2E7D32"       # green-800  → file will be created
COLOR_CONFLICT = "#C62828"   # red-800    → file already exists in target

# ── Shrink output ─────────────────────────────────────────────────────────
SHRINK_BYTE: bytes = b"\x00"  # single null byte written for every output file
