#!/usr/bin/env python3
"""
test_ai_bg_slide.py — Render a single demo slide with an AI-generated,
color-adapted background image.

Usage:
    py scripts/test_ai_bg_slide.py

Output:
    gallery/zz-test-ai-bg-slide.html
"""

import sys
import base64
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from render_carousel import render_carousel

IMAGE_PATH = ROOT / "brand" / "generated-bg" / "s17-ai-bubbles.png"
OUTPUT_PATH = ROOT / "gallery" / "zz-test-ai-bg-slide.html"


def main():
    if not IMAGE_PATH.exists():
        print(f"[FAIL] Image not found: {IMAGE_PATH}", file=sys.stderr)
        sys.exit(1)

    # Base64-encode the PNG for inline embedding
    print(f"Loading image: {IMAGE_PATH}")
    with open(IMAGE_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    print(f"  Base64 length: {len(b64):,} chars")

    # Full-bleed background image + subtle dark overlay for text readability
    bg_html = (
        f'<img src="data:image/png;base64,{b64}" '
        f'style="position:absolute;inset:0;width:100%;height:100%;'
        f'object-fit:cover;z-index:1;opacity:0.9" alt="">\n  '
        f'<div style="position:absolute;inset:0;'
        f'background:linear-gradient(145deg,rgba(8,10,16,0.25) 0%,rgba(8,10,16,0.55) 100%);'
        f'z-index:2;pointer-events:none"></div>'
    )

    spec = {
        "meta": {
            "system": "s17",
            "aspect": "1:1",
            "slides": 1,
            "brand": "@worqai",
            "language": "es-LATAM",
            "topic": "ai-bg-test",
        },
        "pacing": ["data"],
        "slides": [{
            "id": "s1",
            "layout": "slide-hook-lockup",
            "copy": {
                "kicker": "NUEVO GEO",
                "headline": "Fondos generados\\npor IA.",
                "body": "Imagen adaptada al sistema visual automaticamente.",
            },
            "__extras": bg_html,
        }],
    }

    print(f"\nRendering carousel: {OUTPUT_PATH}")
    render_carousel(spec, OUTPUT_PATH)

    # Inject extras into the rendered HTML
    html = OUTPUT_PATH.read_text(encoding="utf-8")
    parts = html.split('<div class="slide')
    if len(parts) >= 2:
        slide_body = parts[1]
        gt = slide_body.find('>')
        if gt > 0:
            slide_body = slide_body[:gt+1] + "\n  " + bg_html + "\n" + slide_body[gt+1:]
            parts[1] = slide_body
            html = '<div class="slide'.join(parts)
            OUTPUT_PATH.write_text(html, encoding="utf-8")

    size_kb = OUTPUT_PATH.stat().st_size // 1024
    print(f"[OK]  Rendered: {OUTPUT_PATH} ({size_kb} KB)")
    print(f"     Open in browser to review text readability over the AI background.")


if __name__ == "__main__":
    main()
