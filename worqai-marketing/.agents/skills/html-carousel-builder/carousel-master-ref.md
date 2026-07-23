---
name: carousel-master-ref
description: >
  Single-file cheat sheet. Replaces tokens.md + build.md + workflow.md +
  spec-schema.md + slide-templates.md for standard builds.
  Read this file, write spec, run build command. Nothing else required.
load: always, first thing, before writing any spec
---

# CAROUSEL MASTER REFERENCE

> **Read this. Write the spec. Run the command. Done.**
> `py scripts/build_carousel.py production/your-spec.json`

---

## 1. SYSTEM SELECTION

Pick one row. Engine applies all tokens automatically from the system ID.

| ID | Name | Family | Accent | Display / Body | Best for |
|----|------|--------|--------|----------------|----------|
| s01 | NOIR GOLD | dark | #C8A84B | Space Grotesk 700 / Inter 300 | Premium, luxury, financial |
| s02 | ROYAL BLUE | dark | #4a8fff | Montserrat 700 / Inter 300 | Tech, SaaS, corporate |
| s03 | DEEP FOREST | dark | #5ab07a | Space Grotesk 700 / Inter 300 | Wellness, sustainability |
| s04 | CRIMSON NIGHT | warm | #e05a7a | Poppins 700 / Cormorant Garamond 400 | Bold emotional, B2C |
| s05 | STARK WHITE | light | #1463F3 | Poppins 700 / Inter 300 | Minimal SaaS, white bg |
| s06 | AURORA | dark | #a855f7 | Space Grotesk 700 / Inter 300 | Artsy, creative studio |
| s07 | BRUTALIST | brutalist | #FF3300 | Space Grotesk 700 / JetBrains Mono 400 | Magazine, high-contrast |
| s08 | GLASSMORPHISM | dark | #60a5fa | Inter 700 / DM Sans 300 | Fintech, AI product |
| s09 | CHROME SILVER | dark | #b0bcd4 | DM Sans 700 / Inter 300 | Architecture, neutral |
| s10 | TERRA COTTA | dark | #e07040 | DM Sans 700 / Cormorant Garamond 400 | Food, lifestyle, LATAM |
| s11 | TROPIC | dark | #00d68f | Nunito 700 / Inter 300 | LATAM youth, tropical |
| s12 | WARM SAND | dark | #d4a862 | DM Sans 700 / Inter 300 | Consultancy, warm brand |
| s13 | OBSIDIAN ROSE | dark | #e879a0 | DM Sans 700 / Cormorant Garamond 400 | Fashion, luxury noir |
| s14 | DEEP SEA | dark | #38bdf8 | Poppins 700 / Inter 300 | Ocean, tech, data |
| s15 | OXFORD NIGHT | dark | #818cf8 | Source Serif 4 700 / Inter 300 | Academic, publishing |
| s16 | NEON GRID | dark | #00f0a0 | Space Grotesk 700 / Inter 300 | Startup, Gen Z, neon |
| s17 | WORQAI VERDE | dark | #C7FF3A | Nunito 700 / Inter 400 | **WorqAI brand — LOCKED** |
| s18 | RISO LAB | light | #ff6b35 | IBM Plex Sans 700 / Space Grotesk 400 | Risograph, zine, print |
| s19 | SWISS GRID | light | #ff0033 | Space Grotesk 700 / Inter 400 | Swiss style, how-to |
| s20 | Y2K CHROME | dark | #44f5ff | Space Grotesk 700 / Inter 400 | Nostalgic tech, Y2K |
| s21 | VAPOR GRIDWAVE | dark | #ffef74 | DM Sans 700 / Space Grotesk 400 | Vaporwave, ironic |
| s22 | DARK ACADEMIA | dark | #c39d63 | Crimson Pro 700 / Inter 400 | Intellectual, book notes |
| s23 | QUIET LUXURY | light | #b89a6c | DM Sans 700 / Cormorant Garamond 400 | Coaching, personal brand |
| s24 | HARAJUKU POP | dark | #ff5faf | Noto Sans JP 700 / Poppins 400 | J-pop, playful edu |
| s25 | SWISS BRUT | brutalist | #ff0015 | Archivo 700 / JetBrains Mono 400 | Swiss brutalist, bold poster |
| s26 | MATTE PASTEL | light | #5c65ff | DM Sans 700 / Inter 300 | Notion/Linear SaaS |
| s27 | NEO RISO | dark | #00ffd1 | Poppins 700 / IBM Plex Sans 400 | Spotify duotone |
| s28 | MONO CONTRAST | dark | #f5f7ff | Work Sans 700 / JetBrains Mono 400 | Single-hue minimalist |
| s29 | CYBERPUNK | cyberpunk | #00ff9c | Space Grotesk 700 / JetBrains Mono 400 | Hacker, tech warnings |
| s30 | ANALOG LO-FI | dark | #ffba3a | Work Sans 700 / Cormorant Garamond 400 | VHS, lo-fi |
| s31 | NEOBRUT | dark | #ff5a5f | Poppins 700 / JetBrains Mono 400 | Neo-brutalism, startup |
| s32 | MAXIMALIST | dark | #ff3f6b | Work Sans 700 / DM Sans 400 | Magazine collage |
| s33 | CLEAN SAAS | dark | #3b82f6 | DM Sans 700 / Inter 400 | Vercel/Linear dark |
| s34 | PANTONE EDI | dark | #ec4899 | Nunito 700 / Inter 400 | Color stories, seasonal |
| s35 | ART DECO | dark | #facc6b | Cinzel Decorative 700 / Cormorant Garamond 400 | Art Deco luxury |
| s36 | MEXICAN MOD | dark | #1f7a8c | Work Sans 700 / DM Sans 400 | Rivera palette, civic |
| s37 | AFROFUTURIST | dark | #f97316 | DM Sans 700 / Space Grotesk 400 | Tech/culture mashup |
| s38 | LATAM MURAL | dark | #1a535c | Nunito 700 / DM Sans 400 | Street art, social |
| s39 | MINIMAL JPN | light | #1f2933 | Noto Sans 700 / Noto Serif 400 | Minimal Japanese, calm |
| s40 | GLITCH | dark | #22d3ee | JetBrains Mono 700 / Space Grotesk 400 | Datamosh, glitch |
| s41 | HOLOGRAPHIC | dark | #c084fc | Nunito 700 / Inter 400 | Holographic, beauty/tech |
| s42 | ARCHITECTURAL | dark | #e5e7eb | DM Sans 700 / Inter 400 | Architecture mag |
| s43 | GEN Z POP | dark | #ff006e | DM Sans 700 / Poppins 400 | Bold Gen Z, playful |
| s44 | CHALKBOARD | dark | #f9fafb | IBM Plex Sans 700 / Space Grotesk 400 | Course notes, frameworks |
| s45 | RISO BLUE-RED | light | #ff3368 | Archivo 700 / Inter 400 | Two-color riso |
| s46 | BLUEPRINT | dark | #38bdf8 | JetBrains Mono 700 / IBM Plex Sans 400 | Technical diagrams |
| s47 | STONE LIBRARY | light | #1f2937 | DM Sans 700 / Source Serif 4 400 | Institutional, public |
| s48 | BOUTIQUE EDI | light | #9A7330 | DM Sans 700 / Cormorant Garamond 400 | Premium editorial, ivory |

