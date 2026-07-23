# Carousel Builder System — Changelog

All notable changes to this system are recorded here. Newest entry at the top.

---

## 2026-05-21 — Gallery overhaul + system cleanup

### PART 1-2: Duplicate removal
- Removed 9 duplicate/near-duplicate gallery entries:
  - `geo-topo-lines` (dup of `geo-contour-flow`)
  - `scan-lines` (dup of `geo-scan-lines`)
  - `slide-cta-solo` (dup of `slide-cta`)
  - `slide-before-after-col` (dup of `slide-before-after`)
  - `glow-orb`, `zoom-rings`, `grid-bg`, `diag-band`, `blob-bg` (all duped by `geo-*` variants)
- Added 3 new CSS technique demos: `css-text-gradient`, `css-text-glow`, `css-text-stroke`
- Final count: **122 components** (was 128)

### PART 3: Dual-view generation
- Every component now renders TWO files:
  - `{id}-{slug}-component.html` — isolated view on dark s01 background, minimal copy, bottom label
  - `{id}-{slug}-context.html` — in-context view with original design system + realistic copy
- `scripts/build_gallery.py` rewritten to generate both views

### PART 4-5: Premium INDEX.html
- Two-panel layout: left nav (~40%, scrollable), right preview (~60%, fixed)
- Mobile: preview stacks above nav
- 6 category filters: Geo (42), Chrome (3), Layout (52), Sub (22), CSS (3), All (122)
- Per-card ISO / CTX toggle buttons
- 300ms crossfade on preview switch
- Accent green hover states, active border-left indicator
- NEW badges on recently-added items
- Real-time header stats from DEMOS array

### Bugfix
- Fixed `templates/slides/slide-comparison-table.html` Jinja2 dict-method collision (`side.items` → `side['items']`)

---

## 2026-05-19 — Kimi audit: 9/15 slides broken + corrective plan

*Reconstructed from Kimi session logs.*

### Audit findings — 3 test carousels (s01, s04, s26)
Claude built 3 carousels on 2026-05-18 (`carousel_ats-diagnostico_s01.html`, `carousel_transformacion-cv_s04.html`, `carousel_personaliza-cv_s26.html`). All scored 94/100 preflight, 100/100 visual richness. All had critical visual errors that preflight didn't catch.

| Carousel | Slide | Error | Severity |
|---|---|---|---|
| s01 NOIR GOLD | 1 | Headline text cut off at viewport edges | Critical |
| s01 NOIR GOLD | 3 | Massive number layout broken — text crammed in narrow column | Critical |
| s01 NOIR GOLD | 4 | Step flow completely broken — 3 boxes overlapping | Critical |
| s26 MATTE PASTEL | 2 | Blob competing with headline ("color winning over title") | Error |
| s26 MATTE PASTEL | 4 | WorqAI badge overlaps headline | Critical |
| s04 CRIMSON NIGHT | 2 | Quote mark renders as tiny speck | Minor |
| s04 CRIMSON NIGHT | 3 | Massive empty void — underdesigned | Weak |
| s04 CRIMSON NIGHT | 4 | Badge overlaps headline (same as s26) | Error |

Result: 9 of 15 slides had significant errors. Only ~6 slides (40%) ready to post. 47% completely unusable.

### Root causes identified
- Zero visual regression testing — Claude never looked at screenshots
- 18 instances of blob/glow-orb across 15 slides (same shape repositioned every slide)
- 80% effort on copy, 20% on visuals
- No "show don't tell" enforcement — zero demo layouts (waffle charts, input/output blocks, glassmorphism panels) despite reference carousels having them

### Kimi vs Claude plan comparison
Both produced plans independently. Key findings:
- Kimi's 6 enforcement rules > Claude's 2 (especially the "identical layer combo" check that catches the glow-orb-on-every-slide problem)
- Kimi's Tier 3 (6 new blob shapes) is **actively harmful** — adding more blob variants enables using a different blob on every slide without triggering the overuse check. The problem is blob overuse, not blob variety.
- Kimi's cross-slide continuity modes are **design theater** — Instagram renders each slide as a separate 1080×1080 PNG. A "wave flowing through all 5 slides" requires seeing two slides simultaneously, which is physically impossible.
- Claude independently built 6 new blob shapes, 3 flow layers, and 4 continuity modes — all of which were explicitly flagged as harmful.

### Corrective plan — what to keep, remove, add
**Keep from Claude's build:** 5 enforcement checks, `slide-input-output`, `slide-waffle-chart`, glassmorphism panel CSS, documentation updates.

**Remove from Claude's build:** 6 new blob shapes (angular, crystal, wave, arch, splatter, ribbon), 3 flow layers (geo-flow-wave, geo-flow-arrow, geo-flow-data), cross-slide-connector layout, 4 continuity modes.

**Add instead:** `slide-before-after` (P0), topographic contour lines (P0), 3D perspective wireframe grid (P1), hexagonal tessellation (P1), particle constellation (P1), neon aura ring (P2), bokeh orbs (P2), scan lines (P2).

