"""
scripts/_config.py — shared tool paths for the motion pipeline.

Resolution order per tool:
  1. shutil.which()              (PATH — works in any env with ffmpeg installed)
  2. env MOTION_FFMPEG / MOTION_FFPROBE
  3. Known WinGet install path   (fallback for this machine)
"""

import os
import shutil
from pathlib import Path

_WINGET_BIN = Path(
    r"C:\Users\kenne\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.1-full_build\bin"
)

FFMPEG = (
    shutil.which("ffmpeg")
    or os.environ.get("MOTION_FFMPEG")
    or str(_WINGET_BIN / "ffmpeg.exe")
)

FFPROBE = (
    shutil.which("ffprobe")
    or os.environ.get("MOTION_FFPROBE")
    or str(_WINGET_BIN / "ffprobe.exe")
)
