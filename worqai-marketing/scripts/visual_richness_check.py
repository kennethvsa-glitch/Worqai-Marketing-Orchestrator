#!/usr/bin/env python3
"""
visual_richness_check.py — Visual Richness Score for carousel HTML files.

Separate from preflight.py (Technical Compliance). This scores creative quality:
font contrast, decorative density, layer diversity, cross-carousel uniqueness.

Usage:
    py scripts/visual_richness_check.py production/carousel_topic_s17.html
    py scripts/visual_richness_check.py production/c1.html production/c2.html production/c3.html

Exit codes:
    0 = all files pass
    1 = one or more files failed
"""

import re
import sys
from pathlib import Path

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"


def extract_system_id(html: str) -> str:
    m = re.search(r"·\s*(s\d+)\s*<", html)
    if m:
        return m.group(1)
    m = re.search(r"system\s+(s\d+)", html, re.IGNORECASE)
    return m.group(1) if m else "unknown"


def count_font_families(html: str) -> set[str]:
    """Extract distinct font family names loaded via Google Fonts URL."""
    m = re.search(r'fonts\.googleapis\.com/css2\?([^"]+)', html)
    if not m:
        return set()
    query = m.group(1)
    families = re.findall(r"family=([A-Za-z+]+)", query)
    return {f.replace("+", " ") for f in families}


def check_font_contrast(html: str) -> tuple[str, str]:
    """--font-display and --font-body must be different families."""
    display_m = re.search(r"--font-display:\s*'([^']+)'", html)
    body_m = re.search(r"--font-body:\s*'([^']+)'", html)
    if not display_m or not body_m:
        return WARN, "Could not extract --font-display / --font-body from CSS vars"
    display_f = display_m.group(1)
    body_f = body_m.group(1)
    if display_f == body_f:
        return FAIL, f"--font-display and --font-body are both '{display_f}' -- must be different typefaces"
    return PASS, f"display='{display_f}' · body='{body_f}'"


def count_loaded_fonts(html: str) -> tuple[str, str]:
    """At least 3 distinct font families must be loaded."""
    families = count_font_families(html)
    n = len(families)
    if n >= 3:
        return PASS, f"{n} families loaded: {', '.join(sorted(families))}"
    if n == 2:
        return WARN, f"Only {n} families loaded ({', '.join(sorted(families))}). Elite bar = 3+"
    return FAIL, f"Only {n} font famil{'y' if n == 1 else 'ies'} loaded. Minimum 3 required."


def count_decoratives(html: str) -> tuple[str, str]:
    """Count decorative elements injected by the render engine."""
    decorative_classes = [
        "deco-watermark", "deco-corner-tl", "deco-corner-br",
        "deco-ornament", "deco-stamp",
        "chrome-badge-stamp", "chrome-vertical-counter", "chrome-header-bar",
        "sub-stamp-circle",
        # v2 — SVG starburst decoratives
        "deco-starburst",
    ]
    found = []
    for cls in decorative_classes:
        # Count class usages in actual HTML elements (not CSS definitions)
        pattern = rf'class="[^"]*{re.escape(cls)}[^"]*"'
        matches = re.findall(pattern, html)
        if matches:
            found.append(f"{cls}×{len(matches)}")

    total = sum(
        len(re.findall(rf'class="[^"]*{re.escape(cls)}[^"]*"', html))
        for cls in decorative_classes
    )
    if total >= 2:
        return PASS, f"{total} decorative elements: {', '.join(found)}"
    if total == 1:
        return FAIL, f"Only 1 decorative element found. Minimum 2 required. Found: {found}"
    return FAIL, "Zero decorative elements. Every carousel needs >=2 (stamps, corner frames, ornaments, watermarks, chrome)."


