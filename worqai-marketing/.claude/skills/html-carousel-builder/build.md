---
name: html-carousel-builder build
load: once per build, after tokens.md
---

# BUILD FILE — Layouts, Voice, Copy, Anti-Slop

---

## PRE-BUILD PLAN GATE (MANDATORY — runs before Step 2 of workflow)

Before writing any JSON spec, declare this block in chat. If building multiple carousels, one block per carousel. If any two blocks read the same, fix the plan before proceeding.

```
CAROUSEL [N]:
  Topic: [one sentence]
  System: s## [NAME] · Background: #hex · Accent: #hex
  System family: [dark | light | warm | brutalist | cyberpunk]
  Fonts: [display font] / [body font] — must be two different typefaces
  Layers S1: [layer1, layer2]  Layers S2: [layer1, layer2]  etc.
  Decoratives: [list of IDs per slide, e.g. "S1: corner-frame, S3: watermark:3×, S4: sub-stamp-circle:GRATIS"]
  Hook type: [hook pattern from build.md]
  Visual signature: [one sentence: "Dark cyberpunk scan lines + circuit traces + Space Grotesk / Inter, neon green"]
```

**Batch diversity law:** When building ≥2 carousels in one session, each MUST use a different system family (dark / light / warm / brutalist / cyberpunk). Not just a different number — a different visual mood. A reviewer must be able to tell at a glance that they came from different design worlds.

**Font law:** `--font-display` and `--font-body` must never be the same typeface. If you're writing both as Nunito or both as Inter, stop and pick a second family.

**Decorative law:** Every carousel must invoke ≥2 decorative elements total across its slides. Zero decoratives = instant fail at the Ship Gate.

---

## BUILD MODES

### Bespoke (Default for all builds)
- Do NOT use L01-L07 templates below for copy-paste. They are reference only.
- Every slide gets custom HTML/CSS with `.s1-`, `.s2-` prefixed class names.
- Minimum 3 techniques per slide from `techniques.md` (geo + type + depth).
- Fixed 1080px canvas, not responsive `clamp()` values.
- Reference the REFERENCE CAROUSEL INDEX above. Start with `carousel_portfolio_07_cyberpunk.html` for base structure, then layer techniques from the elite references.

### Template (Deprecated — rapid prototyping only)
- Use L01-L07 layouts below only when user explicitly says "quick prototype" or "draft."
- Copy `templates/carousel-shell.html`, replace `VAR_*` placeholders.
- This mode exists for speed, not quality. Not for production work.

---

## ELITE QUALITY BAR

The minimum acceptable standard for any production carousel:
- **Directed rhythm, not layer count.** Every carousel must have a TENSION → SILENCE → IMPACT → RELEASE arc. No slide uses all available techniques.
- **File size:** 35–55 KB = ideal. 55+ KB = bloat warning — audit for removal candidates.
- **Fonts:** 3–4 typefaces per carousel (display + body + accent + optional script)
- **Technique budget:** Max 4 layers per slide (background + 1 geo + 1 type effect + 1 accent). Elite = *intentional restraint*, not maxxing every slider.
- **Decorative budget:** Max 2 per slide, but at least ONE slide must have ZERO decorative elements (silence beat).
- **Mock UI:** At least one slide shows a simulated interface (terminal, CV mock, checklist)
- **Absolute positioning:** Editorial layouts use absolute positioning, but NEVER place absolute elements in the central text zone (clipping risk).
- **Multi-layer backgrounds:** 2–4 layers max (gradient + geo + optional grain). Do not stack glow + grain + geo + scan lines + zoom rings on the same slide.
- **Bespoke CSS:** Every slide has `.sN-*` prefixed custom classes
- **Fixed canvas:** 1080px viewer, not responsive `max-width`
- **Subtraction rule:** Before shipping, remove 25% of decorative elements. If the slide still works, keep them removed.
- **Reference:** See REFERENCE CAROUSEL INDEX below

If your carousel is under 35 KB, it is too generic. Rebuild from scratch.
If your carousel is over 55 KB, it is over-decorated. Run the Subtraction Gate.

---

