# Component Catalog — html-carousel-builder

Single source of truth for every component the AI can request in a `carousel-spec.json`.
Updated on every approved component change. The render engine reads `scripts/component_registry.json` at build time to enforce system allowlists.

**How allowlist enforcement works.** Each component has a `systems` field in `scripts/component_registry.json`. Values: a list of system-type groups (`"dark"`, `"light"`, `"brutalist"`, `"warm"`, `"cyberpunk"`) or `"*"` (universal). The render engine will warn (and use a fallback) when a slide spec requests a component on an unsupported system. To override: pass `--ignore-registry` (not built yet — currently warnings only).

**How to use a new component in a spec.** For layouts, set `slide.layout` to the slide name. For geo layers, pass an array via `slide.layers` to override the system default. Sub-components are referenced as inline HTML inside copy fields (the AI must produce them following the patterns shown below).

**Review hub.** Open [`gallery/INDEX.html`](../../../gallery/INDEX.html) in a browser. Click any component on the left, preview the rendered 3-slide demo on the right. Use the category filter (Geo / Chrome / Layout / Sub) to focus.

---

## Tier 1 — Geo Layers (12 new + 8 existing)

Background atmosphere layers. One per slide. `z-index: 1-3`. Selected via `slide.layers` array or inherited from system default in `GEO_HTML` (`scripts/render_carousel.py`).

| Name | Systems | When to use | When NOT |
|---|---|---|---|
| `pw-grid` (existing) | dark, cyberpunk | Tech / data-heavy slides needing depth | Warm or light brands — too cold |
| `grid-bg` (existing) | brutalist, light | Editorial / architectural | Cyberpunk — competes with scan-lines |
| `glow-orb` (existing) | dark, cyberpunk | Mood pieces, hook slides | Light systems — invisible |
| `vol-light` (existing) | warm | Warm brand intros | Tech contexts |
| `blob-bg` (existing) | warm, light | Soft hooks, testimonials | Brutalist (clashes) |
| `diag-band` (existing) | light, brutalist | Editorial accents | Dark heavy slides |
| `zoom-rings` (existing) | dark, cyberpunk | Concentric focus, CTAs | Light or warm |
| `scan-lines` (existing) | cyberpunk only | Terminal slides in s29 | Any other system |
| **`geo-mesh-noise`** | warm, light | Organic motion feel, soft brand intros | Brutalist (too soft) |
| **`geo-pixel-grid`** | cyberpunk, dark | Tech without 3D rotation | Warm / light |
| **`geo-conic-rays`** | brutalist, warm | High-energy editorial hooks | Tech slides |
| **`geo-chevron-stripe`** | brutalist, dark | Graphic rhythm, manifesto | Warm / light |
| **`geo-iso-grid`** | dark, brutalist | Alt to pw-grid, no perspective | Light systems |
| **`geo-paper-texture`** | light only | Print editorial vibe | Dark / cyberpunk |
| **`geo-halftone`** | brutalist, light | Print magazine feel | Tech systems |
| **`geo-ribbon-flow`** | warm, light | Soft motion-feel testimonials | Brutalist / tech |
| **`geo-circuit-trace`** | cyberpunk only | Identity hits for s29 | Anywhere else |
| **`geo-topo-lines`** | dark, brutalist | Cartographic editorial | Warm / cyberpunk |
| **`geo-starfield`** | dark, cyberpunk | Atmosphere, depth | Light systems |
| **`geo-gradient-bands`** | warm, light | Editorial magazine stripe | Dark / cyberpunk |

**Demos:** `gallery/01-geo-mesh-noise.html` … `gallery/12-geo-gradient-bands.html`

---

## Tier 2 — Chrome / Frame Variants (3 new + 5 existing)

Wrapper elements that frame the canvas. Position absolute, `z-index: 8-10`. Always rendered after geo + content.

| Name | Systems | When to use | When NOT |
|---|---|---|---|
| `brand` (existing) | * | Always — bottom-left handle | Never skip |
| `counter` (existing) | * | Slides 2-N (slide 1 uses swipe-pill) | Slide 1 |
| `swipe-pill` (existing) | * | Slide 1 only | Slides 2+ |
| `kicker` (existing) | * | Top of any layout — short uppercase label | Pull-quote / silence slides |
| `prog` (existing) | * | Always — bottom-center dots | Never skip |
| **`chrome-vertical-counter`** | light, brutalist | Editorial magazine feel — rotated 90° on right edge | Dark / cyberpunk |
| **`chrome-badge-stamp`** | * | Promo / category callout — top-right wax-seal stamp | Avoid stacking with other top-right elements |
| **`chrome-header-bar`** | light only | Magazine top bar — date + logo | Dark systems clash |

