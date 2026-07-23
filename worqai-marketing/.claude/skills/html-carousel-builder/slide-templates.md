# Slide Templates Reference — templates/slides/

All 24 available layout templates. Each is a Jinja2 partial rendered into the shell.

Variables available in every template: `copy`, `slide_num`, `total`, `brand`, `is_active`, `is_silence`, `beat`, `system_type`, `geo_html`

All templates include the chrome footer: `.brand`, `.counter`, `.prog` (progress dots).

---

## slide-hook-lockup

**Best for:** Slide 1 (hook). Opening statement, identity/result hook.

**Copy fields consumed:**
- `kicker` — top label
- `headline` — main display headline
- `body` — supporting sentence
- `swipe_prompt` — default `"Desliza →"` (rendered as `.swipe-pill`)
- `stat_number` *(optional)* — if present, triggers result-grid variant with stat
- `stat_context` *(optional)* — context below the stat number

**Variants:** If `stat_number` is set, renders a result grid (stat + context) alongside the headline. Without it, pure text lockup.

---

## slide-big-number

**Best for:** Slide 2 (data/shock). Single oversized stat with context.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)* — if present, triggers grid layout with headline alongside stat
- `stat_number` — the oversized number/symbol (e.g., `"3×"`, `"76%"`)
- `stat_context` — 1–2 line context below the stat
- `stat_side_tag` *(optional)* — small side label
- `source` *(optional)* — citation line (must pass stat-validator allow-list)
- `body` *(optional)* — additional body text

**Important:** `stat-context` class matches `[class*=stat]` → classified as **headline** by preflight (55 char / 10 word budget, not body budget).

---

## slide-terminal

**Best for:** Slide 2 (shock/diagnostic). Simulated terminal output showing a problem.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` — description above the terminal
- `command` — the `$ command` line
- `output_lines` — array of `{type, text}` objects. Types:
  - `cmd` — command echo
  - `ok` — success (green)
  - `warn` — warning (yellow)
  - `err` — error (red)
  - `info` — info (muted)
- `source` *(optional)* — citation below terminal

**Note:** This layout contains the `terminal-panel` class, satisfying preflight check 6 (Mock UI).

---

## slide-tip-blocks

**Best for:** Slide 3 (solution). Problem/fix pairs or simple item list.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline`
- `tips` *(optional)* — array of `{problem, fix}` objects. Renders as problem/fix card pairs.
- `items` *(optional)* — fallback simple string list if `tips` is empty

**Rendering logic:** If `tips` has entries, renders tip-block cards. If `tips` is absent/empty, falls back to `items` as a plain list.

**Note:** `tip-blk-label` class matches `[class*=lbl]` → classified as **label** by preflight (40 char / 6 word budget). Keep `tips[].problem` under 6 words.

---

## slide-before-after

**Best for:** Slide 2–3 (diagnostic/solution). Side-by-side before/after comparison.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline`
- `body` *(optional)*
- `before_items` — array of strings (left column)
- `after_items` — array of strings (right column)
- `before_score` — label below left column
- `after_score` — label below right column
- `bad_label` *(optional)* — column header, default `"Antes"`
- `good_label` *(optional)* — column header, default `"Ahora"`

---

## slide-checklist

**Best for:** Slide 3 (solution). Actionable checklist items.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline`
- `body` *(optional)*
- `tips` *(optional)* — if present, renders problem/fix pairs (same as tip-blocks)
- `items` *(optional)* — fallback simple string list

**Note:** `chk-title` class matches `[class*=title]` → classified as **headline** by preflight (55 char / 10 word budget). Keep `items[]` strings under 55 chars / 10 words.

---

## slide-cta

**Best for:** Final slide (cta). DM keyword call to action.

**Copy fields consumed:**
- `question` — the question (also accepts `headline` if `question` absent)
- `cta_keyword` — the keyword users DM (rendered in `.keyword-text`)
- `reward` — specific deliverable promise
- `url` — target handle or URL (replaces counter if present)

**Preflight check 7** requires all three: a `?`/`¿`, a `.keyword-text` element, and a reward word (gratis/free/etc.).

---

## slide-pull-quote

**Best for:** Testimonial or philosophy statement.

**Copy fields consumed:**
- `quote` — the quote text (also accepts `headline`)
- `attribution` — attribution line

---

## slide-pull-quote-author

**Best for:** Testimonial with author identity card.

**Copy fields consumed:**
- `quote` — quote text (also accepts `headline`)
- `kicker` *(optional)*
- `author` — author name (also accepts `attribution`)
- `role` *(optional)* — role/title line
- Avatar is rendered as the first letter of `author`/`attribution`

---

## slide-proof

**Best for:** Social proof with client result.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline`
- `quote` — testimonial or result quote
- `attribution` — who said it
- `stat_number` *(optional)* — highlight metric
- `stat_context` *(optional)* — metric context
- `body` *(optional)* — mechanism explanation section

---

## slide-step-flow

**Best for:** Process or workflow (numbered steps with arrows).

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline`
- `steps` — array of `{title, desc}` objects. Rendered with `sub-arrow-flow` connectors between steps.