### Enforcement rules locked (7 total)
1. Blob overuse — >2× same blob = FAIL
2. Glow-orb cap — >50% slides = FAIL
3. Identical layer combos — >50% same layers = FAIL
4. Badge collision — <150px from headline = FAIL
5. Shape diversity cap — >4 slides same shape = FAIL
6. Show don't tell — zero demo layouts = FAIL
7. Decoration purpose — "visual interest" as justification = rejected

### 23 visual components identified in reference carousels (missing from system)
Waffle chart, donut chart, glassmorphism panels, before/after comparison blocks, horizontal data bars, input/output demo blocks, topographic contour lines, 3D perspective wireframe grid, neon aura ring, particle constellation network, hexagonal tessellation, scan lines/CRT, bokeh/lens blur orbs, and others. Reference carousels already had most of these — Claude's output had zero.

---

## 2026-05-18 — 3 test carousels built (preflight passed, visual errors found next day)

- `carousel_ats-diagnostico_s01.html` — s01 NOIR GOLD, 5 slides, 101.9 KB
- `carousel_transformacion-cv_s04.html` — s04 CRIMSON NIGHT, 5 slides
- `carousel_personaliza-cv_s26.html` — s26 MATTE PASTEL, 5 slides
- All passed preflight (94/100) and visual richness (100/100)
- All had critical visual errors caught by Kimi audit the following day (see 2026-05-19 entry)

---

## 2026-05-17 — v2 Visual Primitives + carousel-master-ref consolidation

### Added
- `carousel-master-ref.md` — consolidated reference replacing 17 separate skill docs. Contains all 48 systems, 24 layouts, 25 geo layers, 12 decoratives, copy budgets, ship gate, v2 SVG primitive library, and JSON template.
- `scripts/build_carousel.py` — new top-level build command that runs render + preflight + visual_richness_check in one pass. Supports batch processing multiple specs.
- Gallery items 51–58 (v2 primitive showcases):
  - `51-svg-blob-organic.html` — SVG bezier blob variants
  - `52-svg-starburst.html` — SVG starburst variants (spark, burst, mark)
  - `53-svg-icon-library.html` — 21-icon SVG sprite reference
  - `54-text-gradient.html` — SVG-based gradient text treatment
  - `55-text-glow.html` — multi-layer text-shadow glow treatment
  - `56-text-stroke.html` — `-webkit-text-stroke` outlined text
  - `57-svg-drop-shadow.html` — SVG `feDropShadow` filter classes (sm/md/lg)
  - `58-svg-grain-texture.html` — SVG `feTurbulence` grain texture
- `roadmap/visual-primitives-v2-spec.md` — design spec and decision log for the v2 primitive system
- `ideation/auditfeebdack.md` — Kimi v1 audit feedback
- `ideation/kimis'feedback v2.md` — Kimi v2 feedback used to scope Tier A primitives
- Production carousels: `carousel_feral-cdmx_s25.html`, `carousel_negociacion-salarial-cr_s25.html`, `carousel_reclutadores-ghosting_s04.html`, `carousel_velar-sleep_s01.html`
- Spec files: `production/feral-spec.json`, `production/velar-spec.json`

### Changed
- `CLAUDE.md` — updated with v2 primitives documentation, pipeline policy, and `build_carousel.py` as the new canonical build command
- `scripts/preflight.py` — updated to emit soft warnings for deprecated v1 primitives (`blob-bg`, `ornament*`) instead of blocking
- `scripts/visual_richness_check.py` — updated for v2 primitive awareness
- `scripts/render_carousel.py` — updated to support v2 spec fields (`copy.text_treatment`, `effects.requires_playwright_export`)
- `templates/slides/slide-terminal.html` — minor fix

### Architecture decisions locked
- **Playwright (`carousel_exporter.py`) is canonical export.** In-HTML html2canvas button = quick preview only.
- CSS `background-clip:text`, `box-shadow`, `backdrop-filter`, `mix-blend-mode`, `filter:blur()` confirmed broken in html2canvas → SVG is the escape hatch for all of these.
- All v2 effects are html2canvas-safe by SVG-first design. Playwright-only effects must be tagged `effects.requires_playwright_export: true`.
- `carousel-master-ref.md` replaces reading 17 individual docs before a build.

---

## 2026-05-17 — System refocus + Component gallery (50 components)

### Added
- **Component gallery** (`gallery/`) — 50 HTML component files organized in 4 categories:
  - Geo layers (01–12): mesh-noise, pixel-grid, conic-rays, chevron-stripe, iso-grid, paper-texture, halftone, ribbon-flow, circuit-trace, topo-lines, starfield, gradient-bands
  - Chrome elements (13–15): vertical-counter, badge-stamp, header-bar
  - Slide layouts (16–30): myth-vs-fact, step-flow, comparison-table, faq-stack, quote-cascade, bento-grid, timeline, stat-row, pull-quote-author, warning-banner, icon-grid, progress-bars, list-numbered, data-viz-donut, typeset-poster
  - Sub-components (31–50): stamp-circle, pill-tag, arrow-flow, icon-circle, dotted-divider, rating-stars, logo-row, avatar-stack, fact-bubble, timeline-dot, bento-card, inline-stat, status-pill, comment-mock, handle-line, stat-card, chip-list, download-card, emoji-callout, swipe-arrow-stack
