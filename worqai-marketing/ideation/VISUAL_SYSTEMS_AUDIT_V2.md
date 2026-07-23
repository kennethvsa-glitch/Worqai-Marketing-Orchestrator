# PASTE THIS ENTIRE FILE INTO CLAUDE

---

## CONTEXT

Two AI analyses were done on our WorqAI carousel gallery (124 components, 97 slide layouts):

- **Claude opened the actual files** and found: tokens are consistent (gold #C8A84B, not cyan), glow is already cinematic, the REAL problem is identical decorative elements (sparkle stars at 0.85 opacity, corner brackets, glow orb, rings) stamped on every slide regardless of content.
- **ChatGPT analyzed screenshots** and found: need 3 visual languages, reduce visible effects, art direction over quantity, serif headlines on dark backgrounds, glassmorphism panels, thin borders, wide tracking.

**Both agree on:** 3 visual languages, reduce decorative clutter, atmosphere > literal effects.

Claude already wrote `premium-patch.css` that kills sparkle stars and calms corners. We need to go further.

---

## PHASE 1: APPLY CLAUDE'S EXISTING PATCH (premium-patch.css)

This file was already generated. Paste it as the LAST `<style>` block in the shell template so it applies globally:

```css
/* From premium-patch.css — already written */
.deco-starburst { display: none !important; }
.cta-star-svg   { display: none !important; }
.deco-corner-tl,
.deco-corner-br { opacity: 0.18 !important; }
.zoom-rings .ring:nth-child(1) { opacity: 0.04 !important; }
.zoom-rings .ring:nth-child(2) { opacity: 0.025 !important; }
.zoom-rings .ring:nth-child(3) { opacity: 0.015 !important; }
.glow-orb { filter: blur(90px) !important; opacity: 0.7 !important; }
.cta-reward { opacity: 0.5 !important; font-weight: 300 !important; }

/* Hero-budget switch — THE systemic fix */
.slide.hero-type  .geo-layer { opacity: 0.06 !important; }
.slide.hero-type  .glow-orb  { opacity: 0.4 !important; }
.slide.hero-flow  .cta-wrap .cta-reward { opacity: 0.45 !important; }
.slide.hero-flow  .geo-layer { opacity: 0.9 !important; }
.slide.hero-glass .geo-layer { opacity: 0.05 !important; }
```

This is ALREADY DONE — just verify it's in `carousel-shell.html`.

---

## PHASE 2: 3-VISUAL-LANGUAGE SYSTEM

Map every slide layout to ONE hero class. This is the systemic fix for "everything has equal weight."

### hero-type (Typography is the star, geo barely visible)
Layouts where text IS the design:
- slide-hook-lockup (94)
- slide-big-number (93)
- slide-full-bleed-type (67)
- slide-stacked-type (71)
- slide-typeset-poster (60)
- slide-pull-quote (90)
- slide-quote-cascade (50)
- slide-editorial-column (77)
- slide-contrast-knockout (79)

CSS effect: geo-layer drops to 0.06 opacity, glow-orb to 0.4

### hero-flow (Geo/flow/particle layer is the star, text recedes)
Layouts where the background effect IS the design:
- All geo-* layers (01-28) when used as primary
- slide-liquid-morph (21)
- slide-data-streaks (20)
- slide-contour-flow (12)
- slide-frame-within-frame (75)

CSS effect: geo-layer stays at 0.9, cta-reward dims to 0.45

### hero-glass (Glass panel/CTA is the star)
Layouts with cards, panels, comparison boxes:
- slide-before-after (97)
- slide-cta (95)
- slide-bento-grid (51)
- slide-tip-blocks (65)
- slide-minimal-card-stack (83)
- slide-glass-panel (118)
- slide-compare-table (48)
- slide-faq-stack (49)
- slide-input-output (62)
- slide-receipt (85)

CSS effect: geo-layer drops to 0.05 (barely visible), panels get full glassmorphism

### Generator Logic

When rendering a slide, auto-assign hero class based on layout:
```python
HERO_MAP = {
    # hero-type: typography-heavy
    'slide-hook-lockup': 'hero-type',
    'slide-big-number': 'hero-type',
    'slide-full-bleed-type': 'hero-type',
    'slide-typeset-poster': 'hero-type',
    'slide-pull-quote': 'hero-type',
    'slide-stacked-type': 'hero-type',
    'slide-quote-cascade': 'hero-type',
    'slide-editorial-column': 'hero-type',
    'slide-contrast-knockout': 'hero-type',
    
    # hero-flow: geo/atmosphere-heavy
    'slide-liquid-morph': 'hero-flow',
    'slide-data-streaks': 'hero-flow',
    'slide-contour-flow': 'hero-flow',
    'slide-frame-within-frame': 'hero-flow',
    
    # hero-glass: card/panel-heavy
    'slide-before-after': 'hero-glass',
    'slide-cta': 'hero-glass',
    'slide-bento-grid': 'hero-glass',
    'slide-tip-blocks': 'hero-glass',
    'slide-minimal-card-stack': 'hero-glass',
    'slide-glass-panel': 'hero-glass',
    'slide-compare-table': 'hero-glass',
    'slide-faq-stack': 'hero-glass',
    'slide-input-output': 'hero-glass',
    'slide-receipt': 'hero-glass',
}
# Default: no hero class (all layers at normal opacity)
```

Add this map to `render_carousel.py` and inject the class on the `.slide` div.

---

## PHASE 3: PER-LAYOUT PREMIUM UPGRADES

Apply ChatGPT's design principles to specific high-impact layouts. These are CSS changes in `carousel-shell.html` + HTML changes in the slide templates.

### Layout 94: slide-hook-lockup (THE first slide — most important)

**A. Kicker ("—— WORQAI")**
```css
.hook-kicker {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  font-size: 13px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--accent);
  opacity: 0.85;
}
.hook-kicker::before {
  content: '';
  display: inline-block;
  width: 24px;
  height: 1px;
  background: var(--accent);
  margin-right: 12px;
  vertical-align: middle;
  opacity: 0.6;
}
```

**B. Headline ("Tu CV fue bloqueado.")**
On DARK backgrounds, use serif:
```css
.hook-display {
  font-family: 'Cormorant Garamond', 'Playfair Display', var(--font-display), serif;
  font-size: clamp(48px, 10cqw, 76px);
  font-weight: 500;
  line-height: 0.94;
  letter-spacing: -0.035em;
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.06);
}
.hook-display .highlight {
  color: #42F5FF;
  font-style: italic;
  text-shadow: 0 0 20px rgba(66, 245, 255, 0.14);
}
```

**C. Subtitle**
```css
.hook-subtitle {
  font-family: var(--font-body);
  font-size: clamp(16px, 3cqw, 24px);
  font-weight: 400;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.58);
  max-width: 480px;
  margin-top: 32px;
}
```

**D. Star Icon** — Replace Unicode with SVG in template:
```html
<svg class="hook-star" viewBox="0 0 64 64" width="48" height="48" aria-hidden="true">
  <defs>
    <filter id="hook-star-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <path d="M32 4 L35.5 26 L58 22 L39 34 L58 46 L35.5 42 L32 64 L28.5 42 L6 46 L25 34 L6 22 L28.5 26 Z"
        fill="none" stroke="var(--accent)" stroke-width="1.2"
        filter="url(#hook-star-glow)" opacity="0.85"/>
</svg>
```

**E. Footer**
```css
.brand {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  font-size: 14px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  opacity: 0.42;
}
```

### Layout 97: slide-before-after (Glass panel comparison)

**A. Headline**
```css
.ba-headline {
  font-family: 'Cormorant Garamond', 'Playfair Display', var(--font-display), serif;
  font-size: clamp(36px, 8cqw, 64px);
  font-weight: 500;
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: rgba(255, 255, 255, 0.92);
  text-align: center;
  margin-bottom: 40px;
}
.ba-headline .highlight {
  color: #42F5FF;
  font-style: italic;
  text-shadow: 0 0 18px rgba(66, 245, 255, 0.18);
}
```

**B. Panels (true glassmorphism)**
```css
.ba-panel {
  width: 48%;
  min-height: 600px;
  border-radius: 38px;
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  overflow: hidden;
  padding: 40px 32px;
}
.ba-panel.before { box-shadow: 0 0 30px rgba(255, 80, 140, 0.12); }
.ba-panel.after  { box-shadow: 0 0 35px rgba(66, 245, 255, 0.10); }
```

**C. Labels (ANTES/DESPUÉS)**
```css
.ba-label {
  font-family: 'IBM Plex Mono', var(--font-mono), monospace;
  font-size: 18px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  font-weight: 500;
  margin-bottom: 32px;
}
.ba-label::before {
  content: '';
  display: inline-block;
  width: 20px;
  height: 1px;
  background: currentColor;
  opacity: 0.5;
  margin-right: 12px;
  vertical-align: middle;
}
.ba-label.before { color: rgba(255, 80, 140, 0.85); }
.ba-label.after  { color: rgba(66, 245, 255, 0.85); }
```

**D. Icons** — Replace Unicode with SVG in template:
```html
<!-- X mark -->
<svg width="14" height="14" viewBox="0 0 14 14" class="ba-icon-x">
  <line x1="2" y1="2" x2="12" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="12" y1="2" x2="2" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>
<!-- Check mark -->
<svg width="14" height="14" viewBox="0 0 14 14" class="ba-icon-check">
  <polyline points="2,7 6,11 12,3" stroke="currentColor" stroke-width="1.5" fill="none" 
            stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

**E. Dividers between items**
```css
.ba-item-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
  margin: 20px 0;
}
```

### Layout 95: slide-cta (Verify Previous Work)

From previous session, verify these exist:
- [ ] Pill button: `border-radius: 999px`
- [ ] 4-layer glow
- [ ] Glassmorphism: `backdrop-filter: blur(12px)`
- [ ] `letter-spacing: 0.38em`
- [ ] `font-weight: 500`
- [ ] SVG 8-point star
- [ ] Corner L-brackets

If any missing, add them now.

### Other High-Impact Layouts (Lighter Pass)

| Layout | Changes |
|---|---|
| slide-big-number (93) | Number: serif, weight 500, subtle text-shadow. Label: mono, 0.20em tracking |
| slide-proof (64) | Result number: serif, weight 500. Tag: glassmorphism pill |
| slide-pull-quote (90) | Quote: Cormorant Garamond italic. Attribution: mono, 0.18em tracking |
| slide-terminal (96) | Panel: glassmorphism. Border: 1px at low opacity |
| slide-stat-row (53) | Numbers: weight 700 (not 900). Labels: mono, wide tracking |
| slide-checklist (92) | Icons: thin SVG. Dividers: gradient fade |
| slide-faq-stack (49) | Dividers: gradient fade. Labels: mono, wide tracking |
| slide-bento-grid (51) | Cards: glassmorphism. Numbers: serif option |
| slide-tip-blocks (65) | Cards: glassmorphism. Labels: mono, wide tracking |
| slide-minimal-card-stack (83) | Cards: glassmorphism, 1px borders |

---

## PHASE 4: COMPONENT-SPECIFIC FIXES

### Keep (already premium direction):
- geo-contour-flow (lovely 1px strokes fading 0.7→0.06)
- geo-constellation
- geo-liquid-morph
- geo-data-streaks
- glass-panel
- ai-bubbles
- vector-field-distortion

### Calm (reduce intensity):
- geo-neon-ring: reduce to subtle ambient, not literal neon
- geo-glow-orb: already good, keep as-is
- geo-starfield: reduce opacity further to 0.35
- geo-bokeh: reduce to atmospheric only

### Rework (too literal/generic):
- geo-circuit-trace: abstract more — thinner lines, lower opacity, less "PCB board"
- geo-iso-grid: add fading edges, partial visibility
- geo-pixel-grid: reduce to atmospheric texture, not literal pixels
- slide-data-wall: reduce information density, more negative space
- slide-waffle-chart: thinner lines, lower opacity

---

## PHASE 5: REBUILD GALLERY

After all changes:
```bash
py scripts/build_gallery.py
```

---

## DELIVERABLES CHECKLIST

- [ ] Phase 1: premium-patch.css verified in carousel-shell.html
- [ ] Phase 2: HERO_MAP added to render_carousel.py, hero-* classes inject on .slide
- [ ] Phase 3: Layout 94 restyled (serif headline, mono kicker, SVG star)
- [ ] Phase 3: Layout 97 restyled (glassmorphism panels, mono labels, SVG icons)
- [ ] Phase 3: Layout 95 verified (pill, glow, glassmorphism from previous session)
- [ ] Phase 3: 10 other layouts get lighter pass
- [ ] Phase 4: Component intensity adjusted (calm/rework categories)
- [ ] Phase 5: Gallery rebuilt (248/248 demos)
