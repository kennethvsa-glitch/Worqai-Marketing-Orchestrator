"""
motion_contact_sheet.py — generate a QA frame grid from a rendered MP4

Usage:
    py scripts/motion_contact_sheet.py --input export-video/my-video.mp4
    py scripts/motion_contact_sheet.py --input export-video/my-video.mp4 --mode label --html templates/scenes/scene.html
    (also called automatically by motion_exporter.py after every export)

Output: {video_stem}_contact.png next to the MP4.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("ERROR: Pillow not installed.\nFix: pip install Pillow")

import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent))
from _config import FFMPEG, FFPROBE
from _browser import launch_chromium

BG      = (8, 10, 16)       # #080a10
GOLD    = (212, 175, 55)     # #d4af37
WHITE   = (255, 255, 255)
DIM     = (120, 120, 130)

THUMB_W = 216
THUMB_H = 384
PADDING = 16
HEADER_H = 56
LABEL_H  = 28
COLS_PER_ROW = 8

PERCENTAGES = [0, 25, 50, 75, 100]


def get_video_info(mp4_path: Path) -> dict:
    cmd = [
        FFPROBE, "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        str(mp4_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"ffprobe FAILED: {result.stderr}")
    data = json.loads(result.stdout)
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            duration = float(stream.get("duration", 0))
            r_frame_rate = stream.get("r_frame_rate", "30/1")
            num, den = r_frame_rate.split("/")
            fps = round(int(num) / int(den))
            return {"duration": duration, "fps": fps}
    raise SystemExit("FAIL: No video stream found in file")


def extract_frame(mp4_path: Path, timestamp: float, out_path: Path) -> None:
    cmd = [
        FFMPEG, "-y",
        "-ss", f"{timestamp:.6f}",
        "-i", str(mp4_path),
        "-frames:v", "1",
        "-q:v", "2",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"ffmpeg frame extract FAILED at t={timestamp:.2f}s: {result.stderr[-500:]}")


def fmt_time(seconds: float) -> str:
    m = int(seconds) // 60
    s = seconds % 60
    return f"{m}:{s:04.1f}"


def make_contact_sheet(
    mp4_path: Path,
    info: dict,
    frames: list,
    timestamps: list,
    frame_labels: list | None = None,
) -> Path:
    n = len(frames)
    cols = min(n, COLS_PER_ROW)
    rows = (n + cols - 1) // cols
    canvas_w = THUMB_W * cols + PADDING * (cols + 1)
    canvas_h = HEADER_H + rows * (THUMB_H + LABEL_H + PADDING) + PADDING

    canvas = Image.new("RGB", (canvas_w, canvas_h), BG)
    draw   = ImageDraw.Draw(canvas)

    try:
        font_label = ImageFont.truetype("arial.ttf", 12)
        font_header = ImageFont.truetype("arial.ttf", 14)
    except (OSError, IOError):
        font_label  = ImageFont.load_default()
        font_header = ImageFont.load_default()

    # Header
    header_text = f"{mp4_path.name}   {info['duration']:.1f}s  {info['fps']}fps"
    draw.text((PADDING, PADDING + 8), header_text, fill=WHITE, font=font_header)

    # Frames + labels
    for i, (frame_path, ts) in enumerate(zip(frames, timestamps)):
        thumb = Image.open(frame_path).resize((THUMB_W, THUMB_H), Image.LANCZOS)
        col = i % cols
        row = i // cols
        x = PADDING + col * (THUMB_W + PADDING)
        y = HEADER_H + PADDING + row * (THUMB_H + LABEL_H + PADDING)
        canvas.paste(thumb, (x, y))

        # Timestamp label
        if frame_labels and i < len(frame_labels):
            label_text = f"{frame_labels[i]}  {fmt_time(ts)}"
            label_color = GOLD
        else:
            pct = int(round(ts / info["duration"] * 100)) if info["duration"] else 0
            label_text = f"{pct}%  {fmt_time(ts)}"
            label_color = DIM
        draw.text((x + 4, y + THUMB_H + 6), label_text, fill=label_color, font=font_label)

    out_path = mp4_path.parent / f"{mp4_path.stem}_contact.png"
    canvas.save(str(out_path), "PNG")
    return out_path


def resolve_labels(html_path: Path) -> dict:
    """Open scene in headless Chromium, return {label_name: seconds}."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("playwright not installed: pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        browser = launch_chromium(p)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file:///{html_path.as_posix()}")
        try:
            page.wait_for_function("window.motionReady === true", timeout=20_000)
        except Exception:
            browser.close()
            raise SystemExit(f"FAIL: motionReady never fired for {html_path.name}")
        raw = page.evaluate("window.MOTION_LABELS || {}")
        browser.close()
    return {k: v / 1000.0 for k, v in raw.items()}