- `gallery/INDEX.html` — visual review hub for all 50 components
- Skill docs for `html-carousel-builder`: `layouts.md`, `preflight.md`, `render-engine.md`, `slide-templates.md`, `spec-schema.md`, `stat-validator.md`

### Removed — Profile Pro LATAM system (scope reduction)
- Agents: `audit-agent.md`, `client-delivery-agent.md`
- Skills: `ats-resume-rewriter/`, `auditoria/`, `intake-workflow/`, `linkedin-profile-rewriter/`, `profile-pro-latam-context/`
- Commands: `audit.md`, `client-cv.md`, `client-linkedin.md`

### Changed
- `AGENTS_BREAKDOWN.md` — rewritten to reflect 4 remaining agents (strategy, ads, content, growth)
- `CLAUDE.md` — updated structure, removed Profile Pro LATAM references, added render engine docs
- `ROADMAP.md` — simplified, WorqAI marketing focus only
- `html-carousel-builder/SKILL.md` — updated to reference new skill sub-docs
- `html-carousel-builder/techniques.md`, `workflow.md`, `build.md` — updated

---

## 2026-05-16 — Render engine Phase 2 + 50-component expansion

### Added — Deterministic render engine (Phase 2)
- `scripts/render_carousel.py` — headless render engine. AI now outputs JSON spec only; system assembles HTML deterministically from templates. Zero AI tokens at render time. Eliminates AI hallucinating CSS/HTML.
- `templates/carousel-shell.html` — full HTML shell as Jinja2 template
- Initial 9 slide templates in `templates/slides/`:
  - `slide-hook-lockup.html`, `slide-big-number.html`, `slide-terminal.html`, `slide-tip-blocks.html`, `slide-before-after.html`, `slide-checklist.html`, `slide-proof.html`, `slide-cta.html`, `slide-pull-quote.html`
- `scripts/stat_source_validator.py` — catches fabricated citations in specs

### Added — Phase 2.5: 50-component expansion
- **Gallery grew from ~34 to 84 total components** across 4 tiers:
  - **Geo layers** — 8 existing + 12 new (mesh-noise, pixel-grid, conic-rays, chevron-stripe, iso-grid, paper-texture, halftone, ribbon-flow, circuit-trace, topo-lines, starfield, gradient-bands)
  - **Chrome** — 5 existing + 3 new (vertical-counter, badge-stamp, header-bar)
  - **Slide layouts** — 9 existing + 15 new (myth-vs-fact, step-flow, comparison-table, faq-stack, quote-cascade, bento-grid, timeline, stat-row, pull-quote-author, warning-banner, icon-grid, progress-bars, list-numbered, data-viz-donut, typeset-poster)
  - **Sub-components** — ~12 existing + 20 new (stamp-circle, pill-tag, arrow-flow, icon-circle, dotted-divider, rating-stars, logo-row, avatar-stack, fact-bubble, timeline-dot, bento-card, inline-stat, status-pill, comment-mock, handle-line, stat-card, chip-list, download-card, emoji-callout, swipe-arrow-stack)
- `gallery/INDEX.html` — split-pane review hub with live iframe preview + filter by tier
- `scripts/build_gallery.py` — generates all 50 demo files + INDEX
- `scripts/component_registry.json` — system allowlist (maps components to compatible design systems)
- `scripts/carousel-spec.schema.json` — JSON schema v2 with `maxLength`/`maxItems` on all copy fields

### Fixed — Cropping bugs (from Gemini review)
- `.stat-grid` grid template fixed to `minmax(min-content,55%) minmax(0,1fr)` — prevented right-column bleed
- `.stat-num` clamp reduced from `clamp(100px,18vw,180px)` to `clamp(88px,14vw,148px)`
- Content safety wrapper added: all layout wrappers get `max-height: calc(100% - 24px); overflow: hidden`
- `slide-cta.html` URL slot now replaces counter instead of stacking under reward

### Architecture decisions
- Render engine design: AI decides content + layout, never markup. Kimi + Kenneth decision.
- `render_carousel.py` uses `copy.get('items', [])` not `copy.items` — avoids `dict.items()` name shadow in Jinja2.

---

## ~2026-05-15 — Layout Pre-Commit system + CSS surgery

*Pre-git. Reconstructed from Gemini session logs.*

### Added
- **Layout Pre-Commit (Phase 3, Step 2.9):** Hard constraint — engine must declare the layout for every slide before writing any copy. Solved the "AI wall of text" problem where layout and copy were decided simultaneously.
- **Layout Map Assert v2 (Phase 9):** 6 mathematical design rules enforcing human-like graphic design instincts:
  - Adjacency check — no identical adjacent slides
  - Visual rest check — minimum 2 rest slides required per carousel
  - Max consecutive run — max 2 of the same layout category in a row
  - Mid-deck rest enforcement
  - S1 locked to Poster/Hero, S8 locked to CTA, S2 locked to Myth vs Reality or Data Stat
  - Pull quote slides: 1 sentence maximum, no instructions allowed

