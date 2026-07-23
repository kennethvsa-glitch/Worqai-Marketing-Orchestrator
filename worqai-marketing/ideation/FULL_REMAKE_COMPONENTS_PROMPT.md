# PASTE THIS ENTIRE FILE INTO CLAUDE

---

## CONTEXT

The user wants ALL 124+ components upgraded to premium quality. Not ~15, not ~30 — ALL of them. Mid-tier components dragging down premium ones in random carousel combinations is unacceptable.

The approach: DON'T hand-edit 124 files. Instead:
1. Build **premium utility CSS classes** in carousel-shell.html (global)
2. Write a **Python batch script** that upgrades component templates by category
3. Every component category gets its own **upgrade rule set**
4. Run the batch, rebuild gallery

---

## PHASE 0: GLOBAL PREMIUM CSS UTILITIES

Add these to `carousel-shell.html` BEFORE any component-specific styles. Every component will use them.

```css
/* ════════════════════════════════════════════════════════════════
   PREMIUM SYSTEM — Global Utilities (ALL components use these)
   ════════════════════════════════════════════════════════════════ */

/* ── 1. HEADLINE SYSTEM ──────────────────────────────────────────── */
/* Use on any large headline text */
.headline-premium {
  font-family: 'Cormorant Garamond', 'Playfair Display', var(--font-display), serif;
  font-weight: 500;
  line-height: 0.94;
  letter-spacing: -0.03em;
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.06);
}
/* For light-background systems */
.light-system .headline-premium {
  color: rgba(0, 0, 0, 0.88);
  text-shadow: none;
}

/* Accent word within headline */
.headline-accent {
  color: #42F5FF;
  font-style: italic;
  text-shadow: 0 0 20px rgba(66, 245, 255, 0.14);
}

/* ── 2. LABEL SYSTEM ─────────────────────────────────────────────── */
/* Use on ALL uppercase labels, kickers, tags, mastheads */
.label-premium {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  font-weight: 500;
  color: var(--accent);
}
.label-premium::before {
  content: '';
  display: inline-block;
  width: 20px;
  height: 1px;
  background: var(--accent);
  margin-right: 10px;
  vertical-align: middle;
  opacity: 0.5;
}
/* Label without the line prefix */
.label-premium-plain {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  font-size: 11px;
  letter-spacing: 0.20em;
  text-transform: uppercase;
  font-weight: 500;
}

/* ── 3. BODY TEXT SYSTEM ─────────────────────────────────────────── */
/* Use on paragraph/body text */
.body-premium {
  font-family: var(--font-body);
  font-size: clamp(14px, 2.5cqw, 18px);
  font-weight: 400;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.58);
}
.light-system .body-premium {
  color: rgba(0, 0, 0, 0.58);
}

/* ── 4. GLASSMORPHISM SYSTEM ────────────────────────────────────── */
/* Use on ANY card, panel, box, container */
.glass-premium {
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 24px; /* generous radius */
  overflow: hidden;
}
/* For smaller elements (tags, pills) */
.glass-premium-sm {
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.10);
  border-radius: 12px;
}
/* Light system variant */
.light-system .glass-premium,
.light-system .glass-premium-sm {
  background: linear-gradient(180deg, rgba(0,0,0,0.03), rgba(0,0,0,0.01));
  border-color: rgba(0, 0, 0, 0.08);
}

/* ── 5. GLOW SYSTEM ──────────────────────────────────────────────── */
/* Multi-layer ambient glow — use on CTA buttons, active elements */
.glow-premium {
  box-shadow:
    0 0 10px rgba(var(--accent-rgb), 0.55),
    0 0 30px rgba(var(--accent-rgb), 0.22),
    0 15px 40px rgba(var(--accent-rgb), 0.12),
    inset 0 0 20px rgba(255, 255, 255, 0.03);
}
/* Ambient only (for panels, cards) */
.glow-ambient {
  box-shadow: 0 0 40px rgba(var(--accent-rgb), 0.10);
}
/* Hover intensification */
.glow-premium:hover {
  box-shadow:
    0 0 20px rgba(var(--accent-rgb), 0.70),
    0 0 50px rgba(var(--accent-rgb), 0.30),
    0 20px 60px rgba(var(--accent-rgb), 0.18),
    inset 0 0 30px rgba(255, 255, 255, 0.06);
}

/* ── 6. DIVIDER SYSTEM ───────────────────────────────────────────── */
/* Use between list items, table rows, card sections */
.divider-premium {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}
.light-system .divider-premium {
  background: linear-gradient(90deg, transparent, rgba(0,0,0,0.06), transparent);
}

/* ── 7. BUTTON SYSTEM ────────────────────────────────────────────── */
/* Use on ALL CTA buttons, action buttons */
.btn-premium {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  color: var(--accent);
  font-family: 'Space Grotesk', var(--font-display), sans-serif;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  text-decoration: none;
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1.5px solid rgba(var(--accent-rgb), 0.35);
  padding: 16px 40px;
  transition: all 0.35s ease;
  @extend .glow-premium; /* if using SCSS, else copy glow */
}
.btn-premium:hover {
  border-color: rgba(var(--accent-rgb), 0.65);
  @extend .glow-premium:hover;
}

/* ── 8. ICON SYSTEM ──────────────────────────────────────────────── */
/* Base class for all SVG icons — thin stroke, glow */
.icon-premium {
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}
.icon-premium-glow {
  filter: drop-shadow(0 0 8px rgba(var(--accent-rgb), 0.35));
}

/* ── 9. CORNER SYSTEM ────────────────────────────────────────────── */
/* Corner L-bracket decoratives — subtle framing */
.corner-premium-tl,
.corner-premium-br {
  position: absolute;
  width: 32px;
  height: 32px;
  border-color: var(--accent);
  border-style: solid;
  opacity: 0.22;
  z-index: 6;
  pointer-events: none;
}
.corner-premium-tl {
  top: var(--pad-y);
  left: var(--pad-x);
  border-width: 1.5px 0 0 1.5px;
}
.corner-premium-br {
  bottom: calc(var(--pad-bottom) + 16px);
  right: var(--pad-x);
  border-width: 0 1.5px 1.5px 0;
}

/* ── 10. FOOTER SYSTEM ───────────────────────────────────────────── */
/* Use on brand marks, counters, footers */
.footer-premium {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--text-muted);
  opacity: 0.42;
}

/* ── 11. DOT NAV SYSTEM ──────────────────────────────────────────── */
/* Pagination dots at bottom */
.dot-premium {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.20);
  transition: all 0.3s ease;
}
.dot-premium.active {
  width: 28px;
  background: var(--accent);
  box-shadow: 0 0 14px rgba(var(--accent-rgb), 0.35);
}

/* ── 12. STAT NUMBER SYSTEM ──────────────────────────────────────── */
/* Large numbers used in stats */
.stat-premium {
  font-family: 'Cormorant Garamond', var(--font-display), serif;
  font-weight: 500;
  line-height: 0.90;
  letter-spacing: -0.03em;
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.06);
}
```