**Demos:** `gallery/13-chrome-vertical-counter.html`, `gallery/14-chrome-badge-stamp.html`, `gallery/15-chrome-header-bar.html`

---

## Tier 3 — Slide Layouts (15 new + 9 existing)

Full slide compositions. One per slide. `z-index: 5`. The `layout` field in `slide` selects the template from `templates/slides/`.

### Existing (9)

| Layout | Required `copy` fields | Max counts |
|---|---|---|
| `slide-hook-lockup` | `headline` | `stat_number` optional for result-first variant |
| `slide-big-number` | `stat_number` | Adds 2-col stat-grid when `headline` present |
| `slide-terminal` | `output_lines` (≤4), optional `items` (≤3 CV mock rows) | dark/cyberpunk only |
| `slide-tip-blocks` | `tips` (≤3) | bad/mid/good visual order |
| `slide-before-after` | `before_items`, `after_items` (each ≤4) | |
| `slide-checklist` | `tips` (≤5) | |
| `slide-proof` | `quote`, `attribution` | optional `stat_number`, `body` for mechanism |
| `slide-cta` | `question`, `cta_keyword`, `reward` | URL replaces counter when present |
| `slide-pull-quote` | `quote` | silence beat — strip all decoration |

### New (15)

| Layout | Required `copy` | Max counts | Demo |
|---|---|---|---|
| **`slide-myth-vs-fact`** | `myth`, `fact` | each ≤140 chars | `gallery/16-slide-myth-vs-fact.html` |
| **`slide-step-flow`** | `steps[]` | 3-4 steps; each `title` ≤24 chars, `desc` ≤40 | `gallery/17-slide-step-flow.html` |
| **`slide-comparison-table`** | `headers[]`, `rows[]` | 2-3 columns, ≤4 rows. Use `"✓"` / `"✗"` | `gallery/18-slide-comparison-table.html` |
| **`slide-faq-stack`** | `faqs[]` | 2-3 Q/A; q ≤80, a ≤140 | `gallery/19-slide-faq-stack.html` |
| **`slide-quote-cascade`** | `quotes[]` | ≤4 quotes in 2-col grid; text ≤100 | `gallery/20-slide-quote-cascade.html` |
| **`slide-bento-grid`** | `tiles[]`, `grid` | 4-6 tiles; pick `g-2x2`/`g-3x2`/`g-mixed` | `gallery/21-slide-bento-grid.html` |
| **`slide-timeline`** | `events[]` | 3-5 events; titles ≤24, desc ≤50 | `gallery/22-slide-timeline.html` |
| **`slide-stat-row`** | `stats[]` | exactly 3 stats | `gallery/23-slide-stat-row.html` |
| **`slide-pull-quote-author`** | `quote`, `author` | quote ≤180; add `role` optional | `gallery/24-slide-pull-quote-author.html` |
| **`slide-warning-banner`** | `headline` | headline can contain `<em>` for accent word | `gallery/25-slide-warning-banner.html` |
| **`slide-icon-grid`** | `tiles[]` | exactly 6 tiles; title ≤16, desc ≤30 | `gallery/26-slide-icon-grid.html` |
| **`slide-progress-bars`** | `bars[]` | 3-4 bars; each `pct` 0-100 | `gallery/27-slide-progress-bars.html` |
| **`slide-list-numbered`** | `items[]` | 4-5 items; title ≤40, desc ≤70 | `gallery/28-slide-list-numbered.html` |
| **`slide-data-viz-donut`** | `percent`, `legend[]` | dark/cyberpunk/light only; ≤3 legend rows | `gallery/29-slide-data-viz-donut.html` |
| **`slide-typeset-poster`** | `headline` | brutalist/light only; supports `<span class="accent-line">` and `<span class="strike-line">` | `gallery/30-slide-typeset-poster.html` |

---

## Tier 4 — Sub-Components (20 new)

Reusable inline CSS classes. Used INSIDE layouts via HTML in copy fields. The AI must produce the correct markup; the render engine doesn't insert these automatically.

