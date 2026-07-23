# AGENCY (A) UPGRADE PLAN — Carousel System v3

**Status:** Implementation-ready specification
**Target:** Elevate output from B+ commercial to A agency grade
**Approach:** Keep what works, fix what's weak, add what's missing

---

## PART 1: GAP ANALYSIS — B+ vs Agency (A)

### What's Already Working (Keep)
- Clean, readable, no obvious bugs
- 48 design systems with real color/font curation
- SVG primitives working (blobs, starbursts, icons, text-stroke, gradient text)
- 21 SVG icon library
- Grain texture overlay
- Dual export pipeline (Playwright for quality, html2canvas for speed)
- 14-point preflight + visual richness check + ship gate
- Batch diversity enforcement

### What's Missing (The Gap)

| Dimension | Current (B+) | Agency (A) |
|-----------|-------------|------------|
| **Layout variety** | 24 layouts, mostly "centered text block" variations | 40+ layouts with genuine structural diversity |
| **Typography hierarchy** | "Readable" — everything proportional, nothing extreme | **Intentional tension** — 64px headline vs 13px micro-label vs 18px body. Size contrast IS the design. |
| **Composition** | Elements placed by template logic | Elements placed with **intentional visual weight** — asymmetric balance, overlapping layers, diagonal tension |
| **System personality** | Same layout approach regardless of system | Each system family has **layout preferences, type personality, decorative density rules** |
| **Visual surprise** | Predictable — same blob placement, same gradient direction | One slide per carousel has an **unexpected moment** — full bleed, diagonal split, massive type |
| **Whitespace usage** | Consistent padding everywhere | **Varied rhythm** — tight/tight/LOOSE/tight creates breathing moments |
| **Copy integration** | Text sits in designated areas | Text and visuals **interact** — type over shapes, text following curves, negative space as design element |
| **Consistency vs variety** | Every slide feels "same family" | Family identity holds, but **each slide has distinct personality within it** |

---

## PART 2: TYPOGRAPHY OVERHAUL — Real Hierarchy Tension

This is the single highest-impact change. Current output reads as "text on a background." Agency work reads as **typography as design**.

### 2.1 Size Ratio System

Every slide MUST use at least 3 of these 5 type tiers. Never use only 2.

| Tier | Size | Weight | Tracking | Use Case |
|------|------|--------|----------|----------|
| **DISPLAY** | `clamp(48px, 10cqw, 84px)` | 900 | `-0.04em` | Main headline — the ONE thing you read first |
| **SUB-HEAD** | `clamp(22px, 4cqw, 32px)` | 700 | `-0.01em` | Supporting statement, secondary message |
| **BODY** | `clamp(14px, 2.5cqw, 17px)` | 400 | `0` | Explanatory text, descriptions |
| **LABEL/MICRO** | `10px-11px` | 600 | `0.15em-0.25em` | Kickers, metadata, sources, slide counters |
| **MONO** | `12px-13px` | 500 | `0` | Terminal, code, data points, technical details |

**The ratio rule:** Display should be **3-5x larger** than body text in the same slide. If display is 64px, body should be 13-16px. Not 24px. The contrast IS the hierarchy.

### 2.2 Type Personality Per System Family

| Family | Display Character | Body Character | Personality Rule |
|--------|------------------|----------------|-----------------|
| **dark (s01-s04, s06, s08-s14, s16, s20-s22, s27-s32, s34, s36, s37, s40-s43)** | Bold condensed or geometric sans | Light weight, generous leading | "Quiet confidence" — massive display + whisper body |
| **light (s05, s18, s19, s23, s25, s26, s39, s45, s47, s48)** | Medium weight, tighter tracking | Regular weight, tight leading | "Editorial clarity" — refined, magazine-like, lots of whitespace |
| **warm (s10, s12, s13, s24, s35, s38)** | Rounded or serif display | Soft weight, warm tone | "Approachable authority" — friendly but not casual |
| **brutalist (s07, s31)** | Black weight, tight/negative tracking | Regular, neutral | **"Violent contrast"** — type crashes into edges, bleeds off canvas |
| **cyberpunk (s29, s40)** | Monospace or tech display | Monospace body | "System output" — type feels like terminal data, not marketing |

### 2.3 Implementation Rules

1. **Never use the same size for two different text roles** on the same slide. If headline is 48px, sub-head cannot be 42px. Minimum 1.5x gap.
2. **Labels/kickers are always uppercase, always tracked out.** `letter-spacing: 0.2em; text-transform: uppercase;` This creates visual separation from body text through density, not just size.
3. **Body text max-width is 32ch for centered, 40ch for left-aligned.** Longer lines = harder to read = looks amateur.
4. **Display text should occasionally break words across lines intentionally.** "CREA\nTIVO" not "CREATIVO" — the line break becomes a design element.
5. **Add `line-height: 0.85-0.95` for display headlines.** Tight leading on big type creates density and weight. Default 1.2 looks floaty.

---

## PART 3: 20+ NEW LAYOUTS + EXISTING FIXES

### Current Layouts — Status

| # | Layout | Status | Action |
|---|--------|--------|--------|
| 1 | `slide-hook-lockup` | Keep | Fix: display should bleed closer to edges |
| 2 | `slide-big-number` | Fix | Body text misaligned in S2 — fix split-screen logic |
| 3 | `slide-terminal` | Keep | Good as-is, icons now work |
| 4 | `slide-tip-blocks` | Keep | Minor: increase card contrast |
| 5 | `slide-before-after` | Keep | Good |
| 6 | `slide-checklist` | Deprecate | Too generic, merge with `slide-icon-grid` |
| 7 | `slide-cta` | Keep | Add neon glow by default |
| 8 | `slide-pull-quote` | Keep | Good |
| 9 | `slide-pull-quote-author` | Merge | Into `slide-pull-quote` with optional author fields |
| 10 | `slide-proof` | Merge | Into `slide-pull-quote` with optional stats |
| 11 | `slide-step-flow` | Fix | Increase step title contrast |
| 12 | `slide-list-numbered` | Keep | Good |
| 13 | `slide-bento-grid` | Fix | Allow mixed-size tiles (2x1, 1x2) for visual interest |
| 14 | `slide-comparison-table` | Redesign | Tables look corporate — convert to card-vs-card layout |
| 15 | `slide-faq-stack` | Redesign | Accordion feel — make it editorial Q&A with large typography |
| 16 | `slide-quote-cascade` | Keep | Good but rare |
| 17 | `slide-timeline` | Fix | Add connecting line/vertical axis |
| 18 | `slide-stat-row` | Keep | Good |
| 19 | `slide-warning-banner` | Merge | Into `slide-typeset-poster` with warning styling |
| 20 | `slide-icon-grid` | Fix | Fix empty icon bug (S4) — ensure SVG `<use>` resolves |
| 21 | `slide-progress-bars` | Keep | Good for data |
| 22 | `slide-data-viz-donut` | Keep | Good |
| 23 | `slide-typeset-poster` | Fix | More aggressive type scaling |
| 24 | `slide-myth-vs-fact` | Redesign | Editorial panels (already done by Claude) |