## REFERENCE CAROUSEL INDEX

Study these files before building. They demonstrate what elite looks like in practice.

| File | System | Techniques Demonstrated | File Size |
|------|--------|------------------------|-----------|
| `carousel_consejo-cv-esta-mal_brutalist.html` | s07 Brutalist | Manifesto stack, terminal, warning box, ranked list, proof+CTA grid | ~65 KB |
| `carousel_0-a-4-entrevistas_crimson.html` | s04 Crimson | Big number with from-to, pull quote avatar, counter stack, case study card | ~70 KB |
| `carousel_pdf-ats-error_worqai-verde.html` | s17 WorqAI Verde | Warning icon, mock UI, terminal, checklist, before/after + CTA | ~60 KB |
| `carousel_amby-cr-demo_agency-pain.html` | s48 Bright Boutique | Editorial split, pull quote frame, editorial index, script flourish | ~55 KB |
| `carousel_aura-cr-demo_services.html` | s25 Swiss Brut Accent | Giant lockup, editorial index, corner frames, ticker | ~55 KB |
| `carousel_portfolio_04.html` | Custom | Glassmorphism, stat cards, testimonial cascade, service pillars | ~70 KB |

**What separates elite from good:**
- Multi-font systems (3–4 fonts, never fewer than 3)
- Mock UI components (CV lines, terminal bars, checkboxes — shows instead of tells)
- Absolute positioning for editorial layouts (magazine-style, not just flexbox)
- Decorative elements (ornaments ✦✧, stamps, watermarks, corner frames)
- Slide-specific layout innovation (no two slides share the same structure)

**Use these references in this order:**
1. `carousel_portfolio_07_cyberpunk.html` — base structure, nav, zip export, quality baseline
2. `carousel_amby-cr-demo_agency-pain.html` — editorial layouts, absolute positioning, script fonts
3. `carousel_aura-cr-demo_services.html` — typography mixing, ticker, corner frames
4. `carousel_portfolio_04.html` — glassmorphism, stat cards, testimonial cascade
5. `carousel_0-a-4-entrevistas_crimson.html` — counter stack, case study card, avatar rows
6. `carousel_consejo-cv-esta-mal_brutalist.html` — manifesto density, terminal styling, ranked lists

---

## COMPONENT LIBRARY

Components live in `.claude/skills/html-carousel-builder/components/`. They are **starter blocks**, not rigid templates. Copy them into the carousel, then customize with `.sN-*` prefixed CSS.

**When to use components:**
- Every carousel starts from `shell-base.html`
- Pick 1 layer component per slide (minimum)
- Pick 1 slide layout component per slide
- Pick 0–2 decorative components per slide (at least one slide must have ZERO)
- Pick 1 mock-UI component for at least one slide
- Then **customize everything** with bespoke `.sN-*` CSS

**Directory structure:**
```
components/
  layers/          — 60 background effects (geo-grids, organic, light, textures, patterns, atmospheric, geometric)
  slides/          — 60 layout patterns (hooks, data, tips, proof, CTA, breaks)
  decorative/      — 30 flourishes (ornaments, frames, badges, type-accents, chrome)
  mock-ui/         — 30 interface simulations (terminals, CVs, apps, code, forms, data, messaging, e-commerce, icons)
  shell-base.html  — complete HTML wrapper
  _INDEX.md        — searchable index of all 180 components
  _VARIABLES.md    — CSS variable contract mapped to 48 systems
```

**Rules for component use:**
1. Always copy — never link or import components directly.
2. Always customize — add `.sN-*` prefixed overrides for positioning, sizing, and special effects.
3. Components use CSS variables only (`--accent`, `--text-primary`, etc.). No hardcoded colors.
4. File size target is 35–55 KB. Components get you to 35 KB; bespoke CSS gets you to 45–55 KB. Over 55 KB = audit for bloat.

---

## LAYOUT LIBRARY

Pick 3–4 layouts max per carousel. Never use the same layout twice in a row.

### Core Layouts (used 90% of the time)

