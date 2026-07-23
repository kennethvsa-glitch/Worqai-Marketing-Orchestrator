# Feedback Request — Carousel Generation Skill System (Iteration 6)

## What this system is

A **Claude Code skill system** — a set of markdown files that Claude reads at runtime using its built-in Read tool to execute a structured workflow. Not a traditional software application. No API, no backend, no database, no queue. One operator types a request, Claude reads the skill files, follows the pipeline step by step, and outputs a complete self-contained HTML file.

**Output:** 1080×1080px Instagram/Facebook carousel — 8 slides, agency-level visual design, used for marketing content for two brands: WorqAI (AI resume builder SaaS) and Profile Pro LATAM (done-for-you CV/LinkedIn service). Generated on demand, ~5-20 per week manually.

**Hard constraint on your feedback:** All improvements must be implementable as changes to markdown files that Claude reads at runtime. No Python backends, no APIs, no databases, no infrastructure. The only exception is a one-time offline Python script run manually (not part of the Claude pipeline). This constraint is non-negotiable — don't recommend FastAPI, Redis, Celery, or Pydantic backends.

---

## Full file architecture

```
html-carousel-builder/
  SKILL.md              ← entry point: inputs, routing, REGEN_MODE, visual continuity rules
  workflow.md           ← 9-step execution pipeline (main file)
  anti-slop.md          ← 4 fatal design signals, quality checklist, 5-gate Ship Gate
  layouts.md            ← 15 slide layout components + selection guide
  css-effects.md        ← visual effects, CSS patterns, Midjourney/image prompts
  copy-dna.md           ← DEPRECATED (kept as reference only)
  hooks/
    voice-core.md       ← shared: brand voice DNA, stat policy, CTA formula, proof rules (always loaded)
    hook-result.md      ← loaded only when hook_type = result
    hook-question.md    ← loaded only when hook_type = question
    hook-contrarian.md  ← loaded only when hook_type = contrarian
    hook-curiosity.md   ← loaded only when hook_type = curiosity
    hook-negative.md    ← loaded only when hook_type = negative
    hook-identity.md    ← loaded only when hook_type = identity/confession
    hook-reframe.md     ← loaded only when hook_type = reframe/warning
    hook-transformation.md
    hook-authority-borrow.md
    hook-specificity.md
    hook-confession.md
    hook-warning.md

design-systems/
  SKILL.md              ← selection guide: 48 systems with vibe descriptions only
  selection-intelligence.md  ← selection matrix, 9 archetypes, Style DNA
  tokens/
    typography.md             ← font pairings, Google Fonts CDN URLs (loaded on demand)
    system_01_noir_gold.md    ← full CSS tokens for System 01 only (~35 lines)
    system_02_royal_blue.md   ← full CSS tokens for System 02 only
    ...                       ← one file per system
    system_48_bright_boutique_editorial.md
  blobs-textures.md
  geometry-modules.md
  continuity-engine.md
```

**Key architectural principle:** Claude loads only what it needs at each step via the Read tool. It does not load all files at once. Per-generation context load has been reduced significantly through two rounds of file splitting:
- Design tokens: from ~800 lines (monolithic) → ~35 lines (one system file)
- Copy DNA: from full file → `voice-core.md` (~65% of content, always loaded) + one hook file (~5% of content, hook-specific)

---

## Inputs the user provides

```
1. Topic / copy      — what problem this carousel addresses
2. Style system      — which of 48 systems (or Claude selects from matrix)
3. Slide count       — default 8
4. Language          — default Spanish CR/LATAM
5. Brand handle      — default "@worqai"
6. Hook type         — result / question / contrarian / curiosity / negative / identity / reframe / transformation / authority-borrow / specificity
7. source_facts      — (optional) verified stat + source for Slide 2
                       Format: "75% de los CVs no pasan el ATS. Fuente: LinkedIn Talent Report 2025"
                       If not provided → Slide 2 auto-converts to Myth vs Reality. No exceptions.
8. proof_case        — (optional) real client result for Slide 7
                       Format: "Cliente de Heredia, 4 entrevistas en 8 días tras reescribir el headline"
                       If not provided → Slide 7 uses myth vs reality format. No invented specifics.
```

---

## Full execution pipeline (current state — 5 iterations complete)

### Step 1 — Customer Moment Brief
Internal paragraph: who is the viewer, what they feel right now (specific), what shift this carousel promises. Never shown to user. Vague brief = slop output.

