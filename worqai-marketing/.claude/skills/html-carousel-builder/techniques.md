---
name: html-carousel-builder techniques
load: on-demand only, when custom effects needed
---

# TECHNIQUE REFERENCE — GEO Modules + Effects

Load this file ONLY when the default background (gradient + grain) is not enough.
Default for dark systems: gradient + GEO-13 wireframe. Default for warm systems: gradient + blob.

---

## GEO-13 · PERSPECTIVE WIREFRAME (Default for dark systems)

CSS:
```css
.pw-wrap {
  position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1;
  perspective: 600px;
}
.pw-grid {
  position: absolute; width: 200%; height: 200%;
  left: -50%; top: -50%;
  background-image:
    linear-gradient(to right, VAR_ACCENT 1px, transparent 1px),
    linear-gradient(to bottom, VAR_ACCENT 1px, transparent 1px);
  background-size: 60px 60px;
  opacity: 0.08;
  transform: rotateX(60deg) rotateZ(-15deg);
}
```

Usage: Wrap in `.pw-wrap > .pw-grid` inside each slide. Opacity 0.06–0.12 depending on system.

---

## SCAN LINES

CSS:
```css
.scan-lines {
  position: absolute; inset: 0; pointer-events: none; z-index: 1;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px
  );
  mix-blend-mode: overlay;
}
```

Usage: Best on cyberpunk, vaporwave, glitch systems. Add as child of `.slide`.

---

## ZOOM BURST RINGS

CSS:
```css
.zoom-rings {
  position: absolute; inset: 0; pointer-events: none; z-index: 1;
}
.zoom-rings .ring {
  position: absolute; top: 50%; left: 50%;
  border: 1px solid VAR_ACCENT; border-radius: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.12;
}
.zoom-rings .ring:nth-child(1) { width: 200px; height: 200px; }
.zoom-rings .ring:nth-child(2) { width: 400px; height: 400px; opacity: 0.08; }
.zoom-rings .ring:nth-child(3) { width: 600px; height: 600px; opacity: 0.04; }
```

HTML:
```html
<div class="zoom-rings">
  <div class="ring"></div><div class="ring"></div><div class="ring"></div>
</div>
```

Usage: Add to hook slide or stat slide for energy. Works on any system.

---

## WAVE PATHS (SVG)

For oceanic/data systems (s02, s14, s33):
```html
<svg class="wave-bg" viewBox="0 0 1080 1080" preserveAspectRatio="none" style="position:absolute;inset:0;z-index:1;opacity:0.15;">
  <path d="M0,540 Q270,400 540,540 T1080,540" fill="none" stroke="VAR_ACCENT" stroke-width="2"/>
  <path d="M0,600 Q270,460 540,600 T1080,600" fill="none" stroke="VAR_ACCENT" stroke-width="1.5" opacity="0.6"/>
  <path d="M0,480 Q270,340 540,480 T1080,480" fill="none" stroke="VAR_ACCENT" stroke-width="1" opacity="0.4"/>
</svg>
```

---

## GLOW ORBS

CSS:
```css
.glow-orb {
  position: absolute; width: 55%; aspect-ratio: 1/1; border-radius: 50%;
  background: radial-gradient(circle, rgba(ACCENT_R,ACCENT_G,ACCENT_B,0.18) 0%, transparent 65%);
  filter: blur(70px); pointer-events: none; z-index: 1;
}
```

Usage: Position varies per slide. Rotate positions for visual interest:
- S1: top -15%, right -10%
- S2: top 60%, right -20%
- S3: top -10%, right 55%

---

## STACKED OFFSET ECHO (Typography Effect)

For brutalist/editorial systems (s07, s19, s25, s29):
```css
.echo-text {
  position: relative;
  text-shadow: 3px 3px 0 rgba(255,255,255,0.08), 6px 6px 0 rgba(255,255,255,0.04);
}
```

---

## NEON TUBE GLOW