| Class | Used in | HTML snippet pattern |
|---|---|---|
| **`sub-stamp-circle`** | Any layout (absolute positioned) | `<div class="sub-stamp-circle">GRATIS</div>` |
| **`sub-pill-tag`** | Any text field | `<span class="sub-pill-tag">Tag</span>` or `.sub-pill-tag.solid` for filled |
| **`sub-arrow-flow`** | step-flow, timeline | `<div class="sub-arrow-flow"></div>` or `.down` variant |
| **`sub-icon-circle`** | icon-grid, bento | `<div class="sub-icon-circle">A</div>` or `.solid` variant |
| **`sub-dotted-divider`** | Any layout | `<div class="sub-dotted-divider"></div>` |
| **`sub-rating-stars`** | proof | `<div class="sub-rating-stars"></div>` (auto 5 stars) |
| **`sub-logo-row`** | proof, cta | `<div class="sub-logo-row"><span class="logo">FORBES</span>…</div>` |
| **`sub-avatar-stack`** | proof, hook | `<div class="sub-avatar-stack"><span class="av">C</span>…<span class="av more">+99</span></div>` |
| **`sub-fact-bubble`** | myth-vs-fact | `<div class="sub-fact-bubble fact"><span class="bub-label">Realidad</span>…</div>` |
| **`sub-timeline-dot`** | timeline | Automatically used by `slide-timeline` |
| **`sub-bento-card`** | bento-grid | Automatically used by `slide-bento-grid` |
| **`sub-inline-stat`** | Any text field | `<span class="sub-inline-stat">4x</span>` |
| **`sub-status-pill`** | comparison, terminal | `<span class="sub-status-pill pass">PASS</span>` (pass/warn/fail) |
| **`sub-comment-mock`** | proof, hook | `<div class="sub-comment-mock"><div class="com-av">S</div><div class="com-body">…</div></div>` |
| **`sub-handle-line`** | proof | `<div class="sub-handle-line"><span class="handle">@user</span><span class="dot">·</span>2h</div>` |
| **`sub-stat-card`** | stat-row | Automatically used by `slide-stat-row` |
| **`sub-chip-list`** | Any | `<div class="sub-chip-list"><span class="chip">Python</span>…</div>` |
| **`sub-download-card`** | cta | `<div class="sub-download-card"><div class="dl-icon">PDF</div><div class="dl-body">…</div></div>` |
| **`sub-emoji-callout`** | warning-banner | `<div class="sub-emoji-callout"><div class="ec-emoji">📄</div><div class="ec-text">…</div></div>` |
| **`sub-swipe-arrow-stack`** | hook (alt to swipe-pill) | `<div class="sub-swipe-arrow-stack"><span>›</span><span>›</span><span>›</span></div>` |

**Demos:** `gallery/31-sub-stamp-circle.html` … `gallery/50-sub-swipe-arrow-stack.html`

---

## Content safety wrapper

As of 2026-05-16, the shell enforces `max-height: calc(100% - 24px); overflow: hidden` on every layout's primary wrapper (`.hook-wrap`, `.stat-wrap`, `.term-wrap`, `.tip-wrap`, `.ba-wrap`, `.chk-wrap`, `.proof-wrap`, `.cta-wrap`, `.quote-wrap`, plus all new layout wrappers).

This means content that would overflow the 1080px canvas now gets clipped instead of crashing into the chrome (brand / counter / progress dots). The schema's `maxLength` and `maxItems` limits are the first line of defense; the wrapper is the safety net. If a slide gets clipped you have a copy-budget problem, not a CSS problem — reduce the spec data.

## Schema limits (carousel-spec.schema.json, v2)

| Field | Limit |
|---|---|
| `kicker` | 32 chars |
| `headline` | 70 chars |
| `body` | 140 chars |
| `stat_number` | 8 chars |
| `stat_context` | 90 chars |
| `source` | 60 chars |
| `command` | 60 chars |
| `output_lines` | 4 items, each `text` ≤50 chars |
| `before_items`, `after_items` | 4 items, each ≤60 chars |
| `before_score`, `after_score` | 40 chars |
| `quote` | 180 chars |
| `attribution` | 60 chars |
| `question` | 80 chars |
| `cta_keyword` | 14 chars |
| `reward` | 100 chars |
| `url` | 40 chars |
| `tips` | 3 items; `problem` ≤60, `fix` ≤90 |
| `items` (generic) | 5 items, each ≤70 chars |
