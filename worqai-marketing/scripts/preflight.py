#!/usr/bin/env python3
"""
preflight.py — Deterministic pre-flight validator for carousel HTML files.

Usage:
    py scripts/preflight.py production/carousel_nuevo.html
    py scripts/preflight.py production/carousel_nuevo.html --aspect 4:5

Checks:
    1.  Text overflow (heuristic-based for bespoke .sN-* classes)
    2.  VAR_ placeholder cleanup
    3.  File size tier (35-55 KB ideal, 55+ = bloat warning)
    4.  Layout diversity
    5.  Anti-slop pattern detection
    6.  Mock UI presence
    7.  CTA completeness
    8.  html2canvas compatibility (conic-gradient, backdrop-filter)
    9.  Grid divider bug (separate div inside flex/grid)
    10. Decorative density heuristic (absolute position count)
    11. Brand consistency (brand leak + language mix)
    12. Container fit (copy too long for narrow containers)
    13. Opacity floor (readability floor 0.75 — warn only)
    14. Template artifact scan (double-dollar, default tab titles)
    15. Dict literal detection (raw Python dict repr in visible output — FAIL)
    16. Text edge safety (text within 8px of slide edge — warn)
    17. Composition asymmetry (>3 consecutive center-aligned slides — warn)
    18. Body text max-width (body wrappers without width constraint — warn)

Exit codes:
    0 = all checks passed (score >= 90)
    1 = issues found
"""

import argparse
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

SCRIPT_DIR = Path(__file__).parent
DATA_PATH = SCRIPT_DIR / "component_data.json"

ANTI_SLOP_PATTERNS = [
    ("COLORED_LEFT_BORDER", re.compile(r"border-left\s*:\s*\d+px\s+solid\s+[^;]+", re.IGNORECASE)),
    ("PILL_BADGE", re.compile(r"border-radius\s*:\s*999px[^;]*;\s*border\s*:\s*1px\s+solid", re.IGNORECASE)),
    ("DECORATIVE_BG_NUMBER", re.compile(r"deco-num.*opacity\s*:\s*0\.0[0-8]", re.IGNORECASE)),
]

HTML2CANVAS_RISKS = [
    ("conic-gradient", re.compile(r"conic-gradient\s*\(", re.IGNORECASE)),
    ("backdrop-filter", re.compile(r"(?<!-webkit-)backdrop-filter\s*:", re.IGNORECASE)),
]

GRID_DIVIDER_BUG = re.compile(
    r'<div[^>]*class="[^"]*(?:divider|separator)[^"]*"[^>]*>\s*</div>',
    re.IGNORECASE
)

FILE_SIZE_TIERS = [
    (20, "generic", "CRITICAL: Under 20 KB — too generic, rebuild"),
    (35, "good", "PASS: 20-35 KB — good, restrained build"),
    (80, "very_good", "PASS: 35-80 KB — ideal range (v2 SVG sprite adds ~20 KB overhead)"),
    (9999, "bloat", "WARN: 80+ KB — audit for unused CSS or oversized assets"),
]

TEXT_HEURISTICS = {
    "headline": {
        "selectors": ["h1", "h2", ".display", "[class*=headline]", "[class*=title]", "[class*=stat]"],
        "max_chars": 55,
        "max_words": 10,
    },
    "body": {
        "selectors": ["p", ".body", "[class*=txt]", "[class*=text]", "[class*=context]"],
        "max_chars": 140,
        "max_words": 22,
    },
    "label": {
        "selectors": [".label", "[class*=tag]", "[class*=lbl]"],
        "max_chars": 40,
        "max_words": 6,
    },
    "cta_keyword": {
        "selectors": [".keyword-text", "[class*=keyword]"],
        "max_chars": 18,
        "max_words": 2,
    },
}


def load_budgets():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    raw = data.get("text_budgets", {})
    resolved = {}
    for key, val in raw.items():
        if key.startswith("_"):
            continue
        if "inherits" in val:
            parent = raw.get(val["inherits"], {})
            merged = dict(parent)
            merged.update({k: v for k, v in val.items() if k != "inherits"})
            resolved[key] = merged
        else:
            resolved[key] = val
    return resolved


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.tag_stack = []
        self.in_style = False
        self.in_script = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")
        self.tag_stack.append({"tag": tag, "class": cls, "id": attrs_dict.get("id", "")})
        if tag in ("style", "script"):
            setattr(self, f"in_{tag}", True)

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1]["tag"] == tag:
            self.tag_stack.pop()
        if tag in ("style", "script"):
            setattr(self, f"in_{tag}", False)

    def handle_data(self, data):
        if self.in_style or self.in_script:
            return
        stripped = data.strip()
        if stripped:
            current = self.tag_stack[-1] if self.tag_stack else {"tag": "", "class": "", "id": ""}
            self.texts.append({
                "text": stripped,
                "tag": current["tag"],
                "class": current["class"],
                "id": current["id"],
            })


def detect_slides(html):
    """Detect slides by <section class="slide"> or <div class="slide">."""
    # Split on slide tags — avoid matching 'slides' container by using negative lookahead
    pattern = re.compile(r'(<(?:section|div)[^>]*class="[^"]*slide(?!s)[^"]*"[^>]*>)', re.IGNORECASE)
    parts = pattern.split(html)
    slides = []
    current = ""
    for part in parts[1:]:
        if re.search(r'<(section|div)[^>]*class="[^"]*slide(?!s)', part, re.IGNORECASE):
            if current:
                slides.append(current)
            current = part
        else:
            current += part
    if current:
        slides.append(current)
    return slides


def classify_text_element(item):
    """Classify a text element based on tag and class names."""
    tag = item.get("tag", "")
    cls = item.get("class", "")
    cls_lower = cls.lower()
    tag_lower = tag.lower()

    if tag_lower in ("h1", "h2") or "headline" in cls_lower or "display" in cls_lower or "title" in cls_lower or "stat" in cls_lower:
        return "headline"
    if "keyword" in cls_lower:
        return "cta_keyword"
    if "label" in cls_lower or "tag" in cls_lower or "lbl" in cls_lower:
        return "label"
    if tag_lower == "p" or "body" in cls_lower or "txt" in cls_lower or "text" in cls_lower or "context" in cls_lower:
        return "body"
    return None


def check_text_overflow(slide_html, slide_idx, aspect):
    issues = []
    multiplier = {"1:1": 1.0, "4:5": 1.15, "9:16": 1.3}.get(aspect, 1.0)
    extractor = TextExtractor()
    try:
        extractor.feed(slide_html)
    except Exception:
        pass

    for item in extractor.texts:
        text_type = classify_text_element(item)
        if not text_type:
            continue
        rules = TEXT_HEURISTICS[text_type]
        txt = item["text"]
        max_chars = int(rules["max_chars"] * multiplier)
        max_words = int(rules["max_words"] * multiplier)

        if len(txt) > max_chars:
            issues.append(f"  slide-{slide_idx}: [{text_type}] '{txt[:45]}...' = {len(txt)} chars, budget = {max_chars}")
        words = len(txt.split())
        if words > max_words:
            issues.append(f"  slide-{slide_idx}: [{text_type}] '{txt[:45]}...' = {words} words, budget = {max_words}")

    return issues


