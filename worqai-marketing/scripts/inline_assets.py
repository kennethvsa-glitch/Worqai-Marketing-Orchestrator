#!/usr/bin/env python3
"""
inline_assets.py — Base64-inline external images for bulletproof html2canvas export.

Scans carousel HTML for <img> tags referencing brand/generated-bg/ images
and replaces them with data:image/png;base64,... URIs.

Usage:
    py scripts/inline_assets.py gallery/my-carousel.html
    py scripts/inline_assets.py gallery/my-carousel.html --output production/my-carousel-inlined.html
"""

import argparse
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def inline_images(html: str, html_dir: Path) -> str:
    """Find <img src="brand/generated-bg/..."> tags and inline them as base64."""
    # Match img src attributes pointing to brand/generated-bg/
    pattern = re.compile(r'<img\s+([^>]*?)src="([^"]*brand/generated-bg/[^"]+)"([^>]*?)>', re.IGNORECASE)

    def replace_img(match):
        pre_attrs = match.group(1)
        src = match.group(2)
        post_attrs = match.group(3)

        # Resolve path relative to HTML file location or ROOT
        if src.startswith("/"):
            img_path = ROOT / src.lstrip("/")
        else:
            img_path = html_dir / src
            if not img_path.exists():
                img_path = ROOT / src

        if not img_path.exists():
            print(f"  [WARN] Image not found, skipping: {img_path}", file=sys.stderr)
            return match.group(0)

        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")

        mime = "image/png"
        if img_path.suffix.lower() in (".jpg", ".jpeg"):
            mime = "image/jpeg"
        elif img_path.suffix.lower() == ".webp":
            mime = "image/webp"

        print(f"  [INLINED] {src} -> {len(b64):,} chars base64")
        return f'<img {pre_attrs}src="data:{mime};base64,{b64}"{post_attrs}>'

    return pattern.sub(replace_img, html)


def main():
    parser = argparse.ArgumentParser(description="Inline external images in carousel HTML")
    parser.add_argument("input", type=str, help="Input HTML file path")
    parser.add_argument("--output", "-o", type=str, help="Output HTML file path (default: overwrite input)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[FAIL] Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path
    html_dir = input_path.parent

    print(f"Reading: {input_path}")
    html = input_path.read_text(encoding="utf-8")

    inlined = inline_images(html, html_dir)

    output_path.write_text(inlined, encoding="utf-8")
    size_kb = output_path.stat().st_size // 1024
    print(f"[OK]  Saved: {output_path} ({size_kb} KB)")


if __name__ == "__main__":
    main()
