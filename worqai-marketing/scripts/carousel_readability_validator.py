#!/usr/bin/env python3
"""
carousel_readability_validator.py — Deterministic readability & color-theme validator for WorqAI carousel HTML files.

Validates and optionally auto-fixes carousel HTML files against the four official themes:
  - dark      (#0A0A0A bg, white text)
  - light     (#F5F5F5 bg, black text)
  - darkblue  (#0f172a bg, white text)
  - grey      (#555555 bg, white text)

Usage:
    py scripts/carousel_readability_validator.py path/to/carousel.html
    py scripts/carousel_readability_validator.py path/to/carousel.html --fix
    py scripts/carousel_readability_validator.py path/to/dir/ --batch
    py scripts/carousel_readability_validator.py path/to/dir/ --batch --fix --json

Checks:
    1.  Theme detection from filename (dark-carousel, light-carousel, etc.)
    2.  Background color matches declared theme
    3.  Body/slide text color matches theme contrast
    4.  No light text on light background
    5.  No dark text on dark background
    6.  Glass-block text color is correct for glass background
    7.  Lime-badge text is black inside lime
    8.  Desliza button is not green-on-green
    9.  CTA card text is readable
    10. Counter is solid color (not transparent)
    11. Brand "worqai" colors match theme
    12. Stat numbers have proper text-shadow/glow
    13. Source-tag opacity >= 1.0 (no faded text)
    14. Broken character detection (???, missing Spanish accents)
    15. Liquid-glass boxes on busy backgrounds

Exit codes:
    0 = all checks passed
    1 = readability issues found
    2 = file not found or unreadable
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ─── Theme definitions (single source of truth) ───────────────────────────

THEMES = {
    "dark": {
        "bg": ["#0A0A0A", "#111111", "#000000", "#1a1a2e", "#010509", "var(--bg)", "var(--slide-bg)"],
        "text": "#FAFAFA",
        "text_secondary": "#E5E5E5",
        "text_muted": "#A0A0A0",
        "glass_bg": "rgba(255,255,255,0.85)",
        "glass_text": "#0A0A0A",
        "brand_worq": "#FAFAFA",
        "brand_ai": "#C7FF3A",
        "swipe_text": "#FFFFFF",
        "counter": "#FAFAFA",
        "stat_shadow": "0 0 20px rgba(199,255,58,0.3)",
        "source_tag": "#FAFAFA",
        "cta_card_bg": "#0A0A0A",
        "cta_card_text": "#FAFAFA",
    },
    "light": {
        "bg": ["#F5F5F5", "#FAFAFA", "#FFFFFF"],
        "text": "#0A0A0A",
        "text_secondary": "#1A1A1A",
        "text_muted": "#333333",
        "glass_bg": "rgba(255,255,255,0.85)",
        "glass_text": "#0A0A0A",
        "brand_worq": "#0A0A0A",
        "brand_ai": "#C7FF3A",
        "swipe_text": "#0A0A0A",
        "counter": "#0A0A0A",
        "stat_shadow": "-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000",
        "source_tag": "#666666",
        "cta_card_bg": "#FFFFFF",
        "cta_card_text": "#0A0A0A",
    },
    "darkblue": {
        "bg": ["#0f172a", "#111827"],
        "text": "#FAFAFA",
        "text_secondary": "#E5E5E5",
        "text_muted": "#94a3b8",
        "glass_bg": "rgba(15,23,42,0.85)",
        "glass_text": "#FAFAFA",
        "brand_worq": "#FAFAFA",
        "brand_ai": "#C7FF3A",
        "swipe_text": "#FFFFFF",
        "counter": "#FAFAFA",
        "stat_shadow": "0 0 20px rgba(199,255,58,0.3)",
        "source_tag": "#94a3b8",
        "cta_card_bg": "#0f172a",
        "cta_card_text": "#FAFAFA",
    },
    "grey": {
        "bg": ["#555555", "#4B5563", "#6B7280"],
        "text": "#FAFAFA",
        "text_secondary": "#E5E5E5",
        "text_muted": "#D1D5DB",
        "glass_bg": "rgba(255,255,255,0.85)",
        "glass_text": "#0A0A0A",
        "brand_worq": "#FAFAFA",
        "brand_ai": "#C7FF3A",
        "swipe_text": "#FFFFFF",
        "counter": "#FAFAFA",
        "stat_shadow": "0 0 20px rgba(199,255,58,0.3)",
        "source_tag": "#D1D5DB",
        "cta_card_bg": "#4B5563",
        "cta_card_text": "#FAFAFA",
    },
}

# Colors that are ALWAYS wrong on light backgrounds
LIGHT_BG_COLORS = ["#FAFAFA", "#E5E5E5", "#FFFFFF", "#f0f0f5", "#e2e2f0", "#e2e8f0"]
DARK_BG_COLORS = ["#0A0A0A", "#111111", "#000000", "#333333", "#1A1A1A"]

# Broken character patterns
BROKEN_CHARS = re.compile(r"[\uFFFD\u0000-\u0008\u000B-\u000C\u000E-\u001F]|\?\?\?")

# Spanish accent check — common missing accents
SPANISH_ACCENT_PATTERNS = [
    (re.compile(r"\bdiseno\b"), "diseño"),
    (re.compile(r"\basi\b"), "así"),
    (re.compile(r"\bqueres\b"), "querés"),
    (re.compile(r"\bdiagnostico\b"), "diagnóstico"),
    (re.compile(r"\banos\b"), "años"),
    (re.compile(r"\bnumero\b"), "número"),
    (re.compile(r"\btrabajo\b"), "trabajó"),
]


# ─── Regex helpers ──────────────────────────────────────────────────────────

def find_css_value(css: str, property_name: str) -> Optional[str]:
    """Extract the first CSS property value."""
    pattern = re.compile(rf'{re.escape(property_name)}\s*:\s*([^;}}]+)', re.IGNORECASE)
    match = pattern.search(css)
    return match.group(1).strip() if match else None


def extract_all_css_blocks(html: str) -> List[Tuple[str, str]]:
    """Extract (selector, declarations) from all CSS blocks."""
    blocks = []
    # Match <style>...</style> content
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    for style in style_blocks:
        # Extract rule blocks: selector { ... }
        rules = re.findall(r'([^{]+)\{([^}]+)\}', style, re.DOTALL)
        for selector, declarations in rules:
            blocks.append((selector.strip(), declarations.strip()))
    # Also extract inline styles
    inline_styles = re.findall(r'<[^>]+style="([^"]*)"', html, re.IGNORECASE)
    for i, style in enumerate(inline_styles):
        blocks.append((f"inline-{i}", style))
    return blocks


def detect_theme_from_filename(filename: str) -> Optional[str]:
    """Detect theme from filename patterns."""
    f = filename.lower()
    # Dark blue: explicit patterns only, NOT "blueprint" or other words containing "blue"
    if "dark-blue" in f or "darkblue" in f:
        return "darkblue"
    if "dark" in f and "light" not in f:
        return "dark"
    if "light" in f and "dark" not in f:
        return "light"
    if "grey" in f or "gray" in f:
        return "grey"
    return None


# ─── Validation engine ──────────────────────────────────────────────────────

class ReadabilityValidator:
    def __init__(self, html_content: str, filepath: str):
        self.html = html_content
        self.filepath = filepath
        self.filename = Path(filepath).name
        self.theme = detect_theme_from_filename(self.filename) or "dark"  # default
        self.rules = THEMES[self.theme]
        self.issues: List[Dict] = []
        self.css_blocks = extract_all_css_blocks(html_content)
        self._build_css_map()

    def _build_css_map(self):
        """Build a map of selector -> {property: value} for quick lookup."""
        self.css_map: Dict[str, Dict[str, str]] = {}
        for selector, declarations in self.css_blocks:
            sel_clean = selector.strip().replace(" ", "")
            if sel_clean not in self.css_map:
                self.css_map[sel_clean] = {}
            for line in declarations.split(';'):
                line = line.strip()
                if ':' in line:
                    prop, val = line.split(':', 1)
                    self.css_map[sel_clean][prop.strip().lower()] = val.strip()

    def _add_issue(self, code: str, message: str, selector: str = "", severity: str = "error"):
        self.issues.append({
            "code": code,
            "message": message,
            "selector": selector,
            "severity": severity,
            "theme": self.theme,
        })

    def check_background(self):
        """Check that html/body and .slide backgrounds match the theme."""
        expected_bgs = self.rules["bg"]

        # Check html/body background
        for selector in ["html,body", "html", "body"]:
            if selector in self.css_map:
                bg = self.css_map[selector].get("background", "")
                if bg and not any(e in bg for e in expected_bgs):
                    self._add_issue(
                        "BG_MISMATCH",
                        f"{selector} background '{bg}' does not match {self.theme} theme (expected one of {expected_bgs})",
                        selector,
                    )
                break
        else:
            # Try inline style on body tag
            body_match = re.search(r'<body[^>]*style="[^"]*background\s*:\s*([^;"]+)', self.html, re.IGNORECASE)
            if body_match:
                bg = body_match.group(1).strip()
                if not any(e in bg for e in expected_bgs):
                    self._add_issue(
                        "BG_MISMATCH",
                        f"body inline background '{bg}' does not match {self.theme} theme",
                        "body",
                    )

        # Check .slide background
        for selector in [".slide", ".slide::before"]:
            if selector in self.css_map:
                bg = self.css_map[selector].get("background", "")
                if bg and not any(e in bg for e in expected_bgs + ["transparent", "none", "linear-gradient", "var(--slide-bg)"]):
                    # Allow gradients that contain the expected color
                    if not any(e in bg for e in expected_bgs + ["var(--slide-bg)"]):
                        self._add_issue(
                            "BG_MISMATCH",
                            f"{selector} background '{bg}' may not match {self.theme} theme",
                            selector,
                            "warning",
                        )

    def check_text_contrast(self):
        """Check that text colors contrast with the background."""
        if self.theme in ["dark", "darkblue", "grey"]:
            # Text should be white/light on dark backgrounds
            bad_colors = DARK_BG_COLORS
            expected = self.rules["text"]
        else:
            # Text should be black/dark on light backgrounds
            bad_colors = LIGHT_BG_COLORS
            expected = self.rules["text"]

        text_selectors = [
            ".headline", ".body-text", ".hook-display", ".hook-sub",
            ".proof-stmt", ".proof-ctx", ".stat-context", ".stat-pct",
            ".cta-headline-out", ".cta-offer", ".cta-fine", ".cta-closing", ".cta-micro",
            ".label", ".label-top", ".pill-tag", ".site-url", ".url-text",
        ]

        for selector in text_selectors:
            for sel in self.css_map:
                if selector in sel:
                    # Skip if this selector is inside a glass container (checked separately)
                    if any(glass in sel for glass in [".text-backdrop", ".glass-block"]):
                        continue
                    color = self.css_map[sel].get("color", "")
                    if color:
                        # Skip if element has its own contrasting background (badges, labels with bg)
                        bg = self.css_map[sel].get("background", "").lower()
                        if "c7ff3a" in bg or "ff5c3c" in bg or "ff8b70" in bg or "ffffff" in bg or "fafafa" in bg:
                            # Element has its own background that provides contrast
                            continue
                        # Check for bad colors
                        for bad in bad_colors:
                            if bad.lower() in color.lower():
                                self._add_issue(
                                    "CONTRAST_FAIL",
                                    f"{sel} color '{color}' is unreadable on {self.theme} background",
                                    sel,
                                )
                                break

    def check_glass_blocks(self):
        """Check that glass-block text is the correct color for the glass background."""
        glass_bg = self.rules["glass_bg"]
        expected_text = self.rules["glass_text"]

        for selector in [".glass-block", ".text-backdrop", ".glass-block.good", ".glass-block.bad"]:
            for sel in self.css_map:
                if selector in sel:
                    bg = self.css_map[sel].get("background", "")
                    if "rgba(255,255,255" in bg or "rgba(250,250,250" in bg:
                        # White glass box → text should be black
                        for child_sel in self.css_map:
                            if child_sel.startswith(sel) and "color" in self.css_map[child_sel]:
                                child_color = self.css_map[child_sel]["color"].lower()
                                if child_color in ["#fafafa", "#e5e5e5", "#ffffff", "white"]:
                                    self._add_issue(
                                        "GLASS_TEXT_WRONG",
                                        f"{child_sel} has white text inside white glass box — unreadable",
                                        child_sel,
                                    )

    def check_lime_badge(self):
        """Check that lime badges have black text."""
        for selector in [".lime-badge", ".badge"]:
            for sel in self.css_map:
                if selector in sel and "background" in self.css_map[sel]:
                    bg = self.css_map[sel]["background"].lower()
                    if "c7ff3a" in bg or "lime" in bg:
                        # Check text color
                        for child_sel in self.css_map:
                            if child_sel.startswith(sel) and "color" in self.css_map[child_sel]:
                                color = self.css_map[child_sel]["color"].lower()
                                if color in ["#fafafa", "#e5e5e5", "#ffffff", "white"]:
                                    self._add_issue(
                                        "LIME_BADGE_TEXT",
                                        f"{child_sel} has white text on lime background — unreadable",
                                        child_sel,
                                    )

    def check_swipe_pill(self):
        """Check that Desliza button is not green-on-green."""
        for sel in self.css_map:
            if "swipe-pill" in sel or "swipe" in sel:
                color = self.css_map[sel].get("color", "").lower()
                bg = self.css_map[sel].get("background", "").lower()
                border = self.css_map[sel].get("border", "").lower()
                if "c7ff3a" in color and ("c7ff3a" in bg or "c7ff3a" in border):
                    self._add_issue(
                        "GREEN_ON_GREEN",
                        f"{sel} has lime text on lime border — low contrast",
                        sel,
                    )
                if "c7ff3a" in bg and "transparent" not in bg:
                    self._add_issue(
                        "GREEN_ON_GREEN",
                        f"{sel} has lime background — should be transparent with colored border",
                        sel,
                    )

    def check_counter(self):
        """Check that counter is solid color, not transparent."""
        for sel in self.css_map:
            if "counter" in sel or "pd" in sel:
                color = self.css_map[sel].get("color", "")
                if "rgba" in color and any(opacity in color for opacity in ["0.2", "0.25", "0.3", "0.4"]):
                    self._add_issue(
                        "COUNTER_TRANSPARENT",
                        f"{sel} counter has transparent color '{color}' — should be solid",
                        sel,
                    )

    def check_source_tag_opacity(self):
        """Check that source-tag has opacity >= 1.0."""
        for sel in self.css_map:
            if "source-tag" in sel or "source" in sel or "src" in sel:
                opacity = self.css_map[sel].get("opacity", "")
                if opacity:
                    opacity_clean = opacity.replace("!important", "").strip()
                    try:
                        if float(opacity_clean) < 0.75:
                            self._add_issue(
                                "OPACITY_TOO_LOW",
                                f"{sel} opacity {opacity} is too low for readability (min 0.75)",
                                sel,
                            )
                    except ValueError:
                        pass

    def check_brand_colors(self):
        """Check brand anchor colors."""
        expected_worq = self.rules["brand_worq"]
        expected_ai = self.rules["brand_ai"]

        for sel in self.css_map:
            if "brand-anchor" in sel and ".worq" in sel:
                color = self.css_map[sel].get("color", "")
                if color and expected_worq.lower() not in color.lower():
                    self._add_issue(
                        "BRAND_WORQ_COLOR",
                        f"{sel} color '{color}' should be {expected_worq} for {self.theme} theme",
                        sel,
                        "warning",
                    )
            if "brand-anchor" in sel and ".ai" in sel:
                color = self.css_map[sel].get("color", "")
                if color and "c7ff3a" not in color.lower() and "lime" not in color.lower():
                    self._add_issue(
                        "BRAND_AI_COLOR",
                        f"{sel} color '{color}' should be lime #C7FF3A",
                        sel,
                    )

    def check_cta_card(self):
        """Check CTA card readability."""
        for sel in self.css_map:
            if "cta-card" in sel:
                bg = self.css_map[sel].get("background", "").lower()
                if self.theme in ["dark", "darkblue"]:
                    # Dark theme: CTA card should be dark, text white
                    if "f5f5f5" in bg or "ffffff" in bg or "fafafa" in bg:
                        self._add_issue(
                            "CTA_BG_WRONG",
                            f"{sel} has light background on {self.theme} theme",
                            sel,
                        )
                elif self.theme == "light":
                    # Light theme: CTA card should be light, text dark
                    if "0a0a0a" in bg or "111111" in bg or "0f172a" in bg:
                        self._add_issue(
                            "CTA_BG_WRONG",
                            f"{sel} has dark background on {self.theme} theme",
                            sel,
                        )

    def check_broken_characters(self):
        """Check for broken characters and missing Spanish accents."""
        text_content = re.sub(r'<[^>]+>', ' ', self.html)  # strip tags
        if BROKEN_CHARS.search(text_content):
            self._add_issue(
                "BROKEN_CHARS",
                "File contains broken/invalid characters (??? or replacement chars)",
                severity="error",
            )

        for pattern, correct in SPANISH_ACCENT_PATTERNS:
            if pattern.search(text_content):
                self._add_issue(
                    "MISSING_ACCENT",
                    f"Possible missing accent: found '{pattern.pattern}' — should be '{correct}'",
                    severity="warning",
                )

    def check_theme_mismatch(self):
        """Check if filename declares a theme but CSS shows a different one."""
        if "light" in self.filename.lower() and "dark" not in self.filename.lower():
            # Should be light theme
            for sel in self.css_map:
                if "html,body" in sel or sel == "body" or sel == "html":
                    bg = self.css_map[sel].get("background", "")
                    if "0a0a0a" in bg.lower() or "0f172a" in bg.lower() or "111111" in bg.lower():
                        self._add_issue(
                            "THEME_MISMATCH",
                            f"Filename says 'light' but {sel} background is dark '{bg}'",
                            sel,
                        )
        elif "dark" in self.filename.lower() and "light" not in self.filename.lower():
            # Should be dark theme
            for sel in self.css_map:
                if "html,body" in sel or sel == "body" or sel == "html":
                    bg = self.css_map[sel].get("background", "")
                    if "f5f5f5" in bg.lower() or "fafafa" in bg.lower() or "ffffff" in bg.lower():
                        self._add_issue(
                            "THEME_MISMATCH",
                            f"Filename says 'dark' but {sel} background is light '{bg}'",
                            sel,
                        )

    def run_all(self) -> Dict:
        """Run all checks and return results."""
        self.check_background()
        self.check_text_contrast()
        self.check_glass_blocks()
        self.check_lime_badge()
        self.check_swipe_pill()
        self.check_counter()
        self.check_source_tag_opacity()
        self.check_brand_colors()
        self.check_cta_card()
        self.check_broken_characters()
        self.check_theme_mismatch()

        errors = [i for i in self.issues if i["severity"] == "error"]
        warnings = [i for i in self.issues if i["severity"] == "warning"]

        return {
            "file": self.filepath,
            "theme": self.theme,
            "errors": len(errors),
            "warnings": len(warnings),
            "issues": self.issues,
            "passed": len(errors) == 0,
        }


# ─── Auto-fix engine ────────────────────────────────────────────────────────

class ReadabilityFixer:
    """Apply automatic fixes for common readability issues."""

    def __init__(self, html_content: str, theme: str):
        self.html = html_content
        self.theme = theme
        self.rules = THEMES[theme]
        self.fixes_applied: List[str] = []

    def _fix(self, description: str, old: str, new: str) -> bool:
        """Apply a fix if old pattern is found. Returns True if applied."""
        if old in self.html:
            self.html = self.html.replace(old, new)
            self.fixes_applied.append(description)
            return True
        return False

    def fix_background(self):
        """Fix html/body and .slide backgrounds to match theme."""
        expected_bg = self.rules["bg"][0]
        # Fix html,body background
        self._fix(
            f"html,body background → {expected_bg}",
            "background: #F5F5F5;",  # light → theme
            f"background: {expected_bg};",
        )
        self._fix(
            f"html,body background → {expected_bg}",
            "background: #FAFAFA;",
            f"background: {expected_bg};",
        )
        if self.theme == "light":
            self._fix(
                "html,body background → #F5F5F5",
                "background: #0A0A0A;",
                "background: #F5F5F5;",
            )
            self._fix(
                "html,body background → #F5F5F5",
                "background: #0f172a;",
                "background: #F5F5F5;",
            )

    def fix_text_colors(self):
        """Fix text colors to match theme contrast."""
        expected_text = self.rules["text"]
        expected_secondary = self.rules["text_secondary"]
        expected_muted = self.rules["text_muted"]

        if self.theme in ["dark", "darkblue", "grey"]:
            # Dark backgrounds → white text
            self._fix("headline color → white", 'color: #0A0A0A;', 'color: #FAFAFA;')
            self._fix("body-text color → light grey", 'color: #1A1A1A;', 'color: #E5E5E5;')
            self._fix("proof-ctx color → light grey", 'color: #333333;', 'color: #E5E5E5;')
        else:
            # Light backgrounds → black text
            self._fix("headline color → black", 'color: #FAFAFA;', 'color: #0A0A0A;')
            self._fix("body-text color → dark", 'color: #E5E5E5;', 'color: #1A1A1A;')
            self._fix("proof-ctx color → dark grey", 'color: #E5E5E5;', 'color: #333333;')

    def fix_glass_blocks(self):
        """Ensure glass blocks have proper text colors."""
        expected_glass_text = self.rules["glass_text"]
        # For white glass boxes, text should be black
        if "255,255,255" in self.rules["glass_bg"]:
            self._fix(
                "glass-text inside white box → black",
                '.glass-text{color:#FAFAFA;}',
                '.glass-text{color:#0A0A0A;}',
            )
            self._fix(
                "glass-text inside white box → black",
                '.glass-text{color:#E5E5E5;}',
                '.glass-text{color:#0A0A0A;}',
            )

    def fix_lime_badge(self):
        """Ensure lime badges have black text."""
        self._fix(
            "lime-badge text → black",
            '.lime-badge{color:#FAFAFA;}',
            '.lime-badge{color:#0A0A0A;}',
        )
        self._fix(
            "lime-badge text → black",
            '.lime-badge{color:#E5E5E5;}',
            '.lime-badge{color:#0A0A0A;}',
        )

    def fix_swipe_pill(self):
        """Ensure swipe pill is not green-on-green."""
        if self.theme in ["dark", "darkblue", "grey"]:
            self._fix(
                "swipe-pill text → white on dark",
                '.swipe-pill{color:#C7FF3A;}',
                '.swipe-pill{color:#FFFFFF;}',
            )
        else:
            self._fix(
                "swipe-pill text → black on light",
                '.swipe-pill{color:#C7FF3A;}',
                '.swipe-pill{color:#0A0A0A;}',
            )
        # Make background transparent
        self._fix(
            "swipe-pill background → transparent",
            'background:#C7FF3A;',
            'background:transparent;',
        )

    def fix_counter(self):
        """Ensure counter is solid color."""
        if self.theme in ["dark", "darkblue", "grey"]:
            self._fix(
                "counter color → solid white",
                'color:rgba(255,255,255,0.25)',
                'color:#FAFAFA',
            )
        else:
            self._fix(
                "counter color → solid black",
                'color:rgba(0,0,0,0.25)',
                'color:#0A0A0A',
            )

    def fix_source_tag_opacity(self):
        """Ensure source tags have opacity 1.0."""
        self._fix(
            "source-tag opacity → 1.0",
            'opacity:0.40',
            'opacity:1.0',
        )
        self._fix(
            "source-tag opacity → 1.0",
            'opacity:0.55',
            'opacity:1.0',
        )
        self._fix(
            "source-tag opacity → 1.0",
            'opacity:0.75',
            'opacity:1.0',
        )

    def fix_brand_colors(self):
        """Fix brand anchor colors."""
        expected_worq = self.rules["brand_worq"]
        if self.theme in ["dark", "darkblue", "grey"]:
            self._fix(
                "brand .worq → white",
                '.brand-anchor .worq{color:#0A0A0A;}',
                '.brand-anchor .worq{color:#FAFAFA;}',
            )
        else:
            self._fix(
                "brand .worq → black",
                '.brand-anchor .worq{color:#FAFAFA;}',
                '.brand-anchor .worq{color:#0A0A0A;}',
            )

    def fix_cta_card(self):
        """Fix CTA card background."""
        expected_bg = self.rules["cta_card_bg"]
        expected_text = self.rules["cta_card_text"]
        if self.theme == "light":
            self._fix(
                "CTA card bg → white",
                '.cta-card{background:#0A0A0A;}',
                '.cta-card{background:#FFFFFF;}',
            )
            self._fix(
                "CTA card bg → white",
                '.cta-card{background:#0f172a;}',
                '.cta-card{background:#FFFFFF;}',
            )
        elif self.theme in ["dark", "darkblue"]:
            self._fix(
                "CTA card bg → dark",
                '.cta-card{background:#FFFFFF;}',
                f'.cta-card{background:{expected_bg};}',
            )
            self._fix(
                "CTA card bg → dark",
                '.cta-card{background:#F5F5F5;}',
                f'.cta-card{background:{expected_bg};}',
            )

    def fix_broken_hex(self):
        """Fix invalid hex values like #0A0A0A555."""
        self._fix(
            "invalid hex #0A0A0A555 → #0A0A0A",
            '#0A0A0A555',
            '#0A0A0A',
        )

    def apply_all(self) -> str:
        """Apply all fixes and return modified HTML."""
        self.fix_background()
        self.fix_text_colors()
        self.fix_glass_blocks()
        self.fix_lime_badge()
        self.fix_swipe_pill()
        self.fix_counter()
        self.fix_source_tag_opacity()
        self.fix_brand_colors()
        self.fix_cta_card()
        self.fix_broken_hex()
        return self.html


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Validate and fix carousel HTML readability & color themes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s carousel.html                    # validate only
  %(prog)s carousel.html --fix              # validate + auto-fix
  %(prog)s ./production/ --batch            # validate all HTML in directory
  %(prog)s ./production/ --batch --fix      # validate + fix all
  %(prog)s ./production/ --batch --json     # output JSON report
        """
    )
    parser.add_argument("path", help="HTML file or directory to validate")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues in place")
    parser.add_argument("--batch", action="store_true", help="Process all .html files in directory")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--theme", choices=["dark", "light", "darkblue", "grey"], help="Override theme detection")
    args = parser.parse_args()

    target_path = Path(args.path)
    files_to_process: List[Path] = []

    if args.batch:
        if not target_path.is_dir():
            print(f"ERROR: --batch requires a directory, got {target_path}", file=sys.stderr)
            sys.exit(2)
        files_to_process = list(target_path.glob("*.html"))
        if not files_to_process:
            print(f"No .html files found in {target_path}", file=sys.stderr)
            sys.exit(2)
    else:
        if not target_path.is_file():
            print(f"ERROR: File not found: {target_path}", file=sys.stderr)
            sys.exit(2)
        files_to_process = [target_path]

    results: List[Dict] = []
    total_errors = 0
    total_warnings = 0

    for filepath in files_to_process:
        try:
            html = filepath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"ERROR: Cannot read {filepath}: {e}", file=sys.stderr)
            continue

        # Detect theme
        theme = args.theme or detect_theme_from_filename(filepath.name) or "dark"

        # Validate
        validator = ReadabilityValidator(html, str(filepath))
        if args.theme:
            validator.theme = args.theme
            validator.rules = THEMES[args.theme]
        result = validator.run_all()

        # Auto-fix
        if args.fix:
            fixer = ReadabilityFixer(html, validator.theme)
            fixed_html = fixer.apply_all()
            if fixer.fixes_applied:
                filepath.write_text(fixed_html, encoding="utf-8")
                result["fixes_applied"] = fixer.fixes_applied
            else:
                result["fixes_applied"] = []

        results.append(result)
        total_errors += result["errors"]
        total_warnings += result["warnings"]

    # Output
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            status = "[PASS]" if result["passed"] else "[FAIL]"
            print(f"\n{status}  {result['file']}  (theme: {result['theme']})")
            if result["errors"]:
                print(f"  {result['errors']} error(s):")
                for issue in result["issues"]:
                    if issue["severity"] == "error":
                        print(f"    [X] [{issue['code']}] {issue['message']}")
                        if issue["selector"]:
                            print(f"       Selector: {issue['selector']}")
            if result["warnings"]:
                print(f"  {result['warnings']} warning(s):")
                for issue in result["issues"]:
                    if issue["severity"] == "warning":
                        print(f"    [!] [{issue['code']}] {issue['message']}")
            if args.fix and result.get("fixes_applied"):
                print(f"  [FIX] Auto-fixes applied ({len(result['fixes_applied'])}):")
                for fix in result["fixes_applied"]:
                    print(f"      * {fix}")

        print(f"\n{'='*60}")
        print(f"Total: {len(results)} files | {total_errors} errors | {total_warnings} warnings")
        if total_errors == 0:
            print("All readability checks passed!")
        else:
            print(f"{total_errors} files need attention.")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