def check_var_placeholders(html):
    issues = []
    matches = re.findall(r"VAR_\w+", html)
    for m in set(matches):
        for i, line in enumerate(html.splitlines(), 1):
            if m in line:
                issues.append(f"  Line {i}: Unresolved placeholder [{m}]")
                break
    return issues


def check_file_size(filepath):
    kb = filepath.stat().st_size / 1024
    for limit, tier, msg in FILE_SIZE_TIERS:
        if kb < limit:
            return kb, tier, msg
    return kb, "elite", "PASS: 55+ KB -- elite tier"


def check_layout_diversity(html):
    issues = []
    slides = detect_slides(html)
    sigs = []
    for s in slides:
        # Extract class names from the slide
        classes = re.findall(r'class="([^"]*)"', s)
        sig = " ".join(sorted(set(" ".join(classes).split())))
        sigs.append(sig)
    for i in range(len(sigs) - 1):
        if sigs[i] == sigs[i + 1]:
            issues.append(f"  slide-{i+1} and slide-{i+2}: Identical structure (layout diversity violation)")
    return issues


DECORATIVE_SELECTOR_EXCEPTIONS = re.compile(
    r"\.(deco-corner|deco-ornament|deco-stamp|deco-watermark|"
    r"chrome-badge-stamp|chrome-vertical-counter|chrome-header-bar|"
    r"stamp-label|stamp-value|term-bar|term-dot|brand-corner|"
    r"sub-fact-bubble|"
    # Shell CSS for inactive layouts — border-left here is layout structure,
    # not a content-card Canva pattern. No fix possible without CSS tree-shaking.
    r"comp-card|comp-col|faq-item|sbs-right|sbs-left|mcs-card|"
    r"edit-col|edc-col|wfall-item|wfall-num)",
    re.IGNORECASE,
)


def check_anti_slop(html):
    issues = []
    lines = html.splitlines()
    for name, pattern in ANTI_SLOP_PATTERNS:
        for i, line in enumerate(lines, 1):
            # Exclude pseudo-element rules — border-left in ::before/::after is decorative
            # (e.g. file-icon corner fold), not a content card left border
            if name == "COLORED_LEFT_BORDER" and ("::before" in line or "::after" in line):
                continue
            # Exclude CSS rules that style known decorative elements. The render
            # engine uses border-left/right on L-bracket corners and ornament
            # frames by design — those are not content-card "Canva" borders.
            if name == "COLORED_LEFT_BORDER" and DECORATIVE_SELECTOR_EXCEPTIONS.search(line):
                continue
            if pattern.search(line):
                issues.append(f"  Line {i}: ANTI-SLOP [{name}] -- {line.strip()[:80]}")
    return issues


def check_mock_ui(html):
    mock_patterns = [
        "terminal-panel", "mock-cv", "mock-app", "mock-form", "mock-checklist",
        "mock-display", "mock-metric", "message-chat", "message-email",
        "ecom-product", "ecom-pricing", "icon-avatar", "code-syntax", "cmd", ">$ "
    ]
    found = any(p in html for p in mock_patterns)
    if not found:
        return ["  No mock UI detected (terminal, CV mock, checklist, etc.)"]
    return []


def check_cta(html):
    issues = []
    slides = detect_slides(html)
    if not slides:
        return ["  Could not detect slides for CTA check"]
    last = slides[-1]
    # diagnostic/editorial CTA variants render keyword without keyword-box class but with "Comenta la palabra"
    has_keyword = bool(re.search(r'keyword-(?:box|text)', last, re.IGNORECASE)) or \
                  bool(re.search(r'Comenta la palabra', last, re.IGNORECASE))
    has_question = bool(re.search(r'[\?\xbf]', last))
    reward_patterns = [
        "checklist", "plantilla", "guion", "guión", "protocolo",
        "diagnóstico", "diagnostico", "reporte", "auditoria", "audit",
        "gratis", "sin costo", "sin cargo", "free",
    ]
    has_reward = any(p in last.lower() for p in reward_patterns)
    if not has_keyword:
        issues.append("  Last slide missing keyword box (CTA incompleto)")
    if not has_question:
        issues.append("  Last slide missing question (CTA incompleto)")
    if not has_reward:
        issues.append("  Last slide missing specific deliverable/reward (CTA incompleto)")
    return issues


def check_html2canvas_safe(html):
    issues = []
    for name, pattern in HTML2CANVAS_RISKS:
        if name == "conic-gradient":
            # Only flag if the geo-conic-rays layer is actually activated in HTML body.
            # The shell CSS always defines the class, but it's only a risk when the div exists.
            if '<div class="geo-conic-rays"' not in html:
                continue
        if name == "backdrop-filter":
            # If -webkit-backdrop-filter is present anywhere in the file the rule is
            # properly prefixed — skip line-level false positives from minified CSS.
            if "-webkit-backdrop-filter" in html:
                continue
        for i, line in enumerate(html.splitlines(), 1):
            if pattern.search(line):
                issues.append(f"  Line {i}: html2canvas RISK [{name}] — {line.strip()[:80]}")
    return issues


def check_grid_dividers(html):
    issues = []
    for match in GRID_DIVIDER_BUG.finditer(html):
        start = max(0, match.start() - 200)
        snippet = html[start:match.start()]
        line_num = snippet.count('\n') + 1
        issues.append(f"  Line ~{line_num}: Separate divider div inside flex/grid — use border-right instead")
    return issues


# Class-based copy budgets for narrow containers. Word counts derived from
# observed visual failures (cramped boxes wrapping to 8+ lines). FAIL threshold
# is "this will visibly clip"; WARN is "this will look tight".
CONTAINER_BUDGETS = {
    "step-desc":   {"warn": 11, "fail": 14, "container": "step-flow description"},
    "chk-title":   {"warn": 10, "fail": 13, "container": "checklist item"},
    "chk-desc":    {"warn": 14, "fail": 18, "container": "checklist description"},
    "tip-blk-text":{"warn": 14, "fail": 18, "container": "tip-block fix text"},
}


# ── v2: Visual primitive checks ────────────────────────────────────────────────
# Per Kenneth's Q5 decision: soft warnings only, never blocks export.

V2_DEPRECATED = [
    {
        "name": "blob-bg ellipse",
        "pattern": re.compile(r'<div\s+class="[^"]*\bblob-bg\b[^"]*"', re.IGNORECASE),
        "suggest": "Replace with svg-blob-tr / svg-blob-bl / svg-blob-center for real organic shape.",
    },
    {
        "name": "✦✧✦ unicode ornament",
        "pattern": re.compile(r'<div\s+class="[^"]*\bdeco-ornament\b[^"]*"', re.IGNORECASE),
        "suggest": "Replace with svg-starburst-spark / svg-starburst-burst / svg-starburst-mark.",
    },
    {
        "name": "CSS gradient-text (background-clip:text)",
        # Require trailing ; or whitespace+} to skip doc comments and body text.
        "pattern": re.compile(r"background-clip\s*:\s*text\s*[;}]", re.IGNORECASE),
        "suggest": "BROKEN in html2canvas. Use text_treatment: 'gradient' in spec (renders via SVG instead).",
    },
]

