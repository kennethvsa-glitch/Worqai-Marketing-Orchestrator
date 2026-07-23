# Changelog — Session ~2025-05-13

## What We Built or Changed

### Architecture Planning (Plan Mode)
- **Read and analyzed** `ideation/feedbackonarchitecture.md` (565 lines of feedback from Claude, Gemini, and ChatGPT).
- **Consensus reached**: the current monolithic AI-generated-HTML architecture is the root cause of probabilistic quality, visual bugs, token waste, and fabricated stats.
- **Target architecture defined**: 5-layer system separating GENERATION (AI creative director) from COMPOSITION (deterministic render engine).
  - L1: Frozen Infrastructure (parameterized component templates)
  - L2: Layout Composer (JSON spec output)
  - L3: Creative Director (AI outputs brief → JSON spec only)
  - L4: Deterministic Render Engine (`render_carousel.py`)
  - L5: Deterministic QA (bounding-box + stat validation)
- **Revised phase order agreed**:
  1. Phase 0: Fix stat fabrication (live credibility risk)
  2. Phase 1A: Spec schema + brief template (foundation)
  3. Phase 1B: Component curation + usage audit (parallel with 1A)
  4. Phase 2: Render engine + parameterized templates
  5. Phase 3: AI skill refactor (only after render engine exists)
  6. Phase 4: Deterministic QA v2

### Phase 0: Stat Fabrication Fix (Executed)
- **Modified** `.claude/skills/html-carousel-builder/build.md` — replaced the permissive "Source policy" (lines ~509–513) with a **ZERO TOLERANCE** policy:
  - Defined a verified source allow-list (Jobscan internal analysis, WorqAI database, LinkedIn Economic Graph, WEF Future of Jobs Report, internal analysis)
  - Listed explicitly banned fabricated phrases ("LinkedIn Talent Report 2025", "Jobscan ATS Report 2024", etc.)
  - Mandated `<!-- STAT_REVIEW_REQUIRED -->` HTML comment on any external source
  - Made the default fallback: `Dato interno WorqAI · base de datos 2025`
- **Modified** `.claude/skills/html-carousel-builder/workflow.md` — added "Stat source clean" as a binary check in the Ship Gate checklist.
- **Created** `scripts/stat_source_validator.py` — Python script that scans HTML for source tags, matches against verified allow-list, flags fabricated patterns, and exits non-zero if issues found.
- **Patched 14 production carousels** to remove fabricated/unverifiable stat citations:
  - `production/carousel_0-a-4-entrevistas_crimson.html`
  - `production/carousel_ats-te-elimino_cyberpunk.html`
  - `production/carousel_ats-latam_worqai-verde.html`
  - `production/carousel_consejo-cv-esta-mal_brutalist.html`
  - `production/carousel_cv-no-entrevistas_worqai.html`
  - `production/carousel_cv-silencio-reclutadores_glass.html`
  - `production/carousel_linkedin-fantasma_aurora.html`
  - `production/carousel_pdf-ats-error_worqai-verde.html`
  - `production/carousel_tu-cv-nunca-fue-leido_worqai.html`
  - `production/carousel_aplicar-usa-latam_worqai.html`
  - `production/carousel_ats-espanol-bombas_worqai.html`
  - `production/carousel_ats-data-dashboard_beyond-elite.html`
  - `production/carousel_negociacion-salarial_terra.html`
  - `production/carousel_cv-silencio-reclutadores_glass.html` (TheLadders attribution)

### Phase 1A: Spec Schema + Brief Template (Executed)
- **Created** `scripts/carousel-spec.schema.json` — formal JSON Schema for carousel specs:
  - `meta`: system, aspect, slides, brand, language, set, density
  - `pacing`: emotional arc array
  - `slides[]`: id, layout, layers, decoratives, mock_ui, copy slots (kicker, headline, body, stat_number, stat_context, source, command, output_lines, before/after items, quote, attribution, question, cta_keyword, reward, url, tips, items)
  - `constraints`: max_weight, technique_budget, decorative_budget, mock_ui_required, silence_slide_required, subtraction_gate, file_size_target_kb
- **Created** `scripts/brief-template.yaml` — Creative Director constraint layer:
  - Topic, angle, one_truth, transformation_promise
  - Audience (who, pain, desired_state)
  - Emotional arc, tone_register, forbidden phrases/framings/visuals
  - verified_stats array with source and verified flag
  - proof_case (name, location, result, mechanism)
  - Technical hints (system_hint, aspect_ratio, slides_count, brand)

