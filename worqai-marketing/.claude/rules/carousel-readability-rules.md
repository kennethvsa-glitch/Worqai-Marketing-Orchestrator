# Carousel Readability & Color Theme Rules

Applies to every HTML carousel built with html-carousel-builder or any carousel-skills. These rules are **non-negotiable** — text must always be readable from 3 feet away.

---

## The Golden Rule

**TEXT MUST ALWAYS BE READABLE.** The text color must contrast strongly with the background. Never put light text on a light background. Never put dark text on a dark background. If the background is busy/complex, put the text inside a semi-transparent liquid-glass box so the text is readable.

---

## The Four Themes (Always Distribute Evenly)

When generating carousels in batches, produce **equal counts** across these four themes:

| Theme | Background | Body Text | Accent Text | Glass Box | Use Case |
|---|---|---|---|---|---|
| **Dark** | `#0A0A0A` | `#FAFAFA` | `#C7FF3A` (lime) | `rgba(255,255,255,0.85)` + `blur(10px)` | Black, sleek, high-contrast |
| **Light** | `#F5F5F5` | `#0A0A0A` | `#C7FF3A` (lime) | `rgba(255,255,255,0.85)` + `blur(10px)` | Clean, bright, accessible |
| **Dark Blue** | `#0f172a` | `#FAFAFA` | `#C7FF3A` (lime) | `rgba(15,23,42,0.85)` + `blur(10px)` | Professional, corporate |
| **Grey** | `#555555` | `#FAFAFA` | `#C7FF3A` (lime) | `rgba(255,255,255,0.85)` + `blur(10px)` | Neutral, balanced |

**Distribution rule:** If building 19 carousels, split ~5 dark, ~5 light, ~5 dark-blue, ~4 grey. Never put all of them in one theme.

---

## Element-by-Element Rules

### 1. Backgrounds (`html, body, .slide`)

| Theme | `html, body` | `.slide` |
|---|---|---|
| Dark | `#0A0A0A` | `#0A0A0A` |
| Light | `#F5F5F5` | `#FAFAFA` |
| Dark Blue | `#0f172a` | `#0f172a` |
| Grey | `#555555` | `#555555` |

**Theme mismatch:** If the filename says `dark-carousel` but the CSS uses `#F5F5F5`, **fix it.** Theme = filename promise.

---

### 2. Primary Text (Headlines, Body, Proof, Stats)

| Theme | Text Color | NEVER use |
|---|---|---|
| Dark | `#FAFAFA` or `#E5E5E5` | `#0A0A0A`, `#333333`, any dark |
| Light | `#0A0A0A` or `#1A1A1A` | `#FAFAFA`, `#E5E5E5`, any light |
| Dark Blue | `#FAFAFA` or `#E5E5E5` | `#0A0A0A`, `#333333` |
| Grey | `#FAFAFA` or `#E5E5E5` | `#0A0A0A`, `#333333` |

**Specific elements:**

| Element | Dark | Light | Dark Blue | Grey |
|---|---|---|---|---|
| `.headline` | `#FAFAFA` | `#0A0A0A` | `#FAFAFA` | `#FAFAFA` |
| `.body-text` | `#E5E5E5` | `#1A1A1A` | `#E5E5E5` | `#E5E5E5` |
| `.hook-display` | `#FAFAFA` | `#0A0A0A` | `#FAFAFA` | `#FAFAFA` |
| `.hook-sub` | `#E5E5E5` | `#333333` | `#E5E5E5` | `#E5E5E5` |
| `.proof-stmt` | `#FAFAFA` | `#0A0A0A` | `#FAFAFA` | `#FAFAFA` |
| `.proof-ctx` | `#E5E5E5` | `#333333` | `#E5E5E5` | `#E5E5E5` |
| `.stat-context` | `#FAFAFA` | `#0A0A0A` | `#FAFAFA` | `#FAFAFA` |
| `.stat-pct` | `#FAFAFA` | `#0A0A0A` | `#FAFAFA` | `#FAFAFA` |
| `.source-tag` | `#FAFAFA` (opacity 1.0) | `#666666` (opacity 1.0) | `#94a3b8` | `#D1D5DB` |
| `.proof-city` | `#FAFAFA` | `#333333` | `#94a3b8` | `#D1D5DB` |