V2_PRIMITIVE_CLASSES = [
    ("svg-blob", "SVG organic blobs"),
    ("svg-starburst", "SVG starbursts"),
    ("txt-gradient", "SVG gradient text"),
    ("txt-glow", "neon-glow text"),
    ("txt-stroke", "outlined text"),
    ("shadow-md", "drop-shadow filters"),
    ("shadow-sm", "drop-shadow filters"),
    ("shadow-lg", "drop-shadow filters"),
]


def check_v2_primitives(html):
    """v2 visual primitives audit. Soft warnings + positive usage notes.

    Returns (deprecations, used_primitives) — neither blocks export.
    Per Q5 decision: encouragement, not enforcement.
    """
    deprecations = []
    for entry in V2_DEPRECATED:
        if entry["pattern"].search(html):
            deprecations.append(f"  {entry['name']} detected — {entry['suggest']}")

    used = []
    seen = set()
    for css_class, label in V2_PRIMITIVE_CLASSES:
        if css_class in seen:
            continue
        if f'class="{css_class}' in html or f'"{css_class} ' in html or f' {css_class}"' in html \
           or f' {css_class} ' in html or f'class="{css_class}"' in html:
            used.append(label)
            seen.add(css_class)

    icon_uses = len(re.findall(r'<use\s+href="#icon-', html))
    if icon_uses:
        used.append(f"{icon_uses} SVG icon reference(s)")

    return deprecations, used


def check_container_fit(html):
    """Word-count check for layouts where text overflows the visual container.

    Targets narrow boxes (step-flow descriptions, checklist items, tip blocks)
    where copy longer than ~10 words wraps to 6-8 lines and looks cramped.
    Returns ((fails, warns)) — fails block export, warns are advisory.
    """
    fails, warns = [], []
    for cls, budget in CONTAINER_BUDGETS.items():
        # Match <div class="step-desc">...</div> or class="step-desc foo"
        pattern = re.compile(
            rf'<[^>]*class="[^"]*\b{re.escape(cls)}\b[^"]*"[^>]*>([^<]+)</',
            re.IGNORECASE,
        )
        for m in pattern.finditer(html):
            text = m.group(1).strip()
            words = len(text.split())
            if words >= budget["fail"]:
                fails.append(
                    f"  .{cls} ({budget['container']}): '{text[:50]}...' = {words} words "
                    f"(fail >= {budget['fail']}). Will overflow the container."
                )
            elif words >= budget["warn"]:
                warns.append(
                    f"  .{cls} ({budget['container']}): '{text[:50]}...' = {words} words "
                    f"(warn >= {budget['warn']}). Tight fit — consider shorter copy."
                )
    return fails, warns


def _extract_brand(html):
    m = re.search(r'<div\s+class="brand"[^>]*>\s*([^<\s][^<]*?)\s*</div>', html)
    return m.group(1).strip() if m else ""


def _extract_lang(html):
    m = re.search(r'<html[^>]*\blang="([^"]+)"', html, re.IGNORECASE)
    return m.group(1).strip().lower() if m else ""


# English words/phrases that signal a leak in Spanish carousels.
# Standalone-word match only — won't trip on substrings or brand names.
EN_LEAK_WORDS_IN_ES = [
    "free", "follow-up", "follow up", "click here", "swipe up",
    "learn more", "sign up", "get started", "join now",
    "template", "script", "download", "network", "tips",
    "feedback", "update", "upgrade", "dashboard", "profile",
]

TEMPLATE_ARTIFACTS = [
    ("double-dollar", re.compile(r"\$\$\s"), "Double dollar sign in terminal — use single $"),
    ("ats-scanner-tab", re.compile(r"ats-scanner\.sh"), "Default tab title 'ats-scanner.sh' not overridden"),
]

LOW_OPACITY_PATTERN = re.compile(
    r"opacity\s*:\s*0\.[0-6]\d*(?!\s*[,)])",  # not inside rgba() — no comma or paren after
    re.IGNORECASE,
)
LOW_OPACITY_EXEMPTIONS = re.compile(
    r"(grain|geo-|glow|orb|::before|::after|overlay|texture|noise|blob|decorative|bg-|background)",
    re.IGNORECASE,
)


def check_brand_consistency(html):
    """Catch brand-name leaks and obvious language mixes in rendered HTML.

    Heuristics:
      1. If meta brand is NOT @worqai but the HTML still says "WORQAI" outside
         of script/style, that's a stamp/badge leaking from the WorqAI default.
      2. If <html lang> starts with "es" but copy contains standalone English
         CTA words ("FREE", "follow-up", etc.), flag as a language mix.
    Returns a list of issue strings (empty if no problems).
    """
    issues = []
    brand = _extract_brand(html)
    lang = _extract_lang(html)
    brand_handle = brand.lstrip("@").lower()

    # Strip <script> and <style> blocks so we only scan rendered content.
    visible = re.sub(r"<(script|style)[\s\S]*?</\1>", "", html, flags=re.IGNORECASE)

    # Leak 1: WorqAI artifacts in non-WorqAI carousels.
    if brand_handle and brand_handle != "worqai":
        for hit in re.finditer(r"\b(WORQAI|WorqAI|worqai)\b", visible):
            # Allow it if the term appears inside a class attribute (e.g. CSS hooks)
            window = visible[max(0, hit.start() - 30): hit.start()]
            if 'class="' in window and '"' not in window.split('class="')[-1]:
                continue
            issues.append(
                f"  Brand leak: '{hit.group(0)}' appears in HTML but meta.brand = '{brand}'. "
                f"Likely a stamp/header decorative defaulting to WorqAI."
            )
            break  # one hit is enough — don't spam

    # Leak 2: English CTAs inside Spanish carousels.
    if lang.startswith("es"):
        text_only = re.sub(r"<[^>]+>", " ", visible)
        for word in EN_LEAK_WORDS_IN_ES:
            pattern = re.compile(rf"(?<!\w){re.escape(word)}(?!\w)", re.IGNORECASE)
            if pattern.search(text_only):
                issues.append(
                    f"  Language mix: English '{word}' found in Spanish (lang='{lang}') carousel — translate to Spanish."
                )

    return issues


def check_opacity_floor(html):
    """Warn when custom CSS sets text-element opacity below the readability floor (0.75).
    Skips known decorative contexts (grain, geo layers, overlays, blobs).
    """
    warnings = []
    style_blocks = re.findall(r"<style[^>]*>([\s\S]*?)</style>", html, re.IGNORECASE)
    for block in style_blocks:
        for i, line in enumerate(block.splitlines(), 1):
            if not LOW_OPACITY_PATTERN.search(line):
                continue
            if LOW_OPACITY_EXEMPTIONS.search(line):
                continue
            match = LOW_OPACITY_PATTERN.search(line)
            if match:
                warnings.append(
                    f"  Opacity floor WARN: '{line.strip()[:80]}' "
                    f"-- body text needs >=0.75, labels >=0.85"
                )
    return warnings