### Fixed — CSS surgery
- **Grid blowout:** Fixed fatal CSS Grid bug where oversized typography pushed right-column text off the 1080px canvas. Added `word-wrap: break-word` and `min-width: 0`.
- **Vertical overlap crash:** Fixed layout bug where tall content (terminal blocks, tip blocks) grew downward and overlapped absolute-positioned footer. Added `padding-bottom: 80px` to all layout wrappers.
- **Ghost dot bug:** Removed `position: absolute` from `::before` list pseudo-elements. Changed to Flexbox gaps so dots stopped floating into the void when text wrapped.
- **Empty void Jinja2 bug:** Added `{% if copy.quotes %}` wrapper gates in Jinja2 templates — engine was rendering empty CSS boxes when AI passed an empty JSON array.
- **Typography clamp() madness:** Stripped aggressive `vw` font scaling that made text massive on 1080×1080 exports. Moved to stable pixel/container sizes.
- **Spanglish hardcoding:** Removed hardcoded Spanish labels ("Mito"/"Realidad") from HTML templates. Bound to dynamic JSON variables (`{{ copy.myth_label | default('Mito') }}`).

---

## ~2026-05-14 — Hallucination Killer: stat source validator

*Pre-git. Reconstructed from Gemini session logs.*

### Added
- `scripts/stat_source_validator.py` (v1) — Python regex scan catching fabricated stats in HTML output before delivery.
- **Verified sources allow-list** — hardcoded acceptable sources (Jobscan internal analysis, World Economic Forum, etc.)
- **Default fallback enforced** — when no external data available, system defaults to `Dato interno WorqAI · base de datos 2025`

### Banned
- Fabricated citation patterns: hallucinated titles like "LinkedIn Talent Solutions Report 202X"
- Soft quantifiers applied as facts: "la mayoría", "muchos", "según expertos" — blocked unless a real source is injected

---

## 2026-05-10 — Carousel portfolio fixes + Pattern Layer Scan

### Fixed — Portfolio carousels (C01, C02, C03, C05, C06)
- **C01 Halden & Co.** — upload zones were rhombus shapes (`clip-path:none!important` to `.upload-zone`), S1 upload not clickable (`pointer-events:none` to `.marque`), S2 quote bleeding into dark trapezoid (width 480px → 420px)
- **C02 Vault07** — S7 overlapping text: h2 148px → 116px, top 240px → 200px
- **C03 Sela Studio** — stamp circle hard to read: letter-spacing 0.18em → 0.12em, background opacity 0.4 → 0.88, font-size 9px → 10px
- **C05 Reps & Sets** — line-height crash (Anton at 0.84–0.88 caused glyph overlap): `stack-num` 0.85 → 1.05, h1 0.86 → 1.1, all h2 0.84–0.88 → 1.05. ChatGPT visual feedback incorporated: splat position, right-text inset, clip-shape dimensions, stat color differentiation, list spacing, table row padding, CTA positioning
- **C06 Mesa Verde** — upload zones rhombus fix, S1 headline 148px → 96px

### Added
- **Step 2.95 — Pattern Layer Scan** (`workflow.md`) — mandatory step between Layout Pre-Commit and Copy Writing. Triggers 7 pattern sub-files:
  - Always-load: `density-composition.md` (deck pacing), `chromatic-logic.md` (color roles)
  - Conditional: `relationship-layouts.md`, `type-architecture.md`, `motion-effects.md`, `spatial-distortion.md`, `carousel-wayfinding.md`
  - Required output: `PATTERN LAYER SCAN:` block before advancing to Step 3
- Agent skill lists updated (`ads-agent.md`, `content-agent.md`) — enumerated all 9 pattern sub-modules with code ranges (RL-01–18, TA-01–16, ME-01–14, DC-01–14, SD-01–16, CL-01–08, CW-01–05)

---

## 2026-05-10 — Carousel monetization strategy

*Strategic advisory session. No files modified.*

### Decisions made
- Business model ranking: freelance → white-label → productized → agency → SaaS
- White-label agency outreach = highest priority path (volume, recurring revenue, fast close)
- New studio brand required (not WorqAI) — prevents confusion with resume SaaS
- Floor pricing: $100 US / $50 LATAM per carousel; lead offer $250 test project for agencies
- Production time revelation (~2 min/carousel) recalibrated entire model: business is a sales problem, not a capacity problem
- Never disclose production speed to clients

### What was produced
- 7/14/30-day path to first revenue
- 3-offer stack (door opener, core offer, agency retainer)
- Outbound message templates (cold DM, follow-up, cold email)
- Income scenarios (survival/stable/aggressive)
- Upwork as parallel channel for first reviews

### What was rejected
- SaaS/startup path (6–18 months to revenue, wrong for survival mode)
- Agency model (requires staff, case studies)
- Website before first client
- Paid ads (CAC too high with no proof stack)
- Selling under WorqAI brand

---

## 2026-05-07 — Batch 01 stress test + quality-log.md

