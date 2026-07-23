# Carousel Layout Checks

Applies to every HTML carousel built with html-carousel-builder. Run these checks mentally before marking a slide done.

**Also see:** `carousel-readability-rules.md` — the companion rules for text contrast, color themes, and readability. These two files work together: layout-checks covers structure and composition, readability-rules covers color contrast and theme consistency.

---

## The Most Common Failure: Text Wider Than Its Container

Letter-spacing multiplies. At `letter-spacing: 0.30em` a 14-character string at 8px is roughly 170px wide — wider than a 132px circle. This is the #1 source of clipped text.

**Rule:** Any text inside a container narrower than 200px (stamps, badges, pills, tags) must use `letter-spacing` no higher than `0.15em`. Cut to `0.10em` if the string is longer than 12 characters.

**Stamp/circle containers specifically:**
- Size the circle AFTER you know the text, not before.
- Formula: `container_width ≥ (font_size × char_count × 1.6) + horizontal_padding`
- Prefer splitting long strings across two lines rather than shrinking font-size below 8px.
- Never put more than 3 lines inside a circle stamp. Two is safer.

---

## Absolute-Positioned Decorative Elements Overlapping Content

Stamps, ornaments, and script flourishes are positioned from `bottom` or `right`. Dynamic content (lists, grids) grows downward from `top`. They will collide when the list is taller than expected.

**Rule:** Any decorative element positioned from `bottom` must be placed at `bottom ≤ footer_clearance + element_height`. Default safe zone: `bottom: 72px–100px` for a 1080px slide with a 48px footer.

**Before finalizing slide 3-style list slides:** Count the rows × row height, add the list's `top` value, and confirm the decorative element's top edge starts below that sum.

---

## Z-Index Stacking: Decorative Below Content

Content rows, text, and CTAs: `z-index: 3`
Decorative elements (stamps, ornaments, stripes): `z-index: 2–4`

If a decorative element must sit on top of a background layer but below text, use `z-index: 4` max. Never give a purely decorative element a higher z-index than readable content.

---

## Script Font Overflow in Fixed Containers

Allura, Parisienne, and similar scripts have tall ascenders and deep descenders. A 96px Allura line occupies ~130px of vertical space. A 64px Allura line occupies ~90px.

**Rule:** When stacking a script element above a content block (next steps, CTA info, handle), leave at least 60px of clear vertical space between the script baseline and the next element's top edge.

---

## Hero Text Overflow on Padded Stages

Display headlines on slides with horizontal padding will clip if the font size is not calculated against the actual content width, not the slide width.

**Rule:** Before setting any headline above 100px, calculate the available width first.
`content_width = slide_width (1080) - (padding_left + padding_right)`

For a stage with `padding: 200px 64px`, content width = **952px**.

Archivo Black at 148px × 8 chars ("LLEVEMOS") with `-0.05em` letter-spacing ≈ 950px — safe.
Archivo Black at 220px × 8 chars = ~1400px — clips.

**Formula:** `max_font_size ≈ content_width / (char_count × 0.72)` for Archivo Black / wide grotesques.
For narrower fonts (Cormorant, Fraunces), use `× 0.55` instead of `× 0.72`.

Never set a multi-character display headline above 160px without verifying the longest line fits the content width.

---

## Pre-Export Checklist (run on every slide before delivery)

- [ ] All text inside circles/stamps fits within the border — no clipping
- [ ] No decorative element overlaps a content row or readable text
- [ ] Letter-spacing on strings inside containers < 200px is ≤ 0.15em
- [ ] Script font has 60px+ clearance above the next content block
- [ ] Footer and dots are not covered by any absolute element
- [ ] Slide renders correctly at 1080×1080 in the browser before export

---

## v2 Visual Primitive Rules

These apply to every carousel built after 2026-05-17.

### Text symbols → SVG icons

Inside content containers (terminal output, warning banners, checklist markers, icon grids), text symbols like `!`, `→`, `✓`, `✗`, `i` should be SVG icon references, NOT Unicode characters.

```html
<!-- WRONG: text symbol in a content container -->
<div class="warn-icon">!</div>

<!-- RIGHT: SVG sprite reference -->
<svg class="warn-icon icon" aria-hidden="true"><use href="#icon-warning"/></svg>
```

The sprite is auto-injected at the top of every carousel. 21 names available: `warning`, `error`, `ok`, `info`, `clock`, `arrow-right`, `arrow-down`, `arrow-curved`, `arrow-thick`, `chart`, `trending-up`, `trending-down`, `target`, `lock`, `key`, `shield`, `heart`, `lightning`, `trophy`, `star`, `magnifier`.

### Gradient text MUST be SVG, never CSS

`background-clip: text` is broken in html2canvas — the in-HTML ZIP button exports transparent letters. Use `text_treatment: "gradient"` in the spec; the renderer wraps the text in an inline `<svg><text>` with `linearGradient` fill. Works in both pipelines.