def check_template_artifacts(html):
    """Catch specific regression artifacts: default tab titles, double-dollar, etc."""
    issues = []
    visible = re.sub(r"<(script|style)[\s\S]*?</\1>", "", html, flags=re.IGNORECASE)
    for name, pattern, msg in TEMPLATE_ARTIFACTS:
        if pattern.search(visible):
            issues.append(f"  Template artifact [{name}]: {msg}")
    return issues


DICT_LITERAL_PATTERN = re.compile(r"\{['\"][\w_]+['\"]\s*:", re.IGNORECASE)
JINJA_UNRENDERED_PATTERN = re.compile(r"\{\{|\{%-?")
EDGE_TEXT_INLINE_PATTERN = re.compile(
    r'<(?:div|span|p|h[1-6])[^>]*\bstyle="[^"]*(?:left|right|top|bottom)\s*:\s*([0-7](?:\.\d+)?px|0(?:px)?)\b[^"]*"[^>]*>([^<]{3,})',
    re.IGNORECASE,
)
BODY_WRAP_CLASSES = [
    "hook-body", "ba-sub", "tip-blk-text", "stat-context",
    "hook-wrap", "ba-wrap", "tip-wrap", "slide-body",
]


def check_dict_artifacts(html):
    """Fail if raw Python dict literals or unrendered Jinja2 syntax appear in visible output."""
    issues = []
    visible = re.sub(r"<(script|style)[\s\S]*?</\1>", "", html, flags=re.IGNORECASE)
    text_only = re.sub(r"<[^>]+>", " ", visible)

    hit = DICT_LITERAL_PATTERN.search(text_only)
    if hit:
        snippet = text_only[max(0, hit.start() - 10):hit.start() + 40].strip()
        issues.append(
            f"  Dict literal in output: '{snippet[:60]}' — "
            "item loop missing '{% if item is mapping %}' guard"
        )
    hit = JINJA_UNRENDERED_PATTERN.search(text_only)
    if hit:
        snippet = text_only[max(0, hit.start() - 10):hit.start() + 40].strip()
        issues.append(
            f"  Unrendered Jinja2 tag: '{snippet[:60]}' — template was not fully rendered"
        )
    return issues


def check_text_edge_safety(html):
    """Warn when text elements are positioned within 8px of a slide edge (inline style)."""
    warnings = []
    for hit in EDGE_TEXT_INLINE_PATTERN.finditer(html):
        offset_val = hit.group(1)
        text_preview = hit.group(2)[:40].strip()
        warnings.append(
            f"  Edge safety WARN: text '{text_preview}' at offset {offset_val} "
            "— may clip under overflow:hidden"
        )
        if len(warnings) >= 4:
            break
    return warnings


def check_composition_asymmetry(slides):
    """Warn when more than 3 consecutive slides are all center-aligned."""
    warnings = []
    run = 0
    run_start = 0
    for i, slide in enumerate(slides, 1):
        is_center = bool(re.search(r"text-align\s*:\s*center", slide, re.IGNORECASE))
        if is_center:
            if run == 0:
                run_start = i
            run += 1
        else:
            if run > 3:
                warnings.append(
                    f"  Composition: slides {run_start}–{run_start + run - 1} "
                    f"are all center-aligned ({run} in a row). "
                    "Add a left-aligned layout to break rhythm."
                )
            run = 0
    if run > 3:
        warnings.append(
            f"  Composition: slides {run_start}–{run_start + run - 1} "
            f"are all center-aligned ({run} in a row). "
            "Add a left-aligned layout to break rhythm."
        )
    return warnings


def check_body_text_width(html):
    """Warn when body text CSS rules have no max-width / width constraint."""
    warnings = []
    style_blocks = re.findall(r"<style[^>]*>([\s\S]*?)</style>", html, re.IGNORECASE)
    all_css = "\n".join(style_blocks)
    for cls in BODY_WRAP_CLASSES:
        if f".{cls}" not in all_css:
            continue
        rule_pattern = re.compile(
            rf"\.{re.escape(cls)}\s*\{{([^}}]*)\}}", re.IGNORECASE
        )
        for m in rule_pattern.finditer(all_css):
            rule_body = m.group(1)
            if "max-width" not in rule_body and "width" not in rule_body:
                warnings.append(
                    f"  Body width WARN: .{cls} has no max-width — "
                    "long copy may stretch full slide width on wider viewports"
                )
                break
    return warnings


# ── v3: Visual collision + repetition checks ──────────────────────────────────

BADGE_ZONE_RIGHT = 150  # px clearance needed from right edge
BADGE_ZONE_TOP = 140    # px clearance needed from top edge

HEADLINE_CLASSES = [
    "hook-display", "stat-num", "poster-display", "term-headline",
    "lnum-headline", "chk-headline", "cta-question", "mn-headline",
    "diags-headline", "asym-headline", "tos-headline", "stype-line-1",
    "cman-headline", "sbs-headline", "fwf-quote", "cq-quote",
    "wfl-headline", "at-headline", "mcs-headline", "ec-headline",
    "badgeg-headline", "tip-headline", "ba-headline", "proof-headline",
    "warn-headline", "quote-text", "qauth-text", "fbt-display",
    "mc-headline", "sc-headline", "pg-caption", "tc-word",
]


def check_badge_collision(slides):
    """Detect when chrome-badge-stamp or deco-stamp overlaps with headline text.

    The stamp sits at absolute top-right (104px square). Headlines that are
    wide, right-aligned, or centered can collide with this zone.
    """
    issues = []
    for i, slide in enumerate(slides, 1):
        has_badge = bool(
            re.search(r'class="[^"]*chrome-badge-stamp[^"]*"', slide, re.IGNORECASE)
        )
        has_stamp = bool(
            re.search(r'class="[^"]*deco-stamp[^"]*"', slide, re.IGNORECASE)
        )
        if not has_badge and not has_stamp:
            continue

        # Look for headline elements in this slide
        has_headline = False
        for cls in HEADLINE_CLASSES:
            if f'"{cls}"' in slide or f'"{cls} ' in slide or f' {cls}"' in slide or f' {cls} ' in slide:
                has_headline = True
                break

        # Also flag right-aligned text blocks that could run into the badge zone
        has_right_align = bool(
            re.search(r'text-align\s*:\s*right', slide, re.IGNORECASE)
        )

        if has_badge and (has_headline or has_right_align):
            issues.append(
                f"  slide-{i}: chrome-badge-stamp (top-right 104px) may collide with "
                f"headline or right-aligned text — add `silence: true` to remove decoratives, "
                f"or pick a narrower headline, or move badge to a different slide."
            )
        if has_stamp and has_right_align:
            issues.append(
                f"  slide-{i}: deco-stamp (bottom-right) may overlap right-aligned text."
            )
    return issues