**Total after consolidation:** 20 core layouts + 20 new = **40 layouts**

---

### 20 NEW LAYOUTS (Full Specification)

For each layout, I specify:
- **Visual description** — what it looks like
- **CSS structure** — how to build it
- **Best beat** — which pacing moment it serves
- **Required copy** — minimum fields
- **Why it works** — the design principle

---

#### NEW 1: `slide-full-bleed-type`
**Visual:** Single massive word or short phrase filling 80%+ of the canvas. Background is a solid color or gradient. Text is either the accent color or has text-stroke treatment. No other elements except a micro-label in the corner.

**CSS:**
```css
.full-bleed-wrap { display:flex; align-items:center; justify-content:center; width:100%; height:100%; padding:0; }
.full-bleed-display { font-size:clamp(80px, 18cqw, 140px); font-weight:900; letter-spacing:-0.05em; line-height:0.85; text-align:center; }
.full-bleed-label { position:absolute; bottom:24px; left:24px; font-size:10px; letter-spacing:0.25em; text-transform:uppercase; opacity:0.5; }
```

**Best beat:** `silence`, `hook`, `break`
**Required:** `headline` (max 3 words), opt: `label`
**Why it works:** Maximum impact through minimal elements. One thing, huge. The silence beat physically.

---

#### NEW 2: `slide-diagonal-split`
**Visual:** A diagonal line (45° or 60°) splits the slide. One side is dark/solid, the other has a geo layer. Content is split across the diagonal — headline on the large side, supporting text on the small.

**CSS:**
```css
.diag-split-wrap { position:relative; width:100%; height:100%; overflow:hidden; }
.diag-split-bg { position:absolute; inset:0; clip-path:polygon(0 0, 65% 0, 35% 100%, 0 100%); background:var(--bg-base); }
.diag-split-content { position:relative; z-index:2; display:flex; flex-direction:column; justify-content:center; height:100%; padding:0 48px; }
.diag-split-main { width:55%; }
.diag-split-side { position:absolute; right:0; top:0; width:40%; height:100%; display:flex; align-items:center; padding:24px; }
```

**Best beat:** `shock`, `data`, `diagnostic`
**Required:** `headline`, `body`, opt: `stat_number`
**Why it works:** Diagonal creates dynamic tension. Feels like a magazine spread. The asymmetry is inherently more interesting than a centered block.

---

#### NEW 3: `slide-asymmetric-lockup`
**Visual:** Content occupies only the left 40% of the slide. The right 60% is near-empty — just a subtle geo layer or a single decorative element. Creates massive negative space.

**CSS:**
```css
.asym-wrap { display:flex; align-items:center; width:100%; height:100%; padding:0 0 0 48px; }
.asym-content { width:38%; max-width:380px; }
.asym-empty { flex:1; display:flex; align-items:center; justify-content:center; }
```

**Best beat:** `hook`, `silence`, `break`
**Required:** `headline`, `body`, opt: `kicker`
**Why it works:** Negative space is a luxury signal. When 60% of the canvas is empty, the content that IS there feels important. Bloomberg, The Gentlewoman, Kinfolk all use this.

---

#### NEW 4: `slide-type-over-shape`
**Visual:** An SVG organic blob fills 50% of the slide. The headline overlaps the blob edge — half the text sits on the blob (dark text), half on the background (light text). Creates a "text crossing a boundary" moment.

**CSS:**
```css
.tos-wrap { position:relative; width:100%; height:100%; overflow:hidden; }
.tos-blob { position:absolute; right:-10%; top:10%; width:65%; height:80%; }
.tos-headline { position:relative; z-index:2; font-size:clamp(36px, 7cqw, 64px); font-weight:900; }
/* Text color auto-adjusts: portion over blob uses var(--bg-mid), portion over bg uses var(--accent) */
```

**Best beat:** `hook`, `proof`
**Required:** `headline`, opt: `body` (short)
**Why it works:** The text-shape interaction creates a "designed" feel vs "templated." Requires the SVG blob to be positioned precisely so the text crosses its edge.

---

#### NEW 5: `slide-stacked-type`
**Visual:** 3-4 lines of text stacked vertically, each line a different size/weight. Creates a typographic hierarchy purely through scale. Like a poster.

**CSS:**
```css
.stacked-wrap { display:flex; flex-direction:column; justify-content:center; height:100%; padding:0 48px; gap:0; }
.stacked-line-1 { font-size:clamp(48px, 10cqw, 84px); font-weight:900; line-height:0.9; letter-spacing:-0.04em; }
.stacked-line-2 { font-size:clamp(32px, 6cqw, 48px); font-weight:700; line-height:1.0; opacity:0.9; }
.stacked-line-3 { font-size:clamp(16px, 3cqw, 22px); font-weight:400; line-height:1.3; opacity:0.6; margin-top:16px; }
```

**Best beat:** `hook`, `shock`, `break`
**Required:** `lines[]` (2-4 strings)
**Why it works:** Each line fights for attention differently. The contrast between 80px and 16px on the same vertical axis creates a visual waterfall.

---

#### NEW 6: `slide-corner-manifesto`
**Visual:** Text is pushed into one corner (bottom-left). The rest of the slide is dominated by a massive geo layer or grain texture. Feels like a manifesto pinned to a wall.

