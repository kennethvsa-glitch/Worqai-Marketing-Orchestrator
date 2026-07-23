# Spec Schema Reference — carousel-spec.schema.json

Every carousel is authored as a JSON spec file then rendered by the engine.
Schema: `scripts/carousel-spec.schema.json`

---

## Top-Level Structure

```json
{
  "meta": { ... },       // required
  "pacing": [ ... ],     // required — one beat per slide
  "slides": [ ... ],     // required — one object per slide
  "constraints": { ... } // optional — global overrides
}
```

---

## meta

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `system` | string | yes | — | Design system ID, format `s##` (e.g., `s17`) |
| `aspect` | string | yes | `"1:1"` | `"1:1"`, `"4:5"`, or `"9:16"` |
| `slides` | integer | yes | — | Total slide count, 3–10 |
| `brand` | string | no | `"@worqai"` | Brand handle shown in footer |
| `language` | string | no | `"es-CR"` | `"es-CR"`, `"es-LATAM"`, or `"en"` |
| `title` | string | no | — | Human-readable title (not rendered) |
| `topic` | string | no | `"carousel"` | Used in default output filename |
| `density` | string | no | `"standard"` | `"maximal"`, `"standard"`, `"restrained"` |
| `set` | string | no | — | Visual set ID (e.g., `TECH_SET_A`) |

---

## pacing

Array of beat labels, one per slide. Length must equal `meta.slides`.

Valid values: `hook`, `shock`, `proof`, `data`, `diagnostic`, `solution`, `hope`, `relief`, `action`, `cta`, `silence`, `break`, `myth`, `reality`, `testimonial`, `urgency`

A pacing beat of `"silence"` forces `is_silence = true` on that slide (same as `constraints.silence: true` in the slide spec).

Common arc patterns:
- 4-slide: `["hook", "shock", "solution", "cta"]`
- 4-slide: `["hook", "data", "solution", "cta"]`
- 4-slide: `["hook", "diagnostic", "solution", "cta"]`

---

## slides[n] — slide object

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string | yes | `"s1"`, `"s2"`, etc. |
| `layout` | string | yes | Template name from `templates/slides/` (without `.html`) |
| `layers` | array | no | Override default geo layers. Max 3 items. See render-engine.md for valid layer names. |
| `decoratives` | array | no | Decorative flourish IDs or objects. Max 2. See Decoratives table. |
| `custom_css` | string | no | Raw CSS injected into the carousel `<style>` block, scoped to this slide. Use `.s{N}-*` prefix convention. |
| `mock_ui` | string | no | Single mock-UI component ID |
| `copy` | object | no | Copy content — fields vary by layout (see slide-templates.md) |
| `constraints` | object | no | Per-slide overrides |

### slides[n].decoratives — valid IDs

| ID | Type | Description |
|----|------|-------------|
| `"corner-frame"` | static | Two L-bracket corners (top-left + bottom-right) |
| `"ornament"` | static | ✦ ✧ ✦ cluster, top-right |
| `"ornament-tr"` | static | ✦ ✧ ✦ cluster, top-right |
| `"ornament-bl"` | static | ✦ ✧ ✦ cluster, bottom-left |
| `"chrome-vertical-counter"` | static | Rotated "WORQAI 2026" on right edge |
| `"chrome-header-bar"` | static | Magazine-style top bar (use on light/editorial systems) |
| `"chrome-badge-stamp"` | static | Wax seal badge, top-right |
| `{"id":"watermark","text":"W"}` | parameterized | Giant faint letter/number behind content. `text` = any 1–4 char string. |
| `{"id":"sub-stamp-circle","text":"GRATIS"}` | parameterized | Dashed-circle stamp, bottom-right. `text` = 1–2 word label. |

**Note:** `decoratives` on a `"silence"` beat slide are automatically suppressed by the render engine.

### slides[n].constraints

| Field | Type | Notes |
|-------|------|-------|
| `silence` | boolean | Force zero decorative elements on this slide |
| `max_weight` | integer | 1–10 |
| `technique_count` | integer | 1–6 |

---

## copy — universal fields (valid in any layout)