def check_shape_diversity(html):
    """Cap per-shape usage so no single shape dominates the carousel."""
    issues = []
    shape_patterns = {
        "svg-blob-tr": r'class="[^"]*\bsvg-blob-tr\b[^"]*"',
        "svg-blob-bl": r'class="[^"]*\bsvg-blob-bl\b[^"]*"',
        "svg-blob-center": r'class="[^"]*\bsvg-blob-center\b[^"]*"',
        "svg-blob-asymmetric": r'class="[^"]*\bsvg-blob-asymmetric\b[^"]*"',
        "svg-blob-scattered": r'class="[^"]*\bsvg-blob-scattered\b[^"]*"',
        "glow-orb": r'class="[^"]*\bglow-orb\b[^"]*"',
        "blob-bg": r'class="[^"]*\bblob-bg\b[^"]*"',
        "vol-light": r'class="[^"]*\bvol-light\b[^"]*"',
        "deco-corner-tl": r'class="[^"]*\bdeco-corner-tl\b[^"]*"',
        "deco-corner-br": r'class="[^"]*\bdeco-corner-br\b[^"]*"',
        "deco-starburst": r'class="[^"]*\bdeco-starburst\b[^"]*"',
        "deco-ornament": r'class="[^"]*\bdeco-ornament\b[^"]*"',
        "deco-watermark": r'class="[^"]*\bdeco-watermark\b[^"]*"',
    }
    for shape_name, pattern in shape_patterns.items():
        count = len(re.findall(pattern, html, re.IGNORECASE))
        if count > 4:
            issues.append(
                f"  {shape_name} appears on {count} slides — max 4 per carousel. "
                f"Use different shapes for visual variety."
            )
    return issues


def check_decorative_repetition(slides):
    """Warn when the same decorative element appears on >2 consecutive slides."""
    issues = []
    decorative_classes = [
        "deco-corner-tl", "deco-corner-br", "deco-ornament",
        "deco-starburst", "deco-watermark", "deco-stamp",
        "chrome-badge-stamp", "chrome-vertical-counter", "chrome-header-bar",
    ]
    for dec_cls in decorative_classes:
        run = 0
        max_run = 0
        for slide in slides:
            if re.search(rf'class="[^"]*{re.escape(dec_cls)}[^"]*"', slide, re.IGNORECASE):
                run += 1
                max_run = max(max_run, run)
            else:
                run = 0
        if max_run > 2:
            issues.append(
                f"  {dec_cls} on {max_run} consecutive slides — max 2. "
                f"Break the rhythm with a silence beat or different decorative."
            )
    return issues


# Layouts that visually DEMONSTRATE rather than just describe in text.
DEMONSTRATION_LAYOUTS = {
    "slide-input-output", "slide-waffle-chart", "slide-before-after", "slide-before-after-stacked",
    "slide-data-viz-donut", "slide-progress-bars", "slide-myth-vs-fact",
    "slide-data-viz-donut", "slide-progress-bars", "slide-myth-vs-fact",
    "slide-comparison-table",
}


def check_demonstration_layout(slides):
    """FAIL if no slide uses a demonstration layout (show, don't tell)."""
    issues = []
    found = 0
    # Map layout IDs to their wrapper class fragments in rendered HTML
    DEMO_WRAPPERS = {
        "slide-input-output": ["io-wrap", "io-panel"],
        "slide-waffle-chart": ["waffle-wrap", "waffle-grid"],
        "slide-before-after": ["ba-wrap", "ba-cols"],
        "slide-before-after-stacked": ["bas-wrap", "bas-panels"],
        "slide-data-viz-donut": ["donut-wrap", "donut-chart"],
        "slide-progress-bars": ["pbar-wrap", "pbar-track"],
        "slide-myth-vs-fact": ["mvf-wrap", "mvf-row"],
        "slide-comparison-table": ["comp-table-wrap", "comp-cards"],
    }
    for i, slide in enumerate(slides, 1):
        for layout_id, wrappers in DEMO_WRAPPERS.items():
            if any(w in slide for w in wrappers):
                found += 1
                break

    if found == 0:
        issues.append(
            "  Zero demonstration layouts found. At least one slide must SHOW the problem "
            "visually (input-output, waffle-chart, before-after, data-viz-donut, progress-bars, "
            "myth-vs-fact, comparison-table). Text-only slides are not enough."
        )
    return issues


def check_s1_hook_context(slides):
    """WARN if slide 1 lacks any domain-specific vocabulary (CV, ATS, recruiting context).

    WorqAI carousels are about job applications. Slide 1 must anchor the hook to
    the domain — a headline that could belong to any SaaS product is too generic.
    Formula expected: [Object] + [Problem] + [Mechanism].
    """
    import re as _re
    if not slides:
        return []

    s1 = slides[0]
    # Strip HTML tags, decode common entities, lowercase
    text = _re.sub(r'<[^>]+>', ' ', s1)
    text = text.replace('&amp;', '&').replace('&#39;', "'").replace('&nbsp;', ' ')
    text = text.lower()

    CONTEXT_KEYWORDS = [
        'cv', 'ats', 'currículum', 'curriculum', 'hoja de vida', 'perfil',
        'linkedin', 'reclutador', 'reclutadora', 'filtro', 'entrevista',
        'empleo', 'trabajo', 'resume', 'aplicacion', 'aplicación',
        'postulacion', 'postulación', 'oferta', 'vacante',
    ]

    found = [kw for kw in CONTEXT_KEYWORDS if kw in text]
    if not found:
        return [
            "  Slide 1 contains no domain context keyword (CV, ATS, currículum, "
            "LinkedIn, reclutador, filtro, entrevista, empleo…). "
            "The hook reads as generic — anchor it to the job-application domain. "
            "Expected formula: [Object] + [Problem] + [Mechanism]."
        ]
    return []


# ── Phase 3: AI-background pipeline gates ─────────────────────────────────────

# Kit IDs that must never appear in a production carousel.
QUARANTINED_BG_KITS = {
    "digital-glass-full": (
        "irregular extraction grid — each panel contains 2 sub-panels, "
        "producing a visible vertical split. Re-generate the source image before use."
    ),
    "pastel-waves": (
        "extremely light/pastel imagery that fights dark system text even after trimming. "
        "Only safe on light systems (s25/s26/s48). Re-generate or restrict to light systems."
    ),
}


def _extract_ai_bg_kits(html: str) -> list:
    """Return list of AI-background kit IDs referenced in the rendered HTML.

    Looks for <img> src paths inside brand/generated-bg/. The kit ID is the
    folder name immediately after generated-bg/.

    Example src: ../brand/generated-bg/glass-panel-full/panel_01/s01.png
    → kit ID: glass-panel-full
    """
    import re as _re
    pattern = r'brand/generated-bg/([^/"\s]+)/'
    return list(set(_re.findall(pattern, html)))


def check_ai_bg_quarantine(html: str) -> list:
    """FAIL if any quarantined AI-background kit is referenced in the carousel.

    Quarantined kits have structural flaws (bad panels, unusable imagery on dark systems)
    that make them unsuitable for production without remediation.
    """
    issues = []
    used_kits = _extract_ai_bg_kits(html)
    for kit_id, reason in QUARANTINED_BG_KITS.items():
        if kit_id in used_kits:
            issues.append(f"  QUARANTINED background kit '{kit_id}' used: {reason}")
    return issues