**CSS:**
```css
.corner-wrap { display:flex; flex-direction:column; justify-content:flex-end; align-items:flex-start; width:100%; height:100%; padding:0 0 80px 48px; }
.corner-headline { font-size:clamp(28px, 5cqw, 44px); font-weight:900; line-height:1.0; max-width:70%; }
.corner-body { font-size:14px; font-weight:300; margin-top:12px; max-width:45%; opacity:0.7; }
```

**Best beat:** `silence`, `break`, `testimonial`
**Required:** `headline`, opt: `body`
**Why it works:** Unconventional text placement signals "this isn't a template." The emptiness above the text creates gravitas.

---

#### NEW 7: `slide-data-wall`
**Visual:** 4-6 small data cards arranged in a tight grid, each with a number + label. No headline. Pure data density. Background has subtle grid geo layer.

**CSS:**
```css
.data-wall-wrap { display:grid; grid-template-columns:repeat(3, 1fr); gap:2px; width:100%; height:100%; padding:48px; }
.data-wall-card { display:flex; flex-direction:column; justify-content:center; padding:20px; background:rgba(255,255,255,0.03); }
.data-wall-num { font-size:clamp(28px, 5cqw, 48px); font-weight:900; line-height:1; }
.data-wall-label { font-size:10px; letter-spacing:0.2em; text-transform:uppercase; opacity:0.5; margin-top:8px; }
```

**Best beat:** `data`, `proof`
**Required:** `stats[]` (4-6 of `{number, label}`)
**Why it works:** Information density without overwhelm. The grid structure organizes chaos. Each card is scannable in <1 second.

---

#### NEW 8: `slide-side-by-side`
**Visual:** True 50/50 vertical split. Left side: dark background, large number or word. Right side: lighter background, explanation text. A thin 1px line separates them.

**CSS:**
```css
.sbs-wrap { display:flex; width:100%; height:100%; }
.sbs-left { width:50%; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:48px; background:var(--bg-base); }
.sbs-right { width:50%; display:flex; flex-direction:column; justify-content:center; padding:48px; background:var(--bg-mid); border-left:1px solid rgba(255,255,255,0.08); }
.sbs-big { font-size:clamp(64px, 12cqw, 120px); font-weight:900; line-height:0.85; }
```

**Best beat:** `data`, `diagnostic`, `comparison`
**Required:** `left_content` (number or short word), `right_content` (headline + body)
**Why it works:** The split creates a natural comparison rhythm. Left = what, Right = so what. Classic editorial technique.

---

#### NEW 9: `slide-frame-within-frame`
**Visual:** A smaller rectangle (70% of canvas) is centered, with a 1px border. Inside: content with generous padding. Outside the frame: just the background geo layer peeking through. Creates a "picture frame" effect.

**CSS:**
```css
.fwf-wrap { display:flex; align-items:center; justify-content:center; width:100%; height:100%; padding:48px; }
.fwf-frame { width:75%; height:75%; border:1px solid rgba(255,255,255,0.15); display:flex; flex-direction:column; justify-content:center; padding:48px; position:relative; }
```

**Best beat:** `testimonial`, `proof`, `quote`
**Required:** `quote`, `attribution`, opt: `kicker`
**Why it works:** The frame signals "this is important enough to be framed." Creates a gallery/art feel. The border is a subtle luxury signal.

---

#### NEW 10: `slide-massive-number` (replaces `slide-big-number`)
**Visual:** One number takes up 60% of the slide. It's positioned NOT centered — it's pushed to one side (left or right), bleeding slightly off-edge. Supporting text is tiny, positioned in the opposite corner.

**CSS:**
```css
.mn-wrap { position:relative; width:100%; height:100%; overflow:hidden; }
.mn-number { position:absolute; left:-5%; top:50%; transform:translateY(-50%); font-size:clamp(180px, 35cqw, 320px); font-weight:900; line-height:0.8; opacity:0.15; z-index:0; }
.mn-content { position:relative; z-index:2; width:45%; margin-left:auto; padding:48px; display:flex; flex-direction:column; justify-content:center; height:100%; }
```

**Best beat:** `data`, `shock`
**Required:** `stat_number`, `stat_context`, `headline`, opt: `source`
**Why it works:** The number is so large it becomes texture, not data. The opacity at 0.15 makes it a background element that happens to be a number. The real content floats on top. This is a Wired magazine technique.

---

#### NEW 11: `slide-terminal-fullscreen`
**Visual:** Entire slide is a terminal window. Not a small card — the terminal chrome (red/yellow/green dots) is at the top, and the rest is pure code output. Background is pure dark. No other elements.

**CSS:**
```css
.tfs-wrap { width:100%; height:100%; display:flex; flex-direction:column; padding:0; }
.tfs-chrome { height:36px; display:flex; align-items:center; gap:8px; padding:0 16px; border-bottom:1px solid rgba(255,255,255,0.08); }
.tfs-body { flex:1; padding:24px 16px; font-family:var(--font-mono); font-size:13px; line-height:1.6; overflow:hidden; }
```

**Best beat:** `diagnostic`, `shock`
**Required:** `tab_title`, `output_lines[]`
**Why it works:** Full immersion. The terminal IS the slide, not an element within it. Maximum credibility for technical content.

---

#### NEW 12: `slide-editorial-column`
**Visual:** Two text columns (45%/45%, 10% gap). Left column: headline + body. Right column: pull quote or secondary point. Divider line between columns.

**CSS:**
```css
.ec-wrap { display:flex; gap:40px; width:100%; height:100%; padding:48px; align-items:center; }
.ec-left { width:45%; }
.ec-divider { width:1px; height:60%; background:rgba(255,255,255,0.1); align-self:center; }
.ec-right { width:45%; font-size:clamp(18px, 3cqw, 24px); font-weight:300; font-style:italic; line-height:1.5; }
```

**Best beat:** `proof`, `testimonial`, `solution`
**Required:** `headline`, `body`, `quote`, opt: `attribution`
**Why it works:** Magazine editorial feel. The column structure signals "this is content worth reading, not scanning."

---

#### NEW 13: `slide-badge-grid`
**Visual:** 3-4 horizontal "badge" rows, each with an icon on the left and text on the right. But the badges are NOT cards — they're just text rows with a thin top border, like a specification sheet.

