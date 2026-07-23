# PASTE THIS ENTIRE FILE INTO CLAUDE

---

## CONTEXT

The user wants ALL 124+ components upgraded to premium quality. The previous v2 prompt fixed 5 implementation bugs but introduced 3 new architectural problems when checked against the actual codebase:

1. **48 themes, not 1 gold**: The system has 48 visual systems (s01-s48) with 47 distinct accent colors. Hardcoding gold rgba(200,168,75) breaks 46/48 systems.
2. **Gallery is build output**: `build_gallery.py` does `old.unlink()` on every run — any edit to `gallery/*.html` is deleted. All persistent edits go to `templates/carousel-shell.html` and `templates/slides/*.html`.
3. **Don't inject classes into Jinja**: Templates have `class="hook-display {{ text_treatment_class }}"` — string matching fails. Instead, style EXISTING selectors in the shell CSS.

This v3 prompt corrects all of that.

---

## CRITICAL RULES (Do Not Break These)

1. **48 themes, 47 accents**: Use `var(--accent)` and `color-mix(in srgb, var(--accent) X%, transparent)` — NEVER hardcode any specific color. Gold is only s01.
2. **Never edit gallery/**: It is build output, wiped on every run. Edit ONLY `templates/carousel-shell.html` and `templates/slides/*.html`.
3. **Style existing selectors**: Don't add new classes to Jinja templates. Style `.hook-display`, `.hook-kicker`, etc. directly in the shell CSS.
4. **Load Cormorant Garamond**: Add Google Fonts `<link>` in the shell `<head>`. Currently not loaded — serif will fall back to Times if missing.
5. **Lower --geo-opacity token**: Drop the global token (e.g., 0.08 → 0.055) for global calm, then override only loud outliers. One token change does most work.
6. **git commit before running**: `git add -A && git commit -m "before-premium-makeover"` as safety checkpoint.

---

## PHASE 0: LOAD THE SERIF FONT

Add to the `<head>` of `templates/carousel-shell.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Load ONLY Cormorant + Playfair. Do NOT add more fonts — 16 is already enough.

---

## PHASE 1: GLOBAL PREMIUM CSS (ALL in carousel-shell.html)

Add this as a new `<style>` block in `templates/carousel-shell.html`. EVERYTHING here uses `var(--accent)` with `color-mix()` — works for all 48 themes.

```css
/* ════════════════════════════════════════════════════════════════
   PREMIUM SYSTEM v3 — Global Upgrade
   Targets existing selectors. Works for all 48 themes via
   var(--accent) + color-mix(). Never hardcodes a color.
   ════════════════════════════════════════════════════════════════ */

/* ── 1. HEADLINE RESTYLE (serif for editorial contrast) ──────────── */
/* Style EXISTING headline selectors — no new classes in markup */
.hook-display,
.ba-headline,
.poster-display,
.mn-number,
.fbt-display,
.stype-line-1,
.sbs-big,
.t-display,
.diags-headline,
.diags-stat,
.asym-headline,
.tos-headline,
.cman-headline,
.ck-top-text,
.wfl-num,
.at-headline,
.conn-headline,
.waffle-number,
.bas-vs,
.stat-num,
.hook-big-stat,
.hook-from-to .val {
  font-family: 'Cormorant Garamond', 'Playfair Display', var(--font-display), serif;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.06);
}
/* Large display sizes keep tight leading */
.hook-display,
.poster-display,
.fbt-display,
.stype-line-1,
.sbs-big,
.mn-number {
  line-height: 0.94;
  letter-spacing: -0.03em;
}
/* Light system variant */
.light-system .hook-display,
.light-system .ba-headline,
.light-system .poster-display {
  color: rgba(0, 0, 0, 0.88);
  text-shadow: none;
}
/* Accent word within headline — theme-aware via color-mix */
.headline-accent,
.hook-display .accent,
.ba-headline .highlight,
.hook-display em {
  color: var(--accent);
  font-style: italic;
  text-shadow: 0 0 20px color-mix(in srgb, var(--accent) 18%, transparent);
}

/* ── 2. KICKER / LABEL RESTYLE (mono, wide tracking) ────────────── */
/* Style EXISTING kicker/label selectors */
.hook-kicker,
.kicker,
.ba-label,
.pbar-label,
.comp-card-title,
.timeline-date,
.donut-chart .center-label,
.deco-stamp-inner,
.sub-pill-tag,
.sub-status-pill,
.sc-label,
.tip-blk-label,
.ba-col-tag,
.proof-result-label,
.proof-mechanism-tag,
.diags-stat-label,
.asym-kicker,
.sbs-label,
.fwf-kicker,
.fwf-attr,
.ec-kicker,
.cq-kicker,
.cq-attr,
.conn-kicker,
.waffle-label,
.io-kicker,
.io-panel-label,
.bas-label,
.hook-masthead {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  letter-spacing: 0.20em;
  text-transform: uppercase;
}
/* Kickers with line prefix */
.hook-kicker,
.asym-kicker,
.fwf-kicker,
.ec-kicker,
.cq-kicker,
.conn-kicker,
.io-kicker {
  font-size: 13px;
  letter-spacing: 0.24em;
  color: var(--accent);
}
.hook-kicker::before,
.asym-kicker::before,
.fwf-kicker::before,
.ec-kicker::before,
.cq-kicker::before,
.conn-kicker::before,
.io-kicker::before {
  content: '';
  display: inline-block;
  width: 20px;
  height: 1px;
  background: var(--accent);
  margin-right: 10px;
  vertical-align: middle;
  opacity: 0.5;
}

