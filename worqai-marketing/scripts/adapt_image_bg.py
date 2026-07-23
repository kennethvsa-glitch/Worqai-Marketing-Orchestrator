#!/usr/bin/env python3
"""
adapt_image_bg.py — AI Background Color Adaptation Pipeline

Generates system-specific color variants of AI-generated background images
and maintains a manifest registry for the carousel render pipeline.

Usage:
    py scripts/adapt_image_bg.py --all
    py scripts/adapt_image_bg.py --file bubbles-01.png --name "Liquid Bubbles" --hue 180
"""

import sys
import json
import argparse
from pathlib import Path
from PIL import Image
import colorsys

ROOT = Path(__file__).parent.parent
SOURCE_DIR = ROOT / "ideation" / "ai-backgrounds"
OUTPUT_DIR = ROOT / "brand" / "generated-bg"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"

SYSTEMS = {
    "s01": {"accent": "#C8A84B", "sat_mult": 0.85, "name": "NOIR GOLD"},
    "s04": {"accent": "#e05a7a", "sat_mult": 1.05, "name": "CRIMSON NIGHT"},
    "s17": {"accent": "#C7FF3A", "sat_mult": 1.15, "name": "WORQAI VERDE"},
    "s29": {"accent": "#00ff9c", "sat_mult": 1.25, "name": "CYBERPUNK ALLEY"},
}

DARK_THRESHOLD = 15
DEFAULT_HUE = 180.0


def slugify(name: str) -> str:
    """Convert a human name to a filesystem-safe ID."""
    return name.lower().replace(" ", "-").replace("_", "-").strip("-")


def hex_to_hue(hex_color: str) -> float:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)
    return h * 360.0


def process_image(img: Image.Image, hue_shift_deg: float, sat_mult: float) -> Image.Image:
    pixels = img.load()
    width, height = img.size
    hue_shift = hue_shift_deg / 360.0
    processed = 0

    for y in range(height):
        for x in range(width):
            px = pixels[x, y]
            r, g, b = px[0], px[1], px[2]
            if r <= DARK_THRESHOLD and g <= DARK_THRESHOLD and b <= DARK_THRESHOLD:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            h = (h + hue_shift) % 1.0
            s = min(1.0, s * sat_mult)
            nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
            if len(px) == 4:
                pixels[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255), px[3])
            else:
                pixels[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255))
            processed += 1

        if (y + 1) % 100 == 0 or y == height - 1:
            pct = ((y + 1) * width) / (width * height) * 100
            sys.stdout.write(f"\r  {pct:.1f}%  ({processed} pixels shifted)")
            sys.stdout.flush()
    print()
    return img


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {"backgrounds": []}


def save_manifest(manifest: dict):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def process_one_image(source_path: Path, bg_name: str, dominant_hue: float, manifest: dict) -> dict:
    bg_id = f"ai-{slugify(bg_name)}"
    variant_dir = OUTPUT_DIR / bg_id
    variant_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n-> Processing: {bg_name} (id={bg_id})")
    print(f"   Source: {source_path}")
    print(f"   Dominant hue: {dominant_hue:.1f} deg")

    img = Image.open(source_path).convert("RGBA")
    w, h = img.size
    if w != h:
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        print(f"   Cropped to square: {img.size}")

    variants = {}
    for system_id, config in SYSTEMS.items():
        target_hue = hex_to_hue(config["accent"])
        hue_shift = target_hue - dominant_hue
        print(f"   {system_id} ({config['name']}): shift={hue_shift:+.1f} deg, sat={config['sat_mult']}x")

        variant = img.copy()
        variant = process_image(variant, hue_shift, config["sat_mult"])
        variant = variant.resize((1080, 1080), Image.LANCZOS)

        out_path = variant_dir / f"{system_id}.png"
        variant.save(out_path, "PNG", optimize=True)
        size_kb = out_path.stat().st_size // 1024
        print(f"     -> {out_path} ({size_kb} KB)")
        variants[system_id] = str(out_path.relative_to(ROOT)).replace("\\", "/")

    # Update manifest
    entry = {
        "id": bg_id,
        "name": bg_name,
        "source": str(source_path.relative_to(ROOT)).replace("\\", "/"),
        "systems": list(SYSTEMS.keys()),
        "dominant_hue": dominant_hue,
        "variants": variants,
    }

    # Replace existing entry or append
    existing = next((i for i, b in enumerate(manifest["backgrounds"]) if b["id"] == bg_id), None)
    if existing is not None:
        manifest["backgrounds"][existing] = entry
        print(f"   [UPDATED] Manifest entry '{bg_id}'")
    else:
        manifest["backgrounds"].append(entry)
        print(f"   [ADDED] Manifest entry '{bg_id}'")

    return manifest


def main():
    parser = argparse.ArgumentParser(description="Adapt AI background images to WorqAI visual systems")
    parser.add_argument("--all", action="store_true", help="Process all PNGs in ideation/ai-backgrounds/")
    parser.add_argument("--file", type=str, help="Specific PNG filename in ideation/ai-backgrounds/")
    parser.add_argument("--name", type=str, help="Human-readable name for the background")
    parser.add_argument("--hue", type=float, default=DEFAULT_HUE, help="Dominant hue of source image (0-360)")
    args = parser.parse_args()

    manifest = load_manifest()

    if args.all:
        if not SOURCE_DIR.exists():
            print(f"[FAIL] Source directory not found: {SOURCE_DIR}", file=sys.stderr)
            sys.exit(1)

        pngs = sorted(SOURCE_DIR.glob("*.png"))
        if not pngs:
            print("[INFO] No PNGs found in ideation/ai-backgrounds/")
            sys.exit(0)

        for png in pngs:
            bg_name = args.name or png.stem.replace("-", " ").title()
            manifest = process_one_image(png, bg_name, args.hue, manifest)

    elif args.file:
        source_path = SOURCE_DIR / args.file
        if not source_path.exists():
            print(f"[FAIL] File not found: {source_path}", file=sys.stderr)
            sys.exit(1)
        bg_name = args.name or source_path.stem.replace("-", " ").title()
        manifest = process_one_image(source_path, bg_name, args.hue, manifest)

    else:
        parser.print_help()
        sys.exit(1)

    save_manifest(manifest)
    print(f"\n[DONE] Manifest saved: {MANIFEST_PATH}")
    print(f"       Total backgrounds: {len(manifest['backgrounds'])}")


if __name__ == "__main__":
    main()
