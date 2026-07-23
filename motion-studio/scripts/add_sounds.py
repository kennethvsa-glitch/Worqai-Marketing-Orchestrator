"""
add_sounds.py — mix sound effects into a motion video at precise timestamps.

Supports two timing modes per sound entry:
  label     — resolves to the GSAP timeline label time emitted by the scene (needs --html)
  offset_ms — hardcoded millisecond offset (no HTML needed)

Usage:
    # Hardcoded offsets (no HTML needed):
    py scripts/add_sounds.py --video export-video/v.mp4 --sounds motion/specs/sounds_launch_s01.json --output export-video/v_sound.mp4

    # Label-based timing (reads MOTION_LABELS from rendered HTML):
    py scripts/add_sounds.py --video ... --sounds ... --html templates/scenes/output.html --output ...

Sounds JSON format:
    [
      { "label": "cv_visible",  "file": "smooth_lateral_slide_#4", "volume": 0.75 },
      { "offset_ms": 8300,      "file": "Button_click_Sounds__#3", "volume": 0.90 },
      { "label": "verify_click", "offset_ms_add": 200, "file": "Button_click_Sounds__#3", "volume": 0.85 }
    ]
  label         — look up from MOTION_LABELS in the rendered HTML
  offset_ms     — hardcoded delay in milliseconds
  offset_ms_add — added to label time (optional fine-tuning when using labels)
  file          — prefix of the sound file name in --sounds-dir
  volume        — 0.0–1.0
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT       = Path(__file__).parent.parent
SOUNDS_DIR = ROOT / "Ideation" / "Sound effects"
import sys as _sys; _sys.path.insert(0, str(ROOT / "scripts"))
from _config import FFMPEG
from _browser import launch_chromium


def find_file(prefix: str, sounds_dir: Path) -> Path:
    for f in sounds_dir.iterdir():
        if f.name.startswith(prefix):
            return f
    raise FileNotFoundError(f"No sound file starting with '{prefix}' in {sounds_dir}")


def resolve_labels(html_path: Path) -> dict:
    """Open rendered HTML in Playwright, return MOTION_LABELS {label: ms}."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("playwright not installed: pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        browser = launch_chromium(p)
        page    = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file:///{html_path.as_posix()}")
        try:
            page.wait_for_function("window.motionReady === true", timeout=20_000)
        except Exception:
            browser.close()
            raise SystemExit(f"FAIL: motionReady never fired in {html_path.name}")
        labels = page.evaluate("() => window.MOTION_LABELS || {}")
        browser.close()
    return labels


def main():
    parser = argparse.ArgumentParser(description="Mix sounds into a motion video")
    parser.add_argument("--video",      type=Path, required=True,  help="Input MP4")
    parser.add_argument("--sounds",     type=Path, required=True,  help="JSON array of sound events")
    parser.add_argument("--output",     type=Path, required=True,  help="Output MP4")
    parser.add_argument("--html",       type=Path, default=None,   help="Rendered HTML for label resolution")
    parser.add_argument("--sounds-dir", type=Path, default=SOUNDS_DIR)
    args = parser.parse_args()

    sounds = json.loads(args.sounds.read_text(encoding="utf-8"))

    # Resolve label-based entries via MOTION_LABELS if needed
    labels_needed = any("label" in s for s in sounds)
    label_map: dict = {}
    if labels_needed:
        if not args.html:
            raise SystemExit("FAIL: sounds file uses 'label' entries but --html was not provided")
        if not args.html.exists():
            raise SystemExit(f"FAIL: HTML not found: {args.html}")
        print(f"Reading MOTION_LABELS from {args.html.name}...")
        label_map = resolve_labels(args.html)
        if not label_map:
            print("WARN: MOTION_LABELS is empty — add tl.addLabel() calls to the scene timeline")

    # Compute delay_ms for every entry
    for s in sounds:
        if "label" in s:
            lbl = s["label"]
            if lbl not in label_map:
                raise SystemExit(f"FAIL: label '{lbl}' not in MOTION_LABELS — available: {sorted(label_map)}")
            s["delay_ms"] = int(label_map[lbl]) + s.get("offset_ms_add", 0)
        elif "offset_ms" in s:
            s["delay_ms"] = int(s["offset_ms"])
        else:
            raise SystemExit(f"FAIL: sound entry has neither 'label' nor 'offset_ms': {s}")

    sounds_dir = args.sounds_dir.resolve()

    # Build ffmpeg command
    cmd = [FFMPEG, "-y", "-i", str(args.video.resolve())]
    for s in sounds:
        cmd += ["-i", str(find_file(s["file"], sounds_dir))]

    parts = []
    for i, s in enumerate(sounds):
        d = s["delay_ms"]
        v = s.get("volume", 1.0)
        parts.append(f"[{i + 1}:a]adelay={d}|{d},volume={v}[a{i:02d}]")
    mix_in = "".join(f"[a{i:02d}]" for i in range(len(sounds)))
    parts.append(f"{mix_in}amix=inputs={len(sounds)}:duration=first:normalize=0[amix]")

    cmd += [
        "-filter_complex", ";".join(parts),
        "-map", "0:v", "-map", "[amix]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(args.output.resolve()),
    ]

    print(f"Mixing {len(sounds)} sound events -> {args.output.name}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg error:\n{r.stderr[-2000:]}")
    size_mb = args.output.stat().st_size / 1_048_576
    print(f"Done: {args.output.name}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
