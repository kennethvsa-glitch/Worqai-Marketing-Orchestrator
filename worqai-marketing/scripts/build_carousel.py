#!/usr/bin/env python3
"""
build_carousel.py — One-command pipeline: render → preflight → visual_richness_check.

Usage:
    py scripts/build_carousel.py production/my-spec.json
    py scripts/build_carousel.py production/spec1.json production/spec2.json

Exit codes:
    0 = all checks passed
    1 = one or more checks failed
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent
PYTHON = sys.executable


def output_path_from_spec(spec_path: Path) -> Path:
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except Exception:
        return ROOT / "production" / f"carousel_{spec_path.stem}.html"
    meta = spec.get("meta", {})
    topic = meta.get("topic", spec_path.stem)
    system = meta.get("system", "s00")
    return ROOT / "production" / f"carousel_{topic}_{system}.html"


def run(cmd: list, label: str) -> int:
    print(f"\n{'-' * 60}", flush=True)
    print(f"  {label}", flush=True)
    print(f"{'-' * 60}", flush=True)
    result = subprocess.run(cmd, text=True)
    return result.returncode


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: py scripts/build_carousel.py spec.json [spec2.json ...]")
        return 1

    spec_paths = [Path(p) for p in sys.argv[1:]]
    output_paths: list = []
    failed = False

    for spec_path in spec_paths:
        if not spec_path.exists():
            print(f"ERROR: spec not found: {spec_path}")
            failed = True
            continue

        out = output_path_from_spec(spec_path)
        output_paths.append(out)

        # Step 1: Render
        rc = run(
            [PYTHON, str(SCRIPTS / "render_carousel.py"), str(spec_path), "--output", str(out)],
            f"RENDER  {spec_path.name}  ->  {out.name}",
        )
        if rc != 0:
            print(f"\n  RENDER FAILED: {spec_path.name}")
            failed = True
            continue

        # Step 2: Preflight (technical compliance, per file)
        rc = run(
            [PYTHON, str(SCRIPTS / "preflight.py"), str(out)],
            f"PREFLIGHT  {out.name}",
        )
        if rc != 0:
            failed = True

    # Step 3: Visual richness (all files together for cross-carousel diversity)
    existing = [str(p) for p in output_paths if p.exists()]
    if existing:
        rc = run(
            [PYTHON, str(SCRIPTS / "visual_richness_check.py"), *existing],
            f"VISUAL RICHNESS  [{' · '.join(Path(p).name for p in existing)}]",
        )
        if rc != 0:
            failed = True

    print(f"\n{'=' * 60}")
    if failed:
        print("  BUILD FAILED - review errors above")
        print(f"{'=' * 60}\n")
        return 1
    print("  BUILD PASSED - ready to export")
    print(f"{'=' * 60}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