**Opacity rule:** Never leave `opacity: 0.40` or `0.75` on text. On dark backgrounds, low opacity white text is invisible. On light backgrounds, low opacity black text is invisible. Set `opacity: 1.0` on all text elements.

---

### 3. The Brand "worqai"

| Theme | `.worq` | `.ai` | Shadow/Stroke |
|---|---|---|---|
| Dark | `#FAFAFA` (white) | `#C7FF3A` (lime) | None needed on dark |
| Light | `#0A0A0A` (black) | `#C7FF3A` (lime) | `text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;` |
| Dark Blue | `#FAFAFA` (white) | `#C7FF3A` (lime) | `text-shadow: 0 0 10px rgba(199,255,58,0.4);` (lime glow) |
| Grey | `#FAFAFA` (white) | `#C7FF3A` (lime) | `text-shadow: 0 0 10px rgba(199,255,58,0.4);` (lime glow) |

---

### 4. "Desliza →" Button

| Theme | Text | Border | Background |
|---|---|---|---|
| Dark | `#FFFFFF` (white) | `#C7FF3A` (lime) | `transparent` |
| Light | `#0A0A0A` (black) | `#C7FF3A` (lime) | `transparent` |
| Dark Blue | `#FFFFFF` (white) | `#C7FF3A` (lime) | `transparent` |
| Grey | `#FFFFFF` (white) | `#C7FF3A` (lime) | `transparent` |

**NEVER green-on-green:** Do not use `#C7FF3A` text on a `#C7FF3A` background or border. The text must be a different color from its background.

---

### 5. CTA Card (Last Slide)

| Theme | Card BG | Card Text | Card Border | Offers |
|---|---|---|---|---|
| Dark | `#0A0A0A` | `#FAFAFA` | `#C7FF3A` (lime) | BOLD, `#FAFAFA` |
| Light | `#FFFFFF` | `#0A0A0A` | `#C7FF3A` (lime) | BOLD, `#0A0A0A` |
| Dark Blue | `#0f172a` | `#FAFAFA` | `#C7FF3A` (lime) | BOLD, `#FAFAFA` |
| Grey | `#4B5563` | `#FAFAFA` | `#C7FF3A` (lime) | BOLD, `#FAFAFA` |

---

### 6. "WORQAI.IO" URL Box

| Theme | Text | Border | Box Background |
|---|---|---|---|
| Dark | `#FAFAFA` | `#C7FF3A` (dashed) | `transparent` or dark |
| Light | `#0A0A0A` | `#C7FF3A` (dashed) | `#FAFAFA` |
| Dark Blue | `#FAFAFA` | `#C7FF3A` (dashed) | `transparent` or dark blue |
| Grey | `#FAFAFA` | `#C7FF3A` (dashed) | `transparent` or grey |

**Always add a border or box so it stands out.**

---

### 7. Counter ("01 / 07")

| Theme | Color | NEVER |
|---|---|---|
| Dark | `#FAFAFA` solid | `rgba(255,255,255,0.25)` |
| Light | `#0A0A0A` solid | `rgba(0,0,0,0.25)` |
| Dark Blue | `#FAFAFA` solid | `rgba(255,255,255,0.25)` |
| Grey | `#FAFAFA` solid | `rgba(255,255,255,0.25)` |

---

### 8. Stat Numbers (Big Numbers, Metrics)

| Theme | Color | Enhancement |
|---|---|---|
| Dark | `#C7FF3A` (lime) | `text-shadow: 0 0 20px rgba(199,255,58,0.3);` |
| Light | `#C7FF3A` (lime) | `text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;` (black stroke) |
| Dark Blue | `#C7FF3A` (lime) | `text-shadow: 0 0 20px rgba(199,255,58,0.3);` |
| Grey | `#C7FF3A` (lime) | `text-shadow: 0 0 20px rgba(199,255,58,0.3);` |

---

### 9. Lime Badges (`.lime-badge`)

| Badge BG | Badge Text | NEVER |
|---|---|---|
| `#C7FF3A` (lime) | `#0A0A0A` (black) | `#FAFAFA` or `#E5E5E5` on lime — invisible |

This is universal across all themes. Lime badges ALWAYS have black text inside.

---

### 10. Liquid-Glass Boxes (`.glass-block`, `.text-backdrop`)

When the background is busy (SVG patterns, noise, gradients, complex shapes), **all text blocks must be wrapped in a liquid-glass box:**

```css
.liquid-glass {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 20px;
}
```

