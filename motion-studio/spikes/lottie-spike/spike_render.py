"""
lottie-spike/spike_render.py — double-export determinism gate for the Lottie lane.

PASS criteria:
  1. spike.html loads, anim DOMLoaded fires, motionReady fires.
  2. Both exports complete without error.
  3. sha256(run1.mp4) == sha256(run2.mp4) — goToAndStop is bit-identical across runs.

Prerequisites:
  - Download a Lottie JSON (MIT/CC0), record in motion/lottie/CREDITS.md.
  - Place it as: spikes/lottie-spike/test.json
  - vendor/lottie/lottie-5.12.2.min.js must exist (see vendor/VERSIONS.md).

Usage (from repo root):
    py spikes/lottie-spike/spike_render.py
"""

import hashlib
import sys
import subprocess
from pathlib import Path

ROOT      = Path(__file__).parent.parent.parent
SPIKE_HTML = Path(__file__).parent / "spike.html"
TEST_JSON  = Path(__file__).parent / "test.json"
OUT_DIR    = ROOT / "export-video" / "spike-lottie"


def run_export(output_name: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / output_name
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "motion_exporter.py"),
         "--input", str(SPIKE_HTML), "--output", str(OUT_DIR),
         "--name", output_name.replace(".mp4", "")],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(f"Export FAILED: {output_name}")
    print(f"Export OK: {out.name}")
    return out


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not TEST_JSON.exists():
        raise SystemExit(
            "FAIL: test.json not found.\n"
            "  1. Download a Lottie JSON (MIT/CC0) from lottiefiles.com.\n"
            "  2. Record it in motion/lottie/CREDITS.md.\n"
            "  3. Place it as: spikes/lottie-spike/test.json\n"
            "  4. Re-run this script."
        )

    print("Lottie spike — double-export determinism gate")
    print("=" * 52)

    a = run_export("lottie-spike-run1.mp4")
    b = run_export("lottie-spike-run2.mp4")

    ha, hb = sha256_file(a), sha256_file(b)
    print(f"\nRun 1: {ha[:16]}…")
    print(f"Run 2: {hb[:16]}…")

    if ha == hb:
        print("\nPASS — both exports are bit-identical. Lottie goToAndStop is deterministic.")
        print("Phase 3 lane is clear to proceed.")
    else:
        print("\nFAIL — exports differ. Investigate: is the Lottie renderer doing anything")
        print("asynchronous or time-based outside the proxy tween?")
        sys.exit(1)


if __name__ == "__main__":
    main()