---

## slide-list-numbered

**Best for:** Ranked or ordered list.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline`
- `items` — array of strings OR `{title, desc}` objects. If objects, renders title+desc per item. If strings, renders as simple numbered list.

---

## slide-bento-grid

**Best for:** Feature/metric grid.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `tiles` — array of tile objects. Each: `{label?, title?, body?, accent?: bool, span_2?: bool}`
- `grid` — CSS layout class, default `"g-2x2"`. Options: `g-2x2`, `g-2x3`, or any custom class defined in shell.

**Tile properties:**
- `accent: true` → adds `.accent` class (uses accent color background)
- `span_2: true` → adds `.span-2` class (spans 2 columns)

---

## slide-comparison-table

**Best for:** Feature comparison (product vs product, old vs new).

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `headers` — array of column headers, default `["Feature","Antes","Después"]`
- `rows` — 2D array. First cell in each row = feature name (.feature class). Other cells: use `"✓"`/`"yes"` for green check, `"✗"`/`"no"` for red cross, any other string for plain text.

---

## slide-faq-stack

**Best for:** Q&A format.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `faqs` — array of `{q, a?}` objects. `a` is optional — can show question-only if needed.

---

## slide-quote-cascade

**Best for:** Multiple short testimonials or voice-of-customer quotes.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `quotes` — array of `{text, attr?}` objects. Quotes are rendered **in pairs** per row (2-column layout). Odd number is fine — last row will have one quote.

---

## slide-timeline

**Best for:** Chronological narrative, before/after journey.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `events` — array of `{date?, title?, desc?}` objects. All three fields are optional per event.

---

## slide-stat-row

**Best for:** Multiple metrics side by side.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `stats` — array of stat card objects. Each: `{num, unit?, label?, body?}`
- `source` *(optional)* — citation line

---

## slide-warning-banner

**Best for:** Alert or warning callout. Simple, high-impact single-message slide.

**Copy fields consumed:**
- `icon` — icon character, default `"!"`
- `headline` — warning message (rendered with `| safe` filter — HTML allowed)
- `body` *(optional)* — supporting text

No kicker. Minimal layout by design.

---

## slide-icon-grid

**Best for:** Feature grid with icons.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `tiles` — array of `{icon?, title?, desc?, solid?: bool}`. `icon` default `"●"`. `solid: true` adds `.solid` class to icon circle.

---

## slide-progress-bars

**Best for:** Comparison of values as horizontal bar chart.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `bars` — array of `{label, value, pct?}`. `pct` = fill percentage 0–100, default 50. `value` is the display text shown right of the label.
- `source` *(optional)* — citation line

---

## slide-data-viz-donut

**Best for:** Single percentage stat as donut chart with side panel.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `percent` — integer 0–100, default 75. Controls SVG stroke dashoffset.
- `center_label` *(optional)* — text inside the donut circle
- `body` *(optional)* — additional text in side panel
- `legend` *(optional)* — array of `{label, value, color?}` for legend rows below headline
- `source` *(optional)* — citation line

Donut math: `circ = 314`, `offset = 314 - (314 × pct / 100)`

---

## slide-typeset-poster

**Best for:** Bold editorial title slide or section break.

**Copy fields consumed:**
- `eyebrow` *(optional)* — small label above display
- `headline` — large display text (rendered with `| safe` — HTML/line breaks allowed)
- `footer_left` *(optional)* — default: brand handle
- `footer_right` *(optional)* — default: `"Issue NN"` (slide number)

No kicker, no body, no counter in content — pure typographic composition.

---

## slide-myth-vs-fact

**Best for:** Debunking a common misconception.

**Copy fields consumed:**
- `kicker` *(optional)*
- `headline` *(optional)*
- `myth` — the myth text (left bubble, `.sub-fact-bubble.myth`)
- `fact` — the reality text (right bubble, `.sub-fact-bubble.fact`)
- `myth_label` *(optional)* — default `"Mito"`
- `fact_label` *(optional)* — default `"Realidad"`

---

## Layout Selection Guide

| Pacing beat | Recommended layouts |
|-------------|---------------------|
| hook | slide-hook-lockup |
| shock | slide-terminal, slide-big-number |
| data | slide-big-number, slide-stat-row, slide-data-viz-donut, slide-progress-bars |
| diagnostic | slide-before-after, slide-comparison-table, slide-myth-vs-fact |
| solution | slide-tip-blocks, slide-checklist, slide-step-flow, slide-icon-grid |
| proof | slide-proof, slide-pull-quote-author, slide-quote-cascade |
| cta | slide-cta |
| break | slide-typeset-poster, slide-pull-quote |
| testimonial | slide-pull-quote-author, slide-quote-cascade |
| myth/reality | slide-myth-vs-fact |
