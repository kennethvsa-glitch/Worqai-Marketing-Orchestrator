#!/usr/bin/env python3
"""
usage_logger.py — Append production metadata to carousel-matrix.yaml

Usage (called automatically by build_orchestrator.py or carousel_exporter.py):
    py scripts/usage_logger.py production/carousel_nuevo.html --system s17 --preset brand_worqai_tips

Or manual:
    py scripts/usage_logger.py production/carousel_nuevo.html --system s17 --slides 8 --aspect 4:5
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

MATRIX_PATH = Path("carousel-matrix.yaml")


def parse_args():
    parser = argparse.ArgumentParser(description="Log carousel production metadata")
    parser.add_argument("html_file", help="Path to generated carousel HTML")
    parser.add_argument("--system", help="Design system ID (e.g. s17)")
    parser.add_argument("--preset", help="Preset name used")
    parser.add_argument("--slides", type=int, help="Number of slides")
    parser.add_argument("--aspect", default="1:1", help="Aspect ratio")
    parser.add_argument("--preflight-score", type=int, help="Preflight score (0-100)")
    parser.add_argument("--exported", action="store_true", help="Mark as exported")
    return parser.parse_args()


def extract_metadata_from_html(html_path: Path):
    """Auto-extract what we can from the HTML file itself."""
    html = html_path.read_text(encoding="utf-8")
    
    # Slide count
    slide_count = len(re.findall(r'<(?:section|div)[^>]*class="[^"]*slide[^"]*"', html, re.IGNORECASE))
    
    # Aspect ratio from CSS
    aspect = "1:1"
    if 'aspect-ratio: 4 / 5' in html or 'aspect-ratio: 4/5' in html:
        aspect = "4:5"
    elif 'aspect-ratio: 9 / 16' in html or 'aspect-ratio: 9/16' in html:
        aspect = "9:16"
    
    # Detect system from gradient or accent color (fallback)
    system = None
    # Try to find sN reference in title or comments
    title_match = re.search(r'<title>.*?\b(s\d+)\b.*?</title>', html, re.IGNORECASE)
    if title_match:
        system = title_match.group(1).lower()
    
    # Technique count heuristic: count visual layers
    techniques = 0
    if re.search(r'\.slide::before|\.slide::after', html):
        techniques += 1  # pseudo-element layer
    if 'gradient' in html.lower():
        techniques += 1
    if 'blur(' in html.lower():
        techniques += 1
    if 'backdrop-filter' in html.lower():
        techniques += 1
    if 'mix-blend-mode' in html.lower():
        techniques += 1
    
    # File size
    file_size_kb = round(html_path.stat().st_size / 1024, 1)
    
    return {
        "slides": slide_count,
        "aspect": aspect,
        "system": system,
        "file_size_kb": file_size_kb,
        "techniques_count": techniques,
    }


def load_matrix():
    if not MATRIX_PATH.exists():
        return {"carousel_matrix": {"version": "2.1", "production": {}}}
    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"carousel_matrix": {"production": {}}}


def save_matrix(data):
    with open(MATRIX_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


def generate_entry_id(html_path: Path):
    """Generate a stable ID from filename."""
    name = html_path.stem
    return name.replace("carousel_", "").replace("slide-test_", "test_")


def main():
    args = parse_args()
    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"ERROR: File not found: {html_path}")
        sys.exit(1)
    
    auto = extract_metadata_from_html(html_path)
    
    entry = {
        "file": str(html_path).replace("\\", "/"),
        "system": args.system or auto.get("system"),
        "preset": args.preset,
        "slides": args.slides or auto.get("slides"),
        "aspect": args.aspect or auto.get("aspect"),
        "file_size_kb": auto.get("file_size_kb"),
        "techniques_count": auto.get("techniques_count"),
        "exported": args.exported,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    
    if args.preflight_score is not None:
        entry["preflight_score"] = args.preflight_score
    
    # Remove None values
    entry = {k: v for k, v in entry.items() if v is not None}
    
    data = load_matrix()
    production = data.setdefault("carousel_matrix", {}).setdefault("production", {})
    entry_id = generate_entry_id(html_path)
    production[entry_id] = entry
    
    save_matrix(data)
    print(f"LOGGED: {entry_id}")
    print(f"  system: {entry.get('system')}")
    print(f"  slides: {entry.get('slides')}")
    print(f"  file_size: {entry.get('file_size_kb')} KB")
    print(f"  aspect: {entry.get('aspect')}")


if __name__ == "__main__":
    main()