### Added
- `quality-log.md` — QA tracker with bug report template, scorecard (5 metrics × 1–5 scale), FIXED ISSUES table, RECURRING PATTERNS table, GOLD STANDARDS table, SINGLE-VARIABLE TEST LOG, POST-BATCH DECISION RULE
- 5 production carousels:
  - `carousel_pdf-ats-error_worqai-verde.html` — s17, 7 slides, warning hook
  - `carousel_cv-silencio-reclutadores_glass.html` — s08, 5 slides, identity hook
  - `carousel_linkedin-optimizado_boutique.html` — s48, 4 slides, transformation hook
  - `carousel_consejo-cv-esta-mal_brutalist.html` — s07, 7 slides, contrarian hook
  - `carousel_0-a-4-entrevistas_crimson.html` — s04, 8 slides, result hook

### Fixed
- **Export button overlap** — moved `controls` + `hint` outside `preview-cage` across all 5 carousels (100% defect rate). Root cause: nested `transform: scale(0.5)` caused layout collision with zip button
- **Brutalist slide 6 overflow** — `carousel_consejo-cv-esta-mal_brutalist.html`: `.s6-num` 130px → 90px, list gap 22px → 14px, item padding 22px → 12px, headline 60px → 46px, body 17px → 15px
- **Boutique brand mismatch** — `carousel_linkedin-optimizado_boutique.html`: replaced all `Profile Pro LATAM` → `WorqAI`, handle and copy rewritten to WorqAI product language

### Changed
- `workflow.md` — added HTML nesting diagram with `⛔ CRITICAL` warning on controls placement; added brand identity rule (WorqAI carousels always use WorqAI handle/mark/language regardless of system)
- `anti-slop.md` — added Ranked List ≤95px number ceiling to Mobile Render Sanity checklist

### Architecture decisions locked
- CODE FREEZE on infrastructure — shift to production observation phase
- Visual QA loop established: scorecard + 3-recurrence rule triggers system edits

---

## 2026-05-06 — Adversarial review triage: validation layer overhaul

*Cross-LLM review by Claude, ChatGPT, Gemini. 11 items killed, 9 shipped.*

### Added
- **ContentSpec Hard Gates 5 → 8** (`workflow.md` Step 4.8):
  - Gate 6: Pull Quote `quote_word_count` ≤ 18
  - Gate 7: CTA `keyword_is_single_word: true`
  - Gate 8: All slides `total_slide_word_count` ≤ 45 (Slide 1 exception: ≤ 8)
- **Banned Implied Claims** (`.claude/rules/anti-slop.md`) — 7 categories:
  1. Implied recency/temporal urgency ("hoy en día", "ya no funciona")
  2. Obituary claims ("el CV tradicional está muerto")
  3. Scarcity without data ("solo 6 segundos" unsourced)
  4. Vague consensus / implied authority ("es bien sabido que")
  5. Soft quantifiers as fact ("suele ocurrir que", "es común ver")
  6. Absolute negatives unsourced ("ningún reclutador", "nadie contrata")
  7. Causal claims without mechanism ("activa el filtro ATS")
- `global_layout_map` requirement in **REGEN_MODE** (`SKILL.md`) — partial regeneration must include full 8-slide layout array so Layout Map Assert can check adjacency and category runs
- Dependency declarations at top of all 12 hook files — forces `voice-core.md` load before hook structure

### Changed
- `workflow.md` Step 5 sweep language — changed from "fix every violation" to **verification only, not repair**. Fatal signals emit `BLOCK` notice and route to REGEN_MODE; no silent self-corrections
- `workflow.md` Step 4.8 — fixed hardcoded `"Myth vs Reality"` in example JSON that was nudging engine toward myth format even when real stats provided

### Decisions made (kill list)
- Full pipeline restructure rejected — ContentSpec gate at 4.8 already catches layout-copy mismatches
- NLP semantic checks rejected — checkbox theater, LLMs self-report true regardless
- VOICE_DNA_CHECKSUM handshake rejected — fragile string token check; dependency directive is more reliable
- Windowed density rule rejected — contradicts consecutive run rule; global maximum is simpler

---

## 2026-05-02 — Skill file token trimming

### Changed
- `systems-core.md` — removed redundant DNA fields (`brand_emotion`, `industry_fit`, `svg_complexity`), removed duplicate CAROUSEL PRODUCTION RULES section, compressed Font Pairing Guide. Net: 37.1KB → 33.8KB
- `copy-dna.md` — removed generic Voice DNA template, removed duplicate ANTI-SLOP COPY RULES section (already in global `.claude/rules/anti-slop.md`), compressed hook psychology intro, CTA examples, per-slide emotion labels. Net: 19.0KB → 15.0KB
- `anti-slop.md` (carousel builder) — compressed 4 Fatal Signals from ~15 lines to 3 lines each, compressed Kill Switch and Exception Clause. Net: ~12KB → 8.6KB
- `layouts.md` — expanded 16 → 26 layouts (+10: Icon Grid 2×3, Two-Stat Pair, Manifesto Stack, Badge/Tag Grid, Case Study Card, Product UI Frame, Annotation Diagram, Counter Stack, Quantified Before/After, Asymmetric Vertical Split), then trimmed. Net: ~41KB → ~34.6KB
- `workflow.md` — merged tables, compressed steps. Net: ~29KB → ~23.7KB

