"""
golden_frames.py — deterministic regression harness for motion scenes.

Because the pipeline is deterministic (Lock 1–4), screenshots at MOTION_LABEL
times should be bit-identical across runs unless the scene actually changed.
This script stores SHA-256 hashes of those frames and diffs them on subsequent runs.

Usage:
    # Capture golden hashes for a scene (before refactoring):
    py scripts/golden_frames.py --html templates/scenes/scene-launch-villain.html --write

    # Verify nothing changed (after refactoring):
    py scripts/golden_frames.py --html templates/scenes/scene-launch-villain.html --check

    # Strict mode: exit 1 if any hash differs:
    py scripts/golden_frames.py --html templates/scenes/scene-launch-villain.html --check --strict

Output: export-video/golden/<stem>.json
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
GOLDEN_DIR = ROOT / "export-video" / "golden"

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    raise SystemExit("playwright not installed: pip install playwright && playwright install chromium")

sys.path.insert(0, str(Path(__file__).parent))
from _browser import launch_chromium


def resolve_labels(html_path: Path) -> dict[str, float]:
    """Open scene in headless Chromium, return MOTION_LABELS {name: seconds}."""
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


def capture_hashes(html_path: Path, labels: dict[str, float]) -> dict[str, str]:
    """Screenshot the scene at each label time, return {label: sha256hex}."""
    hashes = {}
    with sync_playwright() as p:
        browser = launch_chromium(p)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file:///{html_path.as_posix()}")
        page.wait_for_function("window.motionReady === true", timeout=20_000)
        page.evaluate("void gsap.ticker.lagSmoothing(0)")
        page.evaluate("void gsap.globalTimeline.pause()")
        for name, t in sorted(labels.items(), key=lambda x: x[1]):
            page.evaluate(f"void gsap.globalTimeline.time({t})")
            png = page.screenshot(type="png")
            hashes[name] = hashlib.sha256(png).hexdigest()
        browser.close()
    return hashes


def write_golden(html_path: Path) -> Path:
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    out = GOLDEN_DIR / f"{html_path.stem}.json"

    print(f"Resolving labels from {html_path.name}...")
    labels = resolve_labels(html_path)
    if not labels:
        raise SystemExit(f"FAIL: no MOTION_LABELS in {html_path.name} — add tl.addLabel() calls")
    print(f"  {len(labels)} labels: {', '.join(sorted(labels))}")

    print("Capturing golden frames...")
    hashes = capture_hashes(html_path, labels)
    out.write_text(json.dumps({
        "scene": html_path.name,
        "labels": labels,
        "hashes": hashes,
    }, indent=2), encoding="utf-8")
    print(f"Written: {out.relative_to(ROOT)}")
    return out


def check_golden(html_path: Path, strict: bool = False) -> bool:
    golden_path = GOLDEN_DIR / f"{html_path.stem}.json"
    if not golden_path.exists():
        print(f"WARN: no golden file for {html_path.name} — run --write first")
        return True

    golden = json.loads(golden_path.read_text(encoding="utf-8"))
    labels = golden["labels"]
    print(f"Checking {len(labels)} frames for {html_path.name}...")

    current = capture_hashes(html_path, labels)
    changed = []
    for name, expected in golden["hashes"].items():
        actual = current.get(name)
        if actual != expected:
            changed.append(name)

    if changed:
        print(f"CHANGED ({len(changed)}): {', '.join(changed)}")
        if strict:
            return False
        print("(pass — use --strict to fail on changes)")
    else:
        print(f"All {len(labels)} frames match golden.")
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description="Golden-frame regression for motion scenes")
    ap.add_argument("--html", type=Path, required=True, help="Scene HTML file")
    ap.add_argument("--write", action="store_true", help="Capture and store golden hashes")
    ap.add_argument("--check", action="store_true", help="Compare current frames to golden")
    ap.add_argument("--strict", action="store_true", help="Exit 1 if any frame differs")
    args = ap.parse_args()

    html_path = args.html.resolve()
    if not html_path.exists():
        raise SystemExit(f"FAIL: not found: {html_path}")

    if args.write:
        write_golden(html_path)
    elif args.check:
        ok = check_golden(html_path, strict=args.strict)
        if not ok:
            sys.exit(1)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