### Card depth MUST come from SVG drop-shadow

CSS `box-shadow` is broken in html2canvas. Don't write `box-shadow:` for visible depth — apply one of the SVG filter classes:

```css
.my-card { filter: url(#shadow-sm); }
/* or use .shadow-sm / .shadow-md / .shadow-lg helper classes */
```

Filters are defined in the sprite block at the top of every carousel.

### Playwright-only effects MUST be flagged

When a slide uses `backdrop-filter` (real glassmorphism), `mix-blend-mode`, or `filter: blur()`, set in the spec:

```json
"effects": { "requires_playwright_export": true }
```

This is documentation for humans — it warns that the in-HTML ZIP button will NOT capture the effect correctly and that `carousel_exporter.py` must be used.

### Decorative budget unchanged

SVG starbursts count as decoratives. Cap is still 2 per slide. Silence-beat slides get 0.

---

## AI-Background Carousels — Additional Rules (2026-05-27)

These apply to every carousel that uses `bg_recipe: "extracted"` or any `geo-ai-bg` panel.

### 1. Every slide MUST declare `density`

AI backgrounds require per-slide scrim control. Every slide spec MUST have a `"density"` field:

| Layout type | Required density | Why |
|---|---|---|
| `slide-hook-lockup`, `slide-big-number`, `slide-pull-quote`, `slide-typeset-poster`, `slide-massive-number`, `slide-full-bleed-type` | `"heavy"` | Large text needs dark background — no exceptions |
| `slide-terminal`, `slide-input-output`, `slide-waffle-chart`, `slide-before-after`, `slide-before-after-stacked` | `"demo"` | Demo layouts benefit from lighter scrim so the photo contextualizes the demo |
| `slide-cta` | `"cta"` | CTA needs high contrast on the button |
| `slide-checklist`, `slide-myth-vs-fact`, `slide-icon-grid`, `slide-stat-row` | `"heavy"` | Multiple text blocks need strong scrim |

Omitting `density` is treated as medium. Medium is not acceptable for hook/stat/CTA slides on AI backgrounds — text will fight the photo.

### 2. Background extraction quality — required before use

Never use a background kit in production unless it has passed ALL of:
- `[SANITY]` check in `panel_extractor.py` — no internal seams
- Edge brightness check — no bright outer borders (mean > 228 in edge band)
- If any panel shows a visible white/gray frame → run `--fix-kit` with `--trim-gutters 3` before use

**Banned kits until re-extracted with trim:**
- `digital-glass-full` — irregular grid, panels contain 2 sub-panels → do NOT use
- `pastel-waves` — extremely light imagery, fights dark system text even after trimming → do NOT use on dark systems

### 3. Spanish accents are MANDATORY — check before render

Missing accents make content non-production-ready. Required in Spanish copy:
- `á é í ó ú ü ñ ¿ ¡`
- Common misses: `diseño` not `diseno`, `así` not `asi`, `querés` not `queres`, `diagnóstico` not `diagnostico`, `años` not `anos`
- Run a grep check: `grep -o "[a-zA-Z]*[aeiouAEIOU]\(n\|s\|o\)[a-zA-Z]*" spec.json` to find words that should have accents

### 4. Cards and panels must not be ultra-transparent

Cards with `rgba(255,255,255,0.03)` or less are invisible on any background. Minimum card backgrounds:
- Dark systems: `rgba(255,255,255,0.07)` minimum
- Light systems: `rgba(0,0,0,0.06)` minimum
- Demo panels (terminal, input-output, before-after): `rgba(255,255,255,0.09)` minimum — they need to read as panels, not suggestions

### 5. Body text minimum opacity on AI-bg slides

Any body copy (not headlines or kickers) on a slide with an AI background must have `opacity >= 0.88`. The default inherit from the system may be 0.7 — always override upward in `custom_css` for AI-bg slides.

### 6. Background focal safety

Before finalizing any AI-bg slide: mentally trace where the photo's brightest/highest-contrast focal points are. They must NOT be behind the headline, CTA button, or primary stat number. If they are → either switch panels (different panel index via `layers`) or increase scrim density.

### 7. Starburst rules on AI-bg carousels

Limit to 1 starburst per carousel (not per slide) when using AI backgrounds. Starbursts on terminal/diagnostic slides look random — reserve for hook slides only.

---

## Pre-Export AI-Background Checklist

In addition to the standard pre-export checklist, also verify:

- [ ] Every slide has `"density"` set in the spec
- [ ] Background kit has passed sanity + edge brightness check
- [ ] All Spanish accents correct (á é í ó ú ñ ¿ ¡)
- [ ] No card or panel is ultra-transparent (< 0.07 opacity)
- [ ] Body text opacity ≥ 0.88 across all slides
- [ ] Photo focal points do not sit behind headline/CTA
- [ ] Max 1 starburst decorative in the whole carousel
