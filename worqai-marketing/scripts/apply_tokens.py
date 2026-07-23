#!/usr/bin/env python3
"""
apply_tokens.py — Post-process carousel HTML to replace VAR_* placeholders.

Usage:
    python scripts/apply_tokens.py --html production/carousel_X.html --system s29

This catches the #1 quality log failure: "VAR clean" misses.
"""

import argparse
import re
import sys
from pathlib import Path


def parse_tokens_md(path: Path) -> dict:
    """Parse tokens.md compact matrix and return a dict of system tokens."""
    tokens_raw = path.read_text(encoding="utf-8")
    systems = {}
    in_compact = False
    for line in tokens_raw.splitlines():
        line = line.strip()
        if line.startswith("s01 |"):
            in_compact = True
        if not in_compact:
            continue
        if not line or line.startswith("```"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 7:
            continue
        sid = parts[0]
        systems[sid] = {
            "BG_BASE": parts[1].split(",")[0].replace("linear-gradient(145deg, ", "").replace("linear-gradient(148deg, ", "").replace("linear-gradient(135deg, ", "").replace("linear-gradient(180deg, ", "").replace("linear-gradient(140deg, ", "").strip(),
            "BG_MID": parts[1].split(",")[1].strip() if "," in parts[1] else parts[1].strip(),
            "ACCENT": parts[2],
            "TEXT_PRIMARY": parts[3],
            "TEXT_SECONDARY": parts[4],
            "GRAIN_OPACITY": parts[5],
        }
    return systems


def build_token_map(system_id: str, systems: dict) -> dict:
    """Build the full VAR_* → value map for a given system."""
    s = systems.get(system_id, {})
    if not s:
        raise ValueError(f"System {system_id} not found in tokens.md")

    # Derive additional tokens
    accent = s["ACCENT"]
    # Convert hex accent to rgba for deco-color fallback
    if accent.startswith("#") and len(accent) == 7:
        r = int(accent[1:3], 16)
        g = int(accent[3:5], 16)
        b = int(accent[5:7], 16)
        deco_color = f"rgba({r},{g},{b},0.06)"
    else:
        deco_color = "rgba(255,255,255,0.06)"

    # Grain opacity → deco opacity mapping (common heuristic)
    try:
        grain = float(s["GRAIN_OPACITY"])
        deco_opacity = min(grain + 0.03, 0.15)
    except ValueError:
        deco_opacity = 0.06

    # Block backgrounds (common heuristic)
    if accent.startswith("#") and len(accent) == 7:
        r = int(accent[1:3], 16)
        g = int(accent[3:5], 16)
        b = int(accent[5:7], 16)
        block_bad = f"rgba({r},{g},{b},0.10)"
        block_good = f"rgba({r},{g},{b},0.08)"
    else:
        block_bad = "rgba(255,92,60,0.10)"
        block_good = "rgba(199,255,58,0.08)"

    token_map = {
        "VAR_FONT_STACK": "'Inter', sans-serif",  # fallback; agent should set correctly
        "VAR_ACCENT": accent,
        "VAR_BG_BASE": s["BG_BASE"],
        "VAR_BG_MID": s["BG_MID"],
        "VAR_TEXT_PRIMARY": s["TEXT_PRIMARY"],
        "VAR_TEXT_SECONDARY": s["TEXT_SECONDARY"],
        "VAR_DECO_COLOR": deco_color,
        "VAR_DECO_OPACITY": str(deco_opacity),
        "VAR_BLOCK_BAD_BG": block_bad,
        "VAR_BLOCK_GOOD_BG": block_good,
        "VAR_GRAIN_OPACITY": s["GRAIN_OPACITY"],
    }
    return token_map


def apply_tokens(html_path: Path, token_map: dict) -> str:
    """Replace all VAR_* placeholders in the HTML file."""
    html = html_path.read_text(encoding="utf-8")
    for key, value in token_map.items():
        html = html.replace(key, value)
    html_path.write_text(html, encoding="utf-8")
    return html


def main():
    parser = argparse.ArgumentParser(description="Replace VAR_* tokens in carousel HTML")
    parser.add_argument("--html", required=True, help="Path to HTML file")
    parser.add_argument("--system", required=True, help="System ID (e.g. s29)")
    parser.add_argument(
        "--tokens",
        default=".claude/skills/html-carousel-builder/tokens.md",
        help="Path to tokens.md",
    )
    args = parser.parse_args()

    html_path = Path(args.html)
    tokens_path = Path(args.tokens)

    if not html_path.exists():
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)
    if not tokens_path.exists():
        print(f"ERROR: tokens.md not found: {tokens_path}", file=sys.stderr)
        sys.exit(1)

    systems = parse_tokens_md(tokens_path)
    token_map = build_token_map(args.system, systems)
    apply_tokens(html_path, token_map)

    # Verify no VAR_ strings remain
    remaining = re.findall(r"VAR_\w+", html_path.read_text(encoding="utf-8"))
    if remaining:
        print(f"WARNING: {len(remaining)} VAR_* placeholders remain:")
        for v in set(remaining):
            print(f"  - {v}")
        sys.exit(2)
    else:
        print(f"OK: All VAR_* tokens replaced in {html_path}")


if __name__ == "__main__":
    main()
