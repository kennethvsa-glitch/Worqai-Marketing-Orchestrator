"""
motion_exporter.py — animated HTML → MP4 via Playwright frame-stepping + ffmpeg stdin

Usage:
    py scripts/motion_exporter.py --input templates/scenes/output.html
    py scripts/motion_exporter.py --input templates/scenes/output.html --output export-video/
"""

import subprocess
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
try:
    from orthography_check import scan_text as _ortho_scan
except ImportError:
    _ortho_scan = None

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    raise SystemExit("ERROR: playwright not installed.\nFix: pip install playwright && playwright install chromium")

ROOT = Path(__file__).parent.parent

from _config import FFMPEG
from _browser import launch_chromium


def get_viewport(aspect: str) -> tuple[int, int]:
    ratios = {
        "9:16":  (1080, 1920),
        "1:1":   (1080, 1080),
        "4:5":   (1080, 1350),
    }
    if aspect not in ratios:
        raise SystemExit(f"FAIL: Unknown aspect ratio '{aspect}'. Supported: {list(ratios)}")
    return ratios[aspect]


def preflight_checks(page) -> None:
    """Lock 6 + Lock 7: run before frame loop."""

    # Lock 6 — safe-zone overflow check
    overflow = page.evaluate("""
      () => {
        const safeBottom = window.innerHeight - 200;
        const safeRight  = window.innerWidth  - 56;
        const safeLeft   = 56;
        const safeTop    = 120;
        return Array.from(document.querySelectorAll('[data-copy]')).filter(el => {
          const r = el.getBoundingClientRect();
          if (r.width === 0 && r.height === 0) return false; // display:none — skip
          return r.bottom > safeBottom || r.right > safeRight || r.left < safeLeft || r.top < safeTop;
        }).map(el => el.dataset.copy);
      }
    """)
    if overflow:
        raise SystemExit(f"OVERFLOW FAIL: {overflow} — fix copy length or layout before export")

    # Lock 7 — no running CSS animations in video mode
    running = page.evaluate("""
      () => Array.from(document.getAnimations())
               .filter(a => a.playState === 'running' && a.constructor.name === 'CSSAnimation')
               .map(a => a.animationName || 'unknown')
    """)
    if running:
        raise SystemExit(f"CSS ANIMATION RUNNING IN VIDEO MODE: {running}\nAdd .geo-layer-animated freeze or check video_mode flag")


def _sanitize_stem(stem: str) -> str:
    """Strip accidental video_ prefix or trailing _YYYY-MM-DD to avoid double-stamping."""
    import re
    stem = re.sub(r'^video_', '', stem)
    stem = re.sub(r'_\d{4}-\d{2}-\d{2}$', '', stem)
    return stem or "motion"


def read_name(html_path: Path) -> str | None:
    """Read data-name attribute from the <html> tag; returns None if absent."""
    import re
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r'data-name=["\']([^"\']+)["\']', text)
    return m.group(1) if m else None