def check_layer_diversity(html: str) -> tuple[str, str]:
    """Slides should not all use identical geo layers."""
    all_geo_classes = [
        "pw-grid", "scan-lines", "glow-orb", "zoom-rings", "grid-bg",
        "diag-band", "blob-bg", "vol-light", "geo-mesh-noise", "geo-pixel-grid",
        "geo-conic-rays", "geo-chevron-stripe", "geo-iso-grid", "geo-paper-texture",
        "geo-halftone", "geo-ribbon-flow", "geo-circuit-trace", "geo-topo-lines",
        "geo-starfield", "geo-gradient-bands",
        # v2 — SVG organic blob variants (count toward layer diversity)
        "svg-blob-tr", "svg-blob-bl", "svg-blob-center",
        "svg-blob-asymmetric", "svg-blob-scattered",
    ]
    # svg-blob classes use multi-class attrs like 'class="svg-blob svg-blob-tr"', so check both forms.
    used = set()
    for cls in all_geo_classes:
        if f'class="{cls}"' in html or f'"{cls} ' in html or f' {cls}"' in html or f' {cls} ' in html:
            used.add(cls)
    non_default = used - {"blob-bg", "vol-light", "pw-grid", "glow-orb", "grid-bg", "diag-band"}

    if len(non_default) >= 2:
        return PASS, f"{len(used)} total layers used, {len(non_default)} non-default: {', '.join(sorted(non_default))}"
    if len(non_default) == 1:
        return WARN, f"Only 1 non-default layer used: {', '.join(non_default)}. Use 2+ to create slide variety."
    if len(used) >= 3:
        return WARN, f"{len(used)} layers used but all are system defaults. Try adding: scan-lines, zoom-rings, geo-circuit-trace, geo-topo-lines, etc."
    return FAIL, "Only default system layers used. Layer monoculture -- every slide looks identical."


def check_bespoke_css(html: str) -> tuple[str, str]:
    """custom_css block presence indicates per-slide bespoke styling."""
    has_bespoke = bool(re.search(r"slide \d+ bespoke", html))
    has_sN_classes = bool(re.search(r'class="[^"]*s\d+-[a-z]', html))
    if has_bespoke:
        return PASS, "custom_css blocks present (injected from spec)"
    if has_sN_classes:
        return PASS, "Found .sN-* prefixed custom classes"
    return WARN, "No custom_css or .sN-* classes found. Use slide 'custom_css' field for bespoke CSS."


# Topic keywords where a terminal/code-mock slide reads as off-brand.
# A street running collective, a luxury candle brand, or a taco truck should
# not present their story through a command-line interface.
NON_TECH_TOPIC_KEYWORDS = (
    "run", "running", "runner", "fitness", "gym", "yoga",
    "food", "taco", "restaurant", "coffee", "cafe", "bakery",
    "fashion", "boutique", "candle", "perfume", "beauty", "skincare",
    "wedding", "florist", "lifestyle", "travel", "vacation",
    "kids", "toy", "pet", "dog", "cat",
)

# Topic keywords where a terminal slide IS thematically appropriate.
TECH_TOPIC_KEYWORDS = (
    "tech", "saas", "ai", "ml", "data", "code", "dev", "developer",
    "cyber", "security", "hack", "api", "cloud", "devops",
    "ats", "scanner", "diagnose", "diagnostic", "medical", "sleep",
    "health", "biotech", "lab", "scan",
)


def check_v2_primitives_used(html: str) -> tuple[str, str]:
    """v2: reward use of SVG primitives (icons, blobs, starbursts, text treatments, shadows).
    Per Kenneth's Q5 decision, this is a soft signal — never a hard FAIL.
    """
    primitives_found = []

    # SVG icon references
    icon_count = len(re.findall(r'<use\s+href="#icon-', html))
    if icon_count:
        primitives_found.append(f"icons×{icon_count}")

    # SVG blob layers
    blob_count = len(re.findall(r'class="svg-blob\b', html))
    if blob_count:
        primitives_found.append(f"svg-blob×{blob_count}")

    # SVG starburst decoratives
    starburst_count = len(re.findall(r'class="deco-starburst\b', html))
    if starburst_count:
        primitives_found.append(f"svg-starburst×{starburst_count}")

    # Text treatments
    for cls, label in (
        ("txt-gradient", "gradient-text"),
        ("txt-glow-bold", "neon-glow"),
        ("txt-glow-medium", "neon-glow"),
        ("txt-glow-subtle", "neon-glow"),
        ("txt-stroke", "text-stroke"),
        ("txt-stroke-filled", "text-stroke"),
    ):
        n = len(re.findall(rf'class="[^"]*\b{re.escape(cls)}\b[^"]*"', html))
        if n:
            primitives_found.append(f"{label}×{n}")

    # Drop-shadow filters (auto-applied so usually present — check explicit use)
    shadow_count = len(re.findall(r'filter:\s*url\(#shadow-', html))
    if shadow_count:
        primitives_found.append(f"svg-shadow×{shadow_count}")

    total = len(primitives_found)
    if total >= 3:
        return PASS, f"v2 primitives used ({total} types): {', '.join(primitives_found)}"
    if total >= 1:
        return WARN, f"Only {total} v2 primitive type(s) used: {', '.join(primitives_found)}. Aim for 3+ per carousel."
    return WARN, "Zero v2 primitives used. Try SVG icons, organic blobs, gradient text, or neon-glow for visual lift."