| Field | Max length | Notes |
|-------|-----------|-------|
| `kicker` | 32 chars | Top label, rendered uppercase, max 4 words |
| `headline` | 70 chars | Main headline, max 8 words |
| `body` | 140 chars | Supporting body, max 18 words |
| `swipe_prompt` | 20 chars | Default: `"Desliza →"` |
| `source` | 60 chars | Stat citation — must match validator allow-list |
| `items` | array, max 5 | Simple string list. Each item max 70 chars. |
| `tips` | array, max 3 | Objects with `problem` (60) and `fix` (90) |

## copy — specialized fields

| Field | Max length | Used by |
|-------|-----------|---------|
| `stat_number` | 8 chars | slide-big-number, slide-hook-lockup (result variant) |
| `stat_context` | 90 chars | slide-big-number, slide-hook-lockup |
| `stat_side_tag` | — | slide-big-number side label |
| `command` | 60 chars | slide-terminal |
| `output_lines` | array, max 4 | slide-terminal. Each: `{type, text}`. Types: `cmd`, `ok`, `warn`, `err`, `info` |
| `before_items` | array, max 4 | slide-before-after. Each max 60 chars. |
| `after_items` | array, max 4 | slide-before-after. Each max 60 chars. |
| `before_score` | 40 chars | slide-before-after score label |
| `after_score` | 40 chars | slide-before-after score label |
| `bad_label` | — | slide-before-after column header (default: "Antes") |
| `good_label` | — | slide-before-after column header (default: "Ahora") |
| `quote` | 180 chars | slide-pull-quote, slide-proof, slide-pull-quote-author |
| `attribution` | 60 chars | slide-pull-quote, slide-pull-quote-author |
| `author` | — | slide-pull-quote-author (also accepts `attribution`) |
| `role` | — | slide-pull-quote-author role line |
| `question` | 80 chars | slide-cta (also accepts `headline`) |
| `cta_keyword` | 14 chars | slide-cta — single keyword for DM |
| `reward` | 100 chars | slide-cta — specific deliverable promise |
| `url` | 40 chars | slide-cta target / link-in-bio |
| `steps` | array | slide-step-flow. Each: `{title, desc}` |
| `stats` | array | slide-stat-row. Each: `{num, unit?, label?, body?}` |
| `tiles` | array | slide-bento-grid. Each: `{label?, title?, body?, accent?, span_2?}` |
| `grid` | string | slide-bento-grid layout class, default `"g-2x2"` |
| `headers` | array | slide-comparison-table. Default: `["Feature","Antes","Después"]` |
| `rows` | array | slide-comparison-table. Each row is an array of cell strings. Use `"✓"`/`"yes"`/`"✗"`/`"no"` for mark cells. |
| `faqs` | array | slide-faq-stack. Each: `{q, a?}` |
| `quotes` | array | slide-quote-cascade. Each: `{text, attr?}`. Rendered in pairs per row. |
| `events` | array | slide-timeline. Each: `{date?, title?, desc?}` |
| `bars` | array | slide-progress-bars. Each: `{label, value, pct?}`. `pct` = fill width 0–100. |
| `percent` | integer | slide-data-viz-donut. 0–100, default 75 |
| `center_label` | — | slide-data-viz-donut label inside circle |
| `legend` | array | slide-data-viz-donut. Each: `{label, value, color?}` |
| `eyebrow` | — | slide-typeset-poster small top label |
| `footer_left` | — | slide-typeset-poster (default: brand) |
| `footer_right` | — | slide-typeset-poster (default: "Issue NN") |
| `icon` | — | slide-warning-banner icon character (default: `"!"`) |
| `myth` | — | slide-myth-vs-fact myth text |
| `fact` | — | slide-myth-vs-fact fact text |
| `myth_label` | — | slide-myth-vs-fact (default: `"Mito"`) |
| `fact_label` | — | slide-myth-vs-fact (default: `"Realidad"`) |

---

## constraints (global)

| Field | Default | Notes |
|-------|---------|-------|
| `mock_ui_required` | true | Whether preflight check 6 should be enforced |
| `silence_slide_required` | true | Whether at least one silence slide is required |
| `subtraction_gate` | true | Whether Subtraction Gate review was applied |
| `max_weight_per_slide` | 6 | Visual weight limit per slide |
| `min_weight_per_slide` | 3 | Minimum visual weight per slide |
| `technique_budget` | 3 | Max techniques per carousel |
| `decorative_budget` | 1 | Max decoratives per slide |
| `file_size_target_kb` | 45 | Target file size |

Note: `constraints` fields in the spec are not currently read by the render engine. They are authoring intent documentation and are used by the preflight/QA layer.
