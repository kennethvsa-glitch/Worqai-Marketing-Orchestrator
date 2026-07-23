#!/usr/bin/env python3
"""
batch_export_approved.py
Exports all approved carousels to numbered PNG folders in export/batch-approved/

Usage:
    py scripts/batch_export_approved.py
"""

import asyncio
import os
import re
import sys
import zipfile
import tempfile
from pathlib import Path

# ── paths ────────────────────────────────────────────────────────────────────

ROOT     = Path(__file__).parent.parent
APPROVED = ROOT / "production" / "Carousels to remake" / "priority 1" / "Batch 1" / "reframed" / "Approved"
OUT_ROOT = ROOT / "export" / "batch1-approved"

# ── pull in helpers from carousel_exporter.py ────────────────────────────────

sys.path.insert(0, str(ROOT / "scripts"))
from carousel_exporter import detect_slide_count, render_slides, build_contact_sheet


def export_one(html_path: Path, out_dir: Path):
    """Render one carousel to numbered PNGs in out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    slide_count, selector = detect_slide_count(str(html_path))

    prefix = "slide"
    with tempfile.TemporaryDirectory() as tmp:
        exported = asyncio.run(render_slides(
            html_path=str(html_path),
            output_dir=tmp,
            selector=selector,
            slide_count=slide_count,
            width=1080,
            height=1080,
            prefix=prefix,
            hide_counter=False,
            quality=95,
        ))

        if not exported:
            print(f"  [ERROR] No slides exported for {html_path.name}")
            return

        # Copy numbered PNGs into output folder
        for src in sorted(exported):
            dst = out_dir / Path(src).name
            import shutil
            shutil.copy2(src, dst)
            print(f"  -> {dst.name}")

        # Contact sheet
        sheet_path = str(out_dir / f"_contact_sheet.png")
        build_contact_sheet(
            image_paths=sorted(exported),
            output_path=sheet_path,
            carousel_name=html_path.stem,
        )


def main():
    html_files = sorted(APPROVED.glob("*.html"))
    if not html_files:
        print(f"No HTML files found in:\n  {APPROVED}")
        sys.exit(1)

    print(f"\nFound {len(html_files)} carousels to export -> {OUT_ROOT}\n")
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    for html in html_files:
        # Use stem as folder name, strip "reframed_" prefix for cleaner dirs
        folder_name = html.stem.removeprefix("reframed_")
        out_dir = OUT_ROOT / folder_name
        print(f"\n[{html.name}]")
        print(f"  Output folder: {out_dir.name}")
        try:
            export_one(html, out_dir)
            print(f"  [ok] done")
        except Exception as e:
            print(f"  [FAILED] {e}")

    print(f"\n\nAll done. Folders in:\n  {OUT_ROOT}\n")


if __name__ == "__main__":
    main()