def check_ai_bg_density_coverage(slides: list, html: str) -> list:
    """FAIL if carousel uses AI backgrounds but any slide is missing the data-density attribute.

    Every slide in an AI-background carousel must declare a density level so the
    scrim system can protect text legibility. Omitting it defaults to medium scrim
    which is unacceptable for hook/stat/CTA slides.
    """
    import re as _re
    # Only runs if this is an AI-background carousel
    if "geo-ai-bg-overlay" not in html and "geo-ai-bg" not in html:
        return []

    issues = []
    for i, slide in enumerate(slides, 1):
        # Look for the slide div opening tag — must have data-density
        first_div = _re.match(r'<div[^>]*>', slide)
        if first_div:
            tag = first_div.group(0)
            if 'data-density' not in tag:
                issues.append(
                    f"  Slide {i} uses an AI background but has no 'density' field in the spec. "
                    f"Add \"density\": \"heavy\" (hook/stat/CTA) or \"demo\" (terminal/IO) or \"cta\" (CTA slide)."
                )
    return issues


def check_ai_bg_card_transparency(html: str) -> list:
    """WARN if cards on an AI-background carousel use ultra-transparent backgrounds (< 0.07).

    Only scans inline style attributes (not shell CSS), since shell geo layers
    intentionally use low opacity values that are not card backgrounds.
    Cards at rgba(255,255,255,0.06) or lower are effectively invisible on any dark background.
    Minimum for dark systems: rgba(255,255,255,0.07).
    """
    import re as _re
    if "geo-ai-bg-overlay" not in html and "geo-ai-bg" not in html:
        return []

    # Extract inline style attributes only (not embedded <style> blocks)
    inline_styles = " ".join(_re.findall(r'style="([^"]*)"', html))
    if not inline_styles:
        return []

    # Match rgba with alpha < 0.07 in those inline styles
    pattern = r'rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*(0\.0[0-6][0-9]*)\s*\)'
    matches = _re.findall(pattern, inline_styles)
    if not matches:
        return []
    unique_vals = list(set(matches))
    return [
        f"  Ultra-transparent card inline style detected: rgba(255,255,255,{v}) is invisible on AI backgrounds. "
        f"Minimum is 0.07 on dark systems. Check card/panel inline background properties."
        for v in unique_vals
    ]


# ── Phase 3 continued: Panel quality gates ────────────────────────────────────

def _get_referenced_panels(html: str) -> list[tuple[str, str]]:
    """Return list of (kit_id, abs_path) for every AI-bg panel PNG in the carousel.

    Looks for <img src="../brand/generated-bg/..."> patterns.
    Returns empty list when PIL is unavailable or no AI-bg panels are used.
    """
    try:
        from PIL import Image as _Image  # noqa
    except ImportError:
        return []

    import re as _re
    ROOT = Path(__file__).parent.parent
    pattern = r'src="(\.\./brand/generated-bg/[^"]+\.png)"'
    results = []
    for m in _re.finditer(pattern, html):
        rel = m.group(1).lstrip("../")
        abs_path = ROOT / rel
        kit_id = rel.split("/")[2] if len(rel.split("/")) > 2 else "unknown"
        results.append((kit_id, str(abs_path)))
    return results


def check_ai_bg_panel_dimensions(html: str) -> list:
    """FAIL if any referenced AI-bg panel PNG is not exactly 1080×1080.

    Non-square panels (e.g. 1080×540 strips extracted to wrong size)
    will visually stretch or show only partial content on a square slide.
    Requires Pillow — silently skips if not installed.
    """
    try:
        from PIL import Image as _Image
    except ImportError:
        return []

    issues = []
    seen = set()
    for kit_id, abs_path in _get_referenced_panels(html):
        if abs_path in seen:
            continue
        seen.add(abs_path)
        try:
            img = _Image.open(abs_path)
            w, h = img.size
            img.close()
            if w != 1080 or h != 1080:
                issues.append(
                    f"  Panel dimension FAIL: {abs_path} is {w}×{h} — expected 1080×1080. "
                    f"Re-extract with panel_extractor.py to fix."
                )
        except Exception as e:
            issues.append(f"  Panel unreadable: {abs_path} — {e}")
    return issues


def check_ai_bg_edge_brightness(html: str) -> list:
    """WARN if any AI-bg panel has near-white edges (mean > 220) indicating baked-in borders.

    White/light edges remain visible even with object-fit:cover and will bleed as
    bright strips at panel boundaries. Fix with: panel_extractor.py --fix-kit <kit> --trim-gutters 5
    Requires Pillow — silently skips if not installed.
    """
    try:
        from PIL import Image as _Image
    except ImportError:
        return []

    EDGE_PX = 10
    BRIGHT_THRESHOLD = 220
    warns = []
    seen = set()
    for kit_id, abs_path in _get_referenced_panels(html):
        if abs_path in seen:
            continue
        seen.add(abs_path)
        try:
            img = _Image.open(abs_path).convert("RGB")
            w, h = img.size
            edges = [
                img.crop((0, 0, w, EDGE_PX)),           # top
                img.crop((0, h - EDGE_PX, w, h)),        # bottom
                img.crop((0, 0, EDGE_PX, h)),            # left
                img.crop((w - EDGE_PX, 0, w, h)),        # right
            ]
            for band_name, band in zip(["top", "bottom", "left", "right"], edges):
                pixels = list(band.getdata())
                avg = sum(sum(p) / 3 for p in pixels) / len(pixels)
                if avg > BRIGHT_THRESHOLD:
                    panel_name = "/".join(abs_path.replace("\\", "/").split("/")[-3:])
                    warns.append(
                        f"  Edge brightness WARN [{band_name}]: {panel_name} avg={avg:.0f} > {BRIGHT_THRESHOLD}. "
                        f"White/light border detected — run: py scripts/panel_extractor.py "
                        f"--fix-kit brand/generated-bg/{kit_id} --trim-gutters 5"
                    )
                    break  # one warning per panel is enough
            img.close()
        except Exception:
            pass
    return warns


def check_slide_content_minimum(slides: list) -> list:
    """WARN if any slide has fewer than 4 visible words total.

    Single-word slides (e.g., 'titular típico', '1 página') render as broken UI —
    the slide looks unfinished or like a template placeholder was left unfilled.
    Minimum viable slide: headline (≥3 words) + any secondary text.
    """
    import re as _re
    warns = []
    for i, slide in enumerate(slides, 1):
        # Strip style/script blocks and HTML tags, decode basic entities
        visible = _re.sub(r"<(style|script)[\s\S]*?</\1>", "", slide, flags=_re.IGNORECASE)
        visible = _re.sub(r"<[^>]+>", " ", visible)
        visible = visible.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'")
        words = [w for w in _re.split(r"\s+", visible.strip()) if len(w) > 1]
        if len(words) < 4:
            preview = " ".join(words[:8]) or "(empty)"
            warns.append(
                f"  Slide {i} has only {len(words)} visible word(s): '{preview}' — "
                f"add context. Minimum: headline ≥3 words + at least one supporting text element."
            )
    return warns


