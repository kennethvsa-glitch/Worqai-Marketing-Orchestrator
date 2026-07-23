# Visual Primitives v2 — Implementation Spec

> **Status:** Draft for Kenneth review. No code written yet.
> **Author:** Claude, synthesizing Kimi v2 audit + html2canvas research + current system state.
> **Date:** 2026-05-17
> **Estimated effort:** ~6 hours for Tier A. Tier B and C scoped here but not in this sprint.
> **Linked feedback:** [ideation/kimis'feedback v2.md](../ideation/kimis%27feedback%20v2.md)

---

## 0. Decision Locks (approved 2026-05-17)

| Decision | Locked Value |
|---|---|
| Export pipeline policy | **Playwright (`carousel_exporter.py`) is canonical.** In-HTML html2canvas button = quick-preview convenience. New primitives must work in html2canvas as a baseline; Playwright-only effects are allowed but must be tagged. |
| Tier A scope | **All 8 items, one pass.** Includes Kimi's two adds: SVG noise/grain texture + SVG drop shadow. |
| Backward compatibility | **Leave existing carousels alone.** New primitives are opt-in via new spec fields. No re-renders forced. Old `blob-bg` and `ornament` keep working — preflight emits soft warnings only. |
| Build approach | **Spec doc first** (this file). Review → approve → implement code + docs + skills + memory in one pass. |

---

## 1. The Core Architectural Insight

Per Kimi v2 research against the html2canvas official supported-features list:

**These CSS properties are BROKEN in html2canvas (the in-HTML ZIP button):**
- `background-clip: text` → can't do CSS gradient text
- `box-shadow` → no shadow on cards
- `filter: blur()` → no blur effects
- `backdrop-filter` → no glassmorphism
- `mix-blend-mode` → no blend mode mesh gradients
- `clip-path` on images → no photo masking

**These WORK in html2canvas:**
- `text-shadow` (multi-layer, any color)
- `-webkit-text-stroke` (outlined text)
- All gradients (`linear`, `radial`, `conic`)
- `transform` (2D fully, 3D partial)
- **Inline SVG (`<svg>` elements)** ← the escape hatch
- **SVG as background-image data URL**
- **SVG filters** (`feGaussianBlur`, `feDropShadow`, `feTurbulence`, `feColorMatrix`)

**Strategy:** Build effects in SVG instead of CSS wherever the CSS version is broken. SVG works in both pipelines (html2canvas captures it correctly, Chromium/Playwright renders it natively). One implementation, two pipelines, zero divergence.

Effects that genuinely require Chromium-only features (real `backdrop-filter`, real `mix-blend-mode`) get tagged `requires_playwright_export: true` in the spec and force-route through `carousel_exporter.py`. These are Tier B/C, not Tier A.

---

## 2. Tier A — 8 Primitives (~6 hours)

All 8 are html2canvas-safe by virtue of using either supported CSS or inline SVG. Listed in build order (cheapest first, so we get visible wins early):

### A1. `-webkit-text-stroke` text treatment — 10 min
Native CSS, html2canvas-safe. Outlined display text (Supreme / Nike aesthetic).

```css
.txt-stroke {
  -webkit-text-stroke: 2px var(--accent);
  color: transparent;
}
.txt-stroke-filled {
  -webkit-text-stroke: 1px var(--accent);
  color: var(--text-primary);
}
```

**Spec usage:** `"text_treatment": "stroke"` on a headline → renders with `class="txt-stroke"`.
**Best for:** s07 BRUTALIST, s25 SWISS BRUT, s31 NEOBRUT, s32 MAXIMALIST poster moments.

### A2. `text-shadow` neon-glow treatment — 15 min
Native CSS, html2canvas-safe. **Text only** — `box-shadow` is broken, so no box glows in this pass.

```css
.txt-glow-subtle {
  text-shadow: 0 0 8px var(--accent), 0 0 24px rgba(0,0,0,0.4);
}
.txt-glow-medium {
  text-shadow: 0 0 10px var(--accent), 0 0 32px var(--accent), 0 0 64px rgba(0,0,0,0.6);
}
.txt-glow-bold {
  text-shadow: 0 0 10px var(--accent), 0 0 24px var(--accent),
               0 0 48px var(--accent), 0 0 96px var(--accent);
}
```

**Spec usage:** `"text_treatment": "glow"` (defaults to medium) or `"text_treatment": "glow-bold"`.
**Best for:** Big-number stats, CTA keywords, terminal headlines, cyberpunk/neon systems.

### A3. SVG gradient-text — 30 min
Replaces broken CSS `background-clip: text`. Renders headlines as inline SVG `<text>` with `<linearGradient>` fill.

**Render pattern:**
```html
<svg class="txt-gradient" viewBox="0 0 800 120" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="g-{slide_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="var(--accent)"/>
      <stop offset="100%" stop-color="#fff"/>
    </linearGradient>
  </defs>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        fill="url(#g-{slide_id})" font-family="var(--font-display)" font-weight="900"
        font-size="96">
    {HEADLINE TEXT}
  </text>
</svg>
```

**Spec usage:** `"text_treatment": "gradient"` on a headline field. Renderer wraps the text in SVG instead of plain `<h2>`/`<h1>`.
**Caveat:** SVG `<text>` doesn't auto-wrap. For 2-line headlines we split into two `<text>` elements at render time. For 3+ lines, fall back to native HTML + neon-glow (warn in preflight).
**Best for:** Display headlines (≤14 chars per line), stat numbers, poster moments.

### A4. SVG starburst — replaces `✦ ✧ ✦` ornament — 30 min
Three variants: `spark` (4-point), `burst` (8-point), `mark` (16-point fine).

**`svg-starburst-spark`:**
```html
<svg class="deco-starburst deco-starburst-tr" viewBox="0 0 100 100">
  <g transform="translate(50,50)">
    <polygon points="0,-32 6,-10 28,-6 11,6 17,28 0,16 -17,28 -11,6 -28,-6 -6,-10"
             fill="var(--accent)" opacity="0.85"/>
  </g>
</svg>
```

**`svg-starburst-burst`** (8-point, double-layer):
```html
<svg class="deco-starburst deco-starburst-tr" viewBox="0 0 100 100">
  <g transform="translate(50,50)">
    <polygon points="0,-40 8,-12 36,-8 14,8 22,36 0,20 -22,36 -14,8 -36,-8 -8,-12"
             fill="var(--accent)" opacity="0.6"/>
    <polygon points="0,-25 5,-8 22,-5 9,5 14,22 0,12 -14,22 -9,5 -22,-5 -5,-8"
             fill="var(--accent)" opacity="0.9" transform="rotate(22.5)"/>
  </g>
</svg>
```

**`svg-starburst-mark`** (16-point fine, decorative):
```html
<svg class="deco-starburst deco-starburst-tr" viewBox="0 0 100 100">
  <g transform="translate(50,50)" fill="var(--accent)" opacity="0.7">
    <!-- 16 radiating thin triangles -->
    {16 polygon rotations}
  </g>
</svg>
```

**Spec usage:** `"decoratives": ["svg-starburst-burst"]` or with position: `[{"id":"svg-starburst-spark","position":"bl"}]`.
**Positions:** `tr`, `tl`, `br`, `bl` (default `tr`).
**Old `ornament*` IDs:** Keep working (no deprecation). Preflight emits soft warning suggesting SVG variant.

### A5. SVG organic blobs — 5 variants — 1 hour
Replaces `blob-bg` (which is an ellipse with `filter: blur` — and `filter: blur` is BROKEN in html2canvas, so the current blob has rendered as just a soft ellipse with halo in many exports).

Five variants, all as `background-image: url("data:image/svg+xml,...")`:

| Layer ID | Position | Description |
|---|---|---|
| `svg-blob-tr` | top-right corner | Asymmetric 6-point bezier, 55% canvas width |
| `svg-blob-bl` | bottom-left corner | Mirror of `tr`, different curve |
| `svg-blob-center` | centered behind hero | 8-point bezier, low opacity |
| `svg-blob-asymmetric` | top-right, organic-asymmetric | More aggressive 7-point curve |
| `svg-blob-scattered` | three small blobs, dispersed | Atmosphere layer |

**Sample (`svg-blob-tr`):**
```css
.svg-blob-tr {
  position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 500'%3E%3Cpath d='M440.5,320.5Q418,391,355.5,442.5Q293,494,226,450.5Q159,407,99,354Q39,301,24.5,222Q10,143,78,93Q146,43,226,34.5Q306,26,362.5,84Q419,142,441,221.5Q463,301,440.5,320.5Z' fill='%23C7FF3A' opacity='0.18'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: top right;
  background-size: 55%;
}
```

**Color binding:** Blobs use `var(--accent)` via SVG `fill` — but data URLs can't reference CSS vars directly. Solution: renderer substitutes `{ACCENT_HEX}` token in the SVG data URL with the system's accent hex at render time. Documented in §5.

**Optional animation** (Kimi v2 add):
```css
.svg-blob-tr.blob-drift {
  animation: blob-drift 60s linear infinite;
}
@keyframes blob-drift {
  0%   { transform: rotate(0deg) scale(1); }
  50%  { transform: rotate(180deg) scale(1.05); }
  100% { transform: rotate(360deg) scale(1); }
}
```
**Spec usage:** `"layers": ["svg-blob-tr"]` or `"layers": [{"id":"svg-blob-tr","animate":true}]`. html2canvas captures whatever frame the animation is on when the screenshot fires — acceptable, still beats an ellipse. Playwright captures the frame deterministically (we pause animations before screenshot — already in `carousel_exporter.py`, verify).
**Old `blob-bg`:** Keep working. Preflight warns: "blob-bg is an ellipse. Try svg-blob-tr for organic shape."

### A6. SVG icon library — 20 core icons — 2 hours
Single sprite block injected once into [templates/carousel-shell.html](../templates/carousel-shell.html), referenced via `<use href="#icon-warning"/>`.

**Sprite structure (added to shell, ~3KB total):**
```html
<svg style="position:absolute;width:0;height:0" aria-hidden="true">
  <defs>
    <symbol id="icon-warning" viewBox="0 0 24 24">
      <path d="M12 2L1 21h22L12 2zm0 6l7 12H5l7-12zm-1 4v3h2v-3h-2zm0 4v2h2v-2h-2z" fill="currentColor"/>
    </symbol>
    <symbol id="icon-error" viewBox="0 0 24 24">{...X path...}</symbol>
    <!-- ... 18 more ... -->
  </defs>
</svg>
```

**The 20 icons:**

| Group | Icons |
|---|---|
| **Status (terminal output)** | `warning`, `error`, `ok` (checkmark), `info`, `clock` |
| **Action arrows** | `arrow-right`, `arrow-down`, `arrow-curved`, `arrow-thick` |
| **Data** | `chart`, `trending-up`, `trending-down`, `target` |
| **Security / trust** | `lock`, `key`, `shield` |
| **Affinity / accent** | `heart`, `lightning`, `trophy`, `star`, `magnifier` |

(That's 21 — I'll drop `magnifier` or `trophy` to keep it 20, or just ship 21. Cheap.)

**Usage in templates:**
```html
<!-- Before (slide-warning-banner.html) -->
<div class="warn-icon">!</div>

<!-- After -->
<svg class="warn-icon" aria-hidden="true"><use href="#icon-warning"/></svg>
```

**CSS sizing:**
```css
.warn-icon { width: 64px; height: 64px; color: var(--accent); }
```
`currentColor` in SVG paths inherits from CSS `color`, so icons auto-tint to system accent.

**Spec usage:** Mostly automatic — templates use icons internally. Optionally exposed for `slide-icon-grid` where users pick icons per tile:
```json
{"tiles": [{"icon": "shield", "title": "ATS-safe"}, ...]}
```

### A7. SVG noise/grain texture (Kimi v2 add) — 20 min
Current grain: 0.035 opacity feTurbulence — barely visible. Upgrade to a real print-feel grain with higher contrast and tunable opacity per system.

**New CSS (replaces current `.slide::before` in shell):**
```css
.slide::before {
  content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 4;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.7 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: var(--grain-opacity, 0.08);
  mix-blend-mode: overlay;  /* Playwright-only — falls back gracefully without */
}
```

**Per-system opacity tuning** (added to `component_data.json` tokens):
| System type | `--grain-opacity` |
|---|---|
| brutalist, light (riso) | 0.12 |
| dark default | 0.08 |
| cyberpunk, neon | 0.05 (don't fight the glow) |

**Note on `mix-blend-mode`:** Broken in html2canvas. Without it, grain renders as a flat overlay (still better than current). With Playwright, grain blends like ink on paper. Acceptable degradation.
**Spec usage:** None. Applies automatically to every slide via shell.

### A8. SVG drop-shadow filter (Kimi v2 add) — 30 min
Since `box-shadow` is broken in html2canvas, cards/stamps currently render flat in exported PNGs. SVG `feDropShadow` survives.

**Approach:** Define as a reusable SVG filter, applied via CSS `filter: url(#shadow-md)` to any element class.

**Sprite addition (to shell, alongside icon sprite):**
```html
<svg style="position:absolute;width:0;height:0" aria-hidden="true">
  <defs>
    <filter id="shadow-sm" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity="0.18"/>
    </filter>
    <filter id="shadow-md" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000" flood-opacity="0.28"/>
    </filter>
    <filter id="shadow-lg" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000" flood-opacity="0.35"/>
    </filter>
  </defs>
</svg>
```

**CSS primitive classes:**
```css
.shadow-sm { filter: url(#shadow-sm); }
.shadow-md { filter: url(#shadow-md); }
.shadow-lg { filter: url(#shadow-lg); }
```

**Templates that benefit (auto-apply in this pass):**
- `chrome-badge-stamp` → `shadow-md`
- `sub-bento-card`, `sub-stat-card` → `shadow-sm`
- `slide-tip-blocks` `.tip-blk` cards → `shadow-sm`
- `slide-checklist` `.chk-row` → none (would compete with list rhythm)
- `slide-warning-banner` `.warn-icon` container → `shadow-md`

**Spec usage:** None for auto-apply targets. Optional override per slide via `custom_css` if a designer wants more/less.

---

## 3. Tier B — Deferred (~6 hours, separate sprint)

Specced briefly so we don't lose them. NOT in this build.

| # | Primitive | What it adds | Notes |
|---|---|---|---|
| B1 | SVG divider lines (wavy, fading-dots, double, gradient) | Section rhythm | 4 variants, ~30 min |
| B2 | SVG badge shapes (shield, hexagon, ribbon, 8-point starburst) | Badge variety | Extends `chrome-badge-stamp`. Add `shape` field. ~45 min |
| B3 | SVG mesh-gradient approximation | Color depth | Overlapping radial gradients in inline SVG. ~45 min |
| B4 | Real glassmorphism primitive (`.glass-panel`) | Premium card surface | Tagged `requires_playwright_export: true`. ~30 min CSS + render flag. |
| B5 | `tilt-3d` opt-in transform | Spatial depth on cards | Only on `.stat-card`, `.tip-blk`, `.bento-tile`. Opt-in via spec. ~30 min |
| B6 | `text_treatment: gradient-stroke` (combined) | Gradient fill + stroke outline | 2026 Adobe trend. ~20 min |

---

## 4. Tier C — Architectural (out of scope, separate planning)

| # | Item | Why not now |
|---|---|---|
| C1 | Photo pipeline + `slide-photo-mask` layout | Image asset management, clip-paths, masking, brand-image library. Needs separate design pass. |
| C2 | Real `mix-blend-mode` mesh gradient | Playwright-only, complex token system, needs B3 first |
| C3 | SVG vector illustrations (key, lock, magnifier, graph) | 10+ custom illustrations, ~6 hrs design work |
| C4 | Frame-by-frame export of animated blobs | Multi-frame ZIP for Reels — needs exporter rework |

---

## 5. Spec Schema Changes

All additions are backward-compatible (optional fields). No required field additions.

### 5.1 Slide-level `copy` additions
```jsonc
"copy": {
  "headline": "...",
  "text_treatment": "gradient" | "glow" | "glow-bold" | "glow-subtle" | "stroke" | "stroke-filled",
  //                ^^^ NEW. Applies to the primary display element (headline or stat_number).
  //                    If omitted, renders as plain text (current behavior).
}
```

### 5.2 Slide-level `layers` extension
`layers` is already an array of strings or objects. The new SVG layer IDs join the existing list:

```jsonc
"layers": ["svg-blob-tr"]
// or with animation:
"layers": [{"id": "svg-blob-tr", "animate": true}]
```

**New layer IDs registered:**
`svg-blob-tr`, `svg-blob-bl`, `svg-blob-center`, `svg-blob-asymmetric`, `svg-blob-scattered`

### 5.3 Slide-level `decoratives` extension
**New decorative IDs:**
`svg-starburst-spark`, `svg-starburst-burst`, `svg-starburst-mark`

Optionally with position:
```jsonc
"decoratives": [{"id": "svg-starburst-burst", "position": "tl"}]
```

### 5.4 Slide-level `effects` (NEW field)
For drop-shadow opt-out and future Tier B opt-ins:
```jsonc
"effects": {
  "shadow": "sm" | "md" | "lg" | "none",  // default: auto-applies to badge/cards
  "grain_opacity": 0.08,                    // override per-slide if needed
  "requires_playwright_export": false       // set true when using B4+ Playwright-only primitives
}
```

### 5.5 Schema file diff
File: [scripts/carousel-spec.schema.json](../scripts/carousel-spec.schema.json)

Add to `properties.slides.items.properties`:
```jsonc
"effects": {
  "type": "object",
  "properties": {
    "shadow": { "type": "string", "enum": ["sm","md","lg","none"] },
    "grain_opacity": { "type": "number", "minimum": 0, "maximum": 0.3 },
    "requires_playwright_export": { "type": "boolean", "default": false }
  }
}
```

Add to `properties.slides.items.properties.copy.properties`:
```jsonc
"text_treatment": {
  "type": "string",
  "enum": ["gradient","glow","glow-bold","glow-subtle","stroke","stroke-filled"]
}
```

---

## 6. File-by-File Change Manifest

### 6.1 Templates
| File | Change | Effort |
|---|---|---|
| [templates/carousel-shell.html](../templates/carousel-shell.html) | Inject `<svg defs>` sprite block at top (icons + shadow filters). Update `.slide::before` grain to new feTurbulence + colormatrix. Add `.txt-stroke*`, `.txt-glow*`, `.shadow-*`, `.svg-blob-*` CSS classes. | 1hr |
| [templates/slides/slide-terminal.html](../templates/slides/slide-terminal.html) | Swap `!`/`✓`/`✗`/`i` text symbols for `<svg><use href="#icon-..."/></svg>` references | 15min |
| [templates/slides/slide-warning-banner.html](../templates/slides/slide-warning-banner.html) | Swap `!` for `<use href="#icon-warning"/>`. Apply `.shadow-md` to icon container. | 10min |
| [templates/slides/slide-checklist.html](../templates/slides/slide-checklist.html) | Swap `✓`/`✗` markers for SVG icons | 10min |
| [templates/slides/slide-icon-grid.html](../templates/slides/slide-icon-grid.html) | Replace any placeholder text/emoji with `<use href="#icon-{slot.icon}"/>` driven by `tile.icon` field | 20min |
| [templates/slides/slide-big-number.html](../templates/slides/slide-big-number.html) | Detect `text_treatment` on stat_number, render via SVG gradient-text template fragment when set to `gradient`. Apply `.txt-glow-bold` when set to `glow`. | 20min |
| [templates/slides/slide-typeset-poster.html](../templates/slides/slide-typeset-poster.html) | Same headline `text_treatment` handling. Default to `stroke` for brutalist systems. | 15min |
| [templates/slides/slide-hook-lockup.html](../templates/slides/slide-hook-lockup.html) | Headline `text_treatment` support | 10min |

### 6.2 Python scripts
| File | Change | Effort |
|---|---|---|
| [scripts/render_carousel.py](../scripts/render_carousel.py) | • Add SVG blob layer IDs (`svg-blob-tr` etc.) to `LAYER_HTML` dict, with `{ACCENT_HEX}` substitution<br>• Add `svg-starburst-*` to `DECORATIVE_HTML`<br>• Add `text_treatment` handling — pre-render SVG gradient-text wrapper when set<br>• Substitute hex accent into SVG data URLs at render time | 1.5hr |
| [scripts/carousel-spec.schema.json](../scripts/carousel-spec.schema.json) | Add `text_treatment` enum, `effects` object (see §5.5) | 10min |
| [scripts/preflight.py](../scripts/preflight.py) | • Soft-warn on `blob-bg` use<br>• Soft-warn on `ornament*` use (raw `✦` Unicode in copy = error)<br>• Soft-warn when terminal `output_lines` contain raw `!`/`✓`/`✗` (suggest SVG-via-template)<br>• Validate `text_treatment` enum | 30min |
| [scripts/visual_richness_check.py](../scripts/visual_richness_check.py) | • Reward use of SVG primitives (each `svg-*` layer/decorative = +1 richness point)<br>• Penalize zero-SVG carousels below richness threshold | 20min |
| [scripts/component_registry.json](../scripts/component_registry.json), [scripts/component_data.json](../scripts/component_data.json) | Register new components (blobs, starbursts, icons). Add per-system `--grain-opacity` overrides. | 30min |
| [scripts/build_gallery.py](../scripts/build_gallery.py) | Pick up new component pages automatically (verify) | 5min |

### 6.3 Gallery additions
New files in `gallery/`:
| # | File | Shows |
|---|---|---|
| 51 | `51-svg-blob-organic.html` | All 5 blob variants on one page |
| 52 | `52-svg-starburst.html` | spark / burst / mark variants in 4 positions |
| 53 | `53-svg-icon-library.html` | All 20 icons in a grid, with hex codes |
| 54 | `54-text-gradient.html` | SVG gradient text on different system accents |
| 55 | `55-text-glow.html` | All 3 glow intensities |
| 56 | `56-text-stroke.html` | stroke + stroke-filled variants |
| 57 | `57-svg-grain-texture.html` | Before/after grain comparison |
| 58 | `58-svg-drop-shadow.html` | sm/md/lg shadow comparison |

Then regenerate `gallery/INDEX.html` via `build_gallery.py`.

### 6.4 Skill / docs / rules updates (THIS pass)
| File | Change |
|---|---|
| [.claude/skills/html-carousel-builder/carousel-master-ref.md](../.claude/skills/html-carousel-builder/carousel-master-ref.md) | • New §3.5 Text Treatments<br>• New §3.6 SVG Primitives (blobs, starbursts, icons, dividers, shadows)<br>• Update §3 Decoratives table (mark `ornament*` as deprecated, add `svg-starburst-*`)<br>• Update §2 Geo Layers (add `svg-blob-*`, mark `blob-bg` deprecated)<br>• Update §7 Ship Gate: add "≥1 SVG primitive used per carousel"<br>• Update §9 JSON spec template with `text_treatment` example |
| [.claude/skills/html-carousel-builder/SKILL.md](../.claude/skills/html-carousel-builder/SKILL.md) | One paragraph: "v2 primitives — SVG gradient text, neon-glow, stroke, organic blobs, starbursts, icon library, drop shadows, real grain." |
| [.claude/rules/carousel-layout-checks.md](../.claude/rules/carousel-layout-checks.md) | New rule: "Text symbols in containers (`!`, `→`, `✓`, `✗`, `i`) must use SVG icons. Gradient text must be SVG-based, never CSS `background-clip: text`." |
| [.claude/rules/anti-slop.md](../.claude/rules/anti-slop.md) | Visual slop list addition: "No `✦✧✦` Unicode ornaments. No `blob-bg` ellipse. No CSS gradient text (it breaks in export)." |
| [CLAUDE.md](../CLAUDE.md) | One-line update under "Carousel Build Reference": mention v2 primitives. |
| [AGENTS_BREAKDOWN.md](../AGENTS_BREAKDOWN.md) | Update Ads / Content agent capability lines |

### 6.5 Memory updates (THIS pass)
| File | Change |
|---|---|
| `memory/project_carousel_render_engine.md` | Add: "v2 primitives shipped 2026-05-17 — SVG blobs, starbursts, icons, gradient-text, neon-glow, stroke, grain, drop-shadow. Spec adds `text_treatment` and `effects` fields. Playwright is canonical export." |
| `memory/feedback_carousel_hierarchy_and_composition.md` | Append: "After v2 primitives — every carousel should use ≥1 SVG primitive (icon, blob, starburst, or text treatment). Zero-SVG carousels fail visual_richness_check." |
| NEW: `memory/project_pipeline_policy.md` | "Playwright (`carousel_exporter.py`) is canonical export. In-HTML html2canvas button = quick preview only. Designs may use modern CSS; SVG fallbacks required when html2canvas-broken (background-clip:text, box-shadow, backdrop-filter, mix-blend-mode, clip-path). Why: Kimi v2 audit forced explicit pipeline decision." |
| NEW: `memory/reference_html2canvas_limits.md` | "html2canvas broken: background-clip:text, box-shadow, filter:blur, backdrop-filter, mix-blend-mode, clip-path on images, animation. Works: text-shadow, -webkit-text-stroke, all gradients, transform 2D, inline SVG, SVG data URLs, SVG filters (feGaussianBlur, feDropShadow, feTurbulence). Reference for any future visual primitive decision." |

---

## 7. Migration Plan

Per Decision Lock #3 — **leave existing carousels alone**.

| Surface | Behavior |
|---|---|
| Old `blob-bg` layer | Still renders. Preflight: soft warning "blob-bg renders as ellipse; svg-blob-tr is the v2 organic shape." |
| Old `ornament*` decoratives | Still render with `✦ ✧ ✦`. Preflight: soft warning "v2 svg-starburst-* available." |
| Old `custom_css` with CSS gradient text (`background-clip: text`) | Still renders in preview. Preflight: WARNING "background-clip:text breaks in html2canvas export — use text_treatment: gradient instead." |
| Old templates without SVG icons | No change. Existing carousels look identical. |
| New ship gate "≥1 SVG primitive" | Applies only to NEW carousels (timestamp check). Old specs grandfathered. |

No spec migration script needed. No re-renders. No file moves.

---

## 8. Validation / Testing Plan

Before declaring Tier A done:

1. **Render a v2 demo carousel** using all 8 primitives at once — `production/v2-primitive-demo-spec.json`. System: s17 (WORQAI VERDE). 5 slides, one primitive showcased per slide + one combo slide.
2. **Export through BOTH pipelines:**
   - In-HTML ZIP button → save 5 PNGs
   - `carousel_exporter.py` → save 5 PNGs
3. **Side-by-side comparison.** Identical look = success. Different = document the degradation and decide if acceptable.
4. **Render one existing carousel** ([production/carousel_velar-sleep_s01.html](../production/carousel_velar-sleep_s01.html) or similar) without modification. Must look identical to before. Backward-compat verified.
5. **Run `preflight.py` on 3 old specs** — must pass (only soft warnings, no errors).
6. **Run `visual_richness_check.py` on the v2 demo** — must score >= previous baseline + delta from new primitives.
7. **Gallery review** — all 8 new gallery pages render correctly. INDEX.html updated.

---

## 9. Open Questions for Kenneth

Before I implement, confirm:

**Q1 — Animation default.** Should `svg-blob-*` animate by default, or strictly opt-in?
- Pro animate-default: every carousel has subtle energy in live preview
- Pro opt-in: predictable behavior; html2canvas screenshot lottery avoided
- **My rec:** opt-in only. Add `"animate": true` per layer use. Reasoning: predictable exports beat surprise energy.

**Q2 — Icon library count.** 20 icons or 21 (keep `magnifier` AND `trophy`)?
- 20 is round; 21 adds magnifier+trophy both. Cost difference: zero.
- **My rec:** ship 21. Round numbers don't matter — usefulness does.

**Q3 — Brand-system primitive defaults.** Should certain systems auto-apply text treatments?
- e.g., s07 BRUTALIST + s25 SWISS BRUT auto-apply `text_treatment: stroke` to headlines
- e.g., s06 AURORA, s08 GLASSMORPHISM, s16 NEON GRID auto-apply `text_treatment: gradient`
- **My rec:** YES for brutalist/neon families. Lets spec stay minimal. Document defaults in master-ref §1.

**Q4 — Sprite injection: every carousel or only when used?**
- Always-inject adds ~3KB to every carousel HTML (negligible) but icons are always available
- On-demand inject keeps file size leaner but renderer needs to scan templates first
- **My rec:** always-inject. 3KB is nothing; complexity savings real.

**Q5 — Ship-gate enforcement.** Should "≥1 SVG primitive per carousel" be a hard preflight FAIL or a visual_richness_check signal?
- Hard fail: enforces discipline; might block legit minimalist carousels (single typeset poster)
- Soft signal: easier to overrule
- **My rec:** soft signal in visual_richness_check. Don't fail builds for design preference.

---

## 10. Estimated Total Effort

| Phase | Hours |
|---|---|
| Tier A primitives (8 items) | 4.5 |
| Renderer + schema + preflight updates | 2.5 |
| Templates touched (8 files) | 1.5 |
| Gallery (8 new pages + INDEX rebuild) | 1.5 |
| Skill / rules / docs / memory updates | 1.5 |
| Demo carousel + validation | 1.0 |
| **Total** | **~12.5 hours** |

Kimi's estimate of "4 hours" only covered the CSS/SVG primitives themselves — not the system integration. Realistic total for a clean, documented, tested ship is ~1.5 working days.

If we want a faster path: ship A1-A6 only (skip A7 grain rework + A8 drop-shadow), defer Tier B, ~7 hours total.

---

## 11. Approval Required

Before any code touches the repo, Kenneth needs to OK:

- [ ] Tier A list of 8 primitives (or trimmed to 6)
- [ ] All decision locks in §0 (already approved)
- [ ] §5 spec schema additions (`text_treatment`, `effects.shadow`, `effects.grain_opacity`)
- [ ] §6.4 docs/skills/rules scope (everything updated in this pass)
- [ ] §6.5 memory updates (especially the two NEW memory files)
- [ ] §9 open questions Q1–Q5

Once approved, implementation is a single PR with all changes.