---

## PHASE 1: BATCH SCRIPT — ALL 124 COMPONENTS

Write `scripts/batch_premium_upgrade.py` that reads every component template and applies category-specific rules.

### Category A: Geo Layers (01-28) — Atmospheric Treatment

For each geo component, apply:
1. Reduce opacity by 30% from current value
2. Add `filter: blur()` for soft edges where not already present
3. Add fading edges via `mask-image: linear-gradient()`
4. For line-based geos (circuit, iso-grid, pixel): reduce stroke width to 1px
5. For glow-based geos (neon-ring, glow-orb, bokeh): reduce opacity, increase blur

```python
GEO_UPGRADES = {
    # component_id: (opacity_multiplier, blur_add, add_fade_edges)
    'geo-mesh-noise':      (0.7, 0, True),
    'geo-pixel-grid':      (0.6, 0, True),
    'geo-conic-rays':      (0.7, 0, True),
    'geo-chevron-stripe':  (0.7, 0, False),
    'geo-iso-grid':        (0.6, 0, True),
    'geo-paper-texture':   (0.8, 4, False),
    'geo-halftone':        (0.75, 0, False),
    'geo-ribbon-flow':     (0.7, 8, False),
    'geo-circuit-trace':   (0.5, 0, True),   # abstract more
    'geo-starfield':       (0.6, 0, False),
    'geo-gradient-bands':  (0.7, 0, False),
    'geo-contour-flow':    (1.0, 0, False),  # already good, keep
    'geo-hex-mesh':        (0.6, 0, True),
    'geo-constellation':   (0.8, 0, False),
    'geo-neon-ring':       (0.4, 20, False), # ambient only
    'geo-bokeh':           (0.5, 10, False),
    'geo-scan-lines':      (0.7, 0, True),
    'geo-chromatic-edge':  (0.5, 0, True),
    'geo-data-streaks':    (0.8, 8, False),
    'geo-liquid-morph':    (0.9, 12, False),
    'geo-blob-bg':         (0.8, 8, False),
    'geo-glow-orb':        (1.0, 30, False), # already good, more blur
    'geo-zoom-rings':      (0.5, 0, True),
    'geo-grid-bg':         (0.5, 0, True),
    'geo-diag-band':       (0.7, 0, True),
    'geo-flow-wave':       (0.8, 8, False),
    'geo-flow-arrow':      (0.7, 0, False),
    'geo-flow-data':       (0.7, 0, False),
    'geo-perspective-grid':(0.6, 0, True),
}
```