**CSS:**
```css
.bg-wrap { display:flex; flex-direction:column; width:100%; padding:48px; gap:0; }
.bg-row { display:flex; align-items:center; gap:16px; padding:20px 0; border-top:1px solid rgba(255,255,255,0.08); }
.bg-icon { width:32px; height:32px; flex-shrink:0; }
.bg-title { font-size:16px; font-weight:700; }
.bg-desc { font-size:13px; font-weight:300; opacity:0.6; margin-left:auto; text-align:right; max-width:50%; }
```

**Best beat:** `solution`, `data`
**Required:** `items[]` (3-4 of `{icon, title, description}`)
**Why it works:** Specification sheet aesthetic = technical credibility. No decoration, just information in a clear hierarchy.

---

#### NEW 14: `slide-contrast-knockout`
**Visual:** Slide is split into two massive color blocks (e.g., black top half, accent-color bottom half). Text on each half uses the opposite color for contrast. Zero geo layers, zero decoratives. Pure color + type.

**CSS:**
```css
.ck-wrap { display:flex; flex-direction:column; width:100%; height:100%; }
.ck-top { flex:1; display:flex; flex-direction:column; justify-content:center; padding:48px; background:var(--bg-base); color:var(--text-primary); }
.ck-bottom { flex:1; display:flex; flex-direction:column; justify-content:center; padding:48px; background:var(--accent); color:var(--bg-base); }
```

**Best beat:** `shock`, `hook`, `break`
**Required:** `top_text` (headline), `bottom_text` (body or stat)
**Why it works:** The color block split is the design. No layers needed. This is a poster technique that works because of the color shock, not despite it.

---

#### NEW 15: `slide-circular-quote`
**Visual:** A large circle (SVG or CSS border) is centered. Inside: a short quote or stat. Outside the circle: attribution or context text, positioned asymmetrically.

**CSS:**
```css
.cq-wrap { display:flex; align-items:center; justify-content:center; width:100%; height:100%; position:relative; }
.cq-circle { width:70%; aspect-ratio:1/1; border:1px solid rgba(255,255,255,0.15); border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:48px; text-align:center; }
.cq-quote { font-size:clamp(18px, 3.5cqw, 28px); font-weight:600; line-height:1.3; }
.cq-attr { position:absolute; bottom:48px; right:48px; font-size:11px; letter-spacing:0.15em; text-transform:uppercase; opacity:0.5; }
```

**Best beat:** `testimonial`, `proof`, `break`
**Required:** `quote`, `attribution`, opt: `kicker`
**Why it works:** The circle is a natural focal point. Human eyes are drawn to circles. The border creates a "seal of approval" feel.

---

#### NEW 16: `slide-waterfall-list`
**Visual:** 3-4 items listed vertically, each with a massive number (01, 02, 03) and short text. Numbers are accent-colored, oversized. Items have a 1px bottom border.

**CSS:**
```css
.wfl-wrap { display:flex; flex-direction:column; width:100%; padding:48px; gap:0; }
.wfl-item { display:flex; align-items:baseline; gap:24px; padding:24px 0; border-bottom:1px solid rgba(255,255,255,0.06); }
.wfl-num { font-size:clamp(40px, 7cqw, 72px); font-weight:900; line-height:1; color:var(--accent); opacity:0.4; width:80px; flex-shrink:0; }
.wfl-text { font-size:clamp(16px, 2.5cqw, 20px); font-weight:600; }
```

**Best beat:** `solution`, `step`
**Required:** `items[]` (3-4 strings)
**Why it works:** The oversized numbers create a visual rhythm down the slide. The accent color draws the eye to the sequence. The bottom borders create structure without heaviness.

---

#### NEW 17: `slide-angled-text`
**Visual:** The entire content block is rotated 15-20 degrees. Text follows the angle. A single geo layer (diagonal stripe or ribbon) reinforces the angle. Everything else is clean.

**CSS:**
```css
.at-wrap { display:flex; align-items:center; justify-content:center; width:100%; height:100%; overflow:hidden; }
.at-content { transform:rotate(-15deg); max-width:70%; }
.at-headline { font-size:clamp(32px, 6cqw, 56px); font-weight:900; line-height:1.0; }
```

**Best beat:** `hook`, `break`, `shock`
**Required:** `headline`, opt: `body`
**Why it works:** Angled text breaks the "everything is horizontal" pattern. Creates dynamic energy. Best used as a single "surprise" slide in a carousel, not every slide.

---

#### NEW 18: `slide-minimal-card-stack`
**Visual:** 2-3 cards stacked with slight vertical offset (each card is 10px lower than the one above). Each card has a thin left border in a different color. Cards have no background — just border + text. 

**CSS:**
```css
.mcs-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%; height:100%; gap:16px; padding:48px; }
.mcs-card { width:85%; padding:24px 32px; border-left:2px solid var(--accent); }
.mcs-card:nth-child(2) { margin-left:20px; border-left-color:rgba(255,255,255,0.3); }
.mcs-card:nth-child(3) { margin-left:40px; border-left-color:rgba(255,255,255,0.15); }
.mcs-title { font-size:18px; font-weight:700; margin-bottom:6px; }
.mcs-desc { font-size:13px; font-weight:300; opacity:0.6; }
```

**Best beat:** `solution`, `tip`, `data`
**Required:** `cards[]` (2-3 of `{title, description}`)
**Why it works:** The staggered offset creates depth without 3D transforms. The thin left border is structural, not decorative. Feels like a wireframe that became the design.

---

#### NEW 19: `slide-logo-wall`
**Visual:** A grid of 6-9 brand/client logos (rendered as text or simple SVG shapes), with a central headline above. Logos are low-opacity, headline is high-contrast. "Trusted by" social proof.

**CSS:**
```css
.lw-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%; height:100%; padding:48px; gap:32px; }
.lw-headline { font-size:14px; letter-spacing:0.2em; text-transform:uppercase; opacity:0.5; }
.lw-grid { display:grid; grid-template-columns:repeat(3, 1fr); gap:32px; width:80%; }
.lw-logo { height:40px; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:700; opacity:0.25; }
```

