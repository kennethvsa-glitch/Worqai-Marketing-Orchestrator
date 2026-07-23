# Feedback Request — Carousel Generation Skill System (Iteration 4)

## What this system is

This is a **Claude Code skill system** — a set of markdown files that Claude reads at runtime to execute a structured workflow. It is NOT a traditional software application. There is no API, no backend, no database, no queue. The operator (one person) types a request into Claude Code, Claude reads the skill files, follows the pipeline, and outputs a complete HTML file.

**What it produces:** Self-contained HTML carousel files (1080×1080px) for Instagram and Facebook — 8 slides, agency-level visual design, used for marketing content. Generated on demand, ~5-20 per week.

**Constraint on feedback:** Please give feedback ONLY on improvements that can be made within the Claude Code skill file architecture (markdown + Claude runtime). Do not recommend FastAPI, Redis, Celery, SQLite, Pydantic backends, or any infrastructure. Those are irrelevant at this scale and this use case. The only "code" in this system is markdown files that Claude reads.

---

## Architecture overview

```
html-carousel-builder/
  SKILL.md          ← entry point, inputs, routing rules
  workflow.md       ← 8-step pipeline (main execution file)
  copy-dna.md       ← copywriting frameworks, hook psychology, voice
  anti-slop.md      ← design quality gates, fatal signals, refusal conditions
  layouts.md        ← 15 slide layout components
  css-effects.md    ← visual effects, Midjourney prompts
  
design-systems/
  SKILL.md          ← system selection guide (48 systems, vibe descriptions only)
  selection-intelligence.md  ← selection matrix, archetypes, Style DNA
  tokens/
    typography.md              ← font pairings, Google Fonts CDN URLs
    system_01_noir_gold.md     ← CSS tokens for System 01 only
    system_02_royal_blue.md    ← CSS tokens for System 02 only
    ...
    system_48_bright_boutique_editorial.md   ← CSS tokens for System 48 only
  blobs-textures.md
  geometry-modules.md
  continuity-engine.md
```

Claude reads files using its Read tool. It loads only what it needs at each step — not all files at once.

---

## The execution pipeline (current state after 4 iterations)

When a user asks for a carousel, Claude follows these steps in order:

**Step 1** — Write an internal Customer Moment Brief (who is watching, what they feel, what shift this promises). Never shown to user.

**Step 2** — Decide slide count + hook type before generating anything.

**Step 3** — Write all slide copy BEFORE designing. Hard rules:
- Slide 2 (DATA): only uses a stat the user explicitly provided in `source_facts`. If none provided → automatically becomes Myth vs Reality slide. NEVER invent a stat or source.
- Slide 7 (PROOF): only uses a proof case the user explicitly provided in `proof_case`. If none → uses generic myth vs reality format. NEVER invent city, number, timeframe, or quote.

**Step 4** — Select one design system from 48 options using Selection Intelligence matrix.

**Step 4.5** — Read only the selected system's token file (`design-systems/tokens/system_NN_name.md`). Does NOT load the old monolithic files (systems-core.md, systems-extended-a.md, etc.) which contained all 48 systems at once. This was the biggest context reduction — from ~800 lines loaded to ~35 lines per generation.

**Step 4.6** — Continuity setup (only when GEO geometry modules are active).

**Step 4.8 — Content Spec Hard Gate (NEW):**
Claude must output this JSON block BEFORE writing any HTML. Four hard gates are checked. If any fail, that slide is fixed in the JSON before proceeding to HTML.