def main():
    parser = argparse.ArgumentParser(description="Carousel pre-flight validator")
    parser.add_argument("html_file", help="Path to generated carousel HTML")
    parser.add_argument("--aspect", default="1:1", choices=["1:1", "4:5", "9:16"],
                        help="Aspect ratio for text budget multiplier")
    args = parser.parse_args()

    filepath = Path(args.html_file)
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    html = filepath.read_text(encoding="utf-8")
    slides = detect_slides(html)

    all_issues = []
    checks_passed = 0
    checks_total = 29
    bloat_penalty = 0

    print(f"\n{'='*60}")
    print(f"PREFLIGHT: {filepath.name}")
    print(f"Slides detected: {len(slides)}")
    print(f"Aspect: {args.aspect}")
    print(f"{'='*60}\n")

    # 1. Text Overflow
    print("[1/29] Text Overflow Check")
    text_issues = []
    for i, slide in enumerate(slides, 1):
        issues = check_text_overflow(slide, i, args.aspect)
        text_issues.extend(issues)
    if text_issues:
        print("FAIL -- issues found:")
        for issue in text_issues:
            print(issue)
        all_issues.extend(text_issues)
    else:
        print("PASS -- all text within budget")
        checks_passed += 1

    # 2. VAR_ placeholders
    print("\n[2/29] VAR_ Placeholder Check")
    var_issues = check_var_placeholders(html)
    if var_issues:
        print("FAIL -- unresolved placeholders:")
        for issue in var_issues:
            print(issue)
        all_issues.extend(var_issues)
    else:
        print("PASS -- no unresolved VAR_ placeholders")
        checks_passed += 1

    # 3. File Size
    print("\n[3/29] File Size Check")
    kb, tier, msg = check_file_size(filepath)
    print(f"{msg} ({kb:.1f} KB)")
    if tier == "generic":
        all_issues.append(f"File size {kb:.1f} KB is generic tier")
    elif tier == "bloat":
        print("NOTE -- over 80 KB. Audit for unused CSS selectors or oversized assets.")
        checks_passed += 1  # size is informational only — no score penalty
    else:
        checks_passed += 1

    # 4. Layout Diversity
    print("\n[4/29] Layout Diversity Check")
    div_issues = check_layout_diversity(html)
    if div_issues:
        print("FAIL -- layout diversity issues:")
        for issue in div_issues:
            print(issue)
        all_issues.extend(div_issues)
    else:
        print("PASS -- layouts are diverse")
        checks_passed += 1

    # 5. Anti-Slop
    print("\n[5/29] Anti-Slop Check")
    slop_issues = check_anti_slop(html)
    if slop_issues:
        print("FAIL -- anti-slop violations:")
        for issue in slop_issues:
            print(issue)
        all_issues.extend(slop_issues)
    else:
        print("PASS -- no anti-slop patterns detected")
        checks_passed += 1

    # 6. Mock UI
    print("\n[6/29] Mock UI Check")
    mock_issues = check_mock_ui(html)
    if mock_issues:
        print("FAIL -- mock UI missing:")
        for issue in mock_issues:
            print(issue)
        all_issues.extend(mock_issues)
    else:
        print("PASS -- mock UI present")
        checks_passed += 1

    # 7. CTA Completeness
    print("\n[7/29] CTA Completeness Check")
    cta_issues = check_cta(html)
    if cta_issues:
        print("FAIL -- CTA incomplete:")
        for issue in cta_issues:
            print(issue)
        all_issues.extend(cta_issues)
    else:
        print("PASS -- CTA complete (question + keyword + reward)")
        checks_passed += 1

    # 8. html2canvas Compatibility
    print("\n[8/29] html2canvas Compatibility Check")
    h2c_issues = check_html2canvas_safe(html)
    if h2c_issues:
        print("FAIL -- html2canvas risks found:")
        for issue in h2c_issues:
            print(issue)
        all_issues.extend(h2c_issues)
    else:
        print("PASS -- no html2canvas risks detected")
        checks_passed += 1

    # 9. Grid Divider Bug
    print("\n[9/29] Grid Divider Bug Check")
    grid_issues = check_grid_dividers(html)
    if grid_issues:
        print("FAIL -- grid divider bugs found:")
        for issue in grid_issues:
            print(issue)
        all_issues.extend(grid_issues)
    else:
        print("PASS -- no separate divider divs detected")
        checks_passed += 1

    # 10. Decorative Density (heuristic)
    print("\n[10/29] Decorative Density Check")
    deco_count = html.lower().count('position: absolute')
    # Rough heuristic: >15 absolute positioned elements in a 4-slide carousel = over-layered
    threshold = len(slides) * 4 if slides else 16
    if deco_count > threshold:
        print(f"WARN -- {deco_count} absolute positioned elements detected (threshold: {threshold}).")
        print("  Consider running the Subtraction Gate.")
        bloat_penalty = max(bloat_penalty, 5)
    else:
        print(f"PASS -- {deco_count} absolute positioned elements (threshold: {threshold})")
    checks_passed += 1  # heuristic warning, never fails

    # 11. Brand Consistency (T2-A)
    print("\n[11/29] Brand Consistency Check")
    brand_issues = check_brand_consistency(html)
    if brand_issues:
        print("FAIL -- brand/language leaks found:")
        for issue in brand_issues:
            print(issue)
        all_issues.extend(brand_issues)
    else:
        print("PASS -- no foreign brand names or language mixes detected")
        checks_passed += 1

    # 12. Container Fit (T2-B)
    print("\n[12/29] Container Fit Check")
    fit_fails, fit_warns = check_container_fit(html)
    if fit_fails:
        print("FAIL -- copy too long for container:")
        for issue in fit_fails:
            print(issue)
        all_issues.extend(fit_fails)
        for issue in fit_warns:
            print(issue)
    elif fit_warns:
        print("PASS WITH WARNINGS -- tight fits:")
        for issue in fit_warns:
            print(issue)
        checks_passed += 1
    else:
        print("PASS -- all narrow-container copy fits comfortably")
        checks_passed += 1

    # 13. Opacity Floor (WARN — readability check)
    print("\n[13/29] Opacity Floor Check")
    opacity_warns = check_opacity_floor(html)
    if opacity_warns:
        print("WARN -- potential low-opacity text detected (human review needed):")
        for w in opacity_warns:
            print(w)
    else:
        print("PASS -- no suspiciously low opacity values in CSS")
    checks_passed += 1  # warn-only, never blocks

    # 14. Template Artifacts
    print("\n[14/29] Template Artifact Check")
    artifact_issues = check_template_artifacts(html)
    if artifact_issues:
        print("FAIL -- template artifacts found:")
        for issue in artifact_issues:
            print(issue)
        all_issues.extend(artifact_issues)
    else:
        print("PASS -- no template artifacts detected")
        checks_passed += 1

    # 15. Dict Literal / Unrendered Jinja2 in output
    print("\n[15/29] Dict Literal Detection")
    dict_issues = check_dict_artifacts(html)
    if dict_issues:
        print("FAIL -- raw Python dict or unrendered template found:")
        for issue in dict_issues:
            print(issue)
        all_issues.extend(dict_issues)
    else:
        print("PASS -- no dict literals or unrendered tags in output")
        checks_passed += 1

    # 16. Text Edge Safety (warn only)
    print("\n[16/29] Text Edge Safety Check")
    edge_warns = check_text_edge_safety(html)
    if edge_warns:
        print("WARN -- text elements near slide edge:")
        for w in edge_warns:
            print(w)
    else:
        print("PASS -- no text within 8px of slide edge")
    checks_passed += 1  # warn-only

    # 17. Composition Asymmetry (warn only)
    print("\n[17/29] Composition Asymmetry Check")
    asym_warns = check_composition_asymmetry(slides)
    if asym_warns:
        print("WARN -- monotone alignment detected:")
        for w in asym_warns:
            print(w)
    else:
        print("PASS -- layout alignment varies across slides")
    checks_passed += 1  # warn-only

    # 18. Body Text Max-Width (warn only)
    print("\n[18/29] Body Text Width Check")
    width_warns = check_body_text_width(html)
    if width_warns:
        print("WARN -- body wrappers without max-width:")
        for w in width_warns:
            print(w)
    else:
        print("PASS -- body text wrappers have width constraints")
    checks_passed += 1  # warn-only

    # 19. Badge/Stamp Collision Check
    print("\n[19/29] Badge Collision Check")
    badge_issues = check_badge_collision(slides)
    if badge_issues:
        print("FAIL -- badge/stamp may overlap text:")
        for issue in badge_issues:
            print(issue)
        all_issues.extend(badge_issues)
    else:
        print("PASS -- no badge/text collisions detected")
        checks_passed += 1

    # 20. Shape Diversity Cap
    print("\n[20/29] Shape Diversity Check")
    shape_issues = check_shape_diversity(html)
    if shape_issues:
        print("FAIL -- shape overuse detected:")
        for issue in shape_issues:
            print(issue)
        all_issues.extend(shape_issues)
    else:
        print("PASS -- shape variety is healthy")
        checks_passed += 1

    # 21. Decorative Repetition Check (warn only)
    print("\n[21/29] Decorative Repetition Check")
    deco_rep_issues = check_decorative_repetition(slides)
    if deco_rep_issues:
        print("WARN -- decorative repetition detected:")
        for issue in deco_rep_issues:
            print(issue)
    else:
        print("PASS -- no consecutive decorative repetition")
    checks_passed += 1  # warn-only

    # 22. Demonstration Layout Check
    print("\n[22/26] Demonstration Layout Check")
    demo_issues = check_demonstration_layout(slides)
    if demo_issues:
        print("FAIL -- show-don't-tell rule violated:")
        for issue in demo_issues:
            print(issue)
        all_issues.extend(demo_issues)
    else:
        print("PASS -- at least one demonstration layout present")
        checks_passed += 1

    # 23. S1 Hook Context Check (warn only)
    print("\n[23/26] S1 Hook Context Check")
    hook_ctx_warns = check_s1_hook_context(slides)
    if hook_ctx_warns:
        print("WARN -- slide 1 hook is missing domain context:")
        for w in hook_ctx_warns:
            print(w)
    else:
        print("PASS -- slide 1 hook is anchored to the job-application domain")
    checks_passed += 1  # warn-only, never blocks

    # 24. AI-Background Quarantine Check
    print("\n[24/26] AI-bg Quarantine Check")
    quarantine_issues = check_ai_bg_quarantine(html)
    if quarantine_issues:
        print("FAIL -- quarantined background kit in use:")
        for issue in quarantine_issues:
            print(issue)
        all_issues.extend(quarantine_issues)
    else:
        print("PASS -- no quarantined background kits detected")
        checks_passed += 1

    # 25. AI-Background Density Coverage Check
    print("\n[25/26] AI-bg Density Coverage Check")
    density_issues = check_ai_bg_density_coverage(slides, html)
    if density_issues:
        print("FAIL -- AI-bg slides missing density declaration:")
        for issue in density_issues:
            print(issue)
        all_issues.extend(density_issues)
    else:
        print("PASS -- all AI-bg slides have density set (or carousel uses no AI backgrounds)")
        checks_passed += 1

    # 26. AI-Background Card Transparency Check (warn only)
    print("\n[26/26] AI-bg Card Transparency Check")
    transparency_warns = check_ai_bg_card_transparency(html)
    if transparency_warns:
        print("WARN -- ultra-transparent cards detected on AI-bg carousel:")
        for w in transparency_warns:
            print(w)
    else:
        print("PASS -- no ultra-transparent card backgrounds (or no AI backgrounds)")
    checks_passed += 1  # warn-only, never blocks

    # 27. AI-bg Panel Dimensions Check
    print("\n[27/29] AI-bg Panel Dimensions Check")
    dim_issues = check_ai_bg_panel_dimensions(html)
    if dim_issues:
        print("FAIL -- non-square AI-bg panels found:")
        for issue in dim_issues:
            print(issue)
        all_issues.extend(dim_issues)
    else:
        print("PASS -- all AI-bg panels are 1080×1080 (or no AI-bg panels / PIL not installed)")
    checks_passed += 1  # PIL-gated, only fails when truly bad

    # 28. AI-bg Edge Brightness Check (warn only)
    print("\n[28/29] AI-bg Edge Brightness Check")
    edge_bright_warns = check_ai_bg_edge_brightness(html)
    if edge_bright_warns:
        print("WARN -- bright/white edges detected on AI-bg panels:")
        for w in edge_bright_warns:
            print(w)
    else:
        print("PASS -- no bright panel edges detected (or no AI-bg panels / PIL not installed)")
    checks_passed += 1  # warn-only

    # 29. Slide Content Minimum (warn only)
    print("\n[29/29] Slide Content Minimum Check")
    content_min_warns = check_slide_content_minimum(slides)
    if content_min_warns:
        print("WARN -- slides with too little visible content:")
        for w in content_min_warns:
            print(w)
    else:
        print("PASS -- all slides have minimum content (≥4 visible words)")
    checks_passed += 1  # warn-only

    # v2: Visual primitives audit — informational only, never blocks export.
    print("\n[INFO] v2 Visual Primitives Audit")
    deprecations, used = check_v2_primitives(html)
    if used:
        print(f"  Using v2: {', '.join(used)}")
    else:
        print("  No v2 primitives detected. Consider opting into SVG icons / blobs / text treatments.")
    if deprecations:
        print("  Soft warnings (not blocking):")
        for dep in deprecations:
            print(dep)

    score = int((checks_passed / checks_total) * 100) - bloat_penalty
    score = max(0, score)
    print(f"\n{'='*60}")
    print(f"SCORE: {score}/100 ({checks_passed}/{checks_total} checks passed, penalty: {bloat_penalty})")
    if score >= 90:
        print("RESULT: READY TO EXPORT")
    elif score >= 70:
        print("RESULT: GOOD -- fix warnings before export")
    else:
        print("RESULT: NEEDS WORK -- fix errors before export")
    print(f"{'='*60}\n")

    sys.exit(0 if score >= 90 else 1)


if __name__ == "__main__":
    main()