**Best beat:** `proof`, `testimonial`
**Required:** `headline` (e.g., "Trusted by"), `logos[]` (6-9 strings)
**Why it works:** Social proof through association. The low-opacity logos say "we have many clients" without competing with the headline.

---

#### NEW 20: `slide-receipt`
**Visual:** A white-background card (even on dark systems) centered on the slide, styled like a store receipt — dashed top/bottom borders, monospace font, line items with prices/values on the right. A "total" row at the bottom with a thick top border.

**CSS:**
```css
.rcpt-wrap { display:flex; align-items:center; justify-content:center; width:100%; height:100%; padding:48px; }
.rcpt-paper { width:75%; max-width:600px; background:#fff; color:#111; padding:36px; font-family:var(--font-mono); font-size:12px; line-height:2; }
.rcpt-line { display:flex; justify-content:space-between; border-bottom:1px dashed #ccc; padding:4px 0; }
.rcpt-total { border-top:2px solid #111; border-bottom:none; font-weight:700; font-size:14px; margin-top:8px; padding-top:8px; }
```

**Best beat:** `data`, `diagnostic`, `proof`
**Required:** `items[]` (4-6 of `{label, value}`), opt: `total`
**Why it works:** The receipt format makes data feel tangible. "Here's what you got." The white paper on dark background creates a natural focal point. Unexpected format = memorable.

---

#### NEW 21: `slide-polaroid-grid`
**Visual:** 2-3 polaroid-style cards arranged in a loose grid. Each has a thick white border, a small caption below, and a slight random rotation (-3° to +3°). Background is a solid warm color. No geo layers.

**CSS:**
```css
.pg-wrap { display:flex; align-items:center; justify-content:center; gap:24px; width:100%; height:100%; padding:48px; }
.pg-card { background:#fff; padding:12px 12px 48px 12px; box-shadow:0 4px 20px rgba(0,0,0,0.3); width:40%; }
.pg-card:nth-child(1) { transform:rotate(-3deg); }
.pg-card:nth-child(2) { transform:rotate(2deg); margin-top:30px; }
.pg-img { width:100%; aspect-ratio:1/1; background:linear-gradient(135deg, #333, #111); }
.pg-caption { font-size:12px; color:#333; margin-top:12px; font-family:var(--font-mono); }
```

**Best beat:** `proof`, `testimonial`, `break`
**Required:** `cards[]` (2-3 of `{caption, color_gradient}`)
**Why it works:** The polaroid format is nostalgic and tactile. The slight rotations break the grid. This is a "personality" slide — not for every carousel, but unforgettable when used.

---

#### NEW 22: `slide-tag-cloud`
**Visual:** 8-12 words of varying sizes scattered across the slide. Each word is a different size based on importance. Words use the accent color at varying opacities. No traditional headline — the cloud IS the message.

**CSS:**
```css
.tc-wrap { position:relative; width:100%; height:100%; padding:48px; }
.tc-word { position:absolute; font-weight:700; white-space:nowrap; }
.tc-word-1 { font-size:48px; top:15%; left:10%; opacity:1; }
.tc-word-2 { font-size:36px; top:30%; left:50%; opacity:0.8; }
.tc-word-3 { font-size:24px; top:55%; left:15%; opacity:0.6; }
/* etc — positions and sizes distributed across canvas */
```

**Best beat:** `hook`, `data`, `break`
**Required:** `words[]` (8-12 of `{text, size, x, y, opacity}`)
**Why it works:** A tag cloud forces the viewer to explore the slide, not just scan it. The varying sizes create a visual hierarchy without a traditional structure. Best for "mood" or "brand values" slides.

---

#### NEW 23: `slide-morse-code`
**Visual:** A message encoded as dots and dashes (SVG circles and rectangles) arranged horizontally. Below: the decoded text in small type. Background is pure dark with a single scan-line geo layer.

**CSS:**
```css
.mc-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%; height:100%; gap:24px; }
.mc-code { display:flex; align-items:center; gap:8px; font-size:0; }
.mc-dot { width:8px; height:8px; background:var(--accent); border-radius:50%; display:inline-block; }
.mc-dash { width:24px; height:8px; background:var(--accent); display:inline-block; }
.mc-gap { width:16px; }
.mc-word-gap { width:32px; }
.mc-text { font-size:11px; letter-spacing:0.2em; text-transform:uppercase; opacity:0.5; }
```

**Best beat:** `hook`, `shock`, `break`
**Required:** `message`, opt: `decoded_text`
**Why it works:** Forces the viewer to pause and decode. Creates a "secret message" feeling. The reveal (decoded text below) provides satisfaction. Pure engagement play.

---

#### NEW 24: `slide-scroll-code`
**Visual:** A code block styled like a GitHub README or Stack Overflow answer. Syntax highlighting (accent color for keywords, muted for comments). A small "copy" icon in the corner. Clean, technical, credible.

**CSS:**
```css
.sc-wrap { display:flex; flex-direction:column; width:100%; height:100%; padding:48px; }
.sc-header { display:flex; align-items:center; gap:8px; margin-bottom:16px; font-size:11px; opacity:0.5; }
.sc-lang-dot { width:10px; height:10px; border-radius:50%; background:var(--accent); }
.sc-block { background:rgba(0,0,0,0.4); border-radius:8px; padding:24px; font-family:var(--font-mono); font-size:13px; line-height:1.8; overflow:hidden; }
.sc-keyword { color:var(--accent); }
.sc-comment { opacity:0.4; font-style:italic; }
.sc-string { color:rgba(255,255,255,0.8); }
```

**Best beat:** `solution`, `diagnostic`, `proof`
**Required:** `code_lines[]` (strings), `language` (e.g., "python")
**Why it works:** Code is the native language of technical audiences. Syntax highlighting signals "we understand your world." The block format is familiar and trusted.

---

### LAYOUT SUMMARY