**L01 · POSTER LOCKUP** — Slide 1 hook only
- Large headline (max 8 words), centered or left-aligned
- One-line intensifier below (max 15 words)
- Swipe pill bottom-right
- No blocks, no badges. Pure type + background.

**L02 · BIG NUMBER + ANNOTATION** — Slide 2 data
- Oversized stat number (clamp 90–138px)
- 2-line context below
- Source tag bottom-left
- No blocks. The number IS the design.

**L03 · STANDARD ERROR/TIP** — Slides 3–6
- Label: "ERROR N / M" uppercase, tracking 0.2em, accent color
- Headline: max 8 words, weight 700+
- Problem block: tinted bg (block_bad_bg), 3 lines max
- Fix block: tinted bg (block_good_bg), 3 lines max
- Progress dots bottom, active dot = accent

**L04 · TERMINAL BLOCK** — Rhythm break slide
- Monospace font (JetBrains Mono / Roboto Mono)
- Syntax-highlighted code or command-style text
- Dark panel with border-left accent (4px)
- Use for: tech tips, CLI commands, system messages

**L05 · PULL QUOTE CENTERED** — Rhythm break slide
- One sentence, emotionally resonant or contrarian
- Large quote marks or no marks (system dependent)
- Centered, generous padding
- No label, no blocks. The quote IS the slide.

**L06 · SIDE-BY-SIDE COMPARISON** — Myth vs Reality, Before/After
- Left column: "ANTES" / "MITO" — strikethrough or muted
- Right column: "DESPUÉS" / "REALIDAD" — accent highlight
- Divider: 1px line or gap
- No badge, no pill. The comparison IS the structure.

**L07 · CTA CARD** — Slide 8 (always)
- One question (max 10 words)
- One keyword to DM (single word, uppercase, dashed border)
- One reward line (specific deliverable)
- Different treatment from all other slides

### Specialty Layouts (use once per carousel max)

**L08 · BENTO GRID** — 2×2 or 3-cell grid for multi-item slides
**L09 · CHECKLIST PANEL** — Numbered items with check/× icons
**L10 · RANKED LIST** — Large numbers + headlines + 1-line body
**L11 · WARNING/ALERT BOX** — Red-tinted panel with urgent copy
**L12 · CHAT BUBBLES** — Conversation-style, two speakers
**L13 · PRODUCT UI FRAME** — Browser or app mockup with content inside

### Layout Selection Guide

| Slide job | Best layout | Avoid |
|-----------|-------------|-------|
| Hook (S1) | L01 Poster Lockup | L08 Bento, L09 Checklist |
| Data (S2, single stat) | L02 Big Number | L08 Bento |
| Error/Tip (S3–S6) | L03 Standard | L08 Bento, L02 Big Number |
| Rhythm break | L04 Terminal, L05 Pull Quote, L06 Comparison | L03 Standard |
| Myth vs Reality | L06 Comparison | L02 Big Number |
| Tool/Resource list | L09 Checklist, L10 Ranked List | L05 Pull Quote |
| Proof (S7) | L05 Pull Quote, L12 Chat Bubbles | L08 Bento, L04 Terminal |
| CTA (S8) | L07 CTA Card | L03 Standard |

---

## LAYOUT HTML TEMPLATES

Copy the template for the chosen layout. Replace `{placeholders}` with actual content. Every template includes `.brand` and `.counter` — never omit them.

---

## ⚠️ DEPRECATED REFERENCE — L01-L07 TEMPLATES

**Do NOT copy-paste these templates into production carousels.** They exist as layout pattern reference only.

For production work, build bespoke CSS per slide (`.s1-*`, `.s2-*` prefixes) with 3+ techniques from `techniques.md`. See `carousel_portfolio_07_cyberpunk.html` for the correct approach.

---

### L01 · POSTER LOCKUP (Slide 1 only)

```html
<div class="slide">
  <div class="deco-num">{N}</div>
  <div class="display">{headline, max 8 words}</div>
  <div class="body-text">{intensifier, max 15 words}</div>
  <div class="swipe-pill">Desliza →</div>
  <div class="brand">{handle}</div>
  <div class="counter">{N} / {total}</div>
</div>
```