### Combined savings
~22.5KB / ~5,700 tokens across 5 skill files

### Decisions made
- JSON + Python templates pipeline deferred (long-term correct direction, no infrastructure yet)
- Quality checklist items left untouched (enforcement tooling, not prose)

---

## ~2026-04-30 — Selection intelligence + hook type expansion

### Added
- `selection-intelligence.md` — Step 0.5 · Emotional Register pre-filter (4 registers: Dark+Bold, Light/Editorial, Warm/Organic, Chromatic/Maximalist). Collapses 48 systems to ~10–18 candidates in one question.
- Archetype X · Data Editorial added as 10th master archetype (systems 05, 19, 46)
- `copy-dna.md` / `workflow.md` — Hook library expanded from 5 to 12 types (added: Identity, Reframe, Confession, Warning/Interruption, Transformation, Authority Borrow, Specificity)
- Slide count decision matrix (7 content jobs → optimal slides 3–10)
- Hook×count pairing tables
- Completion rate warning: ~15–25% viewer drop per slide past slide 5 on Instagram

### Changed
- `workflow.md` — Step 2 rewritten: slide count decided BEFORE hook type (was: hook type first)
- `selection-intelligence.md` — fixed "47 systems" typo → 48

### Decisions made
- No new design systems added (48 is enough)
- Number List is a format, not a hook type
- POV/Relatable, Timely/Trend, Scrapbook/Collage skipped as additions

---

## ~2026-04-28 — Geometry system overhaul: GEO-13 + system-dependent routing

### Added
- `geometry-modules.md` — GEO-13 PERSPECTIVE WIREFRAME module (~60 lines). CSS `perspective: 600px` grid plane with `rotateX(58deg) rotateZ(-12deg)`, `mask-image` fade, three position variants.
- `production/test_geo13_slide.html`, `test_geo13_noir.html`, `test_wave_slide.html` — single-slide geometry tests
- Rule 16 to `SKILL.md` — forces GEO-13 CSS load for dark systems before writing slide content; prevents custom geometry engine invention

### Changed
- `selection-intelligence.md` — Step 6 Q1 rewritten from "GEO is opt-in" to system-dependent routing: dark/cinematic → GEO-13 at EXPRESSIVE, warm/organic → blob only, editorial/Swiss → flat grid
- `SKILL.md` — Rule 3 updated for dark systems (gradient + GEO-13 instead of gradient + blob), Rule 4 updated with GEO-13 continuity note
- `carousel_ats-cv_worqai-verde.html` — complete rebuild: replaced 140-line JS panoramic bio tendril (opacity 0.22, invisible) with CSS-first aurora-style approach

### Architecture decisions locked
- Dark/cinematic systems: GEO-13 is default, not opt-in
- Geometry opacity range: 0.13 minimum (below = invisible), 0.40 maximum (above = overpowers content), 0.18 standard
- Aurora carousel (`carousel_linkedin-fantasma_aurora.html`) established as visual benchmark for dark systems

---

## 2026-05-12 — Foundation (initial commit)

### Added — Full system, built from scratch

**Agent system (7 agents):**
- `ads-agent.md` — Meta ads + carousel pipeline
- `content-agent.md` — social, blog, SEO, newsletters
- `growth-agent.md` — sales, objections, Reddit, job hunting
- `strategy-agent.md` — roadmap, GTM, positioning, KPIs
- `outreach-agent.md` — personalized DM sequences
- `audit-agent.md` — Profile Pro LATAM audit (later removed 2026-05-17)
- `client-delivery-agent.md` — Profile Pro LATAM delivery (later removed 2026-05-17)

**Skills (initial):**
- `html-carousel-builder/` — carousel build system with design tokens, layout library, shell template
- `worqai-brand-context/` — brand voice, ICP, product positioning
- `saas-gtm-playbook/`, `launch-playbook/`, `analytics-kpi/` — strategy skills
- `social-growth/`, `seo-content-strategy/`, `human-voice-writer/`, `email-marketing/`, `landing-page-cro/` — content skills
- `meta-ads-specialist/`, `carousel-to-zip-exporter/` — ads skills
- `sales-mastery-expert/`, `reddit-job-posting/`, `job-hunter/` — growth skills
- `customer-interviews/`, `pricing-experiments/`, `referral-program/` — research/strategy skills
- Profile Pro LATAM skills (removed 2026-05-17)

**Scripts (initial pipeline):**
- `scripts/carousel_exporter.py` — Playwright HTML → numbered PNGs → ZIP
- `scripts/preflight.py` — carousel validation before export
- `scripts/render_carousel.py` — JSON spec → HTML carousel
- `scripts/apply_tokens.py` — design token injection
- `scripts/build_orchestrator.py` — batch build orchestrator
- `scripts/component_picker.py`, `component_validator.py` — component tools
- `scripts/visual_richness_check.py` — visual quality gate
- `scripts/generate_preview_gallery.py` — gallery generation
- Supporting: `contract_injector.py`, `usage_logger.py`, `usage_report.py`, `linkedin_report.py`

