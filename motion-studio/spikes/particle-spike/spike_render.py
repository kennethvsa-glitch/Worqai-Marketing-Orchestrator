"""
particle-spike/spike_render.py — double-export determinism gate for the particle spike.

PASS criteria:
  1. Both exports complete without error.
  2. golden_frames.py --check --strict passes (both exports hash-identical).

Usage:
    # From repo root:
    py spikes/particle-spike/spike_render.py
"""

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
SPIKE_HTML = Path(__file__).parent / "spike.html"
OUT_DIR    = ROOT / "export-video" / "spike-particle"

sys.path.insert(0, str(ROOT / "scripts"))

try:
    from motion_exporter import export
except ImportError:
    raise SystemExit("motion_exporter not importable — run from repo root")

import subprocess


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
    # Exporter writes video_{stem}_{date}.mp4 — find it by glob
    matches = [p for p in OUT_DIR.glob(f"video_{stem}_*.mp4")
               if "_contact" not in p.name]
    if not matches:
        raise SystemExit(f"Export succeeded but no output file found for stem: {stem}")
    out = sorted(matches)[-1]  # newest if re-run same day
    print(f"Export OK: {out.name}")
    return out


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    print("Particle spike — double-export determinism gate")
    print("=" * 52)

    a = run_export("particle-spike-run1")
    b = run_export("particle-spike-run2")

    ha, hb = sha256_file(a), sha256_file(b)
    print(f"\nRun 1: {ha[:16]}…")
    print(f"Run 2: {hb[:16]}…")

    if ha == hb:
        print("\nPASS — both exports are bit-identical. Canvas particles are deterministic.")
    else:
        print("\nFAIL — exports differ. Canvas particles are NOT deterministic under frame-stepping.")
        print("Investigate: check that drawParticles computes positions analytically from t,")
        print("not from accumulated state or Math.random().")
        sys.exit(1)


if __name__ == "__main__":
    main()