### Step 2 — Slide Count + Hook Type Decision
Selected from a table of 11 hook types paired with slide counts. Stated before any copy is written.

### Step 3 — Write All Copy First
Load `hooks/voice-core.md` + `hooks/hook-[type].md`. Write all slides before any design work.

**Hard rules on copy:**
- Slide 2 (DATA): only uses a stat explicitly provided in `source_facts`. If empty → auto-converts to Myth vs Reality. Stat used verbatim — no rounding, no paraphrasing. Source attribution always included on slide.
- Slide 7 (PROOF): only uses a case explicitly provided in `proof_case`. If empty → myth vs reality format. Never invent city, number, timeframe, or quote.

**BANNED phrases without `source_facts` provided:**
- "la mayoría", "muchos", "casi todos", "la gran mayoría"
- Any percentage without a named source
- Comparative claims without data ("más rápido", "mejor que", "más efectivo")
- Attribution language ("según expertos", "estudios muestran", "los reclutadores dicen")

### Step 3.6 — Retention Gate
S2 must name the gap opened in S1. S3 must open with the tip directly (no setup language).

### Step 4 — Select Design System
Load `design-systems/SKILL.md` (vibe descriptions only, ~156 lines). Run selection matrix. Brand overrides are hard: WorqAI → System 17 always.

### Step 4.5 — Fetch System Tokens
Read only the matching per-system token file (`design-systems/tokens/system_NN_name.md`). Do NOT load monolithic token files. ~35 lines loaded instead of ~800.

### Step 4.6 — Continuity Setup
Only when GEO geometry modules are active. Declares `content_safe_zone` before any HTML.

### Step 4.8 — Content Spec Hard Gate (Phase 1 — must complete before any HTML)

Claude outputs this JSON block and passes 5 gates before proceeding:

```json
{
  "system_selected": "[ID] · [NAME]",
  "hook_type": "[type]",
  "copy_language": "es-LATAM",
  "slide_count": 8,
  "source_facts_provided": false,
  "proof_case_provided": false,
  "slides": [
    { "slide": 1, "layout": "Poster Lockup", "headline": "...", "headline_word_count": 6 },
    { "slide": 2, "layout": "Myth vs Reality", "copy": "..." },
    { "slide": 3, "layout": "Error Card", "label": "ERROR 1 / 4", "headline": "...", "problem": "...", "fix": "..." },
    { "slide": 4, "layout": "Error Card", "label": "ERROR 2 / 4", "headline": "...", "problem": "...", "fix": "..." },
    { "slide": 5, "layout": "Pull Quote", "quote": "..." },
    { "slide": 6, "layout": "Error Card", "label": "ERROR 3 / 4", "headline": "...", "problem": "...", "fix": "..." },
    { "slide": 7, "layout": "Proof Card", "city": "...", "result": "..." },
    { "slide": 8, "layout": "CTA", "question": "...", "keyword": "...", "reward": "..." }
  ]
}
```

**5 hard gates — all must pass before HTML:**
1. Slide 2 uses `source_facts_provided: true` data OR is Myth vs Reality
2. Slide 7 uses `proof_case_provided: true` data OR uses generic myth format
3. At least one slide has a different layout than the others
4. Slide 1 `headline_word_count` integer is ≤ 8
5. `copy_language` matches the language the user requested

### Step 4.9 — Layout Map Assert
Claude outputs one line before any HTML:
```
LAYOUT MAP: [S1 layout] → [S2 layout] → [S3] → [S4] → [S5] → [S6] → [S7] → [S8]
```
Two checks:
- No two adjacent slides share the exact same layout
- At least one visual rest slide exists (Pull Quote, Myth vs Reality, Big Number — not Error Card)

### Step 5 — Build HTML
⚠ Generate as if there is no anti-slop sweep. The sweep is a confirm pass only — not a correction phase. Everything must be correct on the first pass.

All VAR_* tokens replaced with literal values from the fetched system token file. Light-system chrome override applied for cream/white backgrounds. Deco-num suppressed on all systems except documented exceptions.

### Steps 6–7 — Anti-Slop Sweep + Quality Checklist

**4 Fatal Design Signals (hard failures):**
1. Colored left-border cards (`border-left: 3px solid`)
2. Large decorative background numbers (`.deco-num` at low opacity) — except System 07
3. Badge/pill labels (border-radius:999px)
4. 100% identical slide structure