**Templates:**
- `templates/carousel-shell.html` — base HTML shell for all carousels
- `templates/slides/` — 50 slide layout templates

**Rules:**
- `.claude/rules/anti-slop.md` — banned words, visual slop patterns
- `.claude/rules/brand-voice.md` — WorqAI voice guide
- `.claude/rules/carousel-layout-checks.md` — pre-export layout checks
- `.claude/rules/output-conventions.md` — file naming and destinations

**Commands (slash):**
- `/ads-brief`, `/ads-carousel`, `/blog-post`, `/launch-plan`, `/monthly-roadmap`
- `/reddit-post`, `/sales-reply`, `/upgrade-prompt`, `/weekly-content`

**Hooks:**
- `.claude/hooks/bash-guard.sh` — blocks dangerous shell patterns
- `.claude/hooks/format-check.sh` — output formatting validation

**Planning docs:**
- `CLAUDE.md`, `AGENTS_BREAKDOWN.md`, `ROADMAP.md`
- `roadmap/carousel-monetization-strategy.md`, `organic-growth-plan.md`, `outreach-dms.md`
- `quality-log.md` — carousel quality tracking

---

## ~2026-05-11 — 3-tier constrained prompting era

*Pre-git. Reconstructed from Gemini session logs.*

### Added
- **3-tier build architecture:** Separated instructions into `tokens.md` (48 design systems), `build.md` (layouts and voice), `workflow.md` (step-by-step logic). Replaced the previous monolithic prompt approach.
- **`preflight.py` v1:** 10-point Python QA script to mechanically check AI-generated HTML. Included:
  - Anti-slop checks (banned `border-left: Npx solid`, `border-radius: 999px`)
  - Layout diversity checks to prevent repetitive slide structures
  - html2canvas compatibility checks (banned raw `conic-gradient`, enforced `-webkit-backdrop-filter`)
- **Subtraction Gate:** Forced prompt step requiring AI to delete 25% of decorative elements before delivering code — prevents over-designing.

---

## ~2026-05-10 — Anti-slop copy gates

*Pre-git. Reconstructed from Gemini + ChatGPT session logs.*

### Added
- **Causal claims gate:** Blocked causal claims without a verified mechanism (e.g., "esto hace que el reclutador confíe").
- **Recruiter negatives block:** Absolute negatives about recruiter behavior blocked unless a source is provided.
- **Cliché lexicon ban (global):** "hoy en día", "está muerto", "es bien sabido que", "solo 6 segundos" — added to banned phrases list.
- **Source Fact Gate (Phase 0/8):** If `source_facts` are empty, system locked out of generating stats. Defaults to Myth vs Reality format. Banned "la mayoría", "muchos", "según expertos" without an injected source.

---

## ~2026-05-08 — First outreach session + 12 composition rules crystallized

*Pre-git. Reconstructed from memory files.*

### Context
First real outreach session using white-label carousel demos. 3 personalized demos sent to 3 prospects. One polite no (@eimyzuu / @mercadeatecr_ — had 3 in-house designers, not the right target). 2 no-response.

### What was built
- **Mercadeate demo carousel** (`production/carousels-portfolio/mercadeate_services_demo.html`) — 5 versions iterated in one session:
  - v1 Swiss Brut: rejected immediately (dark editorial applied to warm/feminine brand)
  - v2 Pink Aurora: better direction, weak slides 2-3-4 (same layout repeated)
  - v3 Unique layouts: failed (5.3/10 — content-to-canvas ratio too low, blur test failed, ghost numbers stealing attention)
  - v4 Hierarchy aggression + outcome copy: scored 7.7/10 (ghost numbers removed, blob opacity capped at 0.12, outcome copy as hero headlines, rhythm break on slide 3)
  - v5 Fill lower halves: grain, glow, and CTA band refinements
- DM scripts written for 3 prospects (cold DM, Day 3 follow-up, cleaned pitch)
- Memory files created: system selection rule, hierarchy/composition 10-rule checklist, outreach playbook
- 6 portfolio carousel prompts written (not built)
- Notion portfolio structure designed (not built)

### What was learned — Qualification rule
Before building any demo, confirm: (1) active retainer clients, (2) no in-house design team — confirmed via bio/LinkedIn/team posts, not inferred from post quality, (3) visible outsourcing behavior or production strain. If Box 2 can't be confirmed → send portfolio link, don't build a custom demo.