def check_terminal_appropriateness(html: str) -> tuple[str, str]:
    """Warn if a terminal slide appears in a clearly non-tech carousel.

    A terminal block (.term-wrap) is on-brand for tech, medical, diagnostic,
    or security topics. It feels forced in lifestyle, food, fitness, fashion
    carousels where the brand voice is anti-tech or non-digital.
    """
    has_terminal = bool(re.search(r'class="[^"]*term-wrap[^"]*"', html))
    if not has_terminal:
        return PASS, "No terminal slide in this carousel"

    # Extract topic + brand from the title and brand div for context.
    title_m = re.search(r"<title>([^<]+)</title>", html, re.IGNORECASE)
    brand_m = re.search(r'<div\s+class="brand"[^>]*>\s*([^<\s][^<]*?)\s*</div>', html)
    haystack = " ".join(filter(None, [
        title_m.group(1) if title_m else "",
        brand_m.group(1) if brand_m else "",
    ])).lower()

    tech_hits = [k for k in TECH_TOPIC_KEYWORDS if k in haystack]
    non_tech_hits = [k for k in NON_TECH_TOPIC_KEYWORDS if k in haystack]

    if tech_hits:
        return PASS, f"Terminal fits topic ({'/'.join(tech_hits[:3])})"
    if non_tech_hits:
        return WARN, (
            f"Terminal slide in non-tech topic ({'/'.join(non_tech_hits[:3])}). "
            f"Consider slide-myth-vs-fact, slide-big-number, or slide-pull-quote instead."
        )
    return PASS, "Terminal present, topic context neutral"


def check_blob_overuse(html: str) -> tuple[str, str]:
    """v3: FAIL if any single blob/orb appears >2× or total soft circles > slides*1.2."""
    blob_classes = [
        "svg-blob-tr", "svg-blob-bl", "svg-blob-center",
        "svg-blob-asymmetric", "svg-blob-scattered",
        "glow-orb", "blob-bg", "vol-light",
    ]
    issues = []
    total_soft_circles = 0
    for cls in blob_classes:
        count = len(re.findall(rf'class="[^"]*\b{re.escape(cls)}\b[^"]*"', html))
        if count:
            total_soft_circles += count
        if count > 2:
            issues.append(f"{cls} used {count}× — max 2 per carousel")

    slide_count = max(1, len(re.findall(r'<div class="slide', html)))
    if total_soft_circles > slide_count * 1.2:
        issues.append(
            f"Total soft circles: {total_soft_circles} on {slide_count} slides — "
            f"max {int(slide_count * 1.2)}. Vary geo layers."
        )

    if issues:
        return FAIL, "; ".join(issues)
    return PASS, f"Soft-circle count: {total_soft_circles} (healthy)"


def check_layer_combo_repetition(html: str) -> tuple[str, str]:
    """v3: FAIL if >50% slides share identical layer combo or >3 consecutive same combo."""
    slides = re.split(r'(?=<div class="slide)', html)
    slides = [s for s in slides if '<div class="slide' in s]
    if not slides:
        return PASS, "No slides to analyze"

    layer_sigs = []
    for slide in slides:
        layers = re.findall(
            r'class="([^"]*(?:svg-blob|glow-orb|blob-bg|vol-light|geo-)[^"]*)"',
            slide
        )
        uniq = sorted(set(" ".join(layers).split()))
        layer_sigs.append(tuple(uniq))

    from collections import Counter
    combo_counts = Counter(layer_sigs)
    most_common = combo_counts.most_common(1)[0] if combo_counts else ((), 0)

    issues = []
    if most_common[1] > len(slides) * 0.5:
        issues.append(
            f"Same layer combo on {most_common[1]}/{len(slides)} slides (>50%). "
            f"Vary layers per slide."
        )

    run = 0
    max_run = 0
    current = None
    for sig in layer_sigs:
        if sig == current and sig != ():
            run += 1
            max_run = max(max_run, run)
        else:
            current = sig
            run = 1
    if max_run > 3:
        issues.append(
            f"Same layer combo on {max_run} consecutive slides — max 3. "
            f"Break the rhythm."
        )

    if issues:
        return FAIL, "; ".join(issues)
    return PASS, f"{len(combo_counts)} distinct layer combos across {len(slides)} slides"