**Light systems** — add `class="light-system"` to `<body>`: s05, s18, s19, s23, s25, s26, s39, s47, s48
**Batch law:** ≥2 carousels in one session → each must use a different family (dark / light / warm / brutalist / cyberpunk).
**s17 is brand-locked.** Use only for WorqAI content. Never reassign unless explicitly asked.
**Prefer s18–s48** (Extended 30) over s01–s17 for visual distinctiveness.

---

## 2. GEO LAYERS (pick up to 3 per slide)

| Layer ID | Best for |
|----------|----------|
| `pw-grid` | Cyberpunk wireframe |
| `scan-lines` | Dark, glitch, cyberpunk |
| `glow-orb` | Soft light bloom, emotional |
| `zoom-rings` | Focus burst, shock/data slide |
| `grid-bg` | Brutalist, Swiss, editorial |
| `diag-band` | Light systems, diagonal accent |
| `blob-bg` | Warm organic shape |
| `vol-light` | Volumetric glow, atmospheric |
| `geo-mesh-noise` | Neural/noise texture |
| `geo-pixel-grid` | Pixel aesthetic |
| `geo-conic-rays` | Radial ray burst |
| `geo-chevron-stripe` | Structured diagonal stripes |
| `geo-iso-grid` | Isometric grid |
| `geo-paper-texture` | Print/paper feel |
| `geo-halftone` | Risograph dots |
| `geo-ribbon-flow` | Flowing curves |
| `geo-circuit-trace` | PCB circuit traces |
| `geo-topo-lines` | Topographic contours |
| `geo-starfield` | Cosmic depth |
| `geo-gradient-bands` | Horizontal gradient bands |
| `svg-blob-tr` | **v2** — real SVG bezier blob, top-right (replaces ellipse `blob-bg`) |
| `svg-blob-bl` | **v2** — SVG blob, bottom-left |
| `svg-blob-center` | **v2** — SVG blob, centered behind hero (low opacity) |
| `svg-blob-asymmetric` | **v2** — aggressive asymmetric SVG blob, top-right |
| `svg-blob-scattered` | **v2** — three scattered small blobs as atmosphere |
| `svg-blob-angular` | **v3** — sharp 8-point polygon, no curves. Brutalist/dark edge tension |
| `svg-blob-crystal` | **v3** — faceted gem-like shards. Cyberpunk/tech premium feel |
| `svg-blob-wave` | **v3** — smooth horizontal S-curve, flows left→right. Warm/light continuity |
| `svg-blob-arch` | **v3** — architectural column/vault shape. Art deco, authority |
| `svg-blob-splatter` | **v3** — irregular paint-splatter edges. Creative, energy, disruption |
| `svg-blob-ribbon` | **v3** — twisted Möbius-style loop. Modern SaaS, motion, transformation |
| `geo-flow-wave` | **v3** — sine-wave line spanning the slide. Use with `continuity: "wave"` |
| `geo-flow-arrow` | **v3** — large dashed arrow entering left, pointing right. Progression signal |
| `geo-flow-data` | **v3** — dotted particle trail with nodes. Tech/diagnostic continuity |
| `geo-contour-flow` | **v3** — flowing topographic contour lines. Dark + brutalist editorial |
| `geo-perspective-grid` | **v3** — 3D wireframe receding to vanishing point. **PLAYWRIGHT ONLY** |
| `geo-hex-mesh` | **v3** — hexagonal tessellation. Molecular / honeycomb pattern |
| `geo-constellation` | **v3** — particle network with pre-generated SVG dots + lines. Static, no Canvas |
| `geo-neon-ring` | **v3** — glowing portal/aura ring with multi-layer SVG circles |
| `geo-bokeh` | **v3** — atmospheric lens-blur orbs. CSS radial-gradient + blur |
| `geo-scan-lines` | **v3** — subtle CRT scan-line texture overlay. All renderers |
| `geo-chromatic-edge` | **v3** — RGB lens aberration bleed at viewport edges. CSS only |
| `geo-data-streaks` | **v3** — static diagonal data-stream lines at 45°. SVG stroke elements |
| `geo-liquid-morph` | **v3** — overlapping blurred circles creating metaball intersections. SVG filter |

**Defaults by family:** dark → `["pw-grid","glow-orb"]` · cyberpunk → `["pw-grid","scan-lines","glow-orb","zoom-rings"]` · brutalist → `["grid-bg"]` · light → `["diag-band"]` · warm → `["blob-bg","vol-light"]`

**v2 blob animation (opt-in):** Pass `{"id":"svg-blob-tr","animate":true}` instead of `"svg-blob-tr"` to enable a 60s rotation drift. Live preview gets gentle motion; html2canvas/Playwright capture as a still frame. Default = OFF (per Q1 decision).