**Quality checklist covers:** design (gradients, blob continuity, typography ratio, progress dots), copy (banned words, word counts, narrative arc), mobile render sanity (14px floor at 380px viewport), accessibility/contrast (WCAG AA).

### Ship Gate — 5 Binary Checks (replaces old taste score)
All five must be TRUE before HTML is delivered:
1. **Layout break:** At least one non-standard layout (Pull Quote, Big Number, Two-Column, Before/After)
2. **Continuity:** Exact same blob SVG path on all slides (only rotation/translation changes)
3. **Anti-Canva:** Zero colored left-border cards, zero pill badges
4. **VAR_* clean:** Zero instances of the string `VAR_` anywhere in the output HTML
5. **CTA complete:** Slide 8 has all three — question + keyword to DM + reward copy

### Step 8 — Delivery
State: system used, blob used, font used, hook type.

---

## REGEN_MODE — Partial Regeneration
When user asks to fix a specific slide only:
1. Re-emit ContentSpec JSON for affected slides only
2. Re-run hard gates for those slides
3. Step 4.8 gates apply to every HTML output, full or partial

```json
{ "regen_mode": true, "slides": [{ "slide": 3, "layout": "...", "headline": "..." }] }
```

---

## What changed across the last 2 iterations (for context)

**Iteration 4:**
- Taste score (5×5 self-grading) → replaced with 3 binary Ship Gate checks
- `source_facts` input added — no stat = no stat slide
- `proof_case` input added — no proof = myth format only
- ContentSpec JSON phase (Step 4.8) — structured output before HTML
- 49 per-system token files created (one per system + typography)

**Iteration 5:**
- Ship Gate expanded from 3 → 5 checks (added VAR_* clean + CTA completeness)
- Soft stats ban added to Step 3 (banned phrase list)
- Fake authority ban added ("según expertos", "estudios muestran" without source)
- Verbatim number rule added (copy stat exactly, never round)
- `copy_language` + `headline_word_count` integer added to ContentSpec JSON
- Layout Map Assert added (Step 4.9) — adjacency check before HTML
- "Generate as if no sweep" directive added to Step 5
- REGEN_MODE defined for partial slide regeneration
- copy-dna.md split into 13 hook files — 75-80% context reduction per copy step

---

## Specific questions for iteration 6

Answer each one. Stay within the Claude Code skill file architecture.

**1. Pipeline sequencing — is the step order optimal?**
The current order is: Brief → Hook type → Copy → System selection → Token fetch → Continuity → ContentSpec gate → Layout map → HTML. Is there a sequencing problem — a step that depends on information from a later step, or that should happen earlier to prevent wasted work? What would you reorder and why?

**2. The banned phrases list in Step 3 — what's still missing?**
We blocked "la mayoría", "muchos", percentages without source, "según expertos". What categories of soft or implied claims can still slip through this filter and mislead readers? Give specific examples in Spanish.

**3. Layout Map Assert (Step 4.9) — is the adjacent-layout check strong enough?**
Currently checks: no two adjacent slides share the same layout, at least one visual rest slide exists. A carousel with layouts [Hook → Myth → Error → Error → Error → Error → Proof → CTA] technically passes both checks (adjacency OK, Myth = visual rest) but has four consecutive Error Cards which is visually monotonous. How would you strengthen this check while keeping it as a simple markdown rule?

**4. The ContentSpec JSON — what does it still not catch?**
The schema now includes: system, hook type, language, slide count, source facts flag, proof flag, per-slide layout, headline, word count, problem/fix fields, CTA fields. What structural or content failure mode is still invisible at the JSON stage that only becomes apparent after HTML is generated?

**5. The `voice-core.md` split — new risk introduced?**
By separating shared voice rules from hook-specific frameworks, we created a dependency: Claude must load both files before writing copy. What breaks if Claude loads the hook file but skips `voice-core.md`? Is there a guard we're missing?

**6. Anything the last two iterations broke or weakened?**
Each change that added enforcement also added complexity. Is there a gate or rule added in iterations 4–5 that is contradictory, redundant with another rule, or likely to produce false positives that block legitimate carousels?

---

## Hard constraint reminder

All answers must be implementable as changes to markdown files Claude reads at runtime. No Python services, no databases, no infrastructure. One-time offline Python utilities (run manually, not in the Claude pipeline) are acceptable if the problem genuinely requires code.