| # | ID | Category | Best Beat |
|---|-----|----------|-----------|
| 1 | `slide-hook-lockup` | Lockup | hook |
| 2 | `slide-massive-number` | Data | data, shock |
| 3 | `slide-terminal` | Diagnostic | diagnostic |
| 4 | `slide-terminal-fullscreen` | Diagnostic | diagnostic, shock |
| 5 | `slide-tip-blocks` | Solution | solution |
| 6 | `slide-before-after` | Diagnostic | diagnostic |
| 7 | `slide-icon-grid` | Solution | solution |
| 8 | `slide-badge-grid` | Solution | solution |
| 9 | `slide-cta` | CTA | cta |
| 10 | `slide-pull-quote` | Testimonial | testimonial |
| 11 | `slide-step-flow` | Solution | solution |
| 12 | `slide-list-numbered` | Solution | solution |
| 13 | `slide-waterfall-list` | Solution | solution |
| 14 | `slide-bento-grid` | Data | data |
| 15 | `slide-comparison-table` | Diagnostic | diagnostic |
| 16 | `slide-editorial-column` | Editorial | proof |
| 17 | `slide-faq-stack` | Solution | solution |
| 18 | `slide-timeline` | Solution | solution |
| 19 | `slide-stat-row` | Data | data |
| 20 | `slide-progress-bars` | Data | data |
| 21 | `slide-data-viz-donut` | Data | data |
| 22 | `slide-data-wall` | Data | data, proof |
| 23 | `slide-typeset-poster` | Break | break |
| 24 | `slide-myth-vs-fact` | Myth/Reality | myth, reality |
| 25 | `slide-full-bleed-type` | Impact | silence, hook |
| 26 | `slide-diagonal-split` | Editorial | shock, data |
| 27 | `slide-asymmetric-lockup` | Editorial | hook, silence |
| 28 | `slide-type-over-shape` | Impact | hook, proof |
| 29 | `slide-stacked-type` | Impact | hook, shock |
| 30 | `slide-corner-manifesto` | Editorial | silence, break |
| 31 | `slide-side-by-side` | Data | data, diagnostic |
| 32 | `slide-frame-within-frame` | Editorial | testimonial |
| 33 | `slide-contrast-knockout` | Impact | shock, hook |
| 34 | `slide-circular-quote` | Testimonial | testimonial |
| 35 | `slide-minimal-card-stack` | Solution | solution |
| 36 | `slide-logo-wall` | Proof | proof |
| 37 | `slide-receipt` | Data | data, proof |
| 38 | `slide-polaroid-grid` | Break | testimonial, break |
| 39 | `slide-tag-cloud` | Impact | hook, data |
| 40 | `slide-morse-code` | Impact | hook, shock |
| 41 | `slide-scroll-code` | Solution | solution, proof |
| 42 | `slide-angled-text` | Impact | hook, break |

**42 layouts total.** Organized into 6 categories: Lockup, Data, Diagnostic, Solution, CTA, Editorial, Impact, Testimonial, Break.

---

## PART 4: SYSTEM PERSONALITY ENFORCEMENT

Current problem: Claude picks a system, then treats it like every other system. s07 BRUTALIST should feel like a punk zine. s35 ART DECO should feel like a luxury invitation. Right now they both get the same layout approach.

### Personality Rules Per System Family

#### BRUTALIST (s07, s25, s31)
- **Type:** Black weight (900), negative tracking (-0.05em), all caps for display
- **Padding:** Minimal — 24px-32px, not 64px. Elements should feel crammed, not spacious.
- **Decoratives:** `grid-bg` only. No blobs, no starbursts, no organic shapes.
- **Preferred layouts:** `slide-full-bleed-type`, `slide-stacked-type`, `slide-contrast-knockout`, `slide-corner-manifesto`
- **Forbidden:** Soft curves, warm colors, rounded corners, pastel tones
- **Feel:** This should look like someone yelled the message onto the slide.

#### CYBERPUNK (s29, s40)
- **Type:** Monospace for everything. `JetBrains Mono` or system monospace.
- **Decoratives:** `pw-grid`, `scan-lines`, `geo-circuit-trace`.
- **Preferred layouts:** `slide-terminal-fullscreen`, `slide-terminal`, `slide-data-wall`, `slide-morse-code`, `slide-scroll-code`
- **Color usage:** Accent color at 100% opacity, not faded. Neon = bright.
- **Feel:** You hacked into a system and found this message.

#### ART DECO (s35)
- **Type:** `Cinzel Decorative` for display, `Cormorant` for body. Serif elegance.
- **Decoratives:** `ornament-tr`, `corner-frame`, `chrome-badge-stamp`.
- **Preferred layouts:** `slide-frame-within-frame`, `slide-circular-quote`, `slide-editorial-column`
- **Geometry:** Symmetry is key. Centered compositions, balanced weight.
- **Feel:** A 1920s luxury brand manifesto.

#### LIGHT / EDITORIAL (s05, s18, s19, s23, s26, s39, s47, s48)
- **Type:** Light backgrounds, dark text. Generous whitespace (80px+ padding).
- **Decoratives:** Minimal. `diag-band` or `chrome-header-bar` only.
- **Preferred layouts:** `slide-asymmetric-lockup`, `slide-editorial-column`, `slide-frame-within-frame`, `slide-typeset-poster`
- **Feel:** Kinfolk magazine. Breathing room is the design.

#### DARK / PREMIUM (s01, s13, s42, s43)
- **Type:** High contrast. White/cream on black. Gold or silver accents.
- **Decoratives:** `glow-orb`, `vol-light`, `geo-starfield`.
- **Preferred layouts:** `slide-full-bleed-type`, `slide-massive-number`, `slide-side-by-side`
- **Feel:** A nightclub menu. A luxury watch catalog. Expensive.

#### WARM / LATAM (s10, s11, s12, s24, s36, s38)
- **Type:** Rounded sans (Nunito, DM Sans). Warm accent colors.
- **Decoratives:** `blob-bg`, `vol-light`, `ornament-bl`.
- **Preferred layouts:** `slide-polaroid-grid`, `slide-hook-lockup`, `slide-step-flow`
- **Feel:** Friendly, energetic, not corporate. Like a coffee shop poster.

---

## PART 5: 6 COMPOSITION PRINCIPLES (The "How")

These are the rules every slide should follow, regardless of layout. They separate agency work from commercial.

### Principle 1: The 3-Second Rule
A viewer should understand the slide's message in 3 seconds without reading body text. The headline + visual hierarchy must communicate intent immediately. Body text is for the 10% who pause.