def generate(mp4_path: Path) -> Path:
    info = get_video_info(mp4_path)
    duration = info["duration"]

    timestamps = [duration * p / 100 for p in PERCENTAGES]
    # Clamp last frame slightly back to avoid ffmpeg overshooting
    timestamps[-1] = max(0, duration - 1 / info["fps"])

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        frame_paths = []
        for i, ts in enumerate(timestamps):
            out = tmp_dir / f"frame_{i:02d}.png"
            extract_frame(mp4_path, ts, out)
            frame_paths.append(out)

        out_path = make_contact_sheet(mp4_path, info, frame_paths, timestamps)

    size_kb = out_path.stat().st_size // 1024
    print(f"Contact sheet: {out_path.name}  ({size_kb} KB)")
    return out_path


def generate_label_mode(mp4_path: Path, html_path: Path) -> Path:
    """Label mode: extract frames at every MOTION_LABEL + every 2s, sorted by time."""
    info = get_video_info(mp4_path)
    duration = info["duration"]
    fps = info["fps"]
    clamp = max(0.0, duration - 1.0 / fps)

    print(f"Resolving labels from {html_path.name}...")
    raw_labels = resolve_labels(html_path)
    if not raw_labels:
        print("WARN: no MOTION_LABELS found — falling back to percent mode")
        return generate(mp4_path)

    # Build frame list: label frames (named) + 2s grid (unnamed)
    named: dict[float, str] = {}
    for name, t in raw_labels.items():
        named[min(t, clamp)] = name

    # Every 2 seconds as fill
    t = 0.0
    while t <= clamp:
        rounded = round(t, 3)
        if not any(abs(rounded - nt) < 0.1 for nt in named):
            named[rounded] = ""
        t += 2.0

    sorted_times = sorted(named.keys())
    frame_labels = [named[t] for t in sorted_times]

    print(f"  {len(sorted_times)} frames ({sum(1 for l in frame_labels if l)} label + {sum(1 for l in frame_labels if not l)} grid)")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        frame_paths = []
        for i, ts in enumerate(sorted_times):
            out = tmp_dir / f"frame_{i:03d}.png"
            extract_frame(mp4_path, ts, out)
            frame_paths.append(out)

        out_path = make_contact_sheet(mp4_path, info, frame_paths, sorted_times, frame_labels)

    size_kb = out_path.stat().st_size // 1024
    print(f"Contact sheet: {out_path.name}  ({size_kb} KB)")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate QA contact sheet from MP4")
    parser.add_argument("--input", type=Path, required=True, help="MP4 file")
    parser.add_argument("--mode",  choices=["percent", "label"], default="percent",
                        help="percent: 5-frame grid; label: MOTION_LABELS + 2s grid")
    parser.add_argument("--html",  type=Path, default=None,
                        help="Scene HTML file (required for --mode label)")
    args = parser.parse_args()

    mp4_path = args.input.resolve()
    if not mp4_path.exists():
        raise SystemExit(f"FAIL: File not found: {mp4_path}")

    if args.mode == "label":
        if not args.html:
            raise SystemExit("FAIL: --html <scene.html> required for --mode label")
        html_path = args.html.resolve()
        if not html_path.exists():
            raise SystemExit(f"FAIL: HTML not found: {html_path}")
        generate_label_mode(mp4_path, html_path)
    else:
        generate(mp4_path)


if __name__ == "__main__":
    main()