**Rules:** `.deco-num` suppressed by default via global CSS. Enable only for documented exception systems. `.swipe-pill` = S1 ONLY.

---

### L02 · BIG NUMBER + ANNOTATION (Slide 2, data)

```html
<div class="slide">
  <div class="deco-num">{N}</div>
  <div class="stat-num">{stat_number}</div>
  <div class="body-text">{2-line context below stat}</div>
  <div class="body-text" style="margin-top:8px;opacity:0.6;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;">{source_tag}</div>
  <div class="brand">{handle}</div>
  <div class="counter">{N} / {total}</div>
</div>
```

**Rules:** No blocks. No labels. The number IS the design. Source tag = small, muted, uppercase.

---

### L03 · STANDARD ERROR/TIP (Slides 3–6)

```html
<div class="slide">
  <div class="deco-num">{N}</div>
  <div class="label">{LABEL} {N} / {M}</div>
  <div class="headline">{headline, max 8 words}</div>
  <div class="blk bad">
    <div class="blk-lbl">PROBLEMA</div>
    <div class="blk-txt">{what reader is doing wrong, max 12 words}</div>
  </div>
  <div class="blk good">
    <div class="blk-lbl">SOLUCIÓN</div>
    <div class="blk-txt">{exact action to take, max 14 words}</div>
  </div>
  <div class="prog">
    <!-- Repeat <span class="pd"> for each tip total ({M}); apply .on to active tip {N} -->
    <span class="pd on">01</span>
    <span class="pd">02</span>
    <span class="pd">03</span>
    <span class="pd">04</span>
  </div>
  <div class="brand">{handle}</div>
  <div class="counter">{N} / {total}</div>
</div>
```

**Rules:** Number of `.pd` spans = total tips. Active tip = `.on`. `.deco-num` suppressed by default. Enable only for documented exception systems.

---

### L04 · TERMINAL BLOCK (Rhythm break)

```html
<div class="slide">
  <div class="deco-num">{N}</div>
  <div class="label">{optional label}</div>
  <div class="headline">{headline, max 8 words}</div>
  <div class="terminal-panel">
    <div class="cmd">$ {command_line_1}</div>
    <div class="ok">✓ {success_line_1}</div>
    <div class="ok">✓ {success_line_2}</div>
  </div>
  <div class="brand">{handle}</div>
  <div class="counter">{N} / {total}</div>
</div>
```