def export(
    html_path: Path,
    output_dir: Path,
    fps: int,
    duration: float,
    aspect: str,
    stem: str,
    *,
    from_sec: float = 0.0,
    to_sec: float | None = None,
    draft: bool = False,
) -> Path:
    if draft:
        fps      = 15
        crf      = "28"
        preset   = "ultrafast"
        scale_factor = 0.5
    else:
        crf      = "18"
        preset   = "slow"
        scale_factor = 1.0

    width_full, height_full = get_viewport(aspect)
    width  = int(width_full  * scale_factor)
    height = int(height_full * scale_factor)

    clip_start  = max(0.0, from_sec)
    clip_end    = min(duration, to_sec) if to_sec is not None else duration
    clip_dur    = clip_end - clip_start
    total_frames = max(1, int(fps * clip_dur))

    output_dir.mkdir(parents=True, exist_ok=True)

    stem     = _sanitize_stem(stem)
    date_str = datetime.now().strftime("%Y-%m-%d")
    suffix   = "_draft" if draft else ""
    out_path = output_dir / f"video_{stem}{suffix}_{date_str}.mp4"

    # Orthography gate — scan HTML source before opening the page.
    # This catches JS content-model strings not yet in the live DOM.
    if _ortho_scan:
        ortho = _ortho_scan(html_path.read_text(encoding="utf-8"))
        if ortho:
            lines = "\n".join(f"  '{f}' -> '{s}'  {c}" for f, s, c in ortho[:10])
            raise SystemExit(f"ORTHOGRAPHY FAIL — fix accents before export:\n{lines}")

    range_info = f"  range {clip_start:.2f}s–{clip_end:.2f}s" if (clip_start > 0 or to_sec is not None) else ""
    draft_info = "  [DRAFT 15fps 540×960]" if draft else ""
    print(f"Exporting {html_path.name}{draft_info}")
    print(f"  {width}×{height}  {fps}fps  {clip_dur:.2f}s  ({total_frames} frames){range_info}")
    try:
        display = out_path.relative_to(ROOT)
    except ValueError:
        display = out_path
    print(f"  -> {display}")

    ffmpeg_cmd = [
        FFMPEG, "-y",
        "-f", "image2pipe",
        "-framerate", str(fps),
        "-i", "pipe:0",
        "-crf", crf,
        "-preset", preset,
        "-pix_fmt", "yuv420p",
        str(out_path),
    ]

    with sync_playwright() as p:
        browser = launch_chromium(p)
        page = browser.new_page(
            viewport={"width": width_full, "height": height_full},
            device_scale_factor=scale_factor,
        )
        page.goto(f"file:///{html_path.as_posix()}")

        try:
            page.wait_for_function("window.motionReady === true", timeout=20_000)
        except Exception:
            browser.close()
            raise SystemExit("FAIL: motionReady never fired. Open the HTML in a browser to debug.")

        # Lock 1: verify lag smoothing is disabled in the page
        page.evaluate("void gsap.ticker.lagSmoothing(0)")

        # Lock 6 + 7: preflight checks before frame loop
        preflight_checks(page)

        print("Preflight passed. Starting frame loop...")
        # stderr=None: let ffmpeg write encoder progress directly to console.
        # Piping stderr without reading it fills the OS pipe buffer (64KB) and
        # deadlocks the frame loop on long videos.
        ffmpeg = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=None)

        try:
            for frame in range(total_frames):
                if ffmpeg.poll() is not None:
                    raise SystemExit(f"ffmpeg exited early (code {ffmpeg.returncode}) — check output above")
                t = round(clip_start + frame / fps, 6)
                # Lock 2: seek globalTimeline, not pause(t)
                page.evaluate(f"void gsap.globalTimeline.time({t})")
                png = page.screenshot(type="png")
                ffmpeg.stdin.write(png)
                if frame % 30 == 0:
                    print(f"  frame {frame}/{total_frames}  t={t:.2f}s")
        except (BrokenPipeError, OSError) as e:
            raise SystemExit(f"ffmpeg pipe error: {e} — ffmpeg likely exited. Check output above.")
        finally:
            ffmpeg.stdin.close()
            browser.close()

        ffmpeg.wait()
        if ffmpeg.returncode != 0:
            raise SystemExit(f"ffmpeg FAILED (exit {ffmpeg.returncode}) — check output above")

    size_mb = out_path.stat().st_size / 1_048_576
    print(f"Done: {out_path.name}  ({size_mb:.1f} MB)")
    return out_path


def read_duration(html_path: Path) -> float:
    import re
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r'data-duration=["\'](\d+(?:\.\d+)?)["\']', text)
    if m:
        return float(m.group(1))
    raise SystemExit(f"FAIL: No data-duration attribute in {html_path.name} and --duration not set")


def read_fps(html_path: Path, fallback: int = 30) -> int:
    import re
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r'data-fps=["\'](\d+)["\']', text)
    return int(m.group(1)) if m else fallback