**`blob-bg` is deprecated** (ellipse + `filter: blur` which html2canvas can't capture). Old carousels still render; new builds should use `svg-blob-*`.

**Continuity rule:** Use the same layer IDs across all slides. Only change rotation/translation via CSS.

---

## 3. DECORATIVES (max 2 per slide — silence-beat slides: 0)

| ID | Spec syntax | Description |
|----|-------------|-------------|
| `corner-frame` | `"corner-frame"` | L-brackets top-left + bottom-right |
| `ornament-tr` | `"ornament-tr"` | ✦ ✧ ✦ cluster, top-right |
| `ornament-bl` | `"ornament-bl"` | ✦ ✧ ✦ cluster, bottom-left |
| `ornament` | `"ornament"` | Alias for ornament-tr |
| `chrome-vertical-counter` | `"chrome-vertical-counter"` | Rotated "WORQAI 2026" on right edge |
| `chrome-header-bar` | `"chrome-header-bar"` | Magazine top bar (light/editorial systems) |
| `chrome-badge-stamp` | `{"id":"chrome-badge-stamp","text":"VELAR","value":"PREMIUM"}` | Wax seal badge, top-right. `text` = label (defaults to meta.brand uppercase), `value` = sub-line (defaults to "FREE") |
| `watermark` | `{"id":"watermark","text":"3×"}` | Giant faint letter/symbol behind content |
| `sub-stamp-circle` | `{"id":"sub-stamp-circle","text":"GRATIS"}` | Dashed circle stamp, bottom-right |
| `svg-starburst-spark` | `{"id":"svg-starburst-spark","position":"tr"}` | **v2** — compact 10-point SVG starburst (48px) |
| `svg-starburst-burst` | `{"id":"svg-starburst-burst","position":"bl"}` | **v2** — double-layer 8-point SVG starburst (64px) |
| `svg-starburst-mark` | `{"id":"svg-starburst-mark","position":"tl"}` | **v2** — 16-point fine decorative cluster |

**Minimum:** Every carousel needs ≥2 decoratives total across all slides.

**Brand-aware defaults:** `chrome-badge-stamp`, `chrome-vertical-counter`, `chrome-header-bar`, and `sub-stamp-circle` all pull their default text from `meta.brand`. Override only if you want a different word (e.g. `"GRATIS"` instead of the brand handle on a CTA stamp).

**v2 starburst positions:** `tr` (default), `tl`, `br`, `bl`. Pass as string `"svg-starburst-burst"` (defaults to `tr`) or as dict to override position.

**`ornament` / `ornament-tr` / `ornament-bl` are deprecated** (Unicode `✦ ✧ ✦` looks like phone emoji). Old carousels still render; new builds should use `svg-starburst-*`.

---

## 3.5 LAYOUT → BRAND FIT MATRIX

Pick the layout by **beat AND brand voice**, not beat alone. A correct beat in a wrong-for-the-brand container reads as off-brand.

| Layout | USE for | NEVER use for |
|--------|---------|---------------|
| `slide-terminal` | tech, SaaS, AI, cybersecurity, medical/diagnostic, ATS, dev tools, biotech | food, fashion, fitness/running, lifestyle, candles, beauty, anti-tech brands |
| `slide-terminal-fullscreen` | hacker aesthetic, shock diagnostic, cyberpunk-only deep tech | any warm/light/editorial brand — it always forces dark bg |
| `slide-scroll-code` | dev tools, AI APIs, technical SaaS, code demos | lifestyle, food, fitness, any brand with no code angle |
| `slide-step-flow` | frameworks, protocols, educational content, processes with ≤8-word descriptions | poetic/emotional brands, copy you can't compress to 8 words per step |
| `slide-checklist` | practical, actionable, rule-based brands, contrarian manifestos | luxury (too utilitarian), high-emotion storytelling |
| `slide-tip-blocks` | before/after problem→solution, side-by-side comparisons | single-thought hooks, brands that need silence |
| `slide-pull-quote` | testimonials, manifesto lines, silence beat | data/diagnostic slides |
| `slide-circular-quote` | emotional testimonial beats, warm/personal brands | data-heavy contexts, cyberpunk systems |
| `slide-frame-within-frame` | editorial, luxury, coaching, personal brand | max-data slides, any slide with a long list |
| `slide-big-number` | data/shock, stat-led hooks | mood-led / emotional brands |
| `slide-massive-number` | single dramatic stat with supporting context | multi-stat slides (use data-wall or stat-row instead) |
| `slide-data-wall` | pure data shock, 3–6 simultaneous stats, brutalist/dark systems | warm/lifestyle brands — reads too cold |
| `slide-diagonal-split` | dynamic visual split between a stat and a claim | slides with long body copy (diagonal cuts available space in half) |
| `slide-receipt` | brutalist systems, ironic B2B content, "real numbers" aesthetic | fashion, luxury, warm lifestyle brands |
| `slide-polaroid-grid` | social proof, user-generated content, case study carousels | pure data slides, urgent shock beats |
| `slide-myth-vs-fact` | confrontational beats where a terminal would feel too "tech" | already-quiet brands |
| `slide-typeset-poster` | break/silence beat, poster moments | data-heavy beats |
| `slide-full-bleed-type` | brutalist/Swiss systems, editorial breaks, single-word hooks | data-heavy slides, any slide needing more than 12 words |
| `slide-corner-manifesto` | silence beat, brand positioning statements | any beat that needs visible CTAs or multi-item lists |
| `slide-logo-wall` | social proof / "as seen in" beat | early-stage brands with <5 recognizable logos |
| `slide-morse-code` | playful break slides, WorqAI tech brand moments | any context where the decoded message is the primary CTA |
| `slide-badge-grid` | spec sheets, feature lists, tech SaaS comparison | warm/emotional brands, testimonial beats |
| `slide-waterfall-list` | numbered solution frameworks, step lists that need visual hierarchy | more than 4 steps (numbers collide) |
| `slide-editorial-column` | long-form proof slides, article-style content | hook slides — too much copy for first impression |
| `slide-angled-text` | surprise/break beats, brutalist systems, hook moments | any slide that needs to be readable at a glance for data |
| `slide-tag-cloud` | brainstorm/horizon beats, topic clusters, visual breaks | any slide with a specific CTA or data argument |
| `slide-contrast-knockout` | confrontational hooks, high-contrast brand voices | warm/feminine brands, any brand that avoids hard contrast |
| `slide-stacked-type` | typographic poster moments, silence breaks, brutalist brands | slides with more than 4 lines of unique copy at different sizes |
| `slide-side-by-side` | direct comparison beats, single stat + claim | multi-element slides |
| `slide-minimal-card-stack` | clean solution frameworks, SaaS feature lists | max-visual slides — the spare aesthetic is the point |
| `slide-asymmetric-lockup` | silence beat, editorial emphasis, agency-grade brand demos | any slide that needs balanced visual weight |

**Rule:** If the brand is explicitly anti-tech (running collectives, off-grid lifestyle, analog/lo-fi), the terminal slide reads as ironic at best, dishonest at worst. Pick a non-digital container.

---

## 3.6 v2 TEXT TREATMENTS (opt-in via `copy.text_treatment`)

Apply ONE treatment per slide via the `text_treatment` field in the slide's `copy` block. All are html2canvas-safe.

| Value | Effect | Best for |
|-------|--------|----------|
| `"gradient"` | SVG `<text>` with `linearGradient` fill (accent → white). Renders as inline SVG, NOT CSS `background-clip:text` (which is broken in html2canvas). | Big-number stats, poster headlines, hook display |
| `"glow"` / `"glow-medium"` | Medium `text-shadow` neon glow (multi-layer, accent color) | Headlines on dark systems, CTA keywords |
| `"glow-subtle"` | Light neon-glow | Stat numbers, supporting text |
| `"glow-bold"` | Heavy 4-layer neon-glow | Big-number stats on neon systems |
| `"stroke"` | `-webkit-text-stroke` outlined, transparent fill (Supreme/Nike) | Brutalist systems, poster moments |
| `"stroke-filled"` | Outlined + filled interior | Display headlines that need both punch and readability |

**Rules:**
- One treatment per slide max — they don't stack.
- `gradient` works best on short text (≤14 chars per line). For longer text, prefer `glow` or `stroke`.
- NO auto-apply — every treatment is opt-in (per Q3 decision). Brand systems don't impose defaults.
- `box-shadow` is broken in html2canvas — there's no equivalent for box glow. Apply to text only.

**Spec usage:**
```json
"copy": {
  "headline": "43%",
  "text_treatment": "gradient"
}
```

---

## 3.7 v2 SVG PRIMITIVES (always-available, html2canvas-safe)

All carousels auto-load a single SVG sprite at the top of the file (~3 KB):
- 21 inline icons referenced via `<use href="#icon-NAME"/>`
- 3 drop-shadow filters referenced via `filter: url(#shadow-sm|md|lg)`

### SVG icon library (21 icons)

Reference inside templates with `<svg class="icon" aria-hidden="true"><use href="#icon-warning"/></svg>`. `currentColor` flows through, so size + color come from CSS.

| Group | Names |
|-------|-------|
| Status | `warning`, `error`, `ok`, `info`, `clock` |
| Arrows | `arrow-right`, `arrow-down`, `arrow-curved`, `arrow-thick` |
| Data | `chart`, `trending-up`, `trending-down`, `target` |
| Trust | `lock`, `key`, `shield` |
| Accent | `heart`, `lightning`, `trophy`, `star`, `magnifier` |

**Where they auto-apply (no spec change needed):**
- `slide-warning-banner` → `icon-warning` (override via `copy.icon: "lock"` etc.)
- `slide-terminal` fallback output → `icon-ok` / `icon-warning` / `icon-error`
- `slide-icon-grid` → when `tile.icon` matches a known name (else renders as literal text)

### SVG drop-shadow filters

Auto-applied to: `chrome-badge-stamp`, `proof-card`, `tip-blk`, `step-box`, `faq-item`, `lnum-item`, `cascade-quote`, `sub-stat-card`, `sub-bento-card`, `sub-comment-mock`, `sub-download-card`.

Opt out per-slide via:
```json
"effects": { "shadow": "none" }
```
Or upgrade specific containers in `custom_css` with `.shadow-md` / `.shadow-lg`.

### SVG noise/grain texture

The base `.slide::before` overlay is now a real `feTurbulence` grain (was barely-visible 0.035 opacity). Tunable per slide:
```json
"effects": { "grain_opacity": 0.12 }
```

### Playwright-only effects

When you use real `backdrop-filter` (glassmorphism) or `mix-blend-mode`, mark the slide:
```json
"effects": { "requires_playwright_export": true }
```
This is a flag for humans — it tells you to use `carousel_exporter.py` not the in-HTML button.

---

## 3.8 CROSS-SLIDE CONTINUITY MODES (v3)

Optional `meta.continuity` field creates a visual thread across all slides. When set, decorative rotation is disabled — continuity takes precedence.

| Mode | Effect | Best for |
|------|--------|----------|
| `"wave"` | `geo-flow-wave` on every slide, phase shifts 90° per slide | One continuous sine wave flows through the carousel |
| `"data-pipeline"` | `geo-flow-data` with progressively lighting nodes | Nodes fill in: slide 1 → 2 nodes, slide 5 → all 4 nodes |
| `"corner-frame-evolution"` | Corner frames grow per slide (28px → 70px → 112px...) | Frame builds from minimal to dominant |
| `"number-escalator"` | Watermark counts up per slide (01 → 02 → 03...) | Sequential storytelling, countdowns |
| `dict` (advanced) | Same SVG path with different `transform`/`opacity` per slide via `meta.continuity.positions[]` | Custom flowing shapes, brand blobs, organic continuity |

**Spec usage (string mode):**
```json
"meta": {
  "system": "s17",
  "continuity": "wave",
  ...
}
```

**Spec usage (dict mode):**
```json
"meta": {
  "system": "s17",
  "continuity": {
    "shape": "flow-wave",
    "path": "M200,100 Q400,0 500,200 ...",
    "positions": [
      { "slide": 1, "transform": "translate(100px, 300px) rotate(-20deg) scale(1.2)", "opacity": 0.08 },
      { "slide": 2, "transform": "translate(200px, 250px) rotate(-15deg) scale(1.1)", "opacity": 0.12 }
    ]
  }
}
```

**Rule:** Continuity layers are added *in addition to* per-slide layers. Do not duplicate the flow layer in `slides[].layers`.

---

## 3.9 GLASSMORPHISM PANEL COMPONENT (v3)

First-class depth component: `sub-glass-panel` class. Creates backdrop-filter blur, semi-transparent bg, subtle border, and top highlight line.

```html
<div class="sub-glass-panel">
  <div class="gp-label">ETIQUETA</div>
  <div class="gp-num">73%</div>
  <div class="gp-body">Context text here</div>
</div>
```

**Note:** `backdrop-filter` is Playwright-only (html2canvas flattens it). Mark the slide with `"effects": { "requires_playwright_export": true }` when using glass panels.

---

## 3.10 SYSTEM PERSONALITY — Preferred / Forbidden Layouts per Family

The renderer logs a warning (never a hard fail) when a spec uses a forbidden layout for the active system family. These rules exist because the container and the brand voice must match.

| Family | Preferred layouts | Forbidden layouts |
|--------|-------------------|-------------------|
| `brutalist` | `full-bleed-type`, `diagonal-split`, `contrast-knockout`, `typeset-poster`, `data-wall`, `receipt`, `stacked-type` | `receipt` (too clean), `tag-cloud`, `circular-quote`, `pull-quote` |
| `cyberpunk` | `terminal`, `terminal-fullscreen`, `scroll-code`, `badge-grid`, `big-number`, `massive-number` | `receipt`, `pull-quote`, `circular-quote`, `polaroid-grid`, `editorial-column` |
| `light` | `frame-within-frame`, `editorial-column`, `pull-quote`, `minimal-card-stack`, `waterfall-list`, `checklist`, `step-flow` | `terminal-fullscreen`, `morse-code`, `data-wall`, `contrast-knockout`, `angled-text` |
| `warm` | `pull-quote`, `step-flow`, `checklist`, `stacked-type`, `polaroid-grid`, `circular-quote`, `hook-lockup` | `terminal-fullscreen`, `scroll-code`, `data-wall`, `receipt`, `morse-code` |
| `dark` | all layouts permitted | none |

**Override:** Add `"family_override": true` at the spec level to suppress personality warnings when you intentionally break the rule (e.g., a receipt layout on a brutalist system for ironic effect).

---

## 4. LAYOUTS (one layout per slide, pick by pacing beat)

### 4.1 Core Layouts (original 24)

| Layout | Beat | Required copy fields |
|--------|------|----------------------|
| `slide-hook-lockup` | hook | `headline`, `body`, `swipe_prompt`; opt: `kicker`, `stat_number` |
| `slide-big-number` | data/shock | `stat_number`, `stat_context`; opt: `kicker`, `headline`, `source` |
| `slide-terminal` | shock/diagnostic | `headline`, `command`, `output_lines` [{type,text}] · types: cmd/ok/warn/err/info · opt: `tab_title` (defaults to `terminal.sh`) |
| `slide-tip-blocks` | solution | `headline`, `tips` [{problem,fix}]; opt: `kicker`, `items` |
| `slide-before-after` | diagnostic | `headline`, `before_items`, `after_items`, `before_score`, `after_score` |
| `slide-checklist` | solution | `headline`, `items` or `tips`; opt: `kicker` |
| `slide-cta` | cta | `question`, `cta_keyword`, `reward`; opt: `url` |
| `slide-pull-quote` | break/testimonial | `quote`; opt: `attribution`, `author_name`, `author_role`, `author_initial` |
| `slide-pull-quote-author` | testimonial | `quote`, `author`; opt: `kicker`, `role` |
| `slide-proof` | proof | `headline`, `quote`, `attribution`; opt: `stat_number`, `body` |
| `slide-step-flow` | solution | `headline`, `steps` [{title,desc}]; opt: `kicker` |
| `slide-list-numbered` | solution | `headline`, `items` (strings or {title,desc}) |
| `slide-bento-grid` | data | `tiles` [{label?,title?,body?,accent?,span_2?}]; opt: `grid` |
| `slide-comparison-table` | diagnostic | `rows` [[cells]], `headers`; opt: `headline` |
| `slide-faq-stack` | solution | `faqs` [{q,a?}]; opt: `headline` |
| `slide-quote-cascade` | testimonial | `quotes` [{text,attr?}] |
| `slide-timeline` | solution | `events` [{date?,title?,desc?}] |
| `slide-stat-row` | data | `stats` [{num,unit?,label?,body?}]; opt: `source` |
| `slide-warning-banner` | shock | `headline`, `icon` (default "!") |
| `slide-icon-grid` | solution | `tiles` [{icon?,title?,desc?,solid?}] |
| `slide-progress-bars` | data | `bars` [{label,value,pct?}]; opt: `source` |
| `slide-data-viz-donut` | data | `percent`, `center_label`; opt: `headline`, `legend`, `body` |
| `slide-typeset-poster` | break | `headline`; opt: `eyebrow`, `footer_left`, `footer_right` |
| `slide-myth-vs-fact` | myth/reality | `myth`, `fact`; opt: `kicker`, `myth_label`, `fact_label` |

### 4.2 Extended Layouts — Agency Grade (24 added in v2.5)

| Layout | Beat | Required copy fields |
|--------|------|----------------------|
| `slide-full-bleed-type` | hook/break | `headline`; opt: `eyebrow`, `sub`, `kicker` — fullbleed typographic statement, no padding constraints |
| `slide-diagonal-split` | data/proof | `headline`, `stat_number`; opt: `body`, `kicker` — diagonal clip-path bg splits left content + right stat |
| `slide-asymmetric-lockup` | silence/break | `headline`; opt: `body`, `kicker` — content locked to left 42%, aggressive negative space right |
| `slide-type-over-shape` | hook/break | `headline`; opt: `body`, `sub`, `kicker` — headline renders over layered SVG blob shapes |
| `slide-stacked-type` | break/poster | `lines` [{text,size?,weight?,color?}] — 4-line typographic cascade with size variation |
| `slide-corner-manifesto` | break/silence | `headline`; opt: `body`, `kicker` — content anchored bottom-left, maximum white space above |
| `slide-data-wall` | data/shock | `stats` [{number,unit,label}] — 3-column oversized stat grid, monospace aesthetic |
| `slide-side-by-side` | diagnostic/proof | `left_content` (big number/icon), `headline`, `body`; opt: `kicker` — true 50/50 vertical split |
| `slide-frame-within-frame` | testimonial/break | `quote`; opt: `attribution` — 78%×78% inner border, quote centered inside |
| `slide-terminal-fullscreen` | shock/diagnostic | `headline`; opt: `code_lines` [{text,type}] — always-dark terminal covering full canvas |
| `slide-editorial-column` | solution/proof | `headline`, `body`, `quote`; opt: `attribution` — two-column editorial with ruled divider |
| `slide-badge-grid` | solution | `headline`, `items` [{icon,title,desc}] — spec-sheet layout with SVG icons per row |
| `slide-contrast-knockout` | hook/shock | `headline`, `body`; opt: `kicker` — split bg, headline on dark half, body on accent half |
| `slide-circular-quote` | testimonial/break | `quote`; opt: `attribution` — quote inside circular border, attribution outside |
| `slide-waterfall-list` | solution | `headline`, `items` [{title,desc}] — oversized step numbers (01 02 03) with hanging titles |
| `slide-angled-text` | hook/break | `headline`; opt: `body` — content rotated −15°, creates unexpected reading angle |
| `slide-minimal-card-stack` | solution | `headline`, `cards` [{title,desc}] — left-border staggered cards, maximum legibility |
| `slide-logo-wall` | proof/social | `logos` (strings) — 3-col logo grid at 0.22 opacity, "As seen in" aesthetic |
| `slide-receipt` | data/proof | `headline`, `items` [{label,value}]`; opt: `total` — white paper receipt UI, brutalist data |
| `slide-polaroid-grid` | proof/social | `cards` [{caption,color_gradient?,icon?}] — rotated polaroid cards scattered on canvas |
| `slide-tag-cloud` | hook/data | `words` [{text,size?,x?,y?,opacity?}] — words scattered across canvas with position control |
| `slide-morse-code` | break/hook | `message`; opt: `headline`, `decoded_text` — Jinja2 encodes message as Morse dots/dashes |
| `slide-scroll-code` | shock/diagnostic | `code_lines` (strings), `language`; opt: `headline` — syntax-highlighted code block |
| `slide-massive-number` | data/shock | `stat_number`, `headline`, `body`; opt: `kicker`, `stat_context`, `source` — giant background number at 0.12 opacity with right-anchored content |

### 4.3 Demonstration Layouts — "Show, Don't Tell" (v3)

These layouts **visually demonstrate** the problem rather than describing it in text. Preflight enforces ≥1 per carousel.

| Layout | Beat | Required copy fields |
|--------|------|----------------------|
| `slide-input-output` | diagnostic/shock | `input_text`, `output_text`; opt: `input_label`, `output_label` — side-by-side panels: "what you wrote" vs "what the ATS sees" |
| `slide-waffle-chart` | data/shock | `stat_number`, `filled` (int 0–100); opt: `headline`, `context` — 10×10 grid showing proportion visually |
| `slide-cross-slide-connector` | break/transition | `headline`; opt: `body`, `kicker`, `connector_type` — continuity anchor with wave/arrow/data-flow layer |
| `slide-before-after-stacked` | diagnostic/proof | `headline`, `before_label`, `before_text`, `before_pct`, `after_label`, `after_text`, `after_pct` — stacked panels with VS badge + progress bars. Coexists with column-based `slide-before-after` |

**Mock UI requirement (ship gate):** ≥1 slide must use `slide-terminal`, `slide-terminal-fullscreen`, or `slide-scroll-code`. `slide-terminal` satisfies this automatically.
**Demonstration requirement (ship gate):** ≥1 slide must use a demonstration layout (input-output, waffle-chart, before-after, before-after-stacked, data-viz-donut, progress-bars, myth-vs-fact, comparison-table). Text-only slides are not enough.

---

## 4.5 COMPOSITION PRINCIPLES

Apply these before choosing layouts, not after.

1. **One dominant element per slide.** Pick ONE: big headline, one stat, or one focal image. That element should own 55–65% of the canvas real estate. Everything else is support.

2. **Silence beats create contrast.** Every 3–4 slides needs a beat that strips away most elements — one line of text on negative space. Without silence, all slides feel equally loud and nothing lands.

3. **Vary alignment every 3 slides.** No more than 3 consecutive center-aligned slides. After 3, introduce a left-anchored or edge-anchored layout. Use check #17 in preflight to catch this automatically.

4. **Camera distance rhythm.** Alternate between "close-up" slides (single big type, 1 element) and "wide shot" slides (grid, list, multiple elements with hierarchy). Two close-ups in a row is fine. Three is monotonous.

5. **Anchored over floating.** Text that floats in the center of a large empty canvas reads as an afterthought. Anchor content to a corner, edge, or a defined region. The asymmetric-lockup and corner-manifesto layouts exist for this.

6. **Type size signals importance — use the full range.** If every text element is 28–36px, there's no hierarchy. Use the full 5-tier system: DISPLAY (48–84px), SUB-HEAD (22–32px), BODY (13–15px), LABEL (11px), MONO (13px). Each tier should be visually distinct.

---

## 5. PACING BEATS

Valid `pacing[]` values: `hook` `shock` `proof` `data` `diagnostic` `solution` `hope` `relief` `action` `cta` `silence` `break` `myth` `reality` `testimonial` `urgency`

Common 4-slide arcs:
- `["hook", "silence", "solution", "cta"]` — emotional/pain
- `["hook", "data", "solution", "cta"]` — informational
- `["hook", "diagnostic", "solution", "cta"]` — problem→framework

**`"silence"` beat** auto-suppresses all decoratives on that slide. Use it deliberately — it's the emotional pause that makes the solution land harder.

---

## 6. COPY BUDGETS

| Element | Max chars | Max words | Note |
|---------|-----------|-----------|------|
| `headline` | 55 | 10 | Weight 700+, no filler |
| `body` | 140 | 22 | Weight 300, conversational |
| `kicker` / label | 40 | 6 | Uppercase, tracking 0.2em |
| `cta_keyword` | 18 | 2 | Single DM keyword |
| `tips[].problem` | 60 | 6 | Classified as label by preflight |

### 6.1 CONTAINER CAPACITY (narrow boxes — preflight enforces this)

Word counts here are the **hard maximum** before text wraps to 6+ lines and the box looks cramped. The container_fit check in preflight will FAIL on overruns.

| Container | Class | Max words | Sweet spot |
|-----------|-------|-----------|-----------|
| step-flow description | `.step-desc` | 13 (fail) / 10 (warn) | 6–8 |
| checklist item (no desc) | `.chk-title` | 12 (fail) / 9 (warn) | 5–8 |
| checklist description | `.chk-desc` | 17 (fail) / 13 (warn) | 8–12 |
| tip-block fix text | `.tip-blk-text` | 17 (fail) / 13 (warn) | 8–12 |
| hook body | `.hook-body` | 22 | 14–18 |
| CTA reward | `.cta-reward` | 15 | 8–12 |

If your concept needs more words per box, split into more slides or pick a wider layout.

### 6.2 OPACITY FLOOR (readability)

Body text at low opacity on busy backgrounds becomes invisible. Hard rules:

| Surface | Opacity floor |
|---------|---------------|
| Body text on dark bg | ≥ 0.75 |
| Body text on light bg | ≥ 0.80 |
| Kickers / labels | ≥ 0.85 |
| Reward / footnote text | ≥ 0.70 |

**Never** set readable text below `opacity: 0.70`. Decorative-only elements (watermarks, faint stamps, background script flourishes) may go lower.

---

## 7. SHIP GATE — 22 Checks

All Tier 1 and Tier 2 checks must pass before delivering. Checks marked **[auto]** are enforced by `preflight.py` / `visual_richness_check.py`. Checks marked **[human]** require a deliberate read.

### Tier 1 — Technical (automated)

- [ ] **Silence beat + CTA final [auto]:** pacing array contains `silence` or `diagnostic` AND final slide is `slide-cta` layout
- [ ] **Max 3 layers per slide [auto]:** no single slide exceeds 3 geo layers — hard cap, no averaging
- [ ] **≥2 distinct font families [auto]:** display font ≠ body font. Allows intentional 2-font systems (Swiss brutalist etc.)
- [ ] **≥3 slides with custom_css [auto]:** at minimum the hook, a middle slide, and the CTA have bespoke CSS rules
- [ ] **All slides use different layouts [auto]:** no two slides share the same layout ID
- [ ] **≥1 shared geo layer across all slides [auto]:** visual cohesion — one layer appears on every slide (others can vary)
- [ ] **Anti-Canva [auto]:** zero `border-left: Npx solid` content cards, zero pill badges — `sub-fact-bubble` and named decorative components are exempt
- [ ] **VAR clean [auto]:** zero `VAR_` strings in rendered HTML
- [ ] **CTA complete [auto]:** final slide has question (contains `?` or `¿`) + keyword + concrete reward (checklist / plantilla / guion / diagnóstico / gratis / sin costo / reporte)
- [ ] **File size [auto]:** 35–80 KB ideal (v2 SVG overhead raises ceiling from 55 to 80 KB) · >80 KB = audit for bloat · <35 KB = rebuild
- [ ] **Brand consistency [auto]:** no foreign brand names or wrong brand in stamp/badge
- [ ] **Mock UI [auto, brand-conditional]:** for WorqAI → ≥1 slide uses `slide-terminal` or simulated interface; for other brands → ≥1 slide has a visual proof element (stat, testimonial, or interface)
- [ ] **Blob overuse [auto]:** no single `svg-blob-*` or `glow-orb` appears >2×; total soft circles ≤ slides × 1.2
- [ ] **Badge collision [auto]:** `chrome-badge-stamp` never overlaps headline or right-aligned text
- [ ] **Shape diversity [auto]:** no single shape (blob, orb, starburst, corner-frame) appears on >4 slides
- [ ] **Demonstration layout [auto]:** ≥1 slide uses input-output, waffle-chart, before-after, data-viz-donut, progress-bars, myth-vs-fact, or comparison-table

### Tier 2 — Creative (human review)

- [ ] **Language purity [human]:** zero English words in Spanish carousels — common leaks: "FREE", "follow-up", "template" (use "plantilla"), "HR" (use "RRHH"), "run" (as noun), "script" (use "guion")
- [ ] **2-second comprehension [human]:** read the hook headline cold — does a stranger know what this is about in 2 seconds? No pronoun-without-antecedent, no riddles, no references to previous slides
- [ ] **Brand-positioning match [human]:** terminal/diagnostic slides only for tech/SaaS/medical brands — never for food, fitness, anti-tech, or lifestyle brands (see §3.5 layout-brand-fit matrix)
- [ ] **Opacity floor [human]:** body text ≥ 0.75 opacity, labels/kickers ≥ 0.85, reward text ≥ 0.75 — scan `custom_css` for values below floor
- [ ] **Reward specificity [human]:** CTA reward must name a concrete deliverable — not "te ayudamos", "contáctanos", or "sabemos cómo"
- [ ] **Zero template artifacts [human]:** scan for "ats-scanner.sh" tab title, double-dollar `$$` in terminal, wrong brand name in stamps

**v2 soft signal (not a hard fail):** Aim for ≥3 v2 primitive types per carousel — SVG icons, SVG blob, SVG starburst, text treatment, drop shadow. `visual_richness_check.py` flags zero-v2 carousels with a WARN. Old carousels grandfathered.

---

## 8. ANTI-SLOP

**Never (EN):** unlock, unleash, elevate, leverage, game-changer, dive into, empower, transform, revolutionize, supercharge, seamless, robust, holistic

**Never (ES):** "¿Sabías que...?", "En el mundo de hoy...", "libera tu potencial", "transforma tu carrera", "desbloquea", "potencia tu", "hoy en día", "ya no funciona", "en tiempo récord", "es bien sabido que", "ningún reclutador", "normalmente pasa", "suele ocurrir"

**Instead:** specific numbers · concrete before/after · direct language ("Esto hace X", not "Esto te permite empoderar") · real examples from the industry

---

## 8.5 VISUAL ANTI-PATTERNS

These patterns produce AI-generic output that fails the blur test. Every item here is banned by default.

1. **Parallel bullets with identical weight.** All list items the same font size, weight, and color = no hierarchy. At minimum, vary size between the item title and its description.

2. **Center-aligned monotone.** 4+ consecutive slides with `text-align: center` and no layout variation. Preflight check #17 catches this. Break it with a left-aligned or edge-anchored layout.

3. **Text treatment on every slide.** `gradient`, `glow`, or `stroke` applied to every slide's headline makes each individual treatment meaningless. Cap at 50% of slides; let the others breathe.

4. **Same decorative every slide.** The DECORATIVE_ROTATION system in the renderer prevents this when `decoratives` is omitted. If you specify decoratives manually, rotate through different types — don't repeat the same starburst or stamp on every slide.

5. **Full-bleed type without breathing room.** `slide-full-bleed-type` with 0 padding means characters at the edge clip under the slide's `overflow: hidden`. Always verify the longest line fits at `font-size / char_count` — use the formula in `carousel-layout-checks.md`.

6. **Uniform card height in grids.** A 4-card grid where all cards are exactly the same height at the same weight looks like a spreadsheet. Vary one card's padding, or use `span_2` to create one dominant card.

7. **Body copy that restates the headline.** "CVs con errores no pasan el ATS." → body: "Cuando tu CV tiene errores, no pasa el filtro ATS." = filler. Body should add a new detail or example, never restate.

8. **Stacking geo layers + ornaments + text treatment + blobs.** Each layer adds a few percent of visual noise. At 3 geo layers + 2 ornaments + gradient text + blob, the slide becomes a visual landfill. The decorative budget (max 2) exists for a reason. Pick the one strongest element and let everything else support it.

---

## 9. JSON SPEC TEMPLATE

```json
{
  "meta": {
    "system": "sXX",
    "aspect": "1:1",
    "slides": 4,
    "brand": "@worqai",
    "language": "es-CR",
    "topic": "your-topic",
    "density": "standard",
    "continuity": ""
  },
  "pacing": ["hook", "silence", "solution", "cta"],
  "slides": [
    {
      "id": "s1",
      "layout": "slide-hook-lockup",
      "layers": [
        "glow-orb",
        { "id": "svg-blob-tr", "animate": true }
      ],
      "decoratives": [{ "id": "svg-starburst-burst", "position": "bl" }],
      "copy": {
        "kicker": "KICKER LABEL",
        "headline": "Hook headline eight words max.",
        "body": "Supporting sentence, 18 words max, conversational.",
        "text_treatment": "stroke",
        "swipe_prompt": "Desliza →"
      },
      "custom_css": ".s1-display { font-size: clamp(36px,7cqw,54px); font-weight: 900; letter-spacing: -0.03em; }"
    },
    {
      "id": "s2",
      "layout": "slide-terminal",
      "layers": ["zoom-rings", "glow-orb"],
      "copy": {
        "kicker": "KICKER",
        "headline": "What the system reveals",
        "command": "diagnose --candidate cv.pdf",
        "output_lines": [
          { "type": "warn", "text": "Warning detail here" },
          { "type": "err",  "text": "ERROR: specific result" },
          { "type": "info", "text": "Context. No drama." }
        ]
      },
      "custom_css": ".s2-headline { font-size: clamp(24px,5cqw,34px); font-weight: 800; letter-spacing: -0.02em; }"
    },
    {
      "id": "s3",
      "layout": "slide-step-flow",
      "layers": ["glow-orb", "vol-light"],
      "decoratives": ["ornament-tr"],
      "copy": {
        "kicker": "EL FRAMEWORK",
        "headline": "Three moves. In order.",
        "steps": [
          { "title": "Step one", "desc": "Specific action. Why it matters." },
          { "title": "Step two", "desc": "Next concrete action." },
          { "title": "Step three", "desc": "Final step, direct." }
        ]
      },
      "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,34px); font-weight: 900; text-transform: uppercase; letter-spacing: -0.03em; }"
    },
    {
      "id": "s4",
      "layout": "slide-cta",
      "layers": ["glow-orb"],
      "decoratives": [{ "id": "sub-stamp-circle", "text": "GRATIS" }],
      "copy": {
        "question": "¿Your specific question here?",
        "cta_keyword": "KEYWORD",
        "reward": "Te mando el [recurso específico]. Gratis."
      },
      "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.0; }"
    }
  ]
}
```

**Save spec to:** `production/{topic}-spec.json`
**Output goes to:** `production/carousel_{topic}_{system}.html` (auto-named)

---

## 10. BUILD COMMAND

```bash
# Single carousel
py scripts/build_carousel.py production/your-spec.json

# Batch (runs cross-carousel diversity check automatically)
py scripts/build_carousel.py production/spec1.json production/spec2.json
```

Chains: render_carousel.py → preflight.py → visual_richness_check.py
Exit 0 = all pass, ready to export. Exit 1 = review errors above.

**Export after passing:**
```bash
py scripts/carousel_exporter.py --input production/carousel_topic_sXX.html --output export/
```

---

## QUICK CHECKLIST BEFORE WRITING SPEC

- [ ] System picked (different family from any other carousel in this session)
- [ ] 4 slides with different layouts — no two slides share the same structure
- [ ] Mock UI present (`slide-terminal` OR a non-terminal mock — see brand fit matrix §3.5)
- [ ] One silence beat
- [ ] CTA slide has question + keyword + reward
- [ ] custom_css uses `.sN-` prefix on every slide
- [ ] Language matches target audience (es-CR for CR, es-LATAM for regional)
- [ ] All Spanish carousel copy is fully Spanish — no `"FREE"`, no `"follow-up"`, no `"run"` (use `"GRATIS"`, `"seguimiento"`, `"corrida"`)
- [ ] step-flow descriptions ≤ 10 words, checklist items ≤ 9 words (see §6.1)
- [ ] No readable text below `opacity: 0.70` (see §6.2)
- [ ] If using `slide-terminal`, brand is genuinely tech/medical/diagnostic (see §3.5 — never for fitness/food/lifestyle)
- [ ] Terminal `tab_title` matches the brand (e.g. `velar-diagnose`, not the default)