**Rules:** Monospace font. Syntax colors: pink (#ff6b9d) commands, cyan (#4ecdc4) success. No `.swipe-pill`. No `.prog`.

**Required CSS:**
```css
.terminal-panel {
  background: rgba(0,0,0,0.45);
  border: 1px solid rgba(VAR_ACCENT,0.3);
  border-radius: 12px;
  padding: 20px;
  font-family: 'JetBrains Mono', monospace;
  margin-top: 16px;
}
.cmd { color: #ff6b9d; }
.ok { color: #4ecdc4; margin-top: 8px; }
.ok + .ok { margin-top: 4px; }
```

---

### L05 · PULL QUOTE CENTERED (Rhythm break, proof)

```html
<div class="slide" style="justify-content:center;align-items:center;text-align:center;">
  <div class="deco-num">{N}</div>
  <div class="quote-mark">"</div>
  <div class="headline" style="margin-top:-20px;">{one sentence, emotionally resonant or contrarian, max 12 words}</div>
  <div class="body-text" style="margin-top:16px;opacity:0.7;">— {attribution}</div>
  <div class="brand">{handle}</div>
  <div class="counter">{N} / {total}</div>
</div>
```

**Rules:** Centered. One sentence only. No label, no blocks. Quote mark = decorative, opacity 0.15.

**Required CSS:**
```css
.quote-mark {
  font-size: clamp(60px, 10vw, 90px);
  color: VAR_ACCENT;
  opacity: 0.15;
  line-height: 1;
}
```

---

### L06 · SIDE-BY-SIDE COMPARISON (Myth vs Reality, Before/After)

```html
<div class="slide">
  <div class="deco-num">{N}</div>
  <div class="label">{LABEL}</div>
  <div class="headline">{headline, max 8 words}</div>
  <div class="comparison-row">
    <div class="comparison-col-left">
      <div class="blk-lbl" style="text-decoration:line-through;">ANTES / MITO</div>
      <div class="body-text">{old way / myth, max 10 words}</div>
    </div>
    <div class="comparison-col-right">
      <div class="blk-lbl comparison-right-label">DESPUÉS / REALIDAD</div>
      <div class="body-text comparison-right-text">{new way / reality, max 10 words}</div>
    </div>
  </div>
  <div class="brand">{handle}</div>
  <div class="counter">{N} / {total}</div>
</div>
```

**Rules:** Left = muted, strikethrough. Right = accent, primary text. Divider = `border-right` on left column. No separate divider div. No badge, no pill.

**Required CSS:**
```css
.comparison-row {
  display: flex;
  gap: 0;
  margin-top: 20px;
}
.comparison-col-left {
  flex: 1;
  opacity: 0.5;
  border-right: 1px solid rgba(255,255,255,0.1);
  padding-right: 16px;
}
.comparison-col-right {
  flex: 1;
  padding-left: 16px;
}
.comparison-right-label {
  color: VAR_ACCENT;
}
.comparison-right-text {
  color: VAR_TEXT_PRIMARY;
  font-weight: 500;
}
```

---

### L07 · CTA CARD (Slide 8, always)

```html
<div class="slide" style="justify-content:center;">
  <div class="deco-num">{N}</div>
  <div class="headline" style="text-align:center;">{question, max 10 words}</div>
  <div style="margin-top:32px;text-align:center;">
    <div class="keyword-box">
      <span class="keyword-text">{KEYWORD}</span>
    </div>
  </div>
  <div class="body-text" style="text-align:center;margin-top:20px;opacity:0.8;">{reward line, specific deliverable}</div>
  <div class="brand">{handle}</div>
  <div class="counter">{N} / {total}</div>
</div>
```

**Rules:** Different treatment from ALL other slides. Keyword = ONE word, uppercase, dashed border. No swipe-pill. No progress dots. No blocks.

**Required CSS:**
```css
.keyword-box {
  display: inline-block;
  border: 2px dashed VAR_ACCENT;
  padding: 12px 24px;
  border-radius: 8px;
}
.keyword-text {
  font-size: clamp(24px, 4vw, 36px);
  font-weight: 900;
  color: VAR_ACCENT;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
```

---

## HOOK TYPES — COLLAPSED TO 3 NARRATIVE PATTERNS

### Pattern A: Gap → Amplify → Close
**Hooks:** Curiosity, Question, Result
**Logic:** Open an information gap on S1. Amplify stakes on S2. Close the gap piece by piece on S3–S6.
**S1 form:** Incomplete statement, ellipsis, fragment. "Hay una línea en tu CV que decide todo…"
**S2 role:** Makes stakes higher. NOT the answer. "Why this matters."
**S3–S6 role:** Close the loop piece by piece.
**Proof:** Before/after of the specific element named in the loop.

### Pattern B: Loss → Mechanism → Fix
**Hooks:** Negative, Warning, Contrarian
**Logic:** Lead with a loss on S1. Explain the exact mechanism on S2. Begin pivot on S3.
**S1 form:** Specific loss, not vague. "El 75% de CVs se eliminan antes de ser leídos."
**S2 role:** Concrete mechanism. "Here's exactly how you're losing."
**S3 role:** Pivot — "No es que no sepás trabajar. Es que el sistema filtra antes."
**S4–S6 role:** One concrete fix per slide. Action-oriented.
**Proof:** Someone who stopped the loss. Emotional relief after tension.

### Pattern C: Reframe → New Lens → Action
**Hooks:** Identity, Confession, Transformation, Reframe, Authority Borrow
**Logic:** Reframe the reader's understanding on S1. Give them new vocabulary on S2–S3. Show action on S4–S6.
**S1 form:** "No es X. Es Y." or "Si mandás CVs y no oís nada, no es tu culpa."
**S2 role:** Name the specific behavior that causes the pain.
**S3 role:** The reframe: "it's not about X, it's about Y."
**S4–S6 role:** Action under the new frame.
**Proof:** Transformation story with specific before/after.

### Hook × Slide Count

| Hook | Pattern | Ideal slides | Max |
|------|---------|-------------|-----|
| Identity | C | 4–5 | 6 |
| Confession | C | 4–5 | 6 |
| Transformation | C | 4–6 | 7 |
| Reframe | C | 5–6 | 7 |
| Authority Borrow | C | 5–7 | 8 |
| Result | A | 6–8 | 8 |
| Warning | B | 5–7 | 8 |
| Contrarian | B | 6–8 | 8 |
| Curiosity | A | 6–8 | 8 |
| Negative | B | 7–8 | 8 |
| Specificity | A | 7–8 | 8 |
| Question | A | 6–8 | 8 |

---

## VOICE DNA

### WorqAI (locked)
```json
{
  "brand": "WorqAI",
  "register": "peer",
  "sentence_length": "short",
  "humor": "dry",
  "tone": ["directo", "concreto", "sin formalidad", "anti-corporate"],
  "signatures": ["'No es X. Es Y.' pivots", "Specific number leads", "Short imperative closers"],
  "forbidden": ["¿Sabías que...?", "En la era digital", "potenciá tu carrera", "lleva tu CV al siguiente nivel", "transforma tu búsqueda", "todos los profesionales"],
  "treatment": "tú (default), vos (CR-only Reels)",
  "metaphor": "tools/workshop, gym/training — never magic/unlock/journey"
}
```

### Profile Pro LATAM (locked)
```json
{
  "brand": "Profile Pro LATAM",
  "register": "coach",
  "sentence_length": "medium",
  "humor": "warm",
  "tone": ["profesional", "cercano", "específico", "consultivo"],
  "signatures": ["Mirror client's tratamiento", "Concrete client-result openers", "Short 'lo que cambió:' closers"],
  "forbidden": ["transforma tu carrera", "desbloqueá oportunidades", "potenciá tu perfil", "el éxito está a un clic"],
  "treatment": "mirror client",
  "metaphor": "consulting/diagnosis, craft/tailoring — never warfare/conquest"
}
```

---

## COPY FRAMEWORKS

### Slide 1 — HOOK
- Max 8 words headline, weight 700+, no filler
- One-line intensifier (max 15 words)
- Swipe pill bottom-right: "Desliza →"
- Nothing else on the slide

### Slide 2 — DATA
**Stat hierarchy (pick in order):**
1. Counterintuitive stat — "75% de CVs nunca los lee un humano"
2. Aspiration stat — "Profesionales con CV optimizado reciben 3× más entrevistas"
3. Problem-magnitude stat — "El postulante promedio en LATAM aplica a 87 vacantes sin respuesta"

**Source policy — ZERO TOLERANCE for fabricated citations:**

A fabricated source destroys trust permanently. If a follower googles the citation and finds nothing, you lose credibility forever.

**VERIFIED SOURCE ALLOW-LIST (use ONLY these):**
- `Jobscan internal analysis 2025` — generic ATS stat fallback
- `WorqAI database 2025` — internal platform data
- `LinkedIn Economic Graph` — ONLY if citing the real published report by that name
- `World Economic Forum · Future of Jobs Report` — ONLY the real published edition
- `— Análisis interno Profile Pro LATAM` — original observations, no external claim

**DEFAULT fallback for ANY unverified stat:** `Dato interno WorqAI · base de datos 2025`

**NEVER use these fabricated phrases:**
- ❌ "LinkedIn Talent Report 2025" — this report does not exist with this name
- ❌ "LinkedIn Talent Solutions Report 2024" — fabricated title
- ❌ "Jobscan ATS Report 2024" — fabricated title
- ❌ "Jobscan ATS Optimization Report 2024" — fabricated title
- ❌ "Jobscan · State of the Job Search 2023" — fabricated title
- ❌ Any year-specific report title unless it is in the ALLOW-LIST above

**If the user provides `source_facts`:** Use exactly what they provided. Do not embellish the source name.

**If no `source_facts` are provided:** Use `Dato interno WorqAI · base de datos 2025` or `— Análisis interno Profile Pro LATAM`. Do NOT invent a source.

**Mandatory HTML comment:** Any slide containing a stat with an external source must include `<!-- STAT_REVIEW_REQUIRED -->` immediately after the source tag.

**BANNED without source_facts:** "la mayoría", "muchos", "casi todos", "el 80% de…", "más rápido", "mejor que", "según expertos", "estudios muestran"

### Slides 3–6 — ERROR/TIP
Three lines, never four:
```
PROBLEM     → What the reader is doing wrong (max 12 words, present tense)
CONSEQUENCE → What it costs them (max 10 words, concrete loss)
FIX         → The exact action to take (max 14 words, imperative verb first)
```

### Slide 7 — PROOF
**Specificity ladder:**
1. City + Number + Timeframe + Mechanism + Quote
   "Cliente de Heredia. 4 entrevistas en 8 días después de rescribir el headline LinkedIn. 'No esperaba el cambio tan rápido.' — María, contadora."
2. City + Number + Timeframe (no quote)
   "Cliente de Bogotá pasó de 0 a 3 callbacks en 2 semanas."
3. Number + Timeframe (no city)
   "Un cliente recibió 5 entrevistas en 10 días."

Never invent a proof. If none exists, use Myth vs Reality on S7.

### Slide 8 — CTA
Formula: verb + keyword + reward
```
GOOD: "Escribime CV y te mando el template ATS gratis."
BAD:  "Escribime para más info."
```
Keyword must be ONE single word. Reward must be ONE specific deliverable.

---

## ANTI-SLOP — FATAL SIGNALS

1. **Colored left-border cards** — ⛔ `border-left: 3px solid VAR_ACCENT`. Use tinted bg fill or full-border card instead.
2. **Large decorative background numbers** — ⛔ `deco-num` at opacity 0.05–0.08. Replace with SVG blob or radial glow.
3. **Pill badges at top** — ⛔ `border-radius:999px; border:1px solid ACCENT`. Use plain uppercase label with tracking only.
4. **100% identical slide structure** — ⛔ Every slide = same badge + headline + 2 blocks. Break rhythm minimum once.

**Exceptions (documented only):**
- s07 BRUTALIST: deco-nums at opacity 0.10
- s25 SWISS BRUT ACCENT: border-left rules permitted
- s19 SWISS GRID BRUT: visible grid lines permitted

## SHIP GATE — 13 Binary Checks

Before delivering, verify ALL:
- [ ] **Directed rhythm:** Carousel has at least one "silence" slide (≤2 layers, zero decorative elements)
- [ ] **Technique budget:** No slide exceeds 4 techniques. At least one slide uses ≤2.
- [ ] **Subtraction gate:** 25% of decorative elements removed without breaking any slide
- [ ] **Layout break:** At least one slide uses a non-standard layout (not L03 Standard)
- [ ] **Continuity:** Same blob/path across all slides (only rotation/translation changes)
- [ ] **Anti-Canva:** Zero colored left-border cards. Zero pill badges.
- [ ] **VAR clean:** Zero `VAR_` strings anywhere in output
- [ ] **CTA complete:** S8 has question + single keyword + reward
- [ ] **File size:** 35–55 KB ideal. If >55 KB, list 3 removal candidates.
- [ ] **Mock UI:** At least one slide contains a simulated interface (terminal, CV mock, checklist)
- [ ] **html2canvas safe:** No `conic-gradient()`. `backdrop-filter` has `-webkit-` fallback and passed export test.
- [ ] **Decoratives:** ≥2 decorative elements invoked total across the carousel (stamps, corner frames, ornaments, watermarks, chrome elements). ZERO is an auto-fail.
- [ ] **Font contrast:** `--font-display` and `--font-body` are different typefaces. Two fonts that are the same family at different weights do NOT count.

All TRUE → deliver. Any FALSE → fix that section, re-check.

---

## PLATFORM DELTAS

| Platform | Aspect | Body min | Safe zones (top/bottom) | Copy notes |
|----------|--------|----------|------------------------|------------|
| Instagram feed (mobile) | 4:5 (1080×1350) | 17px | 80px / 140px | Hook ≤8 words, swipe pill |
| Instagram square | 1:1 (1080×1080) | 16px | 80px / 140px | Same as 4:5 |
| Instagram Stories | 9:16 (1080×1920) | 24px | 180px / 220px | One thought per slide |
| Facebook feed | 1:1 (1080×1080) | 16px | 60px / 120px | Slightly more body text OK |
| LinkedIn doc post | 1:1 or PDF | 18px | 100px / 140px | More formal, no slang |
| TikTok carousel | 4:5 forced | 22px | 100px / 200px | Confrontational hook |

Default: Instagram 4:5.

## LOCALIZATION

| Locale | Treatment | Slang | Example |
|--------|-----------|-------|---------|
| es-CR | tuteo (vos optional) | "diay", "pura vida", "mae" | "Mandá tu CV así" |
| es-MX | tú | "neta", "chido", "rollo" | "Esto sí jala" |
| es-CO | tú/usted mirror | "parce", "berraco", "chévere" | "Esto le sirve, parce" |
| es-AR | vos | "che", "posta" | "Probalo, posta funciona" |
| es-CL | tú | "po", "cachái", "fome" | "Esto te sirve, cachái?" |
| es-LATAM-neutral | tú | None | Default for cross-LATAM ads |

Default: es-LATAM-neutral (tuteo, no regional slang).
WorqAI Reels & Profile Pro LATAM: es-CR.

---

## ASPECT RATIO OVERRIDES

Apply in `<style>` after base CSS. Default shell is 1:1.

**4:5 (1080×1350):**
```css
.wrap { aspect-ratio: 4 / 5; }
.viewer { max-width: 432px; }
.display   { font-size: clamp(42px, 6.5vw, 68px); }
.headline  { font-size: clamp(30px, 5.2vw, 48px); }
.stat-num  { font-size: clamp(100px, 16vw, 150px); }
.body-text { font-size: clamp(14px, 2.5vw, 17px); }
.slide     { padding: 64px 56px; }
.slide::before { background-size: 180px 225px; }
```

**9:16 Stories (1080×1920):**
```css
.wrap { aspect-ratio: 9 / 16; }
.viewer { max-width: 320px; }
.display { font-size: clamp(48px, 7.5vw, 78px); }
.slide { padding-top: 180px; padding-bottom: 220px; }
```

## LIGHT SYSTEM UI CHROME

For cream/white background systems (s05, s18, s19, s23, s25, s26, s39, s47, s48):
Add `class="light-system"` to `<body>` or `<html>`. The shell already includes the chrome override rule.

## DECO-NUM SUPPRESSION

```css
.deco-num { display: none; }
```

Exceptions (set `display: block`):
- s07 BRUTALIST: opacity 0.10
- s25 SWISS BRUT ACCENT: opacity 0.85
- s31 NEOBRUT COLOR BLOCKS: opacity 0.90
- s32 MAXIMALIST COLLAGE: visible as collage element
- s44 ACADEMIC CHALKBOARD: opacity 0.40
- s46 BLUEPRINT SYSTEMS: visible as technical drawing reference

## DENSE-SLIDE CONTENT BUDGET

Available vertical space = 1080 − 96 (top) − 140 (bottom safe-zone) = 844px.

```
headline:    font-size 68px (NOT 78px for 3-line slides)
block pad:   24px 28px (NOT 32px 36px)
blk-text:    font-size 25px (NOT 30px)
why-row:     font-size 21px, margin-top 18px
inline margin-top between headline and blocks: 28–32px
```

## VISUAL CONTINUITY RULES

1. Same blob/path on every slide — only rotate/translate changes
2. Brand anchor locked — handle + counter identical position
3. Label style frozen — same font, weight, tracking, color
4. Gradient angle constant — do not change angle per slide
5. Background element always present — blob, glow, or texture
6. Progress dots always same position — only active dot shifts
7. Swipe pill on slide 1 only
8. Accent color used max 3× per slide — label, active dot, one highlight word