```json
{
  "system_selected": "[ID] · [NAME]",
  "hook_type": "[type]",
  "slide_count": 8,
  "source_facts_provided": true,
  "proof_case_provided": false,
  "slides": [
    { "slide": 1, "layout": "Poster Lockup", "headline": "..." },
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

Hard gates:
- [ ] Slide 2 uses `source_facts_provided: true` data OR is Myth vs Reality
- [ ] Slide 7 uses `proof_case_provided: true` data OR uses generic myth format
- [ ] At least one slide has a different layout than the others
- [ ] Slide 1 headline is 8 words or fewer

**Step 5** — Build the full HTML file using tokens fetched in Step 4.5. Replace all VAR_* placeholders with actual hex values from the system token file.

**Step 6-7** — Anti-slop sweep + quality checklist.

**Ship Gate (replacing the old Taste Score):**

```
SHIP GATE — Binary Check (no scoring, no self-grading)

Do not self-score. Run these three checks. If any is FALSE, rewrite that section only.

- [ ] Layout break: At least one slide uses a non-standard layout. True / False?
- [ ] Continuity: Exact same blob SVG path used across all slides. True / False?
- [ ] Anti-Canva: Zero colored left-border cards. Zero pill badges. True / False?

All three TRUE → output HTML. Any FALSE → fix that section only, then re-check.
```

**Step 8** — Deliver: state system used, blob used, font used, hook type.

---

## Inputs the user provides

```
1. Topic / copy — what problem this carousel addresses
2. Style system — which of 48 systems (or Claude selects)
3. Slide count — default 8
4. Language — default Spanish LATAM
5. Brand handle — default "@worqai"
6. Hook type — result / question / contrarian / curiosity / negative
7. source_facts (optional) — verified stat + source for Slide 2
   Format: "75% de los CVs no pasan el ATS. Fuente: LinkedIn Talent Report 2025"
   If not provided → Slide 2 auto-converts to Myth vs Reality
8. proof_case (optional) — real client result for Slide 7
   Format: "Cliente de Heredia, 4 entrevistas en 8 días tras reescribir el headline"
   If not provided → Slide 7 uses generic myth vs reality format
```

---

## What changed in iteration 4 (what was just implemented)

| Change | Where | What it does |
|---|---|---|
| Taste score removed | anti-slop.md | Replaced 5x5 subjective self-scoring with 3 binary True/False gates |
| Source-facts input added | SKILL.md + workflow.md | Forces Claude to use only user-provided stats; no stat = no stat slide |
| Proof-case input added | SKILL.md + workflow.md | Forces Claude to use only user-provided proof; no proof = myth format |
| ContentSpec JSON phase | workflow.md Step 4.8 | Claude outputs structured JSON + passes 4 gates BEFORE generating HTML |
| Per-system token files | design-systems/tokens/ (49 files) | Claude reads only the selected system (~35 lines) instead of the full 800-line monolithic file |

---

## What we want feedback on

Specific questions — please answer each one:

1. **ContentSpec JSON schema completeness.** Is the current schema missing any fields that would catch common failure modes before HTML generation? What fields would you add or remove?

2. **Hard gate coverage.** The current 3 binary gates in the Ship Gate check layout variation, blob continuity, and anti-Canva signals. What failure modes do these gates miss? What 1-2 additional binary checks would cover the most common remaining failure patterns?

3. **Source-facts enforcement holes.** The rule is: "if no user-provided stat, auto-convert Slide 2 to Myth vs Reality." Where can Claude still hallucinate or slip through this rule? How would you tighten it?

4. **ContentSpec → HTML transition.** Currently the JSON spec is generated, hard gates checked, then Claude generates full HTML in one pass. Is there a useful intermediate check between JSON approval and HTML delivery that would catch rendering-level issues before the full output?

5. **Context efficiency.** We reduced token load significantly with per-system files. What else in the pipeline still loads more context than necessary? Identify the highest remaining source of context bloat.

6. **Anything we haven't thought of.** What failure mode, edge case, or structural weakness in this pipeline would you flag that the above questions don't cover?

---

## Hard constraint on your answer

Stay within the Claude Code skill file architecture. All fixes must be implementable as changes to markdown files that Claude reads. No Python scripts, no APIs, no databases — unless a Python script is a one-time offline utility (e.g., a linter run manually after generation, not part of the Claude pipeline itself).