def score_single(path: Path) -> dict:
    html = path.read_text(encoding="utf-8")
    system_id = extract_system_id(html)

    checks = {
        "font_contrast":            check_font_contrast(html),
        "fonts_loaded":             count_loaded_fonts(html),
        "decoratives":              count_decoratives(html),
        "layer_diversity":          check_layer_diversity(html),
        "bespoke_css":              check_bespoke_css(html),
        "v2_primitives":            check_v2_primitives_used(html),
        "terminal_appropriateness": check_terminal_appropriateness(html),
        "blob_overuse":             check_blob_overuse(html),
        "layer_combo_repetition":   check_layer_combo_repetition(html),
    }

    fails = sum(1 for s, _ in checks.values() if s == FAIL)
    warns = sum(1 for s, _ in checks.values() if s == WARN)
    passes = sum(1 for s, _ in checks.values() if s == PASS)

    total_checks = len(checks)
    score = round((passes / total_checks) * 100)

    return {
        "path": path,
        "system_id": system_id,
        "checks": checks,
        "score": score,
        "fails": fails,
        "warns": warns,
    }


def check_cross_carousel(results: list[dict]) -> list[str]:
    """Fail if multiple carousels use the same system or identical visual signatures."""
    issues = []

    system_ids = [r["system_id"] for r in results]
    duplicates = {s for s in system_ids if system_ids.count(s) > 1 and s != "unknown"}
    if duplicates:
        files_per_system = {}
        for r in results:
            sid = r["system_id"]
            if sid in duplicates:
                files_per_system.setdefault(sid, []).append(r["path"].name)
        for sid, fnames in files_per_system.items():
            issues.append(f"System {sid} used by multiple carousels: {', '.join(fnames)}")

    font_sigs = []
    for r in results:
        html = r["path"].read_text(encoding="utf-8")
        display_m = re.search(r"--font-display:\s*'([^']+)'", html)
        body_m = re.search(r"--font-body:\s*'([^']+)'", html)
        sig = (
            display_m.group(1) if display_m else "?",
            body_m.group(1) if body_m else "?",
        )
        font_sigs.append((sig, r["path"].name))

    seen_sigs: dict = {}
    for sig, fname in font_sigs:
        seen_sigs.setdefault(sig, []).append(fname)
    for sig, fnames in seen_sigs.items():
        if len(fnames) > 1:
            issues.append(
                f"Identical font pair '{sig[0]} / {sig[1]}' in: {', '.join(fnames)}"
            )

    return issues


STATUS_ICON = {PASS: "[OK] ", FAIL: "[!!] ", WARN: "[>>] "}
SEP_THIN = "-" * 60
SEP_THICK = "=" * 60


def print_result(r: dict) -> bool:
    path = r["path"]
    score = r["score"]
    system_id = r["system_id"]
    grade = "EXCELLENT" if score == 100 else "GOOD" if score >= 80 else "WEAK" if score >= 60 else "FAIL"

    print(f"\n{SEP_THIN}")
    print(f"  {path.name}  [{system_id}]")
    print(f"  Visual Richness Score: {score}/100  {grade}")
    print()

    for name, (status, detail) in r["checks"].items():
        icon = STATUS_ICON[status]
        label = name.replace("_", " ").upper()
        print(f"  {icon}{label}")
        print(f"       {detail}")

    has_fail = r["fails"] > 0
    if has_fail:
        print(f"\n  RESULT: FAIL -- {r['fails']} check(s) must be fixed before export")
    elif r["warns"] > 0:
        print(f"\n  RESULT: PASS WITH WARNINGS -- address {r['warns']} warning(s)")
    else:
        print(f"\n  RESULT: PASS -- visual richness confirmed")

    return not has_fail


def main():
    paths = [Path(a) for a in sys.argv[1:] if not a.startswith("--")]
    if not paths:
        print("Usage: py scripts/visual_richness_check.py file1.html [file2.html ...]")
        sys.exit(1)

    missing = [p for p in paths if not p.exists()]
    if missing:
        for p in missing:
            print(f"ERROR: File not found: {p}", file=sys.stderr)
        sys.exit(1)

    results = [score_single(p) for p in paths]
    all_pass = True

    for r in results:
        ok = print_result(r)
        if not ok:
            all_pass = False

    if len(results) > 1:
        print(f"\n{SEP_THICK}")
        print("  CROSS-CAROUSEL DIVERSITY CHECK")
        issues = check_cross_carousel(results)
        if issues:
            for issue in issues:
                print(f"  [!!] {issue}")
            print(f"\n  DIVERSITY: FAIL -- {len(issues)} cross-carousel issue(s)")
            all_pass = False
        else:
            print("  [OK]  All carousels use distinct systems and font pairs")
            print(f"\n  DIVERSITY: PASS")

    print(f"\n{SEP_THICK}\n")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
