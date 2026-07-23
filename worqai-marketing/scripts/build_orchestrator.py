#!/usr/bin/env python3
"""
build_orchestrator.py — Reads carousel-matrix.yaml and tells the agent exactly
which files to load for a given preset.

Usage:
    python scripts/build_orchestrator.py --preset awareness_urgent
    python scripts/build_orchestrator.py --custom --system s29 --slides 4 --layouts L01 L02 L04 L07

This removes the matrix (157 lines) from the agent's context entirely.
The agent only loads what this script tells it to.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_matrix(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_preset_context(matrix: dict, preset_name: str) -> dict:
    presets = matrix.get("carousel_matrix", {}).get("presets", {})
    preset = presets.get(preset_name)
    if not preset:
        available = ", ".join(presets.keys())
        raise ValueError(f"Preset '{preset_name}' not found. Available: {available}")

    files_to_load = [
        "html-carousel-builder/tokens.md",
        "html-carousel-builder/build.md",
        "html-carousel-builder/workflow.md",
    ]

    # Load techniques.md only if preset explicitly requests it or geo has custom effects
    geo = preset.get("geo", [])
    techniques_required = preset.get("techniques_required", False)
    if techniques_required or any(g in ("GEO-13", "scan_lines", "zoom_rings", "neon_tubes", "halftone", "ink_bleed", "chromatic", "starburst") for g in geo):
        files_to_load.append("html-carousel-builder/techniques.md")

    return {
        "preset": preset_name,
        "files_to_load": files_to_load,
        "system": preset.get("system"),
        "slides": preset.get("slides"),
        "layouts": preset.get("layouts"),
        "geo": geo,
        "hook_type": preset.get("hook_type"),
        "aspect": preset.get("aspect", "1:1"),
        "brand": preset.get("brand"),
        "build_mode": preset.get("build_mode", "standard"),
        "techniques_required": techniques_required,
    }


def get_custom_context(system: str, slides: int, layouts: list, geo: list = None, aspect: str = "1:1") -> dict:
    files_to_load = [
        "html-carousel-builder/tokens.md",
        "html-carousel-builder/build.md",
        "html-carousel-builder/workflow.md",
    ]
    if geo:
        files_to_load.append("html-carousel-builder/techniques.md")

    return {
        "preset": "custom",
        "files_to_load": files_to_load,
        "system": system,
        "slides": slides,
        "layouts": layouts,
        "geo": geo or [],
        "aspect": aspect,
        "build_mode": "standard",
        "techniques_required": bool(geo),
    }


def print_context(ctx: dict):
    print(f"# Build Context: {ctx['preset']}")
    print(f"system: {ctx['system']}")
    print(f"slides: {ctx['slides']}")
    print(f"layouts: {ctx['layouts']}")
    print(f"aspect: {ctx['aspect']}")
    print(f"build_mode: {ctx['build_mode']}")
    print(f"techniques_required: {ctx.get('techniques_required', False)}")
    if ctx.get("brand"):
        print(f"brand: {ctx['brand']}")
    if ctx.get("hook_type"):
        print(f"hook_type: {ctx['hook_type']}")
    print()
    print("## Files to load (in order):")
    for f in ctx["files_to_load"]:
        print(f"  - {f}")
    print()
    print("## Template:")
    print("  - templates/carousel-shell.html")
    print()
    print("## Next steps:")
    print("  1. Load tokens.md → pick system from selection table")
    print("  2. Load build.md → pick layouts, write copy")
    if ctx.get("techniques_required"):
        print("  3. Load techniques.md → copy GEO CSS")
    print("  4. Copy shell.html → replace VAR_* → build slides")


def main():
    parser = argparse.ArgumentParser(description="Carousel build orchestrator")
    parser.add_argument("--preset", help="Preset name from carousel-matrix.yaml")
    parser.add_argument("--custom", action="store_true", help="Custom build (no preset)")
    parser.add_argument("--system", help="System ID for custom build (e.g. s29)")
    parser.add_argument("--slides", type=int, help="Number of slides for custom build")
    parser.add_argument("--layouts", nargs="+", help="Layouts for custom build")
    parser.add_argument("--geo", nargs="*", default=[], help="GEO effects for custom build")
    parser.add_argument("--aspect", default="1:1", help="Aspect ratio (1:1, 4:5, 9:16)")
    parser.add_argument(
        "--matrix",
        default="carousel-matrix.yaml",
        help="Path to carousel-matrix.yaml",
    )
    args = parser.parse_args()

    if args.preset:
        matrix = load_matrix(Path(args.matrix))
        ctx = get_preset_context(matrix, args.preset)
    elif args.custom:
        if not all([args.system, args.slides, args.layouts]):
            print("ERROR: --custom requires --system, --slides, and --layouts", file=sys.stderr)
            sys.exit(1)
        ctx = get_custom_context(args.system, args.slides, args.layouts, args.geo, args.aspect)
    else:
        print("ERROR: Use --preset <name> or --custom with --system/--slides/--layouts", file=sys.stderr)
        sys.exit(1)

    print_context(ctx)


if __name__ == "__main__":
    main()