### Category B: SVG Blobs (29-39) — Soft Organic Treatment

For each SVG blob:
1. Add `filter: blur(1px)` for soft organic edges
2. Reduce opacity by 20%
3. Add subtle `drop-shadow` glow instead of flat fill
4. Use gradient fills instead of solid colors

```python
BLOB_UPGRADES = {
    # Add filter: blur(1px), reduce opacity, gradient fill
    'svg-blob-tr':          {'blur': 1, 'opacity_mult': 0.8, 'gradient': True},
    'svg-blob-bl':          {'blur': 1, 'opacity_mult': 0.8, 'gradient': True},
    'svg-blob-center':      {'blur': 2, 'opacity_mult': 0.75, 'gradient': True},
    'svg-blob-asymmetric':  {'blur': 1, 'opacity_mult': 0.8, 'gradient': True},
    'svg-blob-scattered':   {'blur': 0.5, 'opacity_mult': 0.85, 'gradient': False},
    'svg-blob-angular':     {'blur': 0, 'opacity_mult': 0.8, 'gradient': True},
    'svg-blob-crystal':     {'blur': 1, 'opacity_mult': 0.8, 'gradient': True},
    'svg-blob-wave':        {'blur': 2, 'opacity_mult': 0.75, 'gradient': True},
    'svg-blob-arch':        {'blur': 1, 'opacity_mult': 0.8, 'gradient': True},
    'svg-blob-splatter':    {'blur': 0.5, 'opacity_mult': 0.85, 'gradient': False},
    'svg-blob-ribbon':      {'blur': 1, 'opacity_mult': 0.8, 'gradient': True},
}
```

### Category C: Chrome Elements (43-45) — Refined Hardware

1. `chrome-vertical-counter`: reduce opacity to 0.35, add `letter-spacing: 0.20em`
2. `chrome-badge-stamp`: thinner border (1.5px), reduce to 0.7 opacity, add glow filter
3. `chrome-header-bar`: glassmorphism background, thinner bottom border (1px at 0.08 opacity)

### Category D: Slide Layouts (46-97) — Template HTML Upgrades

For ALL 52 slide templates, apply these find-and-replace rules:

**Rule 1: Headlines → headline-premium class**
```python
# Find any headline element that uses large display font
# Add class="headline-premium" to it
replacements = [
    # Generic: any div/span/h1 with font-size > 24px in slide templates
    # Add headline-premium class
]
```

**Rule 2: Kickers/Labels → label-premium class**
```python
# Find elements with text-transform:uppercase, small font-size
# Add class="label-premium" or "label-premium-plain"
```

**Rule 3: Body text → body-premium class**
```python
# Find paragraph elements
# Add class="body-premium"
```

**Rule 4: Cards/Panels → glass-premium class**
```python
# Find elements with background/border that look like cards
# Add class="glass-premium" or "glass-premium-sm"
```

**Rule 5: Buttons → btn-premium class**
```python
# Find CTA button elements
# Replace with btn-premium class
```

**Rule 6: Footers → footer-premium class**
```python
# Find brand/counter elements
# Add class="footer-premium"
```

**Rule 7: Unicode icons → SVG inline**
```python
# Find Unicode stars, X marks, checkmarks, arrows
# Replace with inline SVG using icon-premium class
```

**Rule 8: Dot navigation → dot-premium class**
```python
# Find pagination dot elements
# Replace with dot-premium class
```

**Rule 9: Dividers → divider-premium**
```python
# Find hr, border-top separators
# Replace with divider-premium div
```

**Rule 10: Corners → corner-premium**
```python
# Find corner decorative elements
# Replace with corner-premium-tl/br classes
```

### Category E: Sub-Components (98-117) — CSS Batch

In `carousel-shell.html`, update the CSS rules for ALL sub-components:

```css
/* ALL sub-components get these upgrades */
[class^="sub-"] {
  border-width: 1.5px; /* was 2-3px */
}

/* All stat numbers */
[class*="stat"] [class*="num"],
[class*="number"] {
  font-family: 'Cormorant Garamond', var(--font-display), serif;
  font-weight: 500;
}

/* All labels/tags */
[class*="label"],
[class*="tag"],
[class*="kicker"] {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  letter-spacing: 0.20em;
  text-transform: uppercase;
}

/* All cards/panels/bubbles */
[class*="card"],
[class*="panel"],
[class*="bubble"] {
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.10);
}
```

### Category F: Special Effects (118-123)

1. `glass-panel`: already good — enhance with glow-ambient
2. `watermark`: reduce opacity to 0.04
3. `css-text-gradient`: thinner strokes, lower opacity gradient stops
4. `css-text-glow`: reduce glow opacity by 50%, increase blur radius
5. `css-text-stroke`: reduce stroke width to 1.5px
6. `ai-bubbles-01`: enhance with backdrop-filter blur on bubble containers