| Theme | Glass BG | Text Inside |
|---|---|---|
| Dark | `rgba(255,255,255,0.85)` + `blur(10px)` | `#0A0A0A` (black) |
| Light | `rgba(255,255,255,0.85)` + `blur(10px)` | `#0A0A0A` (black) |
| Dark Blue | `rgba(15,23,42,0.85)` + `blur(10px)` | `#FAFAFA` (white) |
| Grey | `rgba(255,255,255,0.85)` + `blur(10px)` | `#0A0A0A` (black) |

**Critical:** When text is inside a white glass box, the text must be **black**. When text is inside a dark blue glass box, the text must be **white**. The glass box provides the contrast, not the text color against the background.

**Apply liquid-glass to:** headlines, body text, CTA cards, hook displays, proof statements, stat contexts, and any text block on a busy background.

---

### 11. Glass Blocks (Good/Bad)

| Element | `.glass-block` | `.glass-block.bad` | `.glass-block.good` |
|---|---|---|---|
| Background | `rgba(255,255,255,0.85)` + `blur(10px)` | `rgba(255,255,255,0.85)` + `blur(10px)` | `rgba(255,255,255,0.85)` + `blur(10px)` |
| Border | `rgba(255,255,255,0.3)` | `rgba(255,92,60,0.3)` (coral) | `rgba(199,255,58,0.3)` (lime) |
| `.glass-tag` | `#0A0A0A` (black) | `#FF5C3C` (coral) | `#0A0A0A` (black) |
| `.glass-text` | `#0A0A0A` (black) | `#0A0A0A` (black) | `#0A0A0A` (black) |

**NEVER put colored text inside a colored box.** Green text on a green box is unreadable. Red text on a red box is unreadable. Always: **white glass box + black text**, with a colored border to indicate good/bad.

---

### 12. Decorative Elements

| Theme | Glows | Dots/Grids | Ghost BG | SVG Strokes |
|---|---|---|---|---|
| Dark | `rgba(199,255,58,0.04)` | `rgba(199,255,58,0.25)` | `rgba(255,255,255,0.035)` | `rgba(255,255,255,0.2)` |
| Light | `rgba(199,255,58,0.04)` | `rgba(199,255,58,0.25)` | `rgba(10,10,10,0.035)` | `rgba(0,0,0,0.15)` |
| Dark Blue | `rgba(96,165,250,0.08)` | `rgba(96,165,250,0.25)` | `rgba(255,255,255,0.025)` | `rgba(96,165,250,0.3)` |
| Grey | `rgba(255,255,255,0.06)` | `rgba(255,255,255,0.25)` | `rgba(255,255,255,0.03)` | `rgba(255,255,255,0.2)` |

Decoratives must never compete with text for attention. They are background texture, not content.

---

## Pre-Export Readability Checklist

Run this on every carousel before delivery:

- [ ] **Theme check:** Does `html, body` background match the filename (dark/light/blue/grey)?
- [ ] **Contrast check:** Is every text element readable from 3 feet away?
- [ ] **Light-on-light check:** No `#FAFAFA` or `#E5E5E5` text on `#F5F5F5` or `#FAFAFA` backgrounds.
- [ ] **Dark-on-dark check:** No `#0A0A0A` or `#333333` text on `#0A0A0A` or `#0f172a` backgrounds.
- [ ] **Glass box check:** Is text inside `.glass-block` or `.text-backdrop` the correct color for the glass background?
- [ ] **Badge check:** `.lime-badge` has black text (`#0A0A0A`), not white.
- [ ] **CTA check:** Last slide text is bold and readable, offers stand out.
- [ ] **Desliza button:** Not green-on-green. Text is different color from background.
- [ ] **Counter:** Solid color, not transparent `rgba(..., 0.25)`.
- [ ] **Broken characters:** No `???` or `` in text. Spanish accents (`á é í ó ú ñ ¿ ¡`) are present.
- [ ] **Liquid-glass on busy slides:** Any slide with complex SVG backgrounds has text in glass boxes.

---

## When in Doubt

> **Put text in a box.** Semi-transparent white or dark-blue glass box behind text makes it readable on ANY background. This is the single most reliable fix for readability issues.

> **Lime green (`#C7FF3A`) is only for accents.** Badges, borders, the "ai" in "worqai", stat numbers, and decorative dots. Never for large body text, headlines, or CTA text on any background.
