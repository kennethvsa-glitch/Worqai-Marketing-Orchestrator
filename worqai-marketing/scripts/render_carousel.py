#!/usr/bin/env python3
"""
render_carousel.py — Assembles carousel HTML from a spec JSON + Jinja2 templates.

Usage:
    py scripts/render_carousel.py my-spec.json
    py scripts/render_carousel.py my-spec.json --output production/carousel_topic_s17.html
    py scripts/render_carousel.py my-spec.json --validate-only

Dependencies:
    pip install jinja2

Exit codes:
    0 = success
    1 = error (missing file, invalid spec, missing template)
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, Undefined
except ImportError:
    print("ERROR: Jinja2 required. Run: pip install jinja2", file=sys.stderr)
    sys.exit(1)

ROOT_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT_DIR / "templates"
DATA_PATH = Path(__file__).parent / "component_data.json"
PRODUCTION_DIR = ROOT_DIR / "production"

# ── AI Background Manifest (lazy load) ─────────────────────────────────────────
def _load_manifest() -> dict:
    manifest_path = ROOT_DIR / "brand" / "generated-bg" / "manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {"backgrounds": []}


def _build_ai_bg_lookup(manifest: dict) -> dict:
    return {bg["id"]: bg for bg in manifest.get("backgrounds", [])}


_MANIFEST = _load_manifest()
_AI_BG_LOOKUP = _build_ai_bg_lookup(_MANIFEST)


def resolve_ai_bg(
    layer_name: str,
    system_id: str,
    slide_num: int = 1,
    bg_recipe: str | None = None,
) -> str | None:
    """Return HTML for an AI-generated background layer if found in manifest.

    v4: Supports per-slide recipe progressions via meta.bg_recipe in the spec.
    When bg_recipe is set, looks up the slide-specific variant from recipe_variants.
    Falls back to the flat base variant when no recipe or no matching sequence.
    """
    bg = _AI_BG_LOOKUP.get(layer_name)
    if not bg:
        return None

    # v4: per-slide recipe progression
    variant_path = None
    if bg_recipe:
        seq = bg.get("recipe_variants", {}).get(bg_recipe, {}).get(system_id, [])
        if seq:
            idx = min(slide_num - 1, len(seq) - 1)
            variant_path = seq[idx]

    # Fallback to flat base variant
    if not variant_path:
        variant_path = bg.get("variants", {}).get(system_id)

    if not variant_path:
        return None
    abs_path = ROOT_DIR / variant_path
    if not abs_path.exists():
        return None
    # HTML files are typically in gallery/ or production/ — prefix with ../
    # to resolve correctly from those subdirectories.
    rel_src = f"../{variant_path}" if not variant_path.startswith(("../", "http", "/")) else variant_path
    return (
        f'<img src="{rel_src}" class="geo-layer geo-ai-bg" alt="" '
        f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;opacity:0.9">\n    '
        f'<div class="geo-ai-bg-overlay"></div>'
    )


# ── System classification ──────────────────────────────────────────────────────

# ── System personality: per-family layout preferences ─────────────────────────
# PREFERRED: layouts weighted for this family (applied when spec omits layout hint)
# FORBIDDEN: layouts that never match this family's aesthetic
SYSTEM_PERSONALITY = {
    "brutalist": {
        "preferred": [
            "slide-full-bleed-type", "slide-stacked-type",
            "slide-contrast-knockout", "slide-corner-manifesto",
            "slide-typeset-poster", "slide-diagonal-split",
        ],
        "forbidden": [
            "slide-polaroid-grid", "slide-circular-quote",
            "slide-logo-wall", "slide-data-viz-donut",
        ],
    },
    "cyberpunk": {
        "preferred": [
            "slide-terminal-fullscreen", "slide-terminal",
            "slide-data-wall", "slide-morse-code",
            "slide-scroll-code", "slide-massive-number",
        ],
        "forbidden": [
            "slide-polaroid-grid", "slide-receipt",
            "slide-pull-quote", "slide-circular-quote",
        ],
    },
    "light": {
        "preferred": [
            "slide-asymmetric-lockup", "slide-editorial-column",
            "slide-frame-within-frame", "slide-typeset-poster",
            "slide-hook-lockup", "slide-pull-quote",
        ],
        "forbidden": [
            "slide-terminal-fullscreen", "slide-morse-code",
            "slide-data-wall",
        ],
    },
    "warm": {
        "preferred": [
            "slide-polaroid-grid", "slide-hook-lockup",
            "slide-step-flow", "slide-circular-quote",
            "slide-minimal-card-stack",
        ],
        "forbidden": [
            "slide-terminal-fullscreen", "slide-morse-code",
            "slide-scroll-code",
        ],
    },
    "dark": {
        "preferred": [
            "slide-full-bleed-type", "slide-massive-number",
            "slide-side-by-side", "slide-hook-lockup",
            "slide-diagonal-split", "slide-stacked-type",
        ],
        "forbidden": [],
    },
}


SYSTEM_TYPES = {
    "s01": "dark",      "s02": "dark",      "s03": "dark",
    "s04": "warm",      "s05": "light",     "s06": "dark",
    "s07": "brutalist", "s08": "dark",      "s09": "dark",
    "s10": "dark",      "s11": "dark",      "s12": "dark",
    "s13": "dark",      "s14": "dark",      "s15": "dark",
    "s16": "dark",      "s17": "dark",      "s18": "light",
    "s19": "light",     "s20": "dark",      "s21": "dark",
    "s22": "dark",      "s23": "light",     "s24": "dark",
    "s25": "brutalist", "s26": "light",     "s27": "dark",
    "s28": "dark",      "s29": "cyberpunk", "s30": "dark",
    "s31": "dark",      "s32": "dark",      "s39": "light",
    "s47": "light",     "s48": "light",
}

LIGHT_SYSTEMS = {"s05","s18","s19","s23","s25","s26","s39","s47","s48"}

# Universal Google Fonts URL — all 16 consolidated families for all 48 systems.
# Per VISUAL_SYSTEMS_AUDIT: Montserrat, Outfit, Lato, Sora, Roboto, Roboto Mono,
# Source Sans 3 were removed. Replacements baked into component_data.json tokens.
UNIVERSAL_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Archivo:wght@400;500;600;700"
    "&family=Cinzel+Decorative:wght@400;700"
    "&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,600"
    "&family=Playfair+Display:wght@400;500;600;700"
    "&family=Crimson+Pro:wght@400;500;600"
    "&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,400"
    "&family=IBM+Plex+Sans:wght@400;500;600"
    "&family=Inter:wght@300;400;500;600;700"
    "&family=JetBrains+Mono:wght@300;400;500;700"
    "&family=Noto+Sans:wght@400;500;700"
    "&family=Noto+Sans+JP:wght@400;500;700"
    "&family=Noto+Serif:wght@400;500;600"
    "&family=Nunito:wght@400;500;600;700"
    "&family=Poppins:wght@400;500;600;700"
    "&family=Source+Serif+4:wght@400;500;600"
    "&family=Space+Grotesk:wght@300;400;500;600;700"
    "&family=Work+Sans:wght@400;500;600;700"
    "&display=swap"
)

DEFAULT_TOKENS = {
    "--bg-base": "#0a0a12",
    "--bg-mid": "#111122",
    "--accent": "#00ff9c",
    "--text-primary": "#ffffff",
    "--text-secondary": "rgba(255,255,255,0.55)",
    "--text-muted": "rgba(255,255,255,0.28)",
    "--font-display": "'Space Grotesk', sans-serif",
    "--font-body": "'Inter', sans-serif",
    "--font-mono": "'JetBrains Mono', monospace",
    "--grain-opacity": "0.05",
    "--geo-opacity": "0.08",
}

# ── Geo layer HTML per system type ────────────────────────────────────────────

GEO_HTML = {
    "cyberpunk": (
        '<div class="pw-wrap"><div class="pw-grid"></div></div>\n'
        '    <div class="scan-lines"></div>\n'
        '    <div class="glow-orb"></div>\n'
        '    <div class="zoom-rings">'
        '<div class="ring"></div><div class="ring"></div><div class="ring"></div>'
        '</div>'
    ),
    "dark": (
        '<div class="pw-wrap"><div class="pw-grid"></div></div>\n'
        '    <div class="glow-orb"></div>'
    ),
    "brutalist": '<div class="grid-bg"></div>',
    "light": '<div class="diag-band"></div>',
    "warm": (
        '<div class="blob-bg"></div>\n'
        '    <div class="vol-light"></div>'
    ),
}

# Individual layer HTML — used when a slide spec overrides via copy.layers.
# Lets us mix and match per slide instead of one set per system.
LAYER_HTML = {
    # Existing
    "pw-grid":         '<div class="pw-wrap"><div class="pw-grid"></div></div>',
    "scan-lines":      '<div class="scan-lines"></div>',
    "glow-orb":        '<div class="glow-orb"></div>',
    "zoom-rings":      '<div class="zoom-rings"><div class="ring"></div><div class="ring"></div><div class="ring"></div></div>',
    "grid-bg":         '<div class="grid-bg"></div>',
    "diag-band":       '<div class="diag-band"></div>',
    "blob-bg":         '<div class="blob-bg"></div>',
    "vol-light":       '<div class="vol-light"></div>',
    # New Tier 1
    "geo-mesh-noise":  '<div class="geo-mesh-noise"></div>',
    "geo-pixel-grid":  '<div class="geo-pixel-grid"></div>',
    "geo-conic-rays":  '<div class="geo-conic-rays"></div>',
    "geo-chevron-stripe":'<div class="geo-chevron-stripe"></div>',
    "geo-iso-grid":    '<div class="geo-iso-grid"></div>',
    "geo-paper-texture":'<div class="geo-paper-texture"></div>',
    "geo-halftone":    '<div class="geo-halftone"></div>',
    "geo-ribbon-flow": '<div class="geo-ribbon-flow"></div>',
    "geo-circuit-trace":'<div class="geo-circuit-trace"><div class="node n1"></div><div class="node n2"></div><div class="node n3"></div></div>',
    "geo-topo-lines":  '<div class="geo-topo-lines"></div>',
    "geo-starfield":   '<div class="geo-starfield"></div>',
    "geo-gradient-bands":'<div class="geo-gradient-bands"></div>',
    # v2 — SVG organic blob layers (replace ellipse blob-bg). Accent hex substituted at render time.
    "svg-blob-tr":          '<div class="svg-blob svg-blob-tr"></div>',
    "svg-blob-bl":          '<div class="svg-blob svg-blob-bl"></div>',
    "svg-blob-center":      '<div class="svg-blob svg-blob-center"></div>',
    "svg-blob-asymmetric":  '<div class="svg-blob svg-blob-asymmetric"></div>',
    "svg-blob-scattered":   '<div class="svg-blob svg-blob-scattered"></div>',
    # v3 — New blob shapes (angular, crystal, wave, arch, splatter, ribbon)
    "svg-blob-angular":     '<div class="svg-blob svg-blob-angular"></div>',
    "svg-blob-crystal":     '<div class="svg-blob svg-blob-crystal"></div>',
    "svg-blob-wave":        '<div class="svg-blob svg-blob-wave"></div>',
    "svg-blob-arch":        '<div class="svg-blob svg-blob-arch"></div>',
    "svg-blob-splatter":    '<div class="svg-blob svg-blob-splatter"></div>',
    "svg-blob-ribbon":      '<div class="svg-blob svg-blob-ribbon"></div>',
    # v3 — Cross-slide flow layers
    "geo-flow-wave":        '<div class="geo-flow-wave"></div>',
    "geo-flow-arrow":       '<div class="geo-flow-arrow"></div>',
    "geo-flow-data":        '<div class="geo-flow-data"><div class="node n1"></div><div class="node n2"></div><div class="node n3"></div><div class="node n4"></div></div>',
    # Phase 1 — contour flow layer ( flowing terrain lines )
    "geo-contour-flow": '<svg viewBox="0 0 1080 1080" class="geo-layer geo-contour-flow" preserveAspectRatio="none"><g opacity="0.35"><path d="M0,200 Q270,100 540,200 Q810,300 1080,200" fill="none" stroke="var(--accent)" stroke-width="1"/><path d="M0,280 Q270,180 540,280 Q810,380 1080,280" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.7"/><path d="M0,360 Q270,260 540,360 Q810,460 1080,360" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.5"/><path d="M0,440 Q270,340 540,440 Q810,540 1080,440" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.35"/><path d="M0,520 Q270,420 540,520 Q810,620 1080,520" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.2"/><path d="M0,600 Q270,500 540,600 Q810,700 1080,600" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.1"/><path d="M0,680 Q270,580 540,680 Q810,780 1080,680" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.06"/></g></svg>',
    # Phase 2 — new geo layers
    "geo-perspective-grid": '<div class="geo-layer perspective-grid"></div>',
    "geo-hex-mesh": '<svg viewBox="0 0 1080 1080" class="geo-layer geo-hex" preserveAspectRatio="none"><defs><pattern id="hexPattern" x="0" y="0" width="52" height="90" patternUnits="userSpaceOnUse"><path d="M26,0 L52,15 L52,45 L26,60 L0,45 L0,15 Z" fill="none" stroke="var(--accent)" stroke-width="0.5" opacity="0.12"/></pattern></defs><rect width="100%" height="100%" fill="url(#hexPattern)"/></svg>',
    "geo-constellation": '<svg viewBox="0 0 1080 1080" class="geo-layer geo-constellation"><g stroke="var(--accent)" stroke-width="0.5" opacity="0.2"><line x1="100" y1="200" x2="250" y2="180"/><line x1="250" y1="180" x2="400" y2="300"/><line x1="400" y1="300" x2="550" y2="250"/><line x1="550" y1="250" x2="700" y2="350"/><line x1="700" y1="350" x2="850" y2="280"/><line x1="200" y1="400" x2="350" y2="380"/><line x1="350" y1="380" x2="500" y2="480"/><line x1="500" y1="480" x2="650" y2="420"/><line x1="150" y1="600" x2="300" y2="580"/><line x1="300" y1="580" x2="450" y2="650"/></g><g fill="var(--accent)"><circle cx="100" cy="200" r="3" opacity="0.7"/><circle cx="250" cy="180" r="4" opacity="0.9"/><circle cx="400" cy="300" r="3" opacity="0.6"/><circle cx="550" cy="250" r="4" opacity="0.8"/><circle cx="700" cy="350" r="3" opacity="0.7"/><circle cx="850" cy="280" r="3.5" opacity="0.8"/><circle cx="200" cy="400" r="3" opacity="0.6"/><circle cx="350" cy="380" r="4" opacity="0.9"/><circle cx="500" cy="480" r="3" opacity="0.7"/><circle cx="650" cy="420" r="3.5" opacity="0.8"/><circle cx="150" cy="600" r="3" opacity="0.6"/><circle cx="300" cy="580" r="4" opacity="0.9"/><circle cx="450" cy="650" r="3" opacity="0.7"/></g></svg>',
    "geo-neon-ring": '<svg viewBox="0 0 400 400" class="geo-layer geo-neon-ring"><circle cx="200" cy="200" r="160" fill="none" stroke="var(--accent)" stroke-width="24" opacity="0.06"/><circle cx="200" cy="200" r="150" fill="none" stroke="var(--accent)" stroke-width="10" opacity="0.15"/><circle cx="200" cy="200" r="140" fill="none" stroke="var(--accent)" stroke-width="3" opacity="0.8"/><circle cx="200" cy="200" r="130" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.25"/></svg>',
    "geo-bokeh": '<div class="geo-layer bokeh-container"><div class="bokeh-orb" style="width:220px;height:220px;top:8%;left:12%"></div><div class="bokeh-orb" style="width:320px;height:320px;top:45%;left:55%"></div><div class="bokeh-orb" style="width:160px;height:160px;top:70%;left:18%"></div><div class="bokeh-orb" style="width:200px;height:200px;top:25%;left:75%"></div></div>',
    "geo-scan-lines": '<div class="geo-layer geo-scan-lines"></div>',
    # Phase 3 — additional static-SVG-compatible geo layers
    "geo-chromatic-edge": '<div class="geo-layer geo-chromatic-edge"><div class="chromatic-left"></div><div class="chromatic-right"></div></div>',
    "geo-data-streaks": '<svg viewBox="0 0 1080 1080" class="geo-layer geo-data-streaks" preserveAspectRatio="none"><g stroke="var(--accent)" stroke-width="1" opacity="0.18"><line x1="-100" y1="200" x2="200" y2="-100"/><line x1="-100" y1="350" x2="350" y2="-100" opacity="0.6"/><line x1="-100" y1="500" x2="500" y2="-100" opacity="0.3"/><line x1="-100" y1="650" x2="650" y2="-100" opacity="0.8"/><line x1="-100" y1="800" x2="800" y2="-100" opacity="0.4"/><line x1="-100" y1="950" x2="950" y2="-100" opacity="0.5"/><line x1="-100" y1="1100" x2="1100" y2="-100" opacity="0.2"/><line x1="200" y1="1100" x2="1100" y2="200" opacity="0.7"/><line x1="400" y1="1100" x2="1100" y2="400" opacity="0.3"/><line x1="600" y1="1100" x2="1100" y2="600" opacity="0.6"/><line x1="800" y1="1100" x2="1100" y2="800" opacity="0.4"/><line x1="1000" y1="1100" x2="1100" y2="1000" opacity="0.5"/></g></svg>',
    "geo-liquid-morph": '<svg viewBox="0 0 1080 1080" class="geo-layer geo-liquid-morph" preserveAspectRatio="none"><defs><filter id="liquidFilter"><feGaussianBlur in="SourceGraphic" stdDeviation="24" result="blur"/><feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="goo"/><feComposite in="SourceGraphic" in2="goo" operator="atop"/></filter></defs><g filter="url(#liquidFilter)"><circle cx="350" cy="350" r="140" fill="var(--accent)" opacity="0.25"/><circle cx="550" cy="280" r="120" fill="var(--accent)" opacity="0.2"/><circle cx="450" cy="500" r="160" fill="var(--accent)" opacity="0.18"/><circle cx="700" cy="450" r="100" fill="var(--accent)" opacity="0.22"/><circle cx="280" cy="600" r="130" fill="var(--accent)" opacity="0.15"/><circle cx="620" cy="650" r="110" fill="var(--accent)" opacity="0.2"/></g></svg>',
    "geo-chromatic-edge": '<div class="geo-layer geo-chromatic-edge"></div>',
    "geo-data-streaks": '<svg viewBox="0 0 1080 1080" class="geo-layer geo-data-streaks" preserveAspectRatio="none"><g stroke="var(--accent)" stroke-width="0.5" opacity="0.15"><line x1="0" y1="200" x2="200" y2="0" opacity="0.12"/><line x1="0" y1="400" x2="400" y2="0" opacity="0.08"/><line x1="0" y1="600" x2="600" y2="0" opacity="0.15"/><line x1="0" y1="800" x2="800" y2="0" opacity="0.06"/><line x1="0" y1="1000" x2="1000" y2="0" opacity="0.10"/><line x1="200" y1="1080" x2="1080" y2="200" opacity="0.12"/><line x1="400" y1="1080" x2="1080" y2="400" opacity="0.08"/><line x1="600" y1="1080" x2="1080" y2="600" opacity="0.15"/><line x1="800" y1="1080" x2="1080" y2="800" opacity="0.06"/><line x1="100" y1="1080" x2="1080" y2="100" opacity="0.10"/><line x1="300" y1="1080" x2="1080" y2="300" opacity="0.07"/><line x1="500" y1="1080" x2="1080" y2="500" opacity="0.13"/><line x1="700" y1="1080" x2="1080" y2="700" opacity="0.09"/><line x1="900" y1="1080" x2="1080" y2="900" opacity="0.11"/><line x1="150" y1="0" x2="0" y2="150" opacity="0.08"/><line x1="350" y1="0" x2="0" y2="350" opacity="0.14"/><line x1="550" y1="0" x2="0" y2="550" opacity="0.06"/><line x1="750" y1="0" x2="0" y2="750" opacity="0.10"/><line x1="950" y1="0" x2="0" y2="950" opacity="0.12"/></g></svg>',
    "geo-liquid-morph": '<svg viewBox="0 0 1080 1080" class="geo-layer geo-liquid-morph" preserveAspectRatio="none"><defs><filter id="liquidBlur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur in="SourceGraphic" stdDeviation="20"/></filter></defs><g filter="url(#liquidBlur)" fill="var(--accent)" opacity="0.10"><circle cx="300" cy="400" r="180"/><circle cx="500" cy="350" r="220"/><circle cx="450" cy="600" r="160"/><circle cx="700" cy="500" r="200"/><circle cx="250" cy="700" r="140"/></g></svg>',
}

# v2 — text_treatment → CSS class mapping. Templates check copy.text_treatment
# and apply the corresponding class to the headline / display element.
TEXT_TREATMENT_CLASS = {
    "gradient":       "txt-gradient",
    "glow":           "txt-glow-medium",
    "glow-subtle":    "txt-glow-subtle",
    "glow-medium":    "txt-glow-medium",
    "glow-bold":      "txt-glow-bold",
    "stroke":         "txt-stroke",
    "stroke-filled":  "txt-stroke-filled",
}


# ── Decorative element HTML ────────────────────────────────────────────────────
# Keyed by ID from slide spec "decoratives" array.
# Parameterized entries ("watermark", "sub-stamp-circle") handled in resolve_decoratives().

DECORATIVE_HTML = {
    "corner-frame": (
        '<div class="deco-corner-tl"></div>\n    '
        '<div class="deco-corner-br"></div>'
    ),
    "ornament-tr":  '<div class="deco-ornament deco-ornament-tr">✦ ✧ ✦</div>',
    "ornament-bl":  '<div class="deco-ornament deco-ornament-bl">✦ ✧ ✦</div>',
    "ornament":     '<div class="deco-ornament deco-ornament-tr">✦ ✧ ✦</div>',
    "chrome-vertical-counter": '<div class="chrome-vertical-counter">WORQAI 2026</div>',
    "chrome-header-bar": (
        '<div class="chrome-header-bar">'
        '<span class="header-logo">WorqAI</span>'
        '<span class="header-date">2026</span>'
        '</div>'
    ),
    # chrome-badge-stamp is rendered dynamically in resolve_decoratives() — keep
    # an empty placeholder here so introspection still lists it as a known ID.
    "chrome-badge-stamp": "__dynamic__",
    # v2 — SVG starbursts (replace unicode ✦✧✦ ornament). All position-aware via class suffix.
    # "svg-starburst-*" handled dynamically in resolve_decoratives() so position can be overridden.
    "svg-starburst-spark":  "__dynamic__",
    "svg-starburst-burst":  "__dynamic__",
    "svg-starburst-mark":   "__dynamic__",
    # v3 — Glassmorphism panel decorative
    "deco-glass-panel": '<div class="glass-panel" style="position:absolute;top:64px;right:64px;width:200px;height:120px;z-index:9;"></div>',
}


# ── v2: SVG starburst variants ─────────────────────────────────────────────────
# Inline SVG. Uses currentColor → inherits from CSS .deco-starburst color (var(--accent)).

SVG_STARBURST = {
    "spark": (
        '<svg viewBox="0 0 100 100" aria-hidden="true">'
        '<g transform="translate(50,50)" fill="currentColor">'
        '<polygon points="0,-32 6,-10 28,-6 11,6 17,28 0,16 -17,28 -11,6 -28,-6 -6,-10"/>'
        '</g></svg>'
    ),
    "burst": (
        '<svg viewBox="0 0 100 100" aria-hidden="true">'
        '<g transform="translate(50,50)" fill="currentColor">'
        '<polygon points="0,-40 8,-12 36,-8 14,8 22,36 0,20 -22,36 -14,8 -36,-8 -8,-12" opacity="0.6"/>'
        '<polygon points="0,-25 5,-8 22,-5 9,5 14,22 0,12 -14,22 -9,5 -22,-5 -5,-8" opacity="0.95" transform="rotate(22.5)"/>'
        '</g></svg>'
    ),
    "mark": (
        '<svg viewBox="0 0 100 100" aria-hidden="true">'
        '<g transform="translate(50,50)" fill="currentColor" opacity="0.85">'
        # 16 thin triangles radiating out, alternating long/short
        + "".join(
            f'<polygon points="0,-{38 if i % 2 == 0 else 22} 2,-4 -2,-4" '
            f'transform="rotate({i * 22.5})"/>'
            for i in range(16)
        )
        + '</g></svg>'
    ),
}


# ── Decorative rotation — prevents identical decoratives on every slide ───────
# Cycles through when a slide spec has no explicit "decoratives" key.
# Rule: no decorative may appear on more than 2 consecutive slides (enforced by design here).
DECORATIVE_ROTATION = [
    ["corner-frame", {"id": "svg-starburst-spark", "position": "tr"}],
    [{"id": "watermark", "text": "•"}],
    [{"id": "chrome-badge-stamp"}],
    [{"id": "svg-starburst-burst", "position": "bl"}, {"id": "sub-stamp-circle"}],
    ["chrome-vertical-counter"],
    ["corner-frame"],
    [{"id": "svg-starburst-mark", "position": "tl"}],
]


def _brand_label(brand: str) -> str:
    """Strip leading @ from brand handles and uppercase for stamp labels."""
    return (brand or "").lstrip("@").upper() or "BRAND"


def resolve_geo(
    slide_spec: dict,
    system_type: str,
    system_id: str = "",
    slide_num: int = 1,
    bg_recipe: str | None = None,
) -> str:
    """Slide can override via copy.layers (list of layer IDs or {id, animate?, ...} dicts);
    otherwise use system default.

    v2: layer entries may be dicts: {"id": "svg-blob-tr", "animate": true}.
    Drift class is added when animate=true.

    v3: Supports AI-generated backgrounds from manifest.json (layer IDs starting with 'ai-').

    v4: Supports per-slide recipe progressions — passes slide_num + bg_recipe to resolve_ai_bg.
    """
    layers_override = slide_spec.get("layers") or slide_spec.get("copy", {}).get("layers")
    if not layers_override:
        return GEO_HTML.get(system_type, GEO_HTML["dark"])

    parts = []
    for entry in layers_override:
        if isinstance(entry, str):
            name, animate = entry, False
        elif isinstance(entry, dict):
            name = entry.get("id", "")
            animate = bool(entry.get("animate") or entry.get("drift"))
        else:
            continue
        html = LAYER_HTML.get(name)
        if not html:
            # v3/v4: AI-generated backgrounds from manifest — slide-aware
            html = resolve_ai_bg(name, system_id, slide_num, bg_recipe)
        if not html:
            continue
        # v2: opt-in animation on SVG blob layers

        parts.append(html)
    return "\n    ".join(parts)


def resolve_continuity(slide_num: int, total: int, continuity) -> str:
    """Generate per-slide continuity HTML based on meta.continuity mode.

    Supports:
    - str: legacy modes ("wave", "data-pipeline", "corner-frame-evolution", "number-escalator")
    - dict: blob continuity with shape path and per-slide transforms

    Continuity creates visual narrative threads across slides.
    Returns HTML string to inject into slide_geo.
    """
    if not continuity:
        return ""

    # Dict-based blob continuity (Phase 2) — same shape, different transform per slide
    if isinstance(continuity, dict):
        positions = continuity.get("positions", [])
        # Find position for this slide (slide_num is 1-based)
        pos = next((p for p in positions if p.get("slide") == slide_num), None)
        if not pos:
            return ""
        path = continuity.get("path", "")
        if not path:
            return ""
        transform = pos.get("transform", "")
        opacity = pos.get("opacity", 0.1)
        return (
            f'<svg class="continuity-shape" viewBox="0 0 600 600" '
            f'style="position:absolute;{transform};opacity:{opacity};'
            f'z-index:0;pointer-events:none;">'
            f'<path d="{path}" fill="var(--accent)" opacity="0.8"/></svg>'
        )

    if continuity == "wave":
        phase = (slide_num - 1) * 90
        return f'<div class="geo-flow-wave flow-phase-{phase}"></div>'

    if continuity == "data-pipeline":
        # Nodes light up progressively
        visible = min(slide_num + 1, 4)
        nodes_html = "".join(
            f'<div class="node n{i}"></div>' for i in range(1, visible + 1)
        )
        return f'<div class="geo-flow-data continuity-pipeline" data-visible="{visible}">{nodes_html}</div>'

    if continuity == "corner-frame-evolution":
        size = 28 + (slide_num * 14)
        opacity = 0.15 + (slide_num * 0.06)
        return (
            f'<div class="deco-corner-tl" style="width:{size}px;height:{size}px;opacity:{opacity:.2f}"></div>\n    '
            f'<div class="deco-corner-br" style="width:{size}px;height:{size}px;opacity:{opacity:.2f}"></div>'
        )

    if continuity == "number-escalator":
        num = f"{slide_num:02d}"
        return f'<div class="deco-watermark" style="opacity:0.06">{num}</div>'

    return ""


def resolve_decoratives(slide_spec: dict, brand: str = "@worqai", language: str = "en") -> str:
    """Build HTML for slide decorative elements from spec 'decoratives' list.

    `brand` is passed so brand-aware decoratives (chrome-badge-stamp,
    chrome-vertical-counter, chrome-header-bar, sub-stamp-circle default text)
    use the current carousel's brand instead of a hardcoded "WORQAI".

    `language` controls the localised default for the stamp value — "FREE" in
    English carousels, "GRATIS" in Spanish ones. Explicit `value`/`text` in
    the spec always wins.
    """
    items = slide_spec.get("decoratives") or []
    if not items:
        return ""
    brand_label = _brand_label(brand)
    free_default = "GRATIS" if language.lower().startswith("es") else "FREE"
    parts = []
    for d in items:
        if isinstance(d, str):
            d_id, d_text, d_value = d, None, None
        elif isinstance(d, dict):
            d_id = d.get("id", "")
            d_text = d.get("text")
            d_value = d.get("value")
        else:
            continue

        if d_id == "watermark":
            text = d_text or "W"
            parts.append(f'<div class="deco-watermark">{text}</div>')
        elif d_id == "sub-stamp-circle":
            text = d_text or brand_label
            inner = text.replace(" ", "<br>", 1) if " " in text else text
            parts.append(
                f'<div class="deco-stamp"><span class="deco-stamp-inner">{inner}</span></div>'
            )
        elif d_id == "chrome-badge-stamp":
            label = d_text or brand_label
            value = d_value or free_default
            parts.append(
                f'<div class="chrome-badge-stamp">'
                f'<span class="stamp-label">{label}</span>'
                f'<span class="stamp-value">{value}</span>'
                f'</div>'
            )
        elif d_id == "chrome-vertical-counter":
            text = d_text or f"{brand_label} 2026"
            parts.append(f'<div class="chrome-vertical-counter">{text}</div>')
        elif d_id == "chrome-header-bar":
            logo = d_text or brand_label.title()
            year = d_value or "2026"
            parts.append(
                f'<div class="chrome-header-bar">'
                f'<span class="header-logo">{logo}</span>'
                f'<span class="header-date">{year}</span>'
                f'</div>'
            )
        elif d_id.startswith("svg-starburst-"):
            # v2: SVG starburst with optional position (tr default, also tl/br/bl)
            variant = d_id.replace("svg-starburst-", "") or "burst"
            svg = SVG_STARBURST.get(variant, SVG_STARBURST["burst"])
            position = "tr"
            if isinstance(d, dict):
                position = d.get("position", "tr") or "tr"
            parts.append(
                f'<div class="deco-starburst deco-starburst-{position} '
                f'deco-starburst-{variant}">{svg}</div>'
            )
        elif d_id in DECORATIVE_HTML and DECORATIVE_HTML[d_id] != "__dynamic__":
            parts.append(DECORATIVE_HTML[d_id])

    return "\n    ".join(parts)


# ── v2: text_treatment + effects helpers ───────────────────────────────────────

def resolve_text_treatment(copy: dict) -> str:
    """Map copy.text_treatment string to a CSS class (empty if unset/invalid)."""
    tt = (copy.get("text_treatment") or "").strip()
    return TEXT_TREATMENT_CLASS.get(tt, "")


def resolve_effects(slide_spec: dict) -> dict:
    """Normalised effects dict for the slide. All keys always present."""
    fx = slide_spec.get("effects") or {}
    return {
        "shadow":                     (fx.get("shadow") or "").strip(),
        "grain_opacity":              fx.get("grain_opacity"),  # None means inherit
        "requires_playwright_export": bool(fx.get("requires_playwright_export")),
    }

ASPECT_CSS = {
    "1:1": "",
    "4:5": (
        ".wrap { aspect-ratio: 4 / 5; }\n"
        ".viewer { max-width: 432px; }\n"
        ".hook-display { font-size: clamp(28px,6cqw,36px); }\n"
        ".stat-num { font-size: clamp(36px,8cqw,48px); }\n"
        ".slide { padding: 64px 56px 120px; }"
    ),
    "9:16": (
        ".wrap { aspect-ratio: 9 / 16; }\n"
        ".viewer { max-width: 320px; }\n"
        ".slide { padding-top: 180px; padding-bottom: 220px; }"
    ),
}


# ── Token loading ──────────────────────────────────────────────────────────────

def load_tokens(system_id: str) -> dict:
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        tokens = data.get("systems", {}).get(system_id)
        if tokens:
            # Ensure text-muted exists
            if "--text-muted" not in tokens:
                tokens["--text-muted"] = "rgba(255,255,255,0.28)"
            return tokens
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    print(f"WARN: No token data for system '{system_id}', using defaults.", file=sys.stderr)
    return DEFAULT_TOKENS.copy()


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    if len(h) != 6:
        return "255, 255, 255"
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r}, {g}, {b}"


def build_css_vars(tokens: dict) -> str:
    return "\n".join(f"    {k}: {v};" for k, v in tokens.items())


def build_fonts_url(system_id: str) -> str:
    # All 48 systems use the same 16-family universal URL (see UNIVERSAL_FONTS_URL above).
    # system_id kept as param for backward compatibility; not used for routing.
    return UNIVERSAL_FONTS_URL


# ── Render engine ──────────────────────────────────────────────────────────────

def render_carousel(spec: dict, output_path: Path) -> None:
    meta = spec["meta"]
    system_id = meta.get("system", "s17")
    brand = meta.get("brand", "@worqai")
    language = meta.get("language", "en")
    total = int(meta.get("slides", len(spec["slides"])))
    aspect = meta.get("aspect", "1:1")
    pacing = spec.get("pacing", [])
    continuity = meta.get("continuity", "")

    tokens = load_tokens(system_id)
    css_vars = build_css_vars(tokens)
    # Derive --accent-rgb and --bg-base-rgb for rgba() usage in overlays, glassmorphism, etc.
    accent_hex = tokens.get("--accent", "#ffffff")
    if accent_hex.startswith("#"):
        css_vars += f"\n    --accent-rgb: {_hex_to_rgb(accent_hex)};"
    bg_base_hex = tokens.get("--bg-base", "#0a0a12")
    if bg_base_hex.startswith("#"):
        css_vars += f"\n    --bg-base-rgb: {_hex_to_rgb(bg_base_hex)};"
    system_type = SYSTEM_TYPES.get(system_id, "dark")
    is_light = system_id in LIGHT_SYSTEMS
    # Light systems: SVG blob opacity baked into data URL — must be set at render time.
    # CSS filters can't fix opacity values inside SVG path attributes.
    blob_op = (
        {"tr": "0.55", "bl": "0.50", "center": "0.33", "asym": "0.60",
         "sc1": "0.38", "sc2": "0.28", "sc3": "0.33",
         "ang": "0.45", "cry": "0.50", "wav": "0.40", "arc": "0.48",
         "spl": "0.35", "rib": "0.42"}
        if is_light else
        {"tr": "0.20", "bl": "0.18", "center": "0.12", "asym": "0.22",
         "sc1": "0.14", "sc2": "0.10", "sc3": "0.12",
         "ang": "0.18", "cry": "0.20", "wav": "0.16", "arc": "0.18",
         "spl": "0.14", "rib": "0.16"}
    )
    fonts_url = build_fonts_url(system_id)
    aspect_css = ASPECT_CSS.get(aspect, "")
    # v4: per-slide recipe background progression
    bg_recipe: str | None = meta.get("bg_recipe")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=Undefined,
        autoescape=False,
    )

    slides_html_parts = []
    custom_css_parts = []
    for i, slide_spec in enumerate(spec["slides"]):
        slide_num = i + 1
        layout = slide_spec.get("layout", "slide-tip-blocks")
        is_active = slide_num == 1
        beat = pacing[i] if i < len(pacing) else ""
        is_silence = slide_spec.get("constraints", {}).get("silence", False) or beat == "silence"

        # Phase 4: warn if a forbidden layout is used for this system family
        personality = SYSTEM_PERSONALITY.get(system_type, {})
        if layout in personality.get("forbidden", []):
            print(
                f"WARN slide {slide_num}: '{layout}' is in the forbidden list for "
                f"'{system_type}' systems. Consider: {personality.get('preferred', [])[:3]}",
                file=sys.stderr,
            )

        try:
            tmpl = env.get_template(f"slides/{layout}.html")
        except Exception:
            print(f"WARN: Template 'slides/{layout}.html' not found, using slide-tip-blocks.", file=sys.stderr)
            tmpl = env.get_template("slides/slide-tip-blocks.html")

        slide_geo = resolve_geo(slide_spec, system_type, system_id, slide_num, bg_recipe)

        # v3: continuity layers override decorative rotation
        continuity_html = resolve_continuity(slide_num, total, continuity)
        if continuity_html:
            slide_geo = slide_geo + "\n    " + continuity_html

        if not is_silence:
            effective_spec = slide_spec
            if not continuity and "decoratives" not in slide_spec:
                # Apply rotation-based defaults when no continuity and no explicit decoratives
                rot_idx = i % len(DECORATIVE_ROTATION)
                effective_spec = dict(slide_spec)
                effective_spec["decoratives"] = DECORATIVE_ROTATION[rot_idx]
            slide_decoratives = resolve_decoratives(effective_spec, brand=brand, language=language)
            if slide_decoratives:
                slide_geo = slide_geo + "\n    " + slide_decoratives

        custom_css = slide_spec.get("custom_css", "").strip()
        if custom_css:
            custom_css_parts.append(f"/* ── slide {slide_num} bespoke ── */\n{custom_css}")

        # Normalise terminal command: strip a leading "$ " (or "$") that authors
        # sometimes type by habit, since the template already renders the prompt.
        slide_copy = dict(slide_spec.get("copy", {}))
        if "command" in slide_copy and isinstance(slide_copy["command"], str):
            cmd = slide_copy["command"].lstrip()
            while cmd.startswith("$"):
                cmd = cmd[1:].lstrip()
            slide_copy["command"] = cmd

        # v2: resolve text_treatment + effects so templates can opt in
        text_treatment_class = resolve_text_treatment(slide_copy)
        effects = resolve_effects(slide_spec)

        # v2: SVG gradient text uses a per-slide gradient ID so multiple slides
        # don't collide on the same fragment identifier.
        gradient_id = f"g-{slide_num}" if text_treatment_class == "txt-gradient" else ""

        slide_html = tmpl.render(
            copy=slide_copy,
            slide_num=slide_num,
            total=total,
            brand=brand,
            is_active=is_active,
            is_silence=is_silence,
            beat=beat,
            system_type=system_type,
            geo_html=slide_geo,
            text_treatment_class=text_treatment_class,
            effects=effects,
            gradient_id=gradient_id,
        )

        # v4: inject data-density attribute for AI background scrim control
        # density values: "heavy" (hook/stat/cta), "demo" (terminal/IO/waffle), "cta"
        # Default (no attribute) = medium scrim (0.52)
        density = slide_spec.get("density", "")
        if density:
            idx = slide_html.find('<div class="slide')
            if idx >= 0:
                end_tag = slide_html.find('>', idx)
                if end_tag > 0:
                    slide_html = (slide_html[:end_tag]
                                  + f' data-density="{density}"'
                                  + slide_html[end_tag:])

        # v3: inject raw HTML extras (e.g. glass-panel wrappers) if specified
        extras = slide_spec.get("extras")
        if extras:
            parts = slide_html.split('<div class="slide')
            if len(parts) >= 2:
                slide_body = parts[1]
                gt = slide_body.find('>')
                if gt > 0:
                    slide_body = slide_body[:gt+1] + "\n  " + extras + "\n" + slide_body[gt+1:]
                    parts[1] = slide_body
                    slide_html = '<div class="slide'.join(parts)

        slides_html_parts.append(slide_html)

    slides_html = "\n\n".join(slides_html_parts)
    custom_css_block = "\n\n".join(custom_css_parts)

    topic = meta.get("topic", "carousel")
    title = f"{topic} · {total} slides · {system_id}"

    # v2: Extract accent hex for SVG data URL substitution (SVG data URLs
    # can't reference CSS variables, so we URL-encode the system accent here).
    accent_hex = tokens.get("--accent", "#C7FF3A").lstrip("#")
    accent_hex_enc = "%23" + accent_hex  # URL-encoded '#' for use inside data URLs

    shell_tmpl = env.get_template("carousel-shell.html")
    final_html = shell_tmpl.render(
        title=title,
        fonts_url=fonts_url,
        css_vars=css_vars,
        aspect_css=aspect_css,
        system_id=system_id,
        system_type=system_type,
        is_light=is_light,
        total=total,
        brand=brand,
        slides_html=slides_html,
        custom_css_block=custom_css_block,
        accent_hex=accent_hex,
        accent_hex_enc=accent_hex_enc,
        blob_op=blob_op,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_html, encoding="utf-8")

    size_kb = output_path.stat().st_size / 1024
    print(f"[OK]  {output_path.name}")
    print(f"      {size_kb:.1f} KB  {total} slides  system {system_id}")
    print()
    print(f"  QA:     py scripts/preflight.py {output_path}")
    print(f"  Stats:  py scripts/stat_source_validator.py {output_path}")
    print(f"  Export: py scripts/carousel_exporter.py --input {output_path} --output export/")


def main():
    parser = argparse.ArgumentParser(description="Render carousel HTML from spec JSON")
    parser.add_argument("spec", help="Path to carousel-spec.json")
    parser.add_argument("--output", "-o", help="Output HTML path")
    parser.add_argument("--validate-only", action="store_true", help="Validate spec without rendering")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: Spec not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    required = {"meta", "slides"}
    missing = required - spec.keys()
    if missing:
        print(f"ERROR: Spec missing required keys: {missing}", file=sys.stderr)
        sys.exit(1)

    if args.validate_only:
        sid = spec["meta"].get("system", "?")
        n = len(spec["slides"])
        print(f"[OK] Valid spec: {n} slides, system {sid}")
        sys.exit(0)

    if args.output:
        output_path = Path(args.output)
    else:
        sid = spec["meta"].get("system", "s17")
        topic = spec["meta"].get("topic", "carousel").lower().replace(" ", "-")
        output_path = PRODUCTION_DIR / f"carousel_{topic}_{sid}.html"

    render_carousel(spec, output_path)


if __name__ == "__main__":
    main()