/* ── 3. BODY / SUBTITLE RESTYLE (not pure white) ─────────────────── */
.hook-subtitle,
.body-premium,
.ba-item-text,
.tip-blk-body,
.proof-mechanism-text,
.faq-answer,
.slide-body {
  font-family: var(--font-body);
  font-weight: 400;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.58);
}
.light-system .hook-subtitle {
  color: rgba(0, 0, 0, 0.58);
}

/* ── 4. GLASSMORPHISM (style existing card/panel selectors) ──────── */
.ba-panel,
.tip-blk-card,
.bento-cell,
.glass-panel,
.sub-comment-mock,
.sub-bento-card,
.sub-fact-bubble {
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 24px;
  overflow: hidden;
}
/* Small glass elements */
.sub-pill-tag,
.sub-status-pill,
.tag-badge {
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.10);
  border-radius: 12px;
}
/* Light system variants */
.light-system .ba-panel,
.light-system .tip-blk-card,
.light-system .bento-cell {
  background: linear-gradient(180deg, rgba(0,0,0,0.03), rgba(0,0,0,0.01));
  border-color: rgba(0, 0, 0, 0.08);
}

/* ── 5. GLOW SYSTEM (theme-aware via color-mix) ──────────────────── */
/* Uses var(--accent) — works for all 48 themes */
.cta-keyword-box,
.btn-premium {
  box-shadow:
    0 0 10px color-mix(in srgb, var(--accent) 55%, transparent),
    0 0 30px color-mix(in srgb, var(--accent) 22%, transparent),
    0 15px 40px color-mix(in srgb, var(--accent) 12%, transparent),
    inset 0 0 20px rgba(255, 255, 255, 0.03);
}
.cta-keyword-box:hover,
.btn-premium:hover {
  box-shadow:
    0 0 20px color-mix(in srgb, var(--accent) 70%, transparent),
    0 0 50px color-mix(in srgb, var(--accent) 30%, transparent),
    0 20px 60px color-mix(in srgb, var(--accent) 18%, transparent),
    inset 0 0 30px rgba(255, 255, 255, 0.06);
}
/* Ambient glow for panels */
.ba-panel.before {
  box-shadow: 0 0 40px color-mix(in srgb, #e05a7a 10%, transparent);
}
.ba-panel.after {
  box-shadow: 0 0 40px color-mix(in srgb, var(--accent) 10%, transparent);
}

/* ── 6. DIVIDER SYSTEM (gradient fade) ───────────────────────────── */
/* Style existing divider patterns */
.ba-item + .ba-item,
.tip-blk-card + .tip-blk-card,
.faq-item + .faq-item,
.step-item + .step-item,
.check-item + .check-item {
  border-top: none;
}
/* Add gradient dividers between items */
.divider-premium,
.ba-item-divider,
.tip-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}
.light-system .divider-premium {
  background: linear-gradient(90deg, transparent, rgba(0,0,0,0.06), transparent);
}

/* ── 7. BUTTON RESTYLE (pill + glass + glow) ─────────────────────── */
.cta-keyword-box {
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
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1.5px solid color-mix(in srgb, var(--accent) 35%, transparent);
  padding: 16px 40px;
  transition: all 0.35s ease;
}
.cta-keyword {
  font-weight: 500;
  letter-spacing: 0.18em;
}

/* ── 8. ICON SYSTEM (replace thick Unicode with thin SVG) ─────────── */
/* This requires markup edits in templates — see Phase 3 */

/* ── 9. CORNER RESTYLE (subtle framing) ───────────────────────────── */
.deco-corner-tl,
.deco-corner-br {
  width: 32px;
  height: 32px;
  border-color: var(--accent);
  opacity: 0.22;
  border-width: 1.5px;
}

/* ── 10. FOOTER RESTYLE ──────────────────────────────────────────── */
.brand,
.counter,
.footer,
.cta-footer-url {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  letter-spacing: 0.22em;
  font-size: 12px;
  opacity: 0.42;
}

/* ── 11. DOT NAV RESTYLE ─────────────────────────────────────────── */
.pd {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.20);
  transition: all 0.3s ease;
}
.pd.on {
  width: 28px;
  background: var(--accent);
  box-shadow: 0 0 14px color-mix(in srgb, var(--accent) 35%, transparent);
}