### Phase 1B: Component Usage Audit (Started, Not Completed)
- Read the component index (`_INDEX.md`) to understand the 181-component inventory.
- Identified that a usage audit is needed to find the top 20% of components that drive 80% of production output before building the render engine.
- **Not yet completed**: actual scan of production HTML files to rank component usage.
- **Not yet completed**: curation of 12 validated visual language sets.

## What We Decided NOT to Do

- **Rejected Option B (Gradual Migration)**. The user explicitly agreed that incremental approaches create a hybrid mess — maintaining two pipelines simultaneously with no quality benefit during transition. Full pivot only.
- **Did NOT start building `render_carousel.py` before the spec schema and brief template were defined.** The user correctly noted that Phase 2 only works after validated inputs exist.
- **Did NOT start parameterizing components yet.** Waiting for the usage audit (Phase 1B) to identify the actual top 20 components used in production, rather than guessing.
- **Did NOT refactor the AI skill yet.** Phase 3 is explicitly gated behind Phase 2 (render engine must exist before AI can output specs for it).

## What Was Broken or Unfinished at the End

- **`scripts/stat_source_validator.py` could not be executed.** The Windows shell had no working Python (`python`, `py`, and `python3` were all blocked by Windows App Execution Alias). We relied on grep-based manual patching instead. The script exists but is unverified.
- **Phase 1B usage audit incomplete.** No component frequency data extracted from production HTMLs yet.
- **`component_sets.json` not created.** The 12 curated visual language sets are still conceptual.
- **`render_carousel.py` not started.** No deterministic assembly engine exists.
- **AI skill still outputs full HTML.** `SKILL.md` and `build.md` have updated stat rules but still instruct the AI to write bespoke CSS and HTML.
- **No bounding-box QA.** `preflight-v2.py` with render-time overflow detection does not exist.
- **The existing 60 production HTML files still use the old architecture.** They are static artifacts, not generated from specs.

## Files Read

| File | What It Contained |
|------|-------------------|
| `ideation/feedbackonarchitecture.md` | 565 lines of cross-model feedback. Claude, Gemini, and ChatGPT all converged on the same diagnosis: separate GENERATION from COMPOSITION. Detailed analysis of 4 carousels' bugs. Proposed 5-layer architecture. |
| `scripts/component_picker.py` | 271 lines. Smart component picker v2. Loads `component_data.json`, filters by system compatibility and conflicts, calculates visual weights, outputs text plans (not JSON). Supports `--system`, `--slides`, `--hook`, `--density`. |
| `scripts/component_data.json` | 4,618 lines. Systems CSS variable maps, system_types, layout_maps, text_budgets, component_contracts (visual_weight, best_for_systems, avoid_systems, conflicts_with, pairs_well_with). |
| `.claude/skills/html-carousel-builder/components/shell-base.html` | 216 lines. Complete HTML wrapper: preview cage, viewer, wrap, track, slide structure, controls, dots, zip button. Includes html2canvas + JSZip CDNs. CSS variables for theming. |
| `.claude/skills/html-carousel-builder/SKILL.md` | 61 lines. Top-level orchestration. Inputs, 3-tier build system (matrix → tokens → build → techniques), rules, workflow pointer. Version 7.0. |
| `.claude/skills/html-carousel-builder/build.md` | 670 lines. Elite quality bar, reference carousel index, component library rules, L01–L13 layout descriptions with HTML templates (deprecated for production), copy frameworks (hook, data, tips, proof, CTA), anti-slop rules, ship gate checklist. |
| `.claude/skills/html-carousel-builder/workflow.md` | 187 lines. 6-step process: Brief → System Pick → Copy → HTML Build → Subtraction Gate → Ship Gate. Aspect ratio notes, deco-num suppression, dense-slide budgets, visual continuity rules. |
| `.claude/skills/html-carousel-builder/components/_INDEX.md` | 132 lines. Full component inventory: 60 layers, 60 slides, 30 decorative, 30 mock-UI, 1 shell. Organized by category and subcategory with component IDs. |
| `production/carousel_*.html` (various) | ~14 individual files read around specific lines to identify and patch fabricated stat citations. Each is a self-contained 1080×1080 Instagram carousel with inline CSS and JS. |

## How the System Worked at That Time

When someone wanted a carousel, this is what actually happened:

1. **User request** → `build_orchestrator.py` suggested which skill files to load.
2. **Agent loaded** `SKILL.md` → `tokens.md` → `build.md` → optionally `techniques.md`.
3. **Agent wrote a brief**, picked a design system from 48 options, and wrote copy for all slides BEFORE designing.
4. **Agent copied** `components/shell-base.html` as the skeleton.
5. **Agent browsed** `_INDEX.md` (181 components) and manually picked per slide:
   - 1 background layer
   - 1 slide layout
   - 0–2 decorative elements
   - 1 mock-UI (for at least one slide)
6. **Agent wrote bespoke CSS** for every slide using `.sN-*` prefixed class names.
7. **Agent customized** all HTML inline — positioning, sizing, effects.
8. **Agent ran Subtraction Gate** (remove 25% of decorative elements).
9. **Agent ran Ship Gate** (14 binary checks: rhythm, technique budget, layout break, anti-Canva, VAR clean, CTA complete, file size, fonts, mock UI, html2canvas safety, etc.).
10. **Agent delivered** one complete `production/carousel_*.html` file.
11. **`preflight.py`** ran 10 heuristic checks (text overflow, file size, anti-slop, mock UI, CTA, html2canvas risks).
12. **`apply_tokens.py`** patched any remaining `VAR_` placeholders.
13. **`carousel_exporter.py`** (Playwright) generated ZIP if html2canvas failed.

**The AI did everything.** It was creative director, layout selector, copywriter, visual stylist, component picker, HTML assembler, and QA reviewer — all in one monolithic prompt. The model reinvented the CSS and layout system on every single run. There was no separation between generation and composition.

## Thinking

### Initial Analysis
The feedback file was unusually convergent — three different models (Claude, Gemini, ChatGPT) all diagnosed the same root cause: the AI had too many jobs. The counterintuitive insight was that reducing AI freedom would increase quality. This matched what I saw in the codebase: 181 components existed, but the AI still wrote bespoke CSS from scratch every time. The components were "starter blocks," not injectable templates.

### Plan Design Reasoning
I initially proposed two options (Full Pivot vs. Gradual Migration). The user rejected gradual migration because maintaining two pipelines is worse than a clean break. The user then provided a detailed revision emphasizing:
- Phase 0 MUST come first because fabricated stats are a live credibility risk.
- The brief template is non-negotiable — without it, the AI just moves chaos from HTML layer to JSON layer.
- Component curation (12 sets) should run parallel to spec design, not as cleanup at the end.
- The render engine must exist BEFORE the skill is refactored.

I revised the plan to reflect this exact sequencing.

### Execution Decisions
For Phase 0, I chose to patch existing production files immediately rather than wait for the validator script to work. The grep results showed 9 clear fabricated citations, and after a broader search I found 5 more. All were replaced with `Dato interno WorqAI · base de datos 2025` or `Dato interno · análisis Profile Pro LATAM 2025`. I used `StrReplaceFile` for precision.

For the spec schema, I used JSON Schema draft-07. I included copy slots for all major layout types (hook, big-number, terminal, tips, before/after, quote, CTA, ranked list). I made `meta.system` required with a pattern `^s[0-9]{2}$` to enforce the existing naming convention.

For the brief template, I structured it as YAML because it's human-readable and machine-parseable. The key innovation is the `forbidden` section (phrases, framings, visuals) — this constrains the AI BEFORE generation starts.

### Problem Hit: Python Unavailable
The shell environment on Windows had Python blocked by App Execution Alias. `python`, `py`, and `python3` all redirected to the Microsoft Store. I tried `where` via cmd and `find /c` but couldn't locate a working interpreter in time. This meant `stat_source_validator.py` was written but not executed. I relied on `Grep` to find fabricated stats and `StrReplaceFile` to patch them manually. This is a tooling gap that needs fixing before Phase 4 (deterministic QA), which also requires Python + Playwright.

### What Was Intentionally Deferred
- Usage audit: I read `_INDEX.md` but did not yet scan production HTMLs for component frequency. This requires parsing CSS class names and structural patterns, which is heuristic-heavy. Better to do it carefully.
- Render engine: Gated behind spec schema + component sets. No code written yet.
- Skill refactor: Gated behind render engine. No code written yet.
- Bounding-box QA: Gated behind render engine + stable pipeline. No code written yet.

### Memory Process Note
I had to reconstruct the exact line numbers and file paths from my tool call history. I am confident about the files read and the patches applied. I am less certain about exact line numbers in `build.md` after edits (the original source policy was around lines 509–513; after replacement it expanded). I noted this uncertainty where appropriate.
