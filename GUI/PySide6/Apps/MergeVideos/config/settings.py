"""Application-wide configuration constants for MergeVideos."""

APP_NAME = "Merge Videos"
APP_VERSION = "1.0.0"

# FFmpeg executable path.
# Using the full path guarantees the correct binary is found even in
# terminal sessions that were opened before WinGet updated the PATH
# environment variable (the PATH change only takes effect in new shells
# opened after installation, or after a reboot).
# If "ffmpeg" is reliably on your PATH in every terminal you use,
# you can replace the line below with just: FFMPEG_EXECUTABLE = "ffmpeg"
FFMPEG_EXECUTABLE = (
    r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
)

# File-dialog filter extensions (QFileDialog glob format).
VIDEO_EXTENSIONS: list[str] = [
    "*.mpeg", "*.mpg", "*.mp4", "*.avi", "*.flv",
    "*.mkv", "*.mov", "*.wmv", "*.m4v", "*.ts",
    "*.webm", "*.3gp", "*.ogv",
]