**Implementation:** Headline must be the largest, highest-contrast element. Nothing competes with it for attention.

### Principle 2: One Hero Element Per Slide
Every slide has ONE thing that dominates. Everything else supports it. The hero could be:
- A massive headline (`slide-full-bleed-type`)
- A huge number (`slide-massive-number`)
- A dramatic shape (`slide-type-over-shape`)
- A color block split (`slide-contrast-knockout`)

**Implementation:** If two elements feel like they're competing for attention, reduce one. Always.

### Principle 3: Asymmetry Creates Energy
Perfect symmetry is boring. Agency work is always slightly off-center. Text blocks aligned left (not center). Shapes placed at 30/70 (not 50/50). The starburst in the corner, not centered.

**Implementation:** Default to left-aligned text, not center. Place the blob at bottom-right (not center). Use 40/60 splits, not 50/50.

### Principle 4: Tight + Loose Rhythm
Don't use the same spacing everywhere. Alternate tight and loose:
- Tight: headline sits close to the kicker above it (4px gap)
- Loose: big gap between the headline block and the body text (32px gap)
- Tight: body lines close together (line-height 1.4)
- Loose: massive bottom padding before the footer

**Implementation:** Use a spacing scale: 4px, 8px, 16px, 32px, 64px, 96px. Never use the same gap twice in a row.

### Principle 5: Typography IS Decoration
Don't add decorative elements to compensate for boring type. Make the type itself the decoration:
- Display text with text-stroke treatment
- A massive number at 0.15 opacity as background texture
- A label tracked out to 0.25em creating a visual line
- Line breaks in headlines creating typographic shapes

**Implementation:** Before adding a starburst or blob, ask: "Can I achieve the same visual interest with type alone?" If yes, skip the decorative.

### Principle 6: The "Off" Detail
Every great design has one thing that's slightly "wrong" — it creates tension:
- A word that breaks across a line awkwardly (but intentionally)
- An element that bleeds 5% off the canvas edge
- A color used exactly once (not repeated)
- Text at a 15° angle while everything else is straight

**Implementation:** In each carousel, one slide should have an "off" detail. The `slide-angled-text` is built for this. Or a `slide-full-bleed-type` with a word intentionally broken across lines.

---

## PART 6: ANTI-PATTERNS TO AVOID

These are the specific things that make carousels look "Canva" instead of "agency":

1. **Center-aligned everything.** Center alignment is the default of non-designers. Left-align headlines, right-align metadata, center only the hero element.

2. **Rounded-corner cards on dark backgrounds.** Sharp corners look more intentional. Rounded = friendly = generic. Use `border-radius: 0` or `2px` max on dark systems.

3. **The same padding on every side.** 48px all around = template. Try 64px left, 32px top, 80px bottom. Asymmetric padding creates visual interest.

4. **Decorative blobs in the same position every time.** Bottom-right corner blob on every slide = pattern = boring. Alternate: top-left, center-edge, behind text, bleeding off-canvas.

5. **Headlines that read like SEO titles.** "5 Tips for Better Resumes" = Canva. "Your resume is invisible." = agency. One is information, the other is provocation.

6. **Body text wider than 40 characters.** Long lines = hard to read = looks like a document, not a design. Max-width body text at 36ch.

7. **The same accent color usage pattern.** "Accent for headlines, white for body" = template. Sometimes use accent for the kicker only. Sometimes use accent as the background. Sometimes use accent at 0.2 opacity for a subtle wash.

8. **No slide feels "risky."** If every slide is safe and balanced, the carousel is forgettable. One slide should feel like it might not work — that's the one people remember.

---

## PART 7: EXPORT PIPELINE HARDENING — Production Blockers

**These bugs destroy output quality regardless of how good the layouts are.**

After reviewing Claude's actual output (2 carousels, 10 slides), these 5 issues must be fixed BEFORE adding new layouts.

---

### Bug 1: LIGHT SYSTEMS ARE INVISIBLE IN EXPORT (P0)

**What happens:** When using light systems (s05, s18, s19, s23, s26, s39, s47, s48), the exported PNG loses all subtle elements:
- SVG blobs at low opacity vanish
- Grain texture disappears
- Accent color at < 0.5 opacity becomes invisible
- Background gradient flattens to near-white

**Evidence:** Carousel 2 (light/purple system) — the purple blob is completely invisible. The 87% number has no visual backing. Everything looks washed out.

**Root cause:** html2canvas flattens `mix-blend-mode` and renders low-opacity elements as invisible on light backgrounds.

**Fix:**
```css
/* Light systems: double all opacity values */
.light-system .slide::before { opacity: calc(var(--grain-opacity) * 2); } /* 0.05 -> 0.10 */
.light-system .blob-bg { opacity: 0.25; } /* instead of 0.12 */
.light-system .geo-layer { opacity: calc(var(--geo-opacity) * 2); } /* 0.10 -> 0.20 */
.light-system .starburst { opacity: 0.6; } /* instead of 0.30 */

/* Light systems: force stronger accent saturation */
.light-system { --accent-saturation-boost: 1.3; }
```

**Also:** Light system backgrounds must never be pure white. Use `#f0ede8` (warm), `#eaeef5` (cool), or `#f5f0eb` (neutral) — a tinted off-white creates warmth and prevents the "hospital" look.

---

### Bug 2: TERMINAL MUST ALWAYS BE DARK (P0)

**What happens:** On light systems, `slide-terminal` gets a gray body background instead of the dark terminal look. It looks like a generic card, not a terminal.

**Evidence:** Carousel 2 S3 — terminal body is medium gray with colored text. Not credible.

**Fix:** Force terminal to always use dark background regardless of system:
```css
.term-body {
  background: #0d0d12 !important; /* Always dark, never inherit system bg */
  border: 1px solid rgba(255,255,255,0.08);
  color: #e0e0e0;
}
```

The terminal chrome (red/yellow/green dots) and the dark body are part of the terminal's identity — they should NOT adapt to the system. The contrast between a light system slide and the dark terminal window is a FEATURE, not a bug.

---

### Bug 3: TEXT CUTOFF IN EXPORT (P0)