For cyberpunk/neon systems (s16, s29):
```css
.neon-glow {
  text-shadow: 0 0 10px VAR_ACCENT, 0 0 20px VAR_ACCENT, 0 0 40px VAR_ACCENT;
}
.neon-border {
  border: 1px solid VAR_ACCENT;
  box-shadow: 0 0 10px VAR_ACCENT, inset 0 0 10px rgba(ACCENT,0.2);
}
```

---

## DATA TERMINAL BLOCK

For tech/data slides:
```html
<div class="terminal" style="background:rgba(0,0,0,0.45);border:1px solid rgba(ACCENT,0.3);border-radius:12px;padding:20px;font-family:'JetBrains Mono',monospace;">
  <div style="color:#ff6b9d">$ comando --fix</div>
  <div style="color:#4ecdc4;margin-top:8px">✓ Proceso completado</div>
</div>
```

Colors: pink (#ff6b9d) for commands, cyan (#4ecdc4) for success, yellow (#ffe66d) for warnings.

---

## RISO HALFTONE TEXTURE

For print/riso systems (s18, s27, s45):
```css
.riso-halftone {
  position: absolute; inset: 0; pointer-events: none; z-index: 1; opacity: 0.15;
  background-image: radial-gradient(circle, VAR_ACCENT 1px, transparent 1px);
  background-size: 8px 8px;
}
```

---

## STARBRUST / SUNRAY

For art deco/luxury systems (s35):
```html
<svg class="sunburst" viewBox="0 0 1080 1080" style="position:absolute;inset:0;z-index:1;opacity:0.08;">
  <g stroke="VAR_ACCENT" stroke-width="1" fill="none">
    <line x1="540" y1="540" x2="540" y2="0"/>
    <line x1="540" y1="540" x2="1080" y2="0"/>
    <line x1="540" y1="540" x2="1080" y2="540"/>
    <line x1="540" y1="540" x2="1080" y2="1080"/>
    <line x1="540" y1="540" x2="540" y2="1080"/>
    <line x1="540" y1="540" x2="0" y2="1080"/>
    <line x1="540" y1="540" x2="0" y2="540"/>
    <line x1="540" y1="540" x2="0" y2="0"/>
    <line x1="540" y1="540" x2="810" y2="135"/>
    <line x1="540" y1="540" x2="945" y2="270"/>
    <line x1="540" y1="540" x2="945" y2="810"/>
    <line x1="540" y1="540" x2="810" y2="945"/>
    <line x1="540" y1="540" x2="270" y2="945"/>
    <line x1="540" y1="540" x2="135" y2="810"/>
    <line x1="540" y1="540" x2="135" y2="270"/>
    <line x1="540" y1="540" x2="270" y2="135"/>
  </g>
</svg>
```

---

## CHROMATIC ABERRATION

For glitch/datamosh systems (s40):
```css
.chromatic {
  position: relative;
}
.chromatic::before, .chromatic::after {
  content: attr(data-text);
  position: absolute; left: 0; top: 0; width: 100%; height: 100%;
}
.chromatic::before {
  left: 2px; color: #ff00ff; clip-path: inset(0 0 50% 0); opacity: 0.5;
}
.chromatic::after {
  left: -2px; color: #00ffff; clip-path: inset(50% 0 0 0); opacity: 0.5;
}
```

---

## CONIC GRADIENT (HOLOGRAPHIC) ⚠️ html2canvas INCOMPATIBLE

**Renders transparent checkerboard on ZIP export. Use `linear-gradient` fallback instead.**

For s41 HOLOGRAPHIC SHEEN, use this html2canvas-safe fallback:
```css
.holo-bg {
  background: linear-gradient(135deg, #ff9ff3, #feca57, #ff6b6b, #48dbfb, #1dd1a1, #5f27cd, #ff9ff3);
}
```

**If you MUST use conic-gradient** (e.g., client specifically requests the spinning effect), export via `scripts/carousel_exporter.py` (Playwright/Chromium) instead of the built-in html2canvas ZIP button.

Text legibility: Use `text-shadow: 0 2px 24px rgba(0,0,0,0.6)` instead of dark panels.

---

## INK BLEED EDGE

For riso/street art systems (s18, s36, s38):
```css
.ink-bleed {
  position: absolute; inset: 0; pointer-events: none; z-index: 1; opacity: 0.12;
  background: radial-gradient(ellipse at 30% 70%, VAR_ACCENT, transparent 60%);
  mix-blend-mode: multiply;
}
```

---

---

## TA-01 · EDITORIAL INDEX

Numbered rows with tags, descriptions, and subtle borders. Magazine-style table of contents.

CSS:
```css
.editorial-index {
  display: flex; flex-direction: column; gap: 0;
  border-top: 1px solid rgba(255,255,255,0.15);
}
.editorial-index .idx-row {
  display: flex; align-items: baseline; gap: 20px;
  padding: 18px 0;
  border-bottom: 1px solid rgba(255,255,255,0.15);
}
.editorial-index .idx-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px; color: VAR_ACCENT; opacity: 0.7;
  min-width: 32px;
}
.editorial-index .idx-tag {
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em;
  color: VAR_ACCENT; border: 1px solid rgba(VAR_ACCENT,0.35);
  padding: 3px 10px; border-radius: 4px;
  min-width: 90px; text-align: center;
}
.editorial-index .idx-body {
  font-size: 15px; line-height: 1.45; opacity: 0.85; flex: 1;
}
```

Usage: Place inside a slide with generous padding. Best on editorial/systems with serif or mixed typography (s25, s48).

---

## TA-02 · TESTIMONIAL CASCADE

Avatar + quote + metadata in a cascading grid. Creates social-proof density.

CSS:
```css
.testimonial-cascade {
  display: grid; grid-template-columns: 56px 1fr;
  gap: 12px 18px; align-items: start;
}
.t-c-avatar {
  width: 56px; height: 56px; border-radius: 50%;
  background: linear-gradient(135deg, VAR_ACCENT, VAR_SECONDARY);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 20px; color: #fff;
}
.t-c-quote {
  font-size: 17px; line-height: 1.5; opacity: 0.9;
  font-style: italic;
}
.t-c-meta {
  grid-column: 2; font-size: 12px; opacity: 0.55;
  letter-spacing: 0.05em; text-transform: uppercase;
}
```

Usage: One cascade per slide, or stack 2–3 with dividers between. Best for S7 proof slides.

---

## TA-03 · SERVICE PILLARS

2×2 or 1×4 numbered cards with headers, short descriptions, and arrow connectors.

CSS:
```css
.pillar-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 16px; margin-top: 24px;
}
.pillar-card {
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px; padding: 22px;
  background: rgba(255,255,255,0.03);
  position: relative;
}
.pillar-card .pillar-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: VAR_ACCENT; margin-bottom: 10px;
}
.pillar-card .pillar-title {
  font-size: 18px; font-weight: 700; line-height: 1.3; margin-bottom: 8px;
}
.pillar-card .pillar-desc {
  font-size: 13px; line-height: 1.45; opacity: 0.7;
}
.pillar-arrow {
  position: absolute; right: -10px; top: 50%; transform: translateY(-50%);
  color: VAR_ACCENT; opacity: 0.4; font-size: 18px;
}
```

Usage: 2×2 grid for square, 1-column stack for Stories. Omit arrows on last card. Best for S4–S6 feature slides.

---

## TA-04 · PRESS QUOTE STRIP

Large italic quote with a horizontal logo/text row beneath. Editorial authority.

CSS:
```css
.press-strip {
  display: flex; flex-direction: column; gap: 28px;
}
.press-quote {
  font-size: clamp(24px, 3.2vw, 32px);
  font-style: italic; line-height: 1.35;
  font-weight: 400; opacity: 0.92;
}
.press-row {
  display: flex; align-items: center; gap: 18px;
  border-top: 1px solid rgba(255,255,255,0.12);
  padding-top: 18px;
}
.press-logo {
  font-size: 13px; font-weight: 700; letter-spacing: 0.08em;
  text-transform: uppercase; color: VAR_ACCENT; opacity: 0.8;
}
.press-divider {
  width: 1px; height: 18px; background: rgba(255,255,255,0.15);
}
.press-source {
  font-size: 12px; opacity: 0.5; letter-spacing: 0.05em;
}
```

Usage: Full-width inside slide. Best for S5–S7 credibility moments.

---

## TA-05 · GLASSMORPHISM PANEL ⚠️ html2canvas PARTIAL

`backdrop-filter` may render as solid color or fail silently on html2canvas ZIP export. **Always test the ZIP export before delivery.**

CSS:
```css
.glass-panel {
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(24px) saturate(140%);
  -webkit-backdrop-filter: blur(24px) saturate(140%);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
  padding: 28px 32px;
}
```

Variants:
- **Light system:** `background: rgba(255,255,255,0.55); border: 1px solid rgba(0,0,0,0.06);`
- **Tinted:** Add `box-shadow: inset 0 1px 0 rgba(255,255,255,0.1);`

**html2canvas-safe fallback:** If export breaks, replace with:
```css
.glass-panel-fallback {
  background: rgba(30,30,40,0.85);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
  padding: 28px 32px;
}
```

Usage: Overlay on busy backgrounds (gradient + geo) to keep text legible. Best for stat cards, testimonial boxes, CTA panels. Always test ZIP export.

---

## TA-06 · TICKER / MARQUEE

Scrolling or repeating text bar. Adds motion energy and brand repetition.

CSS:
```css
.ticker-wrap {
  overflow: hidden; white-space: nowrap;
  border-top: 1px solid rgba(255,255,255,0.1);
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding: 10px 0; opacity: 0.5;
}
.ticker-track {
  display: inline-block;
  font-size: 12px; letter-spacing: 0.15em; text-transform: uppercase;
  animation: ticker 20s linear infinite;
}
@keyframes ticker {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
```

HTML:
```html
<div class="ticker-wrap">
  <div class="ticker-track">
    WORQAI · CV OPTIMIZADO · ATS FRIENDLY · ENTREVISTAS · WORQAI · CV OPTIMIZADO · ATS FRIENDLY · ENTREVISTAS ·
  </div>
</div>
```

Usage: Place at top or bottom of a slide. Best for S1 or S4 rhythm breaks.

---

## TA-07 · MOCK UI COMPONENTS

Simulated interfaces: CV lines, terminal bars, checkboxes. Shows instead of tells.

**CV Line Mock:**
```html
<div class="cv-mock" style="display:flex;flex-direction:column;gap:8px;">
  <div style="height:10px;width:70%;background:linear-gradient(90deg,VAR_ACCENT,transparent);border-radius:4px;opacity:0.5;"></div>
  <div style="height:10px;width:90%;background:linear-gradient(90deg,VAR_SECONDARY,transparent);border-radius:4px;opacity:0.35;"></div>
  <div style="height:10px;width:55%;background:linear-gradient(90deg,VAR_ACCENT,transparent);border-radius:4px;opacity:0.5;"></div>
</div>
```

**Terminal Bar:**
```html
<div class="term-bar" style="display:flex;align-items:center;gap:8px;padding:10px 14px;background:rgba(0,0,0,0.4);border-radius:8px;border:1px solid rgba(255,255,255,0.08);">
  <div style="width:10px;height:10px;border-radius:50%;background:#ff6b6b;"></div>
  <div style="width:10px;height:10px;border-radius:50%;background:#feca57;"></div>
  <div style="width:10px;height:10px;border-radius:50%;background:#1dd1a1;"></div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:12px;opacity:0.5;margin-left:4px;">~/cv-ats.pdf</div>
</div>
```

**Checkbox Panel:**
```html
<div class="chk-panel" style="display:flex;flex-direction:column;gap:12px;">
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="width:20px;height:20px;border-radius:4px;border:2px solid VAR_ACCENT;display:flex;align-items:center;justify-content:center;"><span style="color:VAR_ACCENT;font-size:12px;">✓</span></div>
    <span style="font-size:15px;opacity:0.9;">ATS parseable</span>
  </div>
</div>
```

Usage: Embed inside problem/fix slides. One mock UI per carousel minimum for elite quality.

---

## TA-08 · STAMP / ORNAMENT

Circular stamps, corner frames, hand-drawn ornaments. Adds editorial texture.

**Circular Stamp:**
```css
.stamp {
  width: 90px; height: 90px; border-radius: 50%;
  border: 2px solid VAR_ACCENT; opacity: 0.6;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em;
  text-align: center; line-height: 1.3; color: VAR_ACCENT;
  transform: rotate(-12deg);
}
```

**Corner Frame:**
```css
.corner-frame {
  position: absolute; width: 40px; height: 40px;
  border-color: VAR_ACCENT; opacity: 0.25;
}
.corner-frame.top-left    { top: 28px; left: 28px; border-top: 2px solid; border-left: 2px solid; }
.corner-frame.top-right   { top: 28px; right: 28px; border-top: 2px solid; border-right: 2px solid; }
.corner-frame.bottom-left { bottom: 28px; left: 28px; border-bottom: 2px solid; border-left: 2px solid; }
```

**Ornament Characters:**
```css
.ornament {
  font-size: 18px; color: VAR_ACCENT; opacity: 0.35;
  line-height: 1; display: inline-block;
}
/* Use: ✦ ✧ ✶ ✷ ◆ ◇ ◈ */
```

Usage: Max 2 decorative elements per slide. At least one slide must have ZERO (silence beat). Stamp = authenticity mark. Corner frames = editorial framing. Ornaments = scrapbook texture.

---

## TA-09 · WATERMARK

Large background letter or number for brand presence and depth.

CSS:
```css
.watermark {
  position: absolute; pointer-events: none; z-index: 0;
  font-size: clamp(280px, 40vw, 420px);
  font-weight: 900; line-height: 1;
  color: VAR_ACCENT; opacity: 0.035;
  user-select: none;
}
```

Position variants:
- **Brand letter:** `top: 50%; left: 50%; transform: translate(-50%, -50%);` — centered, huge "W"
- **Bleed numeral:** `top: -40px; right: -20px;` — slide number as giant decoration
- **Offset mark:** `bottom: -60px; left: -30px;` — asymmetric weight

Usage: One watermark per carousel minimum. Always `z-index: 0` so it sits behind content.

---

## RULE OF THUMB

- **Most carousels need only ONE technique beyond the base gradient.**
- **Good carousels use 2–3 layered techniques.**
- **Elite carousels use max 4 techniques per slide.** Intentional restraint beats maxxing every slider. Layer complexity scales with diminishing returns.
- **Never use more than 4 techniques on a single slide.** If you think you need 5, remove the one that contributes least.
- **Default stack for dark systems:** gradient + GEO-13 wireframe + grain (3 layers — at the limit)
- **Default stack for warm systems:** gradient + blob + grain (3 layers — at the limit)
- **Add ONE effect when:** the topic is tech/data (terminal), the hook needs energy (zoom rings), or the system demands it (scan lines for cyberpunk). Remove one existing layer to make room.
- **Elite tier requires:** directed rhythm (tension/silence/impact/release), at least one silence slide (≤2 layers, 0 decorative), 3–4 fonts per carousel, at least one mock UI component, absolute positioning for at least one editorial layout (but never in the central text zone)