---

## PHASE 2: THE BATCH SCRIPT

Write `scripts/batch_premium_upgrade.py`:

```python
"""
Batch upgrade ALL 124+ component templates to premium quality.
Reads every template, applies category-specific rules, writes back.
"""
import json
import re
from pathlib import Path

GALLERY_DIR = Path("gallery")
TEMPLATES_DIR = Path("templates/slides")
GEO_DIR = Path("templates/geo")

# Load upgrade configs
with open("scripts/premium_upgrade_config.json") as f:
    CONFIG = json.load(f)

def upgrade_geo(filepath, rules):
    """Apply geo layer upgrades: opacity, blur, fade edges."""
    src = filepath.read_text(encoding="utf-8")
    # Find opacity values and multiply
    src = re.sub(
        r'opacity:\s*([\d.]+)',
        lambda m: f"opacity:{float(m.group(1)) * rules['opacity_mult']:.3f}",
        src
    )
    if rules.get('blur'):
        src = re.sub(
            r'filter:\s*blur\((\d+)px\)',
            lambda m: f"filter:blur({int(m.group(1)) + rules['blur']}px)",
            src
        )
    if rules.get('fade_edges'):
        src = add_fade_mask(src)
    filepath.write_text(src, encoding="utf-8")

def upgrade_slide_template(filepath):
    """Apply all 10 find-and-replace rules to slide templates."""
    src = filepath.read_text(encoding="utf-8")
    
    # Rule 1: Headlines
    src = add_class_to_headlines(src)
    # Rule 2: Labels
    src = add_class_to_labels(src)
    # Rule 3: Body text
    src = add_class_to_body(src)
    # Rule 4: Cards
    src = add_class_to_cards(src)
    # Rule 5: Buttons
    src = add_class_to_buttons(src)
    # Rule 6: Footers
    src = add_class_to_footers(src)
    # Rule 7: Replace Unicode icons
    src = replace_unicode_icons(src)
    # Rule 8: Dot nav
    src = upgrade_dot_nav(src)
    # Rule 9: Dividers
    src = upgrade_dividers(src)
    # Rule 10: Corners
    src = upgrade_corners(src)
    
    filepath.write_text(src, encoding="utf-8")

def main():
    upgraded = 0
    
    # Geo layers
    for comp_id, rules in CONFIG["geo"].items():
        filepath = GEO_DIR / f"{comp_id}.html"
        if filepath.exists():
            upgrade_geo(filepath, rules)
            upgraded += 1
    
    # Slide templates
    for template in TEMPLATES_DIR.glob("slide-*.html"):
        upgrade_slide_template(template)
        upgraded += 1
    
    # Chrome elements
    for comp_id, rules in CONFIG["chrome"].items():
        filepath = TEMPLATES_DIR / f"{comp_id}.html"
        if filepath.exists():
            upgrade_slide_template(filepath)  # same rules
            upgraded += 1
    
    # Sub-components (CSS updates in shell, not templates)
    upgrade_subcomponent_css()
    
    print(f"Upgraded {upgraded} components")

if __name__ == "__main__":
    main()
```

Also write `scripts/premium_upgrade_config.json` with the GEO_UPGRADES, BLOB_UPGRADES, and CHROME_UPGRADES dicts.

---

## PHASE 3: VERIFY KEY LAYOUTS

After batch script runs, manually verify these 5 layouts render correctly:

1. **hook-lockup** (94) — serif headline, mono kicker, clean
2. **before-after** (97) — glassmorphism panels, thin icons
3. **CTA** (95) — pill button, glow, verified from previous session
4. **big-number** (93) — serif number, mono label
5. **terminal** (96) — glassmorphism panel, thin border

Render test carousels for each, visually compare to ChatGPT references.

---

## PHASE 4: REBUILD GALLERY

```bash
py scripts/build_gallery.py
```

---

## DELIVERABLES

- [ ] Phase 0: All 12 premium CSS utility classes added to carousel-shell.html
- [ ] Phase 1: `batch_premium_upgrade.py` written and executed
- [ ] Phase 1: All 28 geo layers upgraded (opacity, blur, fade)
- [ ] Phase 1: All 11 SVG blobs upgraded (blur, gradient fill)
- [ ] Phase 1: All 3 chrome elements upgraded
- [ ] Phase 1: All 52 slide templates upgraded (10 rules each)
- [ ] Phase 1: All 20 sub-components upgraded (CSS batch)
- [ ] Phase 1: All 6 special effects upgraded
- [ ] Phase 2: Script executed, count verified
- [ ] Phase 3: 5 key layouts render-tested
- [ ] Phase 4: Gallery rebuilt (248/248 demos)