def concat_mp4s(mp4_paths: list, out_path: Path) -> None:
    """Join multiple MP4s in order using ffmpeg concat demuxer (stream copy, no re-encode)."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for p in mp4_paths:
            f.write(f"file '{p.as_posix()}'\n")
        list_path = Path(f.name)
    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(list_path), "-c", "copy", str(out_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    list_path.unlink(missing_ok=True)
    if result.returncode != 0:
        raise SystemExit(f"ffmpeg concat FAILED:\n{result.stderr[-800:]}")


def run_contact_sheet(mp4_path: Path) -> None:
    contact_script = ROOT / "scripts" / "motion_contact_sheet.py"
    if not contact_script.exists():
        print("WARN: motion_contact_sheet.py not found")
        return
    result = subprocess.run([sys.executable, str(contact_script), "--input", str(mp4_path)],
                            capture_output=True, text=True)
    print(result.stdout.strip() if result.returncode == 0 else f"WARN: contact sheet failed: {result.stderr.strip()}")


def main():
    parser = argparse.ArgumentParser(description="Export animated HTML to MP4")
    parser.add_argument("--input",    type=Path,  required=True,  help="Single HTML file or directory of output_scene-N.html files")
    parser.add_argument("--output",   type=Path,  default=ROOT/"export-video", help="Output directory")
    parser.add_argument("--fps",      type=int,   default=None, help="FPS override (reads data-fps from HTML if not set, falls back to 30)")
    parser.add_argument("--duration", type=float, default=None,   help="Duration in seconds (reads from HTML data-duration if not set)")
    parser.add_argument("--aspect",   type=str,   default="9:16")
    parser.add_argument("--name",     type=str,   default=None,   help="Output filename stem")
    parser.add_argument("--from",     type=float, default=0.0,    dest="from_sec", help="Start time in seconds (partial render)")
    parser.add_argument("--to",       type=float, default=None,   dest="to_sec",   help="End time in seconds (partial render)")
    parser.add_argument("--draft",    action="store_true",         help="Draft mode: 15fps, 540x960, fast encode")
    args = parser.parse_args()

    input_path = args.input.resolve()
    output_dir = args.output.resolve()

    # ── Multi-scene: directory of output_scene-N.html files ──────────────────
    if input_path.is_dir():
        html_files = sorted(input_path.glob("output_scene-*.html"),
                            key=lambda p: int(p.stem.split("-")[-1]))
        if not html_files:
            raise SystemExit(f"FAIL: No output_scene-N.html files found in {input_path}")

        print(f"Multi-scene export: {len(html_files)} scenes")
        import tempfile
        tmp_dir = Path(tempfile.mkdtemp())
        scene_mp4s = []
        for i, html_path in enumerate(html_files):
            duration = args.duration or read_duration(html_path)
            fps = args.fps or read_fps(html_path)
            stem = f"_scene{i}_{html_path.stem}"
            mp4 = export(html_path, tmp_dir, fps, duration, args.aspect, stem, draft=args.draft)
            scene_mp4s.append(mp4)

        name = _sanitize_stem(args.name or "multi")
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        out_path = output_dir / f"video_{name}_{date_str}.mp4"
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Concatenating {len(scene_mp4s)} clips...")
        concat_mp4s(scene_mp4s, out_path)
        for p in scene_mp4s:
            p.unlink(missing_ok=True)
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)
        size_mb = out_path.stat().st_size / 1_048_576
        print(f"Done: {out_path.name}  ({size_mb:.1f} MB)")
        run_contact_sheet(out_path)
        return

    # ── Single scene ──────────────────────────────────────────────────────────
    if not input_path.exists():
        raise SystemExit(f"FAIL: Input file not found: {input_path}")

    duration = args.duration or read_duration(input_path)
    fps = args.fps or read_fps(input_path)
    stem = args.name or read_name(input_path) or input_path.stem
    out_path = export(input_path, output_dir, fps, duration, args.aspect, stem,
                     from_sec=args.from_sec, to_sec=args.to_sec, draft=args.draft)
    run_contact_sheet(out_path)


if __name__ == "__main__":
    main()
