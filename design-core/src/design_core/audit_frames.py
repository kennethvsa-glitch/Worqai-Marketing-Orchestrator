"""Pixel-level anti-slop audit for any rendered WorqAI frame.

Works on a single image (carousel slide, post picture) or frames extracted
from a video (reel, motion). Enforces the deterministic visual gates: accent
footprint (lime <= 8% of frame), pure #000/#fff dominance, black frames, and
a caption/text-band contrast estimate. Judgment gates ("could this pass for a
generic SaaS promo?") stay human -- this covers what pixels can prove.

Uses ffmpeg/ffprobe to decode (no Pillow dependency) and numpy to analyze.

Usage:
    python -m design_core.audit_frames <image-or-video> [--frames 12] [--json out.json]
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

from .contract import ACCENT_MAX_FRACTION, COLORS, GateFailure, hex_to_rgb, report

LIME = np.array(hex_to_rgb(COLORS["lime"]), dtype=np.float32)
COLOR_DIST = 60.0
BLACK_LUMA = 8.0
NEARBLACK_FRACTION = 0.985
TEXT_BAND = (0.60, 0.95)   # where captions/headlines usually sit
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm"}
LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def _probe_wh(path: Path) -> tuple[int, int]:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    w, h = (int(x) for x in res.stdout.strip().split(",")[:2])
    return w, h


def _probe_duration(path: Path) -> float:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True)
    try:
        return float(res.stdout.strip())
    except ValueError:
        return 0.0


def _decode(path: Path) -> np.ndarray:
    w, h = _probe_wh(path)
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-frames:v", "1",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(h, w, 3).astype(np.float32)


def audit_image(img: np.ndarray, name: str) -> list[GateFailure]:
    f: list[GateFailure] = []
    h, w, _ = img.shape
    luma = img @ LUMA

    if float((luma < BLACK_LUMA).mean()) > NEARBLACK_FRACTION:
        return [GateFailure("BLACK-FRAME", "BLOCK", "frame is essentially black", name)]

    lime_frac = float((np.linalg.norm(img - LIME, axis=2) < COLOR_DIST).mean())
    if lime_frac > ACCENT_MAX_FRACTION:
        f.append(GateFailure("ACCENT-FOOTPRINT", "BLOCK",
            f"lime covers {lime_frac:.1%} of frame (max {ACCENT_MAX_FRACTION:.0%})", name))

    if float((img.max(axis=2) < 3).mean()) > 0.35:
        f.append(GateFailure("PURE-BLACK", "WARN", "large pure #000 area", name))
    if float((img.min(axis=2) > 252).mean()) > 0.35:
        f.append(GateFailure("PURE-WHITE", "WARN", "large pure #fff area", name))

    band = img[int(h * TEXT_BAND[0]):int(h * TEXT_BAND[1]), :, :]
    bl = band @ LUMA
    bright = bl > 200
    if 0.005 < float(bright.mean()) < 0.5:
        surround = bl[~bright]
        if surround.size:
            l_text, l_bg = 235.0, float(np.median(surround))
            ratio = (l_text / 255 * 0.92 + 0.05) / (l_bg / 255 * 0.92 + 0.05)
            if ratio < 4.5:
                f.append(GateFailure("TEXT-CONTRAST", "BLOCK",
                    f"text-band contrast ~{ratio:.1f}:1 (<4.5:1) - scrim too weak", name))
    return f


def audit(path: Path, n_frames: int) -> list[GateFailure]:
    ext = path.suffix.lower()
    if ext in IMAGE_EXT:
        return audit_image(_decode(path), path.name)
    if ext in VIDEO_EXT:
        findings: list[GateFailure] = []
        dur = _probe_duration(path)
        with tempfile.TemporaryDirectory() as td:
            for i in range(n_frames):
                t = dur * (i + 0.5) / n_frames
                fr = Path(td) / f"f{i:02d}.png"
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}",
                                "-i", str(path), "-frames:v", "1", str(fr)],
                               capture_output=True)
                if fr.exists():
                    findings.extend(audit_image(_decode(fr), f"{path.name}@{t:.1f}s"))
        return findings
    print(f"[warn] unsupported file type: {path}")
    return []


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    path = Path(args[0])
    if not path.exists():
        print(f"[error] not found: {path}")
        return 2
    n = int(argv[argv.index("--frames") + 1]) if "--frames" in argv else 12
    findings = audit(path, n)
    ok = report(findings, "design-core frame audit")
    print("[note] deterministic gates only; run the judgment gates by eye before approval")
    if "--json" in argv:
        out = Path(argv[argv.index("--json") + 1])
        out.write_text(json.dumps([x.as_dict() for x in findings],
                                  indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