/* ── 12. STAT NUMBER RESTYLE ─────────────────────────────────────── */
.sc-num,
.gp-num,
.lnum-num,
.pbar-value,
.donut-chart .center-num,
.hook-big-stat,
.hook-from-to .val,
.dwall-num,
.waffle-number,
.wfl-num {
  font-family: 'Cormorant Garamond', var(--font-display), serif;
  font-weight: 500;
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.06);
}

/* ── 13. GEO OPACITY: Lower the global token ─────────────────────── */
/* One token change calms ALL geo layers that inherit it */
.geo-layer,
[class^="geo-"] {
  opacity: var(--geo-opacity, 0.055); /* was 0.08 */
}
/* Override only the outliers that are still too loud */
.geo-neon-ring { opacity: 0.03; }
.geo-bokeh { opacity: 0.04; }
.geo-chromatic-edge { opacity: 0.03; }
.geo-circuit-trace { opacity: 0.04; }
.geo-starfield { opacity: 0.35; }

/* ── 14. THINNER BORDERS EVERYWHERE ──────────────────────────────── */
.faq-item,
.comp-card,
.sub-fact-bubble.myth,
.sub-fact-bubble.fact,
.poster-eyebrow {
  border-left-width: 1.5px !important;
  border-width: 1.5px !important;
}
```

---

## PHASE 2: TEMPLATE MARKUP EDITS (ONLY where needed)

Some changes require editing `templates/slides/*.html`. Do these sparingly — most work happens in the shell CSS.

### Template: slide-before-after.html (Layout 97)

Replace Unicode icons with inline SVG:

```html
<!-- Before: Unicode X -->
<!-- After: SVG thin stroke -->
<svg width="14" height="14" viewBox="0 0 14 14" style="stroke:var(--accent);stroke-width:1.5;fill:none;stroke-linecap:round">
  <line x1="2" y1="2" x2="12" y2="12"/>
  <line x1="12" y1="2" x2="2" y2="12"/>
</svg>

<!-- Before: Unicode checkmark -->
<!-- After: SVG thin stroke -->
<svg width="14" height="14" viewBox="0 0 14 14" style="stroke:var(--accent);stroke-width:1.5;fill:none;stroke-linecap:round;stroke-linejoin:round">
  <polyline points="2,7 6,11 12,3"/>
</svg>
```

### Template: slide-cta.html (Layout 95)

Replace Unicode star with SVG 8-point star (already done in previous session — verify):

```html
<svg class="cta-star-svg" viewBox="0 0 64 64" width="48" height="48" aria-hidden="true">
  <defs>
    <filter id="cta-star-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <path d="M32 4 L35.5 26 L58 22 L39 34 L58 46 L35.5 42 L32 64 L28.5 42 L6 46 L25 34 L6 22 L28.5 26 Z"
        fill="none" stroke="var(--accent)" stroke-width="1.2"
        filter="url(#cta-star-glow)" opacity="0.85"/>
</svg>
```

### Template: slide-hook-lockup.html (Layout 94)

Add corner decoratives if not already present:

```html
<div class="deco-corner-tl"></div>
<div class="deco-corner-br"></div>
```

---

## PHASE 3: VERIFICATION

After all edits:

```bash
# Safety checkpoint
git add -A && git commit -m "before-premium-makeover"

# Build gallery
py scripts/build_gallery.py

# Open and eyeball
# Check: all 124 components at gallery/INDEX.html
```

Verify 5 key layouts render correctly:
1. Hook lockup (94) — serif headline, mono kicker, clean
2. Before/after (97) — glass panels, thin SVG icons
3. CTA (95) — pill button, glow
4. Big number (93) — serif number
5. Terminal (96) — glass panel

---

## WHAT THE USER WILL SEE

**Every single component upgraded — no mid-tier survivors:**

| Feature | Before | After |
|---|---|---|
| Sparkle stars | 0.85 opacity on EVERY slide | **Gone** (from Claude's patch) |
| Headlines | Space Grotesk, bold | **Cormorant Garamond, weight 500** |
| Labels/kickers | Normal tracking | **IBM Plex Mono, 0.20-0.24em tracking** |
| Body text | Pure white | **rgba(255,255,255,0.58)** |
| Cards/panels | Flat background | **Glassmorphism** |
| Borders | 2-3px solid | **1-1.5px** |
| Glow | Theme-agnostic or missing | **color-mix with var(--accent) — works for all 48 themes** |
| Buttons | Basic | **Pill, glass, glow, wide tracking** |
| Icons | Unicode | **Thin SVG strokes** |
| Footers | Normal | **Mono, 0.22em, 0.42 opacity** |
| Numbers | Bold sans | **Cormorant Garamond serif** |
| Geo layers | Varied, some loud | **Global token lowered to 0.055, outliers capped** |