### What was learned — 12 carousel composition rules
The Mercadeate demo went through 4 rejected versions. Each rejection added a rule. Full rules live in `.claude/rules/carousel-layout-checks.md`.
1. Blur test — content must win, not background atmosphere
2. One dominant gesture per slide, not two
3. Content-to-canvas ratio — content must occupy meaningful portion of canvas
4. Decorative budget — blob opacity 0.12 max, no ghost numbers, no 700px centered circles
5. Secondary scale must reward the swipe (list items 22px minimum)
6. Democratic lists fail — give one item per list hero treatment
7. Outcome copy, not category labels
8. Rhythm breaks — at least one structurally different slide per carousel
9. CTA slide must escalate, not soften — primary phrase 64px minimum
10. Spacing must feel assertive — anchor elements to each other
11. Bottom-takeover slides: hide ALL chrome (progress bars too, not just handle)
12. (Added 2026-05-17) Use v2 SVG primitives, not CSS-only equivalents

### What was learned — System selection rule
Never apply a dark/contrasting system to a warm/feminine brand. Mercadeate v1 was built in SWISS BRUT ACCENT; the agency was pink+warm. Rejected immediately. Rule: match brand energy first, elevation second.

### What was learned — Quality bar set
Carousel for Aura Agencia Creativa rejected as "pretty AI and generic and bad designed." Rule: every carousel gets a visual gut-check — "Would this impress a creative director?" before shipping.

---

## ~Late April 2026 — Anti-AI taste check + html2canvas embedded pipeline

*Pre-git. Reconstructed from Gemini + ChatGPT session logs.*

### Added
- **Anti-AI Taste Check (Phase 10):** Mandatory literal string output before HTML generation. The JSON must physically print `"confirmed no left-border cards, no deco-nums, no pill badges, layout varies"` — a guardrail that forced self-auditing before delivery.
- **Client-side export:** Embedded html2canvas + JSZip via CDN directly into the carousel HTML, eliminating the need for Python or Playwright for quick exports.

### Removed
- **Decorative numbers:** Large decorative numerals suppressed (`display: none`) by default to kill the "cheap Canva" aesthetic. Allowed only on 6 specific design systems.
- **Halftone textures:** Deactivated globally due to visual clashes with error card density.

---

## ~Early April 2026 — Multi-agent organization + deterministic workflow

*Pre-git. Reconstructed from Gemini + ChatGPT session logs.*

### Added
- **Agent separation:** Split the single AI into specialized nodes — Strategy, Ads, Growth, Delivery, Content, Audits. Master Orchestrator (Claude Code) as "General Contractor" — worker agents report up, don't talk to each other.
- **Folder architecture locked:** `production/`, `export/`, `distribution/`, `roadmap/`, `clients/`, `scripts/`, `ideation/`
- **Python automation scripts:** Moved deterministic tasks (zipping exports, creating folders) out of the LLM into Python.
- **REGEN_MODE:** Partial regeneration — instead of regenerating the full carousel, engine halts, retains the `global_layout_map`, and re-emits targeted JSON for a single slide.
- **Token fetching system (Phase 6):** Flat-file token mapping (`VAR_ACCENT`, `VAR_BG_BASE`) to prevent raw hex code hallucination during HTML build.
- **Component-first logic:** AI selects from constrained primitives (1 layout + 2 decorative + 1 mock-ui) instead of inventing HTML from scratch.
- **Anti-slop content engine:** Banned generic Canva clichés — left-border cards, pill badges, generic phrases.
- **Modular hook system:** 6 specific cognitive frameworks for Slide 1 (Result, Question, Contrarian, Curiosity, Identity, Authority-borrow).

### Changed
- **Positioning:** System shifted from "AI tool" to "Premium Creative Infrastructure / White-label Backend."
- **Portfolio framing:** Gallery metrics changed from Likes/Reach to "Tiempo de Producción: [34 min]" — sells pipeline speed to B2B agencies.

### Removed
- **Hallucinated CSS:** Banned the LLM from inventing custom CSS on the fly. All styling from pre-defined system classes only.
- **Monolithic prompts:** Context pollution from single giant prompts replaced by the agent separation architecture.

---

## ~March 2026 — v1.0.0: True origin

*Pre-git. Reconstructed from Gemini + ChatGPT session logs. Kenneth's description: "it started as 2 skills — a carousel builder MD file, the carousel exporter, and some instructions."*

### Added — Original seed system
- `html-carousel-builder/SKILL.md` — first version, a single markdown file with carousel build instructions
- `scripts/carousel_exporter.py` — Playwright-based HTML → PNG → ZIP exporter, the first real script
- **47 design systems index (v1):** Core matrix of archetype systems, color tokens, and subtraction rules (e.g., `system_01_noir_gold`, `system_29_cyber`)
- **Customer Moment Brief (Phase 1):** Internal "working memory" anchor — forces AI to think about a specific person ("26-year-old in San José who sent 40 apps") instead of generic "job seekers"
- **Voice-core.md:** Master brand DNA policy doc and CTA formulas
- **Base ability:** 8-slide carousels generated via LLM prompts with early styling rules and HTML preview

### Design philosophy at this stage
- Moved away from generic SaaS/startup aesthetics toward premium editorial visuals
- Goals: slides that feel expensive, engineered, layered, systemized, and recognizable as a distinct visual language
- "Does this carousel sit next to [X brand] without looking cheap?" became the generation standard

---

*Update this file when doing a big push — new scripts, new components, architecture changes, anything that shifts how the system works. Say "update the changelog" and describe what changed.*
