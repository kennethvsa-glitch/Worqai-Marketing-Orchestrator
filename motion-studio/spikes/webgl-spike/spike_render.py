"""
webgl-spike/spike_render.py — double-export determinism gate for WebGL shaders.

This is the gate for Expansion Phases 4 (shaders) AND 5 (three.js) — both ride the
same renderer, so one verdict covers both lanes.

PASS criteria:
  1. Both exports complete without error.
  2. Both MP4 outputs are bit-identical (sha256 match).

If FAIL: GPU float behavior is non-deterministic on this machine's GL path.
Next step is forcing SwiftShader (CPU GL) and re-testing — see README.

Usage:
    # From repo root:
    py spikes/webgl-spike/spike_render.py
"""

import hashlib
import sys
from pathlib import Path
import subprocess

ROOT = Path(__file__).parent.parent.parent
SPIKE_HTML = Path(__file__).parent / "spike.html"
OUT_DIR    = ROOT / "export-video" / "spike-webgl"


def run_export(stem: str) -> Path:
    """Run exporter with --name stem and return the actual MP4 path the exporter wrote."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "motion_exporter.py"),
         "--input", str(SPIKE_HTML), "--output", str(OUT_DIR),
         "--name", stem],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(f"Export FAILED: {stem}")
    matches = [p for p in OUT_DIR.glob(f"video_{stem}_*.mp4")
               if "_contact" not in p.name]
    if not matches:
        raise SystemExit(f"Export succeeded but no output file found for stem: {stem}")
    out = sorted(matches)[-1]
    print(f"Export OK: {out.name}")
    return out


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    print("WebGL spike — double-export determinism gate (Phases 4 + 5)")
    print("=" * 60)

    a = run_export("webgl-spike-run1")
    b = run_export("webgl-spike-run2")

    ha, hb = sha256_file(a), sha256_file(b)
    print(f"\nRun 1: {ha[:16]}…")
    print(f"Run 2: {hb[:16]}…")

    if ha == hb:
        print("\nPASS — both exports bit-identical. WebGL shaders are deterministic")
        print("on this machine's GL path. Phases 4 (shaders) and 5 (three.js) gates OPEN.")
    else:
        print("\nFAIL — exports differ. GPU float behavior is non-deterministic here.")
        print("Next: force SwiftShader (CPU GL) and re-test:")
        print("  chromium.launch(args=['--use-angle=swiftshader'])")
        print("If SwiftShader passes: shader scenes render on the CPU path (slower, valid).")
        print("If SwiftShader also fails: the WebGL lane closes; Canvas2D fallbacks only.")
        sys.exit(1)


if __name__ == "__main__":
    main()
