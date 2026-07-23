#!/usr/bin/env python3
"""
stat_source_validator.py — Scan carousel HTML for fabricated or unverified stat citations.

Usage:
    py scripts/stat_source_validator.py production/carousel_*.html
    py scripts/stat_source_validator.py production/          # scans all .html

Exit codes:
    0 = all stats clean or using approved fallback
    1 = fabricated/unverified sources found
"""

import argparse
import re
import sys
from pathlib import Path

# Sources that are verified and allowed
VERIFIED_SOURCES = [
    "jobscan internal analysis",
    "worqai database",
    "worqai · base de datos",
    "dato interno worqai",
    "linkedin economic graph",
    "world economic forum",
    "future of jobs report",
    "análisis interno profile pro latam",
]

# Known fabricated patterns — these are EXPLICITLY BANNED
FABRICATED_PATTERNS = [
    re.compile(r"linkedin\s+talent\s+report\s+202[0-9]", re.IGNORECASE),
    re.compile(r"linkedin\s+talent\s+solutions\s+report\s+202[0-9]", re.IGNORECASE),
    re.compile(r"jobscan\s+ats\s+report\s+202[0-9]", re.IGNORECASE),
    re.compile(r"jobscan\s+ats\s+optimization\s+report\s+202[0-9]", re.IGNORECASE),
    re.compile(r"jobscan\s+·\s+state\s+of\s+the\s+job\s+search\s+202[0-9]", re.IGNORECASE),
    re.compile(r"jobscan\s+/\s+linkedin\s+talent\s+report", re.IGNORECASE),
]

# General source-tag detector — catches "Fuente: ..." or "Dato: ..." or similar
SOURCE_TAG_RE = re.compile(
    r"(fuente|dato|source|data)\s*[:·]\s*([^<\n]{3,120})",
    re.IGNORECASE,
)


def is_verified(source_text: str) -> bool:
    """Check if a source text matches the verified allow-list."""
    lowered = source_text.lower()
    return any(vs in lowered for vs in VERIFIED_SOURCES)


def is_fabricated(source_text: str) -> bool:
    """Check if a source text matches any known fabricated pattern."""
    return any(pat.search(source_text) for pat in FABRICATED_PATTERNS)


def scan_file(html_path: Path) -> list[dict]:
    """Scan a single HTML file for stat source issues."""
    issues = []
    text = html_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_style = False
    for line_num, line in enumerate(lines, start=1):
        if "<style" in line:
            in_style = True
        if "</style" in line:
            in_style = False
            continue
        if in_style:
            continue
        if "data:image" in line or "base64," in line or "%3C" in line:
            continue
        for match in SOURCE_TAG_RE.finditer(line):
            source_raw = match.group(2).strip()
            # Clean up trailing HTML/tags
            source_clean = re.sub(r"<[^>]+>", "", source_raw).strip()
            if not source_clean:
                continue

            if is_fabricated(source_clean):
                issues.append({
                    "file": html_path.name,
                    "line": line_num,
                    "type": "FABRICATED",
                    "source": source_clean,
                    "fix": "Dato interno WorqAI · base de datos 2025",
                })
            elif not is_verified(source_clean):
                issues.append({
                    "file": html_path.name,
                    "line": line_num,
                    "type": "UNVERIFIED",
                    "source": source_clean,
                    "fix": "Dato interno WorqAI · base de datos 2025",
                })

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate stat sources in carousel HTML")
    parser.add_argument("paths", nargs="+", help="HTML files or directories to scan")
    args = parser.parse_args()

    files_to_scan: list[Path] = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files_to_scan.extend(sorted(path.glob("*.html")))
        elif path.is_file() and path.suffix == ".html":
            files_to_scan.append(path)

    if not files_to_scan:
        print("No HTML files found.")
        sys.exit(0)

    all_issues: list[dict] = []
    for html_file in files_to_scan:
        issues = scan_file(html_file)
        all_issues.extend(issues)

    if not all_issues:
        print(f"[PASS] All stats in {len(files_to_scan)} file(s) use verified sources or approved fallbacks.")
        sys.exit(0)

    print(f"[FAIL] FOUND {len(all_issues)} ISSUE(S) across {len({i['file'] for i in all_issues})} file(s):\n")
    for issue in all_issues:
        print(f"  [{issue['type']}] {issue['file']}:{issue['line']}")
        print(f"    Found:  \"{issue['source']}\"")
        print(f"    Fix:    \"{issue['fix']}\"")
        print()

    sys.exit(1)


if __name__ == "__main__":
    main()
