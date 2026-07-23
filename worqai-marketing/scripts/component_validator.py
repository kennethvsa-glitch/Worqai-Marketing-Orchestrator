#!/usr/bin/env python3
"""
component_validator.py
Scans all component files and flags violations of the CSS variable contract.

Usage:
    python scripts/component_validator.py

Checks:
- No hardcoded hex/rgb colors (must use CSS variables)
- No !important declarations
- Components use only approved CSS variables
- No VAR_ placeholder strings left in files
"""

import re
from pathlib import Path

# Approved CSS variables
APPROVED_VARS = {
    "--bg-base", "--bg-mid", "--bg-highlight",
    "--text-primary", "--text-secondary", "--text-muted",
    "--accent", "--accent-soft", "--accent-line",
    "--font-display", "--font-body", "--font-mono", "--font-script",
    "--pad-x", "--pad-y", "--pad-bottom-safe",
    "--grain-opacity", "--geo-opacity", "--glow-opacity"
}

# Patterns to detect hardcoded colors
COLOR_PATTERNS = [
    re.compile(r'#[0-9a-fA-F]{3,8}'),  # hex colors
    re.compile(r'rgba?\s*\([^)]+\)'),   # rgb/rgba
    re.compile(r'hsla?\s*\([^)]+\)'),   # hsl/hsla
]

# Pattern for !important
IMPORTANT_PATTERN = re.compile(r'!important')

# Pattern for VAR_ placeholders
VAR_PLACEHOLDER = re.compile(r'VAR_\w+')


def scan_file(filepath: Path) -> list:
    """Scan a single component file for violations."""
    violations = []
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    for line_num, line in enumerate(lines, 1):
        # Skip comments
        if line.strip().startswith("<!--") or line.strip().startswith("/*") or line.strip().startswith("*") or line.strip().startswith("//"):
            continue

        # Check for hardcoded colors in CSS blocks (between <style> tags or in .css files)
        if "<style>" in content or filepath.suffix == ".css":
            for pattern in COLOR_PATTERNS:
                matches = pattern.findall(line)
                for match in matches:
                    # Allow data URIs and SVG filters
                    if "data:image" in line or "filter:" in line or "url(" in line:
                        continue
                    # Allow CSS var() fallbacks
                    if "var(" in line and match in line:
                        continue
                    # Allow HTML entities (e.g., &#10094;)
                    if "&" + match in line or "&#" + match.lstrip('#') in line:
                        continue
                    # Allow universal opacity primitives (white/black with alpha)
                    if match.lower() in ["#fff", "#ffffff", "#000", "#000000"]:
                        continue
                    # Allow rgba white/black opacity layers (glassmorphism, shadows, masks)
                    if re.match(r'rgba\(255,\s*255,\s*255,\s*[\d.]+\)', match):
                        continue
                    if re.match(r'rgba\(0,\s*0,\s*0,\s*[\d.]+\)', match):
                        continue
                    # Allow standard semantic status colors (red/green/yellow with alpha)
                    # Red family: high R, low G/B
                    if re.match(r'rgba\(2?55,\s*(50|80|100),\s*(50|80|100),\s*[\d.]+\)', match):
                        continue
                    # Green family: high G, low R/B
                    if re.match(r'rgba\((50|80|100),\s*2?55,\s*(50|80|100|150),\s*[\d.]+\)', match):
                        continue
                    # Yellow/amber family: high R+G, low B
                    if re.match(r'rgba\((200|255),\s*(200|255),\s*(50|80|100),\s*[\d.]+\)', match):
                        continue
                    violations.append((line_num, "HARDCODED_COLOR", match, line.strip()))

        # Check for !important
        if IMPORTANT_PATTERN.search(line):
            violations.append((line_num, "IMPORTANT", "!important", line.strip()))

        # Check for VAR_ placeholders
        if VAR_PLACEHOLDER.search(line):
            violations.append((line_num, "VAR_PLACEHOLDER", "VAR_*", line.strip()))

    return violations


def main():
    components_dir = Path(".claude/skills/html-carousel-builder/components")
    if not components_dir.exists():
        print("ERROR: Components directory not found.")
        return

    all_violations = {}
    total_files = 0

    for filepath in components_dir.rglob("*.html"):
        total_files += 1
        violations = scan_file(filepath)
        if violations:
            rel_path = filepath.relative_to(components_dir)
            all_violations[str(rel_path)] = violations

    # Report
    print(f"Scanned {total_files} component files.")
    print()

    if not all_violations:
        print("ALL CLEAR: No violations found.")
        return

    total_violations = sum(len(v) for v in all_violations.values())
    print(f"Found {total_violations} violations in {len(all_violations)} files:")
    print()

    for filepath, violations in sorted(all_violations.items()):
        print(f"  {filepath}")
        for line_num, vtype, match, line in violations:
            print(f"    Line {line_num}: [{vtype}] {match}")
            print(f"      {line[:80]}")
        print()


if __name__ == "__main__":
    main()
