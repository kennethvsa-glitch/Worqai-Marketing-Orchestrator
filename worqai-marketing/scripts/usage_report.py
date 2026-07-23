#!/usr/bin/env python3
"""
usage_report.py — Generate analytics report from carousel-matrix.yaml production log.

Usage:
    py scripts/usage_report.py
    py scripts/usage_report.py --days 30
    py scripts/usage_report.py --system s17
"""

import argparse
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

MATRIX_PATH = Path("carousel-matrix.yaml")


def load_matrix():
    if not MATRIX_PATH.exists():
        return {}
    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("carousel_matrix", {}).get("production", {})


def parse_args():
    parser = argparse.ArgumentParser(description="Carousel usage analytics")
    parser.add_argument("--days", type=int, default=9999, help="Only show last N days")
    parser.add_argument("--system", help="Filter by design system")
    return parser.parse_args()


def main():
    args = parse_args()
    production = load_matrix()
    
    if not production:
        print("No production data found. Generate some carousels first.")
        return
    
    cutoff = datetime.now() - timedelta(days=args.days)
    
    # Filter entries
    entries = []
    for key, entry in production.items():
        date_str = entry.get("date", "2026-01-01")
        try:
            entry_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if entry_date < cutoff:
            continue
        if args.system and entry.get("system") != args.system:
            continue
        entries.append((key, entry))
    
    if not entries:
        print(f"No entries match filters (days={args.days}, system={args.system})")
        return
    
    print(f"\n{'='*60}")
    print(f"USAGE REPORT — {len(entries)} carousels")
    if args.days < 9999:
        print(f"Last {args.days} days")
    if args.system:
        print(f"System filter: {args.system}")
    print(f"{'='*60}\n")
    
    # System usage
    system_counts = Counter(e.get("system", "unknown") or "unknown" for _, e in entries)
    print("TOP DESIGN SYSTEMS")
    print("-" * 40)
    for sys_id, count in system_counts.most_common(15):
        bar = "#" * count + "-" * (max(system_counts.values()) - count)
        print(f"  {sys_id:6} | {bar} {count}")
    print()
    
    # Aspect ratio distribution
    aspect_counts = Counter(e.get("aspect", "1:1") for _, e in entries)
    print("ASPECT RATIOS")
    print("-" * 40)
    for aspect, count in aspect_counts.most_common():
        pct = count / len(entries) * 100
        print(f"  {aspect:6} | {count:3} ({pct:.0f}%)")
    print()
    
    # File size stats
    sizes = [e.get("file_size_kb", 0) for _, e in entries if e.get("file_size_kb")]
    if sizes:
        avg = sum(sizes) / len(sizes)
        mini = min(sizes)
        maxi = max(sizes)
        print("FILE SIZE STATS")
        print("-" * 40)
        print(f"  Average: {avg:.1f} KB")
        print(f"  Min:     {mini:.1f} KB")
        print(f"  Max:     {maxi:.1f} KB")
        print(f"  Elite (55+): {sum(1 for s in sizes if s >= 55)} carousels")
        print(f"  Good (45+):  {sum(1 for s in sizes if s >= 45)} carousels")
        print(f"  Under 35:    {sum(1 for s in sizes if s < 35)} carousels")
    print()
    
    # Preflight score stats
    scores = [e.get("preflight_score", 0) for _, e in entries if e.get("preflight_score")]
    if scores:
        avg_score = sum(scores) / len(scores)
        print("PREFLIGHT SCORES")
        print("-" * 40)
        print(f"  Average: {avg_score:.0f}/100")
        print(f"  90+ (ready):     {sum(1 for s in scores if s >= 90)}")
        print(f"  70-89 (good):    {sum(1 for s in scores if 70 <= s < 90)}")
        print(f"  <70 (needs work): {sum(1 for s in scores if s < 70)}")
    print()
    
    # Unused systems (from the 48)
    all_systems = {f"s{i:02d}" for i in range(1, 49)}
    used = set(system_counts.keys())
    unused = sorted(all_systems - used)
    if unused:
        print(f"UNUSED SYSTEMS ({len(unused)} of 48)")
        print("-" * 40)
        for i in range(0, len(unused), 8):
            print("  " + " ".join(unused[i:i+8]))
    print()
    
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