**What happens:** Headlines get clipped at the edges. Characters on the left or right are cut off.

**Evidence:** Carousel 2 S1 — "s ven tu LinkedIn ant" instead of the full headline. Characters are missing from both sides.

**Root cause:** One of:
- `overflow: hidden` on a parent container that's exactly the text width
- Negative `letter-spacing` pushing characters outside the bounding box
- Export pipeline (html2canvas) measuring text width differently than browser
- Container `padding` not accounting for large display text

**Fix:**
```css
/* Add safe margin for display text */
.display-headline {
  margin-left: -0.02em; /* Pull back slightly */
  margin-right: 0.1em; /* Prevent right-edge clipping */
  overflow: visible !important; /* Never clip headlines */
}

/* Ensure parent containers don't clip */
.slide-content-wrap {
  overflow: visible;
  padding-left: 8px; /* Extra buffer for export */
  padding-right: 8px;
}
```

**Also add to preflight:** Check #15 — "Text Edge Safety": verify no text within 8px of slide edge when `overflow: hidden` is present.

---

### Bug 4: RAW JSON IN CARD TEMPLATES (P0)

**What happens:** Template dumps the raw Python dictionary instead of extracting title/description fields.

**Evidence:** Carousel 2 S4 — cards show `{'title': 'Foto profesional', 'desc': 'Fondo neutro, buena luz, sin filtros.'}` instead of rendering the fields.

**Root cause:** Template uses string interpolation (`{{ item }}`) instead of property access (`{{ item.title }}`).

**Fix for template:**
```html
<!-- WRONG -->
<div class="card">{{ item }}</div>

<!-- RIGHT -->
<div class="card">
  <span class="card-title">{{ item.title }}</span>
  <span class="card-desc">{{ item.desc }}</span>
</div>
```

**Also add to preflight:** Check #16 — "Template Artifact Detection": scan output for `{'` (dict literal) or `{{` (unrendered template syntax). FAIL if found.

---

### Bug 5: DECORATIVE REPETITION (P1)

**What happens:** Same decorative elements appear on every slide — corner-frame brackets on S1, S2, S3, S4. Same starburst position. Same blob placement.

**Evidence:** Carousel 1 — corner-frame brackets appear on 4/5 slides. Starburst is always bottom-left.

**Fix — Per-Slide Decorative Rotation:**
```python
# In render_carousel.py — rotate decoratives across slides
DECORATIVE_ROTATION = {
    0: ["corner-frame", "ornament-tr"],      # Slide 1: corners + starburst TR
    1: ["watermark"],                          # Slide 2: watermark only (silence beat)
    2: ["chrome-badge-stamp"],                 # Slide 3: stamp only
    3: ["sub-stamp-circle", "ornament-bl"],    # Slide 4: stamp BL + starburst BL
    4: ["chrome-vertical-counter"],            # Slide 5: side text
}
```

**Rule:** No decorative may appear on more than 2 consecutive slides. Maximum 2 decoratives per slide. Silence beat = 0 decoratives.

---

### Bug 6: BODY TEXT TOO LARGE (P1)

**What happens:** Body text is 16-17px, display is 48px. Ratio is only 3:1. Need 4-5:1 for real hierarchy tension.

**Evidence:** Both carousels — body text reads at the same visual weight as sub-headlines. No clear information hierarchy.

**Fix:**
```css
/* Force body text smaller */
.slide-body {
  font-size: clamp(13px, 2.2cqw, 15px); /* Was 16-17px */
  font-weight: 300; /* Light weight for contrast with bold display */
  line-height: 1.5; /* Was 1.6 — tighter for shorter lines */
  max-width: 36ch; /* Force line breaks, prevent wall-of-text */
}
```

**Also:** Sub-headlines should be 20-24px (not 28-32px) to create a proper 3-step staircase: 64px → 22px → 14px.

---

## PART 8: IMPLEMENTATION PRIORITY FOR CLAUDE

### Phase 1: Typography Overhaul (Highest Impact)
1. Update `carousel-shell.html` with the 5-tier type system
2. Add system-family-specific type personality rules to `render_carousel.py`
3. Fix `slide-big-number` → `slide-massive-number` with opacity background treatment
4. Enforce `line-height: 0.85-0.95` for display headlines

### Phase 2: New Layouts (Add 20+)
1. Build the 24 new layouts as slide templates
2. Merge deprecated layouts (`slide-checklist` → `slide-icon-grid`, etc.)
3. Update `carousel-master-ref.md` with new layout table
4. Update preflight to recognize new layouts

### Phase 3: System Personality Enforcement
1. Add personality rules per family to `carousel-master-ref.md`
2. Update `render_carousel.py` to read system family and apply preferred layout weights
3. Add "forbidden" layout checks per family
4. Update geo layer defaults per family

### Phase 4: Composition Rules
1. Add the 6 principles to `carousel-master-ref.md`
2. Update preflight with composition checks (asymmetry score, hero element detection)
3. Add anti-pattern detection to preflight

### Phase 5: Export Pipeline Hardening + Bug Fixes
**These are production-blockers. Every carousel that exports must match the browser view.**

1. Terminal always uses dark bg regardless of system family
2. Fix text cutoff bug (clipped headlines in export)
3. Fix raw JSON in card templates (S4 bug)
4. Light system contrast 2x boost for export visibility
5. Reduce body text to 14px for type hierarchy
6. SVG blob repositioning per slide (not always bottom-right)

### Phase 6: Viewer App Fix
1. Fix the slide navigation in the viewer app (current bug: blank slides after first)

---

## SUMMARY

**The B+ → A jump requires 4 things:**
1. **Typography with real tension** — massive display vs tiny body, 3-5x size ratio
2. **42 layouts with genuine structural diversity** — not 24 variations of the same thing
3. **System personality enforcement** — each family gets its own visual language
4. **Intentional composition** — asymmetric balance, one hero element, tight/loose rhythm

**The moat deepens with each addition.** Anyone can copy the code. Nobody can copy the encoded design decisions — which layouts work for which beats, which type ratios create tension, which system families prefer which compositions.

This is now a **design system**, not just a template engine. The difference is that a template applies rules. A design system makes decisions.
