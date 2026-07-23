# Carousel Builder System — Changelog

All notable changes to this system are recorded here. Newest entry at the top.

---

## 2026-05-29 — Batch QA: Pipeline hardening + 8 carousel repairs

### Root causes fixed (systemic)

**RC1: Scrims too dark** (`templates/carousel-shell.html`)
- `--ai-scrim` default: `0.52` → `0.36`; heavy: `0.68` → `0.52`; demo: `0.30` → `0.18`; cta: `0.65` → `0.50`
- `--ai-photo-opacity` default: `0.85` → `0.92`; heavy: `0.78` → `0.86`; demo: `0.90` → `0.95`
- Added `object-position: center center` to `.geo-ai-bg`

**RC2: Sub-components visually weak** (`templates/carousel-shell.html` — Phase 2 override)
- Card border: `rgba(255,255,255,0.13)` → `rgba(255,255,255,0.22)` across all content cards
- Card fill: `0.085/0.032` → `0.13/0.055` gradient
- Left accent bar `2px solid rgba(--accent,0.55)` added to: `step-box`, `chk-item`, `lnum-item`, `cascade-quote`
- Top accent bar added to `proof-card`
- Tip block colors boosted: bad/mid/good all raised ~0.04 opacity, borders more visible
- Icon grid, BA cols, statrow, FAQ items, mvf panels, warn-box all strengthened

**RC3: Panel extraction stretch** (`scripts/panel_extractor.py`)
- Replaced `.resize((1080,1080))` with `ImageOps.fit(..., centering=(0.5,0.5))` for non-square source panels
- Non-square extracted panels now center-crop to 1:1 instead of distorting content

**RC4: White-border panels** (`brand/generated-bg/blue-accent-waves/`)
- Ran `panel_extractor.py --fix-kit --trim-gutters 5` on all 8 panel files
- Corner averages dropped from 233→46 (near-white → dark)

**RC5: Bad extraction (cosmic-liquid-orbs)** — 2 sub-panels visible per frame
- No re-extraction possible (source lost). Quarantine added to manifest pending re-gen.
- `carousel_por-que-no-llaman_s41` swapped to `neon-orbs`

### Added — `scripts/preflight.py` checks 27-29 (checks_total 26 → 29)
- **Check 27: AI-bg Panel Dimensions** (FAIL) — verifies each referenced panel PNG is exactly 1080×1080 via Pillow
- **Check 28: AI-bg Edge Brightness** (WARN) — checks each panel's 10px edge bands; warns if mean > 220 (baked-in white border)
- **Check 29: Slide Content Minimum** (WARN) — warns if any slide has fewer than 4 visible words
- All check labels updated from /22 to /29

### Fixed — Individual carousel repairs

| Carousel | Issues fixed |
|---|---|
| `carousel_linkedin-invisible_s08` | Slide 1: awkward hook copy fixed; Slide 2: empty statrow-cards filled; Slide 3: empty io-panel-content filled for both panels |
| `carousel_cv-2026-vs-2020_s20` | Slide 1: SVG gradient text split 2 lines (font 110→68, viewBox adjusted); Slide 2: receipt layout redesigned as dark ATS terminal report |
| `carousel_cv-largo-ignorado_s09` | Slide 1: fbt-label pulled from `position:absolute` into flow (fixes overlap); Slide 2: context added below "1 PÁGINA" |
| `carousel_carta-presentacion_s33` | Phase 2 CSS injected; bento card labels strengthened |
| `carousel_worqai-vs-manual_s40` | Slide 1: fbt layout fixed (label de-absolutized); Slide 2: dwall boxes smaller; Slide 3: badgeg font/wrap reduced |
| `carousel_por-que-no-llaman_s41` | Kit swapped: `cosmic-liquid-orbs` → `neon-orbs`; Phase 2 CSS injected |
| `carousel_tres-cambios-entrevistas_s16` | Slide 3: mn-content filled with headline + body text; Phase 2 CSS injected; neon-orbs panels re-extracted (no more stretch) |
| `carousel_cv-irresistible_s14` | Slide 1: SVG gradient text split 2 lines (font 110→62); Slide 2: `padding:0` restored to `var(--pad-y) var(--pad-x) var(--pad-bottom)`; Phase 2 CSS injected |

### Phase 2 CSS patch (`PHASE 2 COMPONENT BOOST 2026-05-29`)
Injected into all 8 repaired carousels as inline override. Future renders pick up changes from shell automatically.

---

## 2026-05-27 — Phase 5 Carousel Rebuild: 10 AI-bg carousels rebuilt with unique backgrounds

### Changed — Background assignment (each carousel now uses a unique AI background)
| Carousel | System | Background |
|---|---|---|
| rrhh-no-dice-filtro | s01 | satin-waves-full (unchanged) |
| experiencia-valida-formato-no | s06 | energy-flow-full (unchanged) |
| ats-no-lee-como-humano | s04 | glowing-energy-flow (unchanged) |
| palabras-que-busca-bot | s27 | cosmic-ribbons (unchanged) |
| cv-perfecto-no-pasa | s17 | geo-blue-grid (unchanged) |
| tres-ajustes-doble-entrevistas | s11 | **fluid-satin-waves** (was satin-waves-full — duplicate) |
| errores-6-segundos | s01 | glass-panel-full (unchanged) |
| cincuenta-a-cinco | s21 | galactic-dream-full (unchanged) |
| 73-porciento-muere-filtro | s17 | oceanic-wave (unchanged) |
| reclutador-vs-bot | s25 | **futuristic-glass-panel** (was glass-panel-full — duplicate) |

### Changed — Spec files
- `ai-bg-tres-ajustes-doble-entrevistas-s11-spec.json`: `satin-waves-full` → `fluid-satin-waves`
- `ai-bg-reclutador-vs-bot-s25-spec.json`: `glass-panel-full` → `futuristic-glass-panel`

### Process
- All 10 specs re-rendered with `render_carousel.py` → picks up Phase 1 CSS override layer, Phase 2 template redesigns, and Phase 3 density system automatically
- All 10 passed preflight: **100/100, 26/26 checks each**
- All 10 copied to `production/approved/` (new Phase 3 staging folder)

### Why fluid-satin-waves and futuristic-glass-panel
- `fluid-satin-waves` (s11): 8-panel kit, clean trim, dark tones — visually similar register to satin-waves-full but genuinely distinct panels
- `futuristic-glass-panel` (s25): 8-panel kit, light-through-glass, matches s25 SWISS BRUT ACCENT's editorial mood without competing with its high-contrast typography

---

## 2026-05-27 — Phase 4 Contact Sheet: carousel_exporter.py auto-generates QA sheet on export

### Changed — `scripts/carousel_exporter.py`
- Added `build_contact_sheet()` function: generates a dark-background PNG grid after every export
  - All slide thumbnails arranged in auto-calculated grid (≤8 slides → 4 cols, else 5 cols)
  - Thumbnail size: 360×360px. Teal accent strip on left edge, header with carousel name + slide count
  - Slide numbers (01, 02...) below each thumbnail
  - Graceful font fallback (tries arialbd, DejaVuSans-Bold, default bitmap font)
  - Saved next to the ZIP as `{carousel_stem}_contact_sheet.png`
- Added `--no-contact-sheet` flag to skip sheet generation
- Added `--input` as canonical alias for `--html` (matches CLAUDE.md convention)
- `--output` now accepts a directory path (as well as ZIP filename):
  - Directory → saves `{html_stem}.zip` + `{html_stem}_contact_sheet.png` inside it
  - No `--output` → auto-routes to `export/` relative to project root
- Branding updated from "Profile Pro LATAM" to "WorqAI"
- `CLAUDE.md` updated with new export examples showing auto-routing and `--no-contact-sheet`

### Why contact sheet
Visual QA bottleneck: previously you had to open each exported PNG individually or look at the in-browser carousel preview to spot layout problems. Contact sheet collapses all slides into one image — useful for client approval, quick gut-check before posting, and archiving a snapshot of what was sent.

### What was rejected
- Adding contact sheet to the ZIP: it's a QA tool, not a deliverable. Kept outside the ZIP.
- Interactive HTML contact sheet: overkill. Static PNG is what you need for WhatsApp/email approval.

---

## 2026-05-27 — Phase 3 Pipeline Gates: manifest metadata + 3 AI-bg checks + staging folders

### Changed — `brand/generated-bg/manifest.json`
- Added 4 fields to all 23 kit entries: `role`, `density_requirement`, `safe_for_dark_systems`, `quarantine`
- Kit roles assigned: `hero` (7 kits — dramatic, needs heavy scrim), `atmosphere` (7 kits — versatile), `texture` (9 kits — patterned, works under cards)
- `quarantine: true` on `digital-glass-full` (bad extraction) and `pastel-waves` (light imagery on dark systems)
- Legacy kits (4-panel duplicates) flagged with `notes` pointing to canonical replacements

### Changed — `scripts/carousel-spec.schema.json`
- Added `density` field to per-slide items schema (enum: `heavy` / `demo` / `cta`; required on AI-bg carousels)
- Added Phase 2 copy fields: `result`, `output_score`, `cta_variant` to `copy` schema

### Added — `scripts/preflight.py` checks #24–26
- **Check 24: AI-bg Quarantine** (FAIL) — scans HTML for quarantined kit IDs (`digital-glass-full`, `pastel-waves`) in background image src paths
- **Check 25: AI-bg Density Coverage** (FAIL) — if `geo-ai-bg-overlay` present, every `.slide` div must have `data-density` attribute; missing → FAIL
- **Check 26: AI-bg Card Transparency** (WARN) — scans inline style attributes for `rgba(255,255,255,<0.07)` on AI-bg carousels; these are invisible on dark backgrounds
- `checks_total` updated 23 → 26; check labels updated to `[22/26]`, `[23/26]`
- Helper functions: `_extract_ai_bg_kits()`, `check_ai_bg_quarantine()`, `check_ai_bg_density_coverage()`, `check_ai_bg_card_transparency()`

### Added — `production/drafts/`, `production/approved/`
- Two new sub-stage folders with `.gitkeep` files
- `output-conventions.md` updated with 3-stage workflow diagram (drafts → production → approved → export) and gate rules per stage

### Verified
- `preflight.py` on rrhh carousel: **100/100, 26/26 checks passed**
- Check 24 correctly passes (no quarantined kits in rrhh)
- Check 25 correctly passes (all 4 slides have `data-density`)
- Check 26: WARN-only, no false positives from shell CSS (inline-style scan only)

### What was rejected
- Making check 26 scan `<style>` blocks: too many false positives from shell geo layer CSS (zoom rings, overlays use intentionally low opacity). Inline-only scan is precise.
- Adding `bg_id` field to meta schema: redundant with the `layers` field already in the spec.

---

## 2026-05-27 — Phase 2 Component Surgery: 5 template redesigns + preflight check #23

### Changed — `templates/slides/slide-terminal.html` (full rewrite)
- Added `copy.result` field → `.term-result` class: bold, accent-colored, separator-ruled dramatic final line
- Default fallback changed: `ats-scan.sh` tab, 3 lines + `SCORE: 28/100 — RECHAZADO AUTOMÁTICO`
- Rule comments document 4-line max and result field purpose
- Removed redundant `.term-check` / `.term-x` absolute-positioned elements

### Changed — `templates/slides/slide-input-output.html` (full rewrite)
- Replaced all HTML entity icons (`&#10003;`, `&#10007;`, `&#8594;`) with SVG sprite references
- Input label icon: `#icon-ok` (teal), output label icon: `#icon-error` (pink), arrow: `#icon-arrow-right`
- Added `copy.output_score` field → `.io-ats-score` at bottom of ATS panel (bold, accent, large)
- Asymmetric flex: io-human 42, io-ats 58 (locked via Phase 1 CSS override)

### Changed — `templates/slides/slide-before-after.html` (full rewrite)
- `copy.before_score` / `copy.after_score` → `.ba-score.bad-score` / `.ba-score.good-score`
- Score renders ABOVE the list — visual anchor, not an afterthought
- Mock skeleton lines only display when no score is provided
- Phase 1 CSS provides red/teal column tints and 48–72px score sizing

### Changed — `templates/slides/slide-cta.html` (3-variant rewrite)
- Added `copy.cta_variant` field with 3 branches: `button` (default), `diagnostic`, `editorial`
- `button`: existing pill + glow layout; star SVG opacity lowered to 0.80
- `diagnostic`: left-aligned, terminal window with mac dots + mono font, arrow link CTA — for ATS carousels
- `editorial`: large question (24–36px) + underlined link text, no star, no pill — for concept carousels
- "GRATIS" banned across all variants; allowed: SIN COSTO / CV CHECK / ATS CHECK / ESCANEAR / DIAGNÓSTICO

### Changed — `templates/slides/slide-icon-grid.html` (full rewrite)
- Added `t.featured` flag: featured tiles get `icon-xl` SVG in row layout, no `.sub-icon-circle` bubble
- Standard tiles: `icon-lg` inline SVG mark, no bubble container
- Max 3 tiles documented in template comments (4+ weakens the grid)
- Phase 1 CSS adds card backgrounds, accent tint on featured

### Added — `scripts/preflight.py` check #23: S1 Hook Context
- New function `check_s1_hook_context(slides)` added after `check_demonstration_layout()`
- Extracts slide 1 text (strips HTML tags + entities), checks for domain keywords:
  CV, ATS, currículum, LinkedIn, reclutador, filtro, entrevista, empleo, trabajo, postulación, vacante
- WARN-only (never blocks export) — carousel still scores 100 if domain keywords absent
- `checks_total` updated 22 → 23; existing check 22 label updated to `[22/23]`

### Added — `.claude/skills/html-carousel-builder/carousel-master-ref.md` section 6.3
- "S1 Hook Formula" section: `[Object] + [Problem] + [Mechanism]`
- Wrong-vs-right table: generic opener vs. domain-anchored hook
- Notes preflight check #23 will warn on hooks missing domain vocabulary

### Verified
- `preflight.py` run on `carousel_rrhh-no-dice-filtro_s01.html`: **100/100, 23/23 checks passed**
- Check #23 correctly PASS on all rrhh slides (domain keywords present)

### What was rejected
- Making S1 hook check a FAIL (not a WARN): too aggressive — some legitimate carousels start with a universal statement before naming the domain
- Rewriting `slide-before-after-stacked.html`: low priority, stacked variant is rarely used

---

## 2026-05-27 — Phase 1 Premium Override Layer: stamp, starburst, glass, body text, terminal, io-panel, icon grid

### Changed — `templates/carousel-shell.html`
Single CSS injection block (`PHASE 1 PREMIUM OVERRIDE LAYER`) added before `</style>`. Pure CSS — no template edits required. Fixes 9 component-level taste problems identified in visual review.

**P1-1. Stamp → Trust Seal**
- `.deco-stamp` and `.sub-stamp-circle`: removed dashed border, removed rotation, replaced circle with flat pill (`border-radius:999px`, `1px solid` accent, `rgba(accent,0.06)` background)
- "GRATIS" banned in copy — required labels: SIN COSTO / CV CHECK / ATS CHECK / ANÁLISIS

**P1-2. Starburst → Editorial Registration Mark**
- `.deco-starburst`: opacity `0.85 → 0.28`, `scale(0.68)`, width/height `64px → 52px`
- `.deco-starburst-mark`: opacity `→ 0.20`, `scale(0.60)`
- `.deco-starburst-spark`: opacity `→ 0.24`, `scale(0.62)`, `48px → 38px`
- Light systems: `opacity: 0.35` (slightly higher so they register on white)

**P1-3. Glass Panels → Darker Gradient, Stronger Border**
- All panel/card selectors (`.glass-panel`, `.sub-stat-card`, `.sub-bento-card`, `.lnum-item`, `.proof-card`, `.step-box`, `.chk-item`, etc.): background raised from `rgba(255,255,255,0.04–0.06)` to `linear-gradient(rgba(255,255,255,0.085), rgba(255,255,255,0.032))`
- Border raised from `rgba(255,255,255,0.07–0.10)` to `rgba(255,255,255,0.13)`
- NOT applied to semantic `.tip-blk.bad/mid/good` or `.io-human/.io-ats` (preserve semantic colors)

**P1-4. Body Text Floor → 0.76**
- All body copy classes previously at `rgba(255,255,255,0.58)` now `rgba(255,255,255,0.76)`
- Covers: hook-body, ba-sub, tip-blk-text, faq-a, stat-context, timeline-desc, step-desc, lnum-desc, ig-desc, ec-body, tos-body, asym-body, diags-body, cman-body, mn-body, conn-body, sbs-body, at-body, waffle-context, io-panel-content, bas-text, bento-body
- Source/attribution lines intentionally excluded (keep their low opacity)

**P1-5. Terminal Readability**
- `.term-body`: `clamp(11px,2.2cqw,13px) → clamp(13px,2.5cqw,16px)`, line-height raised, padding increased
- `.term-cmd/ok/warn/err`: all raised to `clamp(13px,2.5cqw,15px)`
- New `.term-result` class: `clamp(15px,3cqw,19px)`, bold, accent color, top border separator — for the dramatic final line (SCORE: XX / RECHAZADO / APROBADO)
- `.tfs-body`: raised from `clamp(11px,2cqw,13px)` to `clamp(13px,2.3cqw,15px)`

**P1-6. Input/Output Panels — Asymmetric Sizing**
- `.io-human`: `flex: 42`, `.io-ats`: `flex: 58` (was both `flex: 1`)
- `.io-panel-content`: minimum 13px, max 15px
- New `.io-ats-score` class: `clamp(26px,5.5cqw,38px)`, bold, accent color, for the big result score

**P1-7. Icon Grid — Card Tiles + Featured Variant**
- `.icong-tile`: added card background `rgba(255,255,255,0.055)`, border, `border-radius:14px`, padding
- `.icong-tile.featured`: spans full row (`grid-column: 1/-1`), accent tint background, row flex layout — apply to the primary item
- `.ig-title`: min raised to 13px, `.ig-desc`: min raised to 12px, opacity raised to `0.75`

**P1-8. Before/After Columns — Stronger Tint**
- `.ba-col.bad`: `rgba(255,80,80,0.06 → 0.10)`, border `0.12 → 0.22`
- `.ba-col.good`: `rgba(78,205,196,0.06 → 0.10)`, border `0.14 → 0.22`
- New `.ba-score` + `.ba-score.bad-score/.good-score`: hero score number classes `clamp(48px,10cqw,72px)`

**P1-9. Content Scrim Utility**
- New `.content-scrim`: absolute-positioned radial-gradient scrim at z-index:3 — inject as sibling before content wrapper when AI background focal point bleeds through headline
- New `.content-scrim-bottom`: top-heavy linear gradient variant for slides with bottom focal points

### Verified
- `preflight.py` on `carousel_rrhh-no-dice-filtro_s01.html`: **100/100** — no regressions

### What was rejected
- Modifying SVG starburst fill vs stroke in CSS (requires template attribute changes, not CSS-only)
- Applying glass override to `.tip-blk.bad/mid/good` and `.io-human/.io-ats` — would destroy semantic color coding

---

## 2026-05-27 — Codex AI-bg audit: gutter trimming, scrim system, component fixes, 10 carousel rebuilds

### Fixed
- **`panel_extractor.py` — `--trim-gutters PCT`**: New flag that crops `PCT%` from all 4 edges of each panel after extraction, then resizes back to 1080×1080. Removes ChatGPT canvas margins and white/gray gutters baked into source images. Recommended: `--trim-gutters 3` for all ChatGPT grid images.
- **`panel_extractor.py` — `--fix-kit KIT_DIR`**: New post-hoc trim mode. Pass any extracted kit folder path + `--trim-gutters` to trim all `*.png` files in the kit without re-running the full extraction pipeline. Used to fix 6 failing kits this session.
- **`panel_extractor.py` — edge brightness check**: `check_bright_edges()` added. Warns `[WARN] Panel N has bright edge` if any outer 10px band has mean RGB > 228 after extraction (sign of remaining gutter). Always runs after extraction, so future crops with white borders are caught immediately.
- **`panel_extractor.py` — `--file` now optional**: Required check moved after args parse to support `--fix-kit` mode (which doesn't need `--file`).
- **6 failing background kits re-trimmed** (3% per edge, 264 PNG files updated):
  - `geo-blue-grid` (white borders) — 56 files
  - `oceanic-wave` (gray/white gutters) — 40 files
  - `glowing-energy-flow` (thin white lines) — 40 files
  - `galactic-dream-full` (thin borders) — 48 files
  - `cosmic-ribbons` (white vertical gutters) — 40 files
  - `pastel-waves` (white outer canvas) — 40 files
- **`carousel-shell.html` — scrim system rebuilt**: `.geo-ai-bg-overlay` now includes a strong pure-black scrim layer (`rgba(0,0,0, var(--ai-scrim, 0.52))`) as the first layer, replacing the weak bg-base tint approach. Photo is now properly darkened for text legibility across all dark systems.
- **`carousel-shell.html` — per-slide scrim density**: New CSS custom properties `--ai-scrim` and `--ai-photo-opacity` + `data-density` attribute modifiers: `heavy` (scrim 0.68, opacity 0.78), `demo` (scrim 0.30, opacity 0.90), `cta` (scrim 0.65, opacity 0.78).
- **`carousel-shell.html` — `.cta-reward` opacity**: Was 0.6 (invisible on AI-bg slides) → raised to 0.88.
- **`carousel-shell.html` — footer opacity (`.brand`, `.counter`)**: Was 0.42 (dead on AI-bg slides) → raised to 0.72.
- **`render_carousel.py` — `density` field injection**: Per-slide `"density"` field now read from spec and injected as `data-density` attribute on the `.slide` div. Enables the CSS scrim density system.
- **10 AI-bg carousel specs rebuilt** with density fields, Spanish accent fixes, stronger body opacity, better geo layers:
  - `rrhh-no-dice-filtro_s01` — fixed accents + density + footer opacity
  - `ats-no-lee-como-humano_s04` — fixed accents + density + body opacity 0.95
  - `experiencia-valida-formato-no_s06` — fixed accents + density + slide 3 font sizes
  - `palabras-que-busca-bot_s27` — fixed accents + density + myth/reality border upgrade
  - `cv-perfecto-no-pasa_s17` — fixed accents + density + io-panel styling
  - `tres-ajustes-doble-entrevistas_s11` — **swapped digital-glass-full → satin-waves-full** + density
  - `73-porciento-muere-filtro_s17` — fixed accents + density + 73% stat color to var(--accent)
  - `cincuenta-a-cinco_s21` — fixed accents + density + replaced tag-cloud with hook-lockup slide 1
  - `errores-6-segundos_s01` — **swapped pastel-waves → glass-panel-full** + density + terminal fix
  - `reclutador-vs-bot_s25` — fixed accents + density heavy on all 4 slides + slide 1 redesigned to hook-lockup

### Added — Rules
- **`.claude/rules/carousel-layout-checks.md`** — New section "AI-Background Carousels — Additional Rules" with 7 rules + AI-background pre-export checklist:
  1. Every slide MUST declare `"density"` in spec
  2. Background kit must pass sanity + edge brightness check before use
  3. Spanish accents are MANDATORY
  4. Card backgrounds: minimum `rgba(255,255,255,0.07)` on dark systems
  5. Body text opacity ≥ 0.88 on AI-bg slides
  6. Background focal safety check
  7. Max 1 starburst per AI-bg carousel
- **`CLAUDE.md`** — AI background pipeline docs updated with `--trim-gutters`, `--fix-kit`, ChatGPT prompting rule, per-slide `density` field reference.

### Background kits status (after fixes)
- `satin-waves-full` ✓ Clean
- `energy-flow-full` ✓ Clean
- `glass-panel-full` ✓ Clean
- `geo-blue-grid` ✓ Fixed (trimmed)
- `oceanic-wave` ✓ Fixed (trimmed)
- `glowing-energy-flow` ✓ Fixed (trimmed)
- `galactic-dream-full` ✓ Fixed (trimmed)
- `cosmic-ribbons` ✓ Fixed (trimmed)
- `pastel-waves` ⚠ Trimmed but content is light/pastel — do NOT use on dark systems
- `digital-glass-full` ✗ Irregular grid — panels are structurally bad — DO NOT USE

### What was rejected / deferred
- Complete re-generation of bad background kits in ChatGPT — not needed, trim fixes the extraction issues
- Per-panel art-direction rules (focal point analysis per panel) — too complex to automate, added as manual check to pre-export checklist

---

## 2026-05-23 — AI Background panel extraction fix + light-system overlay fix

### Fixed
- **panel_extractor.py — "always extract everything" policy**: Filename panel count now takes hard priority over visual seam detection. Added `[COUNT]` logging for full traceability. Safety check added: if `rows*cols < n_panels` after seam detection, script re-computes layout with math-based fallback instead of silently truncating.
- **panel_extractor.py — sanity check**: `_sanity_check_panels()` added. After extraction, measures center-edge gradient in each panel. If a strong seam runs through the middle (mean diff > 18), prints `[SANITY] WARNING` — catches bad crops that contain 2 sub-panels before they land in the manifest.
- **panel_extractor.py — old `min(n_panels, rows*cols)` cap removed**: This was the line that silently accepted fewer panels than expected when seam detection underperformed.
- **carousel-shell.html — light-system AI background overlay**: `.light-system .geo-ai-bg-overlay` now applies `rgba(0,0,0,0.48-0.62)` dark scrim instead of a white wash. White bg-base systems (S25 Swiss Brut, S26, etc.) now get a properly darkened AI photo background that doesn't bleed through transparent card content.
- **6 source images re-extracted** with correct panel counts (all panels always stored):
  - `geo-blue-grid` (8 panels, was `blue-geometry` with only 4) — s01/s04/s08/s17/s25/s29
  - `glass-panel-full` (8 panels, was `glass-panel` with only 4) — s01/s04/s11/s17/s25/s27
  - `satin-waves-full` (8 panels, was `dark-satin` with only 4) — s01/s04/s11/s17/s21/s25
  - `energy-flow-full` (6 panels, was `futuristic-flow` with only 4) — s01/s04/s06/s17/s25/s29
  - `digital-glass-full` (6 panels, was `digital-glass` with only 4) — s04/s06/s08/s11/s25/s27
  - `galactic-dream-full` (8 panels, adds s21 missing from original) — s04/s06/s11/s21/s29
- **7 specs patched**: replaced bad background IDs with correct ones; `errores-6-segundos` system changed s25 → s01 (SWISS BRUT is a light system — incompatible with AI photo backgrounds without the dark scrim fix).
- **All 10 ai-bg carousels re-rendered**: 10/10 pass preflight with zero FILs.

### Root cause (for future reference)
The Kimi extension was calling `panel_extractor.py --panels <slide_count>` (e.g. `--panels 4`) when extracting for a 4-slide carousel, instead of `--panels <image_panel_count>`. This extracted exactly 4 panels from 8-panel source images — each "panel" contained 2 original sub-panels squashed to 1080x1080, creating a visible vertical split in the rendered carousel backgrounds.

### Affected carousels (now fixed)
`carousel_cv-perfecto-no-pasa_s17`, `carousel_reclutador-vs-bot_s25`, `carousel_rrhh-no-dice-filtro_s01`, `carousel_experiencia-valida-formato-no_s06`, `carousel_tres-ajustes-doble-entrevistas_s11`, `carousel_cincuenta-a-cinco_s21`, `carousel_errores-6-segundos_s01`

### Note
Old broken HTML `carousel_errores-6-segundos_s25.html` is still in production/ — safe to delete.

---

## 2026-05-25 — Premium Makeover: All 48 Systems + Shell + CTA + Gallery

### Summary
Full 6-phase makeover of the entire carousel builder. Fixed typography hierarchy across all 48 systems, upgraded CSS to premium visual standard, rebuilt CTA slide, and regenerated all 248 gallery files.

### Phase 1a — `scripts/component_data.json`
- Expanded from 11 systems to **all 48 systems** (s01–s48) with full tokens: `--bg-base`, `--bg-mid`, `--accent`, `--text-primary`, `--text-secondary`, `--font-display`, `--font-body`, `--font-mono`, `--grain-opacity`, `--geo-opacity`
- Fixed s20 (Roboto+Roboto → Space Grotesk+Inter), s29 body (Inter → JetBrains Mono), s33 display (Inter → DM Sans), s12 display (Inter → DM Sans), s16 display (Inter → Space Grotesk)
- Corrected two invisible-accent bugs: s41 #111827 → #c084fc (purple), s43 #111827 → #ff006e (pink)
- Font substitutions for removed families: Montserrat→Space Grotesk (s02), Outfit→Poppins (s14), Lato→Work Sans (s30), Sora→Poppins (s31), Roboto→Space Grotesk (s20), Roboto Mono→JetBrains Mono (s40/s46), Source Sans 3→DM Sans (s23/s47)

### Phase 1b — `scripts/render_carousel.py`
- Replaced per-system `GOOGLE_FONTS` dict (8 entries) with `UNIVERSAL_FONTS_URL` — single 16-family Google Fonts URL covering all 48 systems
- `build_fonts_url()` now returns the universal URL regardless of system_id
- 16 families: Archivo, Cinzel Decorative, Cormorant Garamond, Crimson Pro, DM Sans, IBM Plex Sans, Inter, JetBrains Mono, Noto Sans, Noto Sans JP, Noto Serif, Nunito, Poppins, Source Serif 4, Space Grotesk, Work Sans

### Phase 2 — `templates/carousel-shell.html` (CSS overhaul)
- Added 5 luminosity hierarchy CSS vars to `:root`: `--lum-cta: 0.95`, `--lum-active: 0.75`, `--lum-headline: 0.55`, `--lum-body: 0.35`, `--lum-geo: 0.10`
- Geo opacity reductions (~20% cut): mesh-noise 0.14→0.11, pixel-grid 0.12→0.09, conic-rays 0.05→0.04, chevron-stripe 0.06→0.05, iso-grid 0.08→0.06, halftone 0.18→0.14, topo-lines 0.10→0.08, starfield 0.55→0.44, gradient-bands 0.10→0.08, blob-bg 0.18→0.14, contour-flow 0.12→0.10 (+ light-system variants)
- Border thinning: faq-item, comp-card, sub-fact-bubble, poster-eyebrow 3px→1.5px
- Font-weight caps (900→700): sub-stamp-circle, sc-num, sub-inline-stat, gp-num, lnum-num, hook-display, stat-num, pbar-value, warn-headline, donut center-num, hook-big-stat, hook-from-to val, poster-display, plus 17 extended layout classes
- Letter-spacing widening: brand 0.14→0.24em, counter 0.12→0.24em, sub-pill-tag 0.10→0.14em, sub-status-pill 0.10→0.12em, plus 9 label classes
- Added 4 premium utility CSS classes: `.premium-glow` (4-layer box-shadow formula), `.glass-card` (glassmorphism base), `.deco-corner-tl`/`.deco-corner-br` (L-bracket decoratives), `.headline-glow` (subtle text-shadow)

### Phase 3 — `templates/slides/slide-cta.html` full restyle
- CTA pill button: border:2px→1.5px, border-radius:14px→999px, padding:18px 44px→18px 52px
- Glassmorphism: `backdrop-filter:blur(12px)`, gradient background, replaces flat rgba
- 4-layer premium glow formula on `.cta-keyword-box` (hover intensifies)
- `.cta-keyword`: font-weight:900→500, letter-spacing:0.07em→0.38em, size scaled down slightly
- `.cta-question`: font-weight:800→700, added `text-shadow:0 0 12px rgba(255,255,255,0.08)`
- Template HTML: added `.deco-corner-tl` + `.deco-corner-br` + SVG 8-point star with glow filter above headline

### Phase 4 — Shell CSS extended layout pass (via `_patch_shell_p4.py`, deleted after)
- 17 more font-weight 900→700 fixes: stamp-value, header-logo, sub-arrow-flow, warn-icon, proof-result-num, txt-gradient text, t-display, diags-headline, diags-stat, asym-headline, tos-headline, cman-headline, ck-top-text, wfl-num, at-headline, conn-headline, waffle-number
- 10 letter-spacing adjustments on label/tag elements
- Text-shadow added to: hook-display, diags-headline, asym-headline, conn-headline

### Phase 5 — `.claude/skills/html-carousel-builder/carousel-master-ref.md`
- Rewrote entire 48-system table with correct Display/Body font pairings
- Every system now shows explicit font name + weight (e.g. "Space Grotesk 700 / Inter 300")
- Fixed all font substitutions, corrected accent colors for s41 and s43

### Phase 6 — Gallery rebuild
- `py scripts/build_gallery.py` → **248/248 demos rendered** (was 246 + INDEX)
- All gallery files rebuilt from updated shell + templates, incorporating all v4 premium changes

### What was rejected / deferred
- Reducing font-weight to 900 on extreme decorative-only elements (`.deco-watermark`, `.sbs-big`, `.mn-number`, `.fbt-display`, `.stype-line-1`) — these are intentional bold display type at large sizes, not content headlines
- Full font audit of production carousels — those were built with old tokens, will pick up new fonts on next render automatically (render engine reads component_data.json fresh each time)

---

## 2026-05-25 — AI Background Panel Extraction System

### Added
- **`scripts/panel_extractor.py`** — new standalone script. Takes one AI-generated grid image (N panels arranged in a grid), extracts each panel, resizes to 1080x1080, color-adapts to design systems via numpy vectorized HSV, applies visual treatments, and updates `brand/generated-bg/manifest.json` with `recipe_variants["extracted"]`. The render pipeline picks up extracted panels per-slide automatically — zero changes to `render_carousel.py`.
  - Args: `--file`, `--panels`, `--grid "rows,cols"`, `--name`, `--output`, `--systems`, `--treatments`, `--no-variants`, `--preview`, `--compare`, `--manifest`
  - `--preview` mode: draws yellow panel borders on a scaled image so user can confirm crop before running
  - `--compare` mode: generates a matplotlib-style grid visualization (systems as rows, panels as cols) — the "1 image → 20 slides" kit overview
  - Grid auto-detection scores squareness (30%) + fill efficiency (30%) + orientation match (40%) — correctly detects panoramic strips as `1xN` instead of guessing a square grid
  - Color adaptation: numpy vectorized HSV (fast, no per-pixel loops). Auto-detects source dominant hue via circular-mean; no `--hue` argument needed
  - Treatments built-in: `none`, `glow`, `deep`, `soft`, `warm`
  - `--no-variants` writes manifest with `original.png` paths (usable by render pipeline)
  - DESIGN_SYSTEMS dict covers s01, s04, s06, s08, s09, s11, s16, s17, s20, s21, s25, s27, s29, s33
- **`ideation/ai-backgrounds/panels/`** — new input drop folder for grid source images
- **s20 (Y2K CHROME) tokens** added to `scripts/component_data.json`: `bg #03060f`, `accent #44f5ff`, `font Roboto`
- **`production/carousel_vector-field-y2k_s20.html`** — 4-slide WorqAI carousel built as end-to-end test of the new system. s20 Y2K Chrome + `vector-field-distortion` AI background (`recipe_variants["extracted"]`). Score: 100/100 preflight.
- **`production/spec_vector-field-y2k-s20.json`** — spec file for above carousel

### Changed
- **`scripts/render_carousel.py`** — `load_tokens()` now uses `encoding="utf-8-sig"` (BOM-resilient; future PowerShell JSON edits won't break token loading)
- **`scripts/adapt_image_bg.py`** (existing) — unchanged; remains the single-image flat-variant pipeline. `panel_extractor.py` is self-contained and parallel to it, not a replacement.

### Fixed
- Kimi audit applied to `panel_extractor.py` before first use:
  - Grid orientation scoring fixed (was `squareness * 0.70` — last term was duplicate, not orientation)
  - Numpy divide-by-zero warnings suppressed via `warnings.filterwarnings`
  - `--no-variants` now still writes manifest entries
  - Redundant inner `np.where` removed from `_rgb_to_hsv_np`
- `scripts/component_data.json` corrupted by PowerShell `ConvertFrom-Json | ConvertTo-Json` round-trip (outer `{` dropped). Restored via `git checkout`, s20 re-added using Python directly.

### How the pipeline works
```
1. Generate grid image in ChatGPT (e.g. "5 panels in a 1x5 or 2x3 grid, continuous scene")
2. Drop PNG into ideation/ai-backgrounds/panels/
3. py scripts/panel_extractor.py --file grid.png --panels 5 --name "My Scene" --systems s17,s20
4. manifest.json updated with recipe_variants["extracted"]
5. Use in spec: "layers": ["my-scene"], "bg_recipe": "extracted" (in meta)
6. py scripts/render_carousel.py spec.json  (picks up panel_01 → panel_N per slide automatically)
```

### Rejected / deferred
- Panoramic strip crop approach (`crop_panoramic.py`) — planned in previous session, superseded by panel extraction from grids. The grid approach is simpler to generate (one ChatGPT image, any layout) and produces more compositionally varied panels.
- Algorithmic warping recipes (`glow_bloom`, `deep_zoom`, `phase_distort`) remain in `transform_bg_v2.py` but are no longer the recommended approach for background continuity. Panel extraction produces visually superior results.

---

## 2026-05-18 — Phases 1-3: 16 Geo Layers + 4 Layouts + Continuity + Gallery Expansion

### Added
- **Phase 1 — 3 demonstration layouts + 1 geo layer + glassmorphism**:
  - `templates/slides/slide-waffle-chart.html` — 10×10 proportion grid, `copy.filled` (0-100) controls accent-glow squares
  - `templates/slides/slide-input-output.html` — side-by-side ATS demo panels: "what you wrote" vs "what the ATS sees"
  - `templates/slides/slide-before-after-stacked.html` — stacked before/after panels with VS badge + progress bars (coexists with column-based `slide-before-after`)
  - `geo-contour-flow` — flowing topographic contour lines in `LAYER_HTML` + `carousel-shell.html`
  - `.glass-panel` / `.glass-panel-fallback` CSS in `carousel-shell.html` — `backdrop-filter: blur(24px)` with solid-gradient fallback for html2canvas
  - `--accent-rgb` auto-derivation in `render_carousel.py` (`_hex_to_rgb`) for `rgba()` usage in layers
- **Phase 2 — 6 geo layers + dict-based continuity**:
  - `geo-perspective-grid` — CSS 3D wireframe receding to vanishing point (**PLAYWRIGHT ONLY**: uses `perspective()` + `mask-image`)
  - `geo-hex-mesh` — SVG pattern hexagonal tessellation
  - `geo-constellation` — pre-generated SVG dots + lines static network
  - `geo-neon-ring` — multi-layer SVG glowing aura ring (4 circles, varying stroke-width + opacity)
  - `geo-bokeh` — CSS radial-gradient blur orbs using `--accent-rgb`
  - `geo-scan-lines` — CRT texture overlay with `mix-blend-mode: overlay`
  - `resolve_continuity()` in `render_carousel.py` now supports **dict-based config** with `shape`, `path`, `positions[]` — same SVG path, different `transform`/`opacity` per slide
- **Phase 3 — 3 geo layers + gallery + docs**:
  - `geo-chromatic-edge` — RGB lens aberration bleed at viewport edges via CSS linear-gradients
  - `geo-data-streaks` — static diagonal 45° stream lines using SVG `<line>` strokes
  - `geo-liquid-morph` — metaball intersections via SVG `feGaussianBlur` + `feColorMatrix` goo filter
  - `scripts/build_gallery.py` expanded from 50 → 64 demos: all 10 geo layers, 3 layouts, and `glass-panel` sub-component
- **Preflight updates** (`scripts/preflight.py`):
  - `slide-before-after-stacked` added to demonstration-layout CSS-class validation
  - Demonstration layout check expanded to include `slide-input-output` and `slide-waffle-chart`

### Changed
- **`.claude/skills/html-carousel-builder/SKILL.md`** — v9 note expanded: 10 new geo layers, dict-based custom-path continuity, `slide-before-after-stacked`, non-circular shape preference, glassmorphism panel
- **`.claude/skills/html-carousel-builder/carousel-master-ref.md`** — Geo layers table updated (+10 entries), demonstration layouts updated (+`slide-before-after-stacked`), continuity section updated with dict-based `positions[]` spec syntax

### Problems hit
- **`build_gallery.py` edit failures**: Smart quotes (`"` / `"`) and UTF-8 middle dot (`·`) in existing demo entries made `StrReplaceFile` fail. A `content.rfind(']')` approach corrupted the file by matching a `]` inside a Python `print()` string literal instead of the `DEMOS` list closing bracket. **Fixed** by restoring from git and using precise boundary string matching.
- **Phase 2 preflight noise**: Test spec had incomplete CTA + language-mix false positives (test data issues, not production bugs).
- **4 pre-existing gallery build failures** unrelated to these changes: `geo-iso-grid`, `geo-paper-texture`, `geo-topo-lines` (Windows `OSError: [Errno 22] Invalid argument` — likely filename encoding), and `slide-comparison-table` (`'builtin_function_or_method' object is not iterable` — template bug).

### Rejected / deferred
- **Gallery numbering schema**: Keeping simple `01-64` sequential numbering. No category-prefix scheme needed.
- **CSS tree-shaking**: Same deferral as prior entry — complex refactor, low ROI. File size already passes at 80-115 KB.
- **Visual regression gate (screenshot pixel-diff)**: Complex, marginal ROI. Rule-based QA is sufficient.

---

## 2026-05-18 — v9 Enforcement + Premium Layouts + Visual Continuity (revised)

### Added
- **3 new demonstration layouts** (`templates/slides/`):
  - `slide-input-output.html` — side-by-side "what you wrote vs what ATS sees" panels with arrow + check/X icons
  - `slide-waffle-chart.html` — 10×10 grid, `copy.filled` (0-100) controls accent-filled squares
  - `slide-cross-slide-connector.html` — continuity anchor layout for flow layers
- **6 new non-circular blob shapes** (`render_carousel.py` + `carousel-shell.html`): `svg-blob-angular`, `svg-blob-crystal`, `svg-blob-wave`, `svg-blob-arch`, `svg-blob-splatter`, `svg-blob-ribbon`. All use data-URL SVG with accent hex substitution.
- **3 flow layers** (`carousel-shell.html`): `geo-flow-wave`, `geo-flow-arrow`, `geo-flow-data` — CSS/SVG-based directional elements.
- **Glassmorphism panel component** (`carousel-shell.html`): `.sub-glass-panel` with `backdrop-filter: blur(24px)`, semi-transparent bg, top highlight line. Playwright-only.
- **Cross-slide continuity system** (`render_carousel.py`): optional `meta.continuity` field with modes `wave`, `data-pipeline`, `corner-frame-evolution`, `number-escalator`. Auto-injects per-slide continuity HTML, disables decorative rotation when active.
- **Preflight expanded from 18 → 22 checks** (`scripts/preflight.py`):
  - Badge Collision: FAIL if `chrome-badge-stamp` overlaps headline or right-aligned text
  - Shape Diversity: FAIL if any single shape appears on >4 slides
  - Decorative Repetition: WARN if same decorative on >2 consecutive slides
  - Demonstration Layout: FAIL if zero demonstration layouts (input-output, waffle-chart, before-after, etc.)
- **Visual richness expanded** (`scripts/visual_richness_check.py`):
  - Blob Overuse: FAIL if any blob/orb >2× or total soft circles > slides × 1.2
  - Layer Combo Repetition: FAIL if >50% slides share identical layers or >3 consecutive same combo
- **Skill + master reference updated** (`SKILL.md`, `carousel-master-ref.md`): v9.0 rules — decoration purpose statement, shape diversity cap, demonstration requirement, reference gallery review, non-circular preference.
- **Demo carousel built**: `production/carousel_showcase-v3_s29.html` — s29 cyberpunk, 5 slides, hook/diagnostic/data/solution/cta. Scored 95/100 preflight, 100/100 visual richness. Uses angular, crystal, wave, splatter, ribbon blobs + input-output + waffle-chart layouts.

### Fixed
- `check_demonstration_layout()` in `preflight.py` now detects wrapper class fragments (`io-wrap`, `waffle-wrap`, `ba-wrap`, etc.) instead of relying on non-existent `layout-` CSS classes.

### Problems hit
- **Anti-slop false positives**: `border-left` in `slide-comparison-table`, `slide-faq-stack`, `slide-side-by-side`, and `slide-minimal-card-stack` template CSS triggers ANTI-SLOP even when those layouts aren't used. The shell ships all 48 layouts' CSS regardless of which 5 are active. Root cause: no CSS tree-shaking.
- **Continuity features fundamentally incompatible with Instagram export**: `geo-flow-wave`, `geo-flow-arrow`, `slide-cross-slide-connector`, and all 4 continuity modes assume a continuous canvas. Instagram carousels export as separate PNGs — the wave/progression/nodes are invisible to users swiping one slide at a time.

### Rejected / deferred
- **CSS tree-shaking**: Complex refactor, low ROI per triage feedback. File size check already passes at 80-113 KB.
- **Cross-slide continuity modes**: Kept in code (`meta.continuity` still works) but marked as deprecated for Instagram use. May be viable for PDF or web-embedded carousels where slides are viewed in sequence on one screen.
- **Visual regression gate (screenshot pixel-diff)**: Complex, marginal ROI. Better to fix rules so bad layouts don't ship.

---

## ~2026-05-13 — Architecture redesign: 5-layer separation of generation vs. composition

### Read and analyzed
- `ideation/feedbackonarchitecture.md` — 565 lines of cross-model feedback from Claude, Gemini, and ChatGPT. All three models converged on the same diagnosis: the AI had too many jobs simultaneously (creative director, layout selector, copywriter, HTML assembler, QA reviewer). The core insight: **separate GENERATION from COMPOSITION**.

### Architecture planning (plan mode → approved)
- **Target architecture defined:** 5-layer system:
  - L1: Frozen Infrastructure (parameterized component templates, 12 curated visual sets)
  - L2: Layout Composer (JSON spec output)
  - L3: Creative Director (AI outputs structured brief → JSON spec only, never HTML/CSS)
  - L4: Deterministic Render Engine (`render_carousel.py`)
  - L5: Deterministic QA (bounding-box overflow + stat source validation)
- **Revised phase order agreed:**
  1. Phase 0: Fix stat fabrication (live credibility risk)
  2. Phase 1A: Spec schema + brief template (foundation)
  3. Phase 1B: Component curation + usage audit (parallel with 1A)
  4. Phase 2: Render engine + parameterized templates
  5. Phase 3: AI skill refactor (only after render engine exists)
  6. Phase 4: Deterministic QA v2
- **Rejected gradual migration (Option B).** The user explicitly agreed that incremental approaches create a hybrid mess — maintaining two pipelines simultaneously with no quality benefit. Full pivot only.

### Phase 0: Stat fabrication fix (executed)
- **Modified** `.claude/skills/html-carousel-builder/build.md` — replaced the permissive "Source policy" (~lines 509–513) with a **ZERO TOLERANCE** policy:
  - Verified source allow-list: `Jobscan internal analysis`, `WorqAI database`, `LinkedIn Economic Graph`, `World Economic Forum · Future of Jobs Report`, `Análisis interno Profile Pro LATAM`
  - Explicitly banned fabricated phrases: `"LinkedIn Talent Report 2025"`, `"Jobscan ATS Report 2024"`, `"Jobscan ATS Optimization Report 2024"`, `"Jobscan · State of the Job Search 2023"`, `"LinkedIn Talent Solutions Report 2024"`
  - Default fallback: `Dato interno WorqAI · base de datos 2025`
  - Mandatory `<!-- STAT_REVIEW_REQUIRED -->` HTML comment on any external source
- **Modified** `.claude/skills/html-carousel-builder/workflow.md` — added "Stat source clean" as a binary check in the Ship Gate checklist.
- **Created** `scripts/stat_source_validator.py` — Python regex scanner that validates source tags against the allow-list, flags fabricated patterns, exits non-zero if issues found.
- **Patched 14 production carousels** to remove fabricated/unverifiable stat citations:
  - `carousel_0-a-4-entrevistas_crimson.html`
  - `carousel_ats-te-elimino_cyberpunk.html`
  - `carousel_ats-latam_worqai-verde.html`
  - `carousel_consejo-cv-esta-mal_brutalist.html`
  - `carousel_cv-no-entrevistas_worqai.html`
  - `carousel_cv-silencio-reclutadores_glass.html`
  - `carousel_linkedin-fantasma_aurora.html`
  - `carousel_pdf-ats-error_worqai-verde.html`
  - `carousel_tu-cv-nunca-fue-leido_worqai.html`
  - `carousel_aplicar-usa-latam_worqai.html`
  - `carousel_ats-espanol-bombas_worqai.html`
  - `carousel_ats-data-dashboard_beyond-elite.html`
  - `carousel_negociacion-salarial_terra.html`
  - `carousel_cv-silencio-reclutadores_glass.html` (TheLadders attribution)

### Phase 1A: Spec schema + brief template (executed)
- **Created** `scripts/carousel-spec.schema.json` — formal JSON Schema for carousel specs:
  - `meta`: system, aspect, slides, brand, language, set, density
  - `pacing`: emotional arc array (hook, shock, proof, data, diagnostic, solution, hope, relief, action, cta, silence, break, myth, reality, testimonial, urgency)
  - `slides[]`: id, layout, layers, decoratives, mock_ui, copy slots (kicker, headline, body, stat_number, stat_context, source, command, output_lines, before/after items, quote, attribution, question, cta_keyword, reward, url, tips, items)
  - `constraints`: max_weight, technique_budget, decorative_budget, mock_ui_required, silence_slide_required, subtraction_gate, file_size_target_kb
- **Created** `scripts/brief-template.yaml` — Creative Director constraint layer:
  - Topic, angle, one_truth, transformation_promise
  - Audience (who, pain, desired_state)
  - Emotional arc, tone_register, forbidden phrases/framings/visuals
  - verified_stats array with source and verified flag
  - proof_case (name, location, result, mechanism)
  - Technical hints (system_hint, aspect_ratio, slides_count, brand)

### Phase 1B: Component usage audit (started, not completed)
- Read `components/_INDEX.md` (181-component inventory).
- Identified that a usage audit is needed to find the top 20% of components that drive 80% of production output before building the render engine.
- **Not yet completed:** actual scan of production HTML files to rank component usage.
- **Not yet completed:** curation of 12 validated visual language sets.

### Problems hit
- **Python unavailable in Windows shell.** `python`, `py`, and `python3` were all blocked by Windows App Execution Alias (redirected to Microsoft Store). `stat_source_validator.py` was written but could not be executed. Relied on grep-based manual patching instead.

### What was broken/unfinished at the end
- `scripts/stat_source_validator.py` unverified (no Python runtime).
- Phase 1B usage audit incomplete.
- `component_sets.json` not created.
- `render_carousel.py` not started.
- AI skill still outputs full HTML/CSS (skill refactor gated behind render engine).
- No bounding-box QA (`preflight-v2.py`).

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

## 2026-04-30 — Premium carousel studio: 15 files, 8-step pipeline, two brands

*From Perplexity Spaces snapshot. All files created April 30, 2026.*

### What the Space became
Fully automated pipeline to build export-ready HTML carousel ads (1080×1080px) for two brands:
- **WorqAI** — SaaS product, CTA "Sign up free", Spanish (LATAM-neutral)
- **Profile Pro LATAM** — Done-for-you service, CTA "Book consultation", Spanish (es-CR)

Brands never mixed in the same ad; separate design systems enforced.

### The 8-step pipeline
1. Customer Moment Brief — viewer identity, feeling, promised shift
2. Hook Selection — 5 hook types (Result, Question, Contrarian, Curiosity, Negative); headline ≤8 words
3. Copy Writing — 8-slide narrative arc: Hook → Data → 4 Tips/Errors → Proof → CTA
4. System Selection — Selection Intelligence matrix picks 1 of 47 visual design systems
5. HTML Build — single self-contained 1080×1080 HTML file with full CSS, Google Fonts, blobs, geometry, grain
6. Export — `scripts/carousel-exporter.py` → slide01.png…slideN.png + carousel.zip
7. Quality Check — anti-slop sweep + Taste Score
8. Deliver — move final PNGs/ZIP to `/export/` ready for Meta Ads Manager upload

### All 15 files in the Space
**Master Skill Files (the brains):**
- `ads-agent.md` — main agent brain: two brands, full pipeline, campaign types, rules, quality checks
- `carousel-builder-skill.md` — HTML carousel builder skill; produces self-contained 1080×1080 HTML
- `design-systems-skill.md` — index of all 47 visual design systems; maps which sub-files to load for CSS tokens

**Workflow & Copy Files:**
- `workflow.md` — full 8-step execution pipeline with every CSS rule, HTML structure, VAR token replacement, aspect ratio specs, Google Fonts URL construction
- `copy-dna.md` — voice, hook psychology, narrative arc, per-slide copy frameworks, stat source policy (never fabricate stats), proof specificity ladder, CTA formula, LATAM sub-locale localization
- `anti-slop.md` — master banned-word list across all languages (hype words, empowerment fluff, corporate jargon, AI conversational tells)

**Design System Files (the visuals):**
- `systems-core.md` — full CSS tokens, hex colors, fonts, blob specs, background architecture for Systems 01–17, including locked WorqAI brand system (System 17: WORQAI VERDE)
- `systems-extended-a.md` — CSS tokens for Systems 18–32 (Riso Lab, Warm Sand, Glassmorphism variants, Brutalist color blocks)
- `systems-extended-b.md` — CSS tokens for Systems 33–47 (Clean SaaS 2026, Blueprint Systems, Architectural Dark, Swiss Grid)
- `selection-intelligence.md` — decision engine for picking the right system via message type × audience matrix, subtraction rules (texture, typography, color, density), 9 master visual archetypes, Style DNA framework

**Geometry & Visual Architecture Files:**
- `geometry-modules.md` — all geometry modules (wave flows, neural meshes, topographic contours, metaballs, ribbons, fractal branches, particle fields) with SVG/CSS code
- `continuity-engine.md` — panoramic continuity rules across slides — background feels like one continuous scene rather than 8 isolated slides
- `blobs-textures.md` — library of all blob shapes (Fluid Organic, Wave Sweep, Bottom Swell, Corner Slash, Radial Glow), grain textures, layering rules per system
- `layouts.md` — all slide layout templates: big stat hero, comparison columns, checklist, pull quote, bento grid, timeline, before/after, myth vs. reality
- `css-effects.md` — advanced CSS recipes: glassmorphism panels, neon glows, grain overlays, chromatic fringe, volumetric light, backdrop-filter tricks, browser export compatibility notes

### Hard rules (never violated)
- Never fabricate stats or third-party study names
- Never use gradient-only backgrounds — always layer geometry + texture + grain
- Never repeat the same layout on consecutive slides
- Every carousel must pass anti-slop sweep before delivery
- WorqAI always uses System 17 WORQAI VERDE; Profile Pro LATAM defaults to System 12 WARM SAND or System 23 QUIET LUXURY SAND

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

## 2026-04-20 — 7-file creative production Space

*From Perplexity Spaces snapshot. All 7 files added April 20, 2026.*

### What the Space was
Premium social media ad creative production toolkit — end-to-end workflow for agency-level Instagram/Facebook ad creatives. Write copy → design carousel → export as images → post.

### The 7 files
1. **`html-carousel-builder-v2.md`** (Main Builder Spec) — full spec for premium self-contained 1080×1080px HTML carousels with 8 style systems, SVG blobs, grain textures, glassmorphism effects, swipe navigation. Anti-slop rules and quality checklists to ensure human-made designs.
2. **`html-carousel-builder-SKILL.md`** (Skill Shortcut) — distilled skill trigger version for quick AI loading; covers gradients, animated SVGs, grain textures, navigation.
3. **`design-systems.md`** (Style Reference Library) — 8 complete named style systems (Noir Gold, Royal Blue, etc.) with full color palettes, typography rules, blob SVG libraries, grain CSS.
4. **`ad-creative-generator.md`** (Full Ad Creative System) — broadest file; covers carousels, static briefs, image prompts, UGC scripts, copy decks — all with strict anti-AI-looking rules for Facebook/Instagram.
5. **`human-voice-writer.md`** (Copywriting Voice System) — authentic human-sounding text for Reddit, social media, ad copy in English and Spanish; anti-AI-detection filters, tone rules.
6. **`carousel-to-zip-exporter.md`** (Exporter Skill Guide) — documentation for exporting finished HTML carousel into sequentially numbered PNGs packaged in a ZIP file.
7. **`carousel_exporter.script.txt`** (The Python Script) — runnable script that auto-installs Playwright and Pillow, detects carousel slides automatically, renders each one, packages into ZIP.

### Workflow
Write copy (`human-voice-writer.md`) → Design carousel (`html-carousel-builder-v2.md` + `design-systems.md`) → Generate full ad (`ad-creative-generator.md`) → Export (`carousel_exporter.script.txt`) → Post (upload numbered slides to Instagram/Facebook)

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

## 2026-03-31 — ad-creative-generator.md: first carousel builder skill

*From Perplexity Spaces. File created March 31, 2026. Space development: March 25 – April 20, 2026.*

### What it did
Skill activated when the user asked to build a carousel, visual ad, or HTML preview for Instagram/Facebook. Part of the Profile Pro LATAM system built by Kenneth Valverde.

### 5 output formats
1. **HTML Carousel** — complete self-contained mobile-first swipeable HTML (vanilla JS/CSS only), simulating Instagram/Facebook carousel on phone
2. **Static Ad Brief** — pixel-exact spec for Canva/Figma with all layers defined (headline, body, CTA, brand)
3. **AI Image Prompt** — complete prompt packages for Midjourney, DALL-E 3, Firefly, Stable Diffusion (4 mandatory blocks)
4. **UGC Video Script** — timestamped 15–30 second vertical video script written as real human voice
5. **Carousel Copy Deck** — all 8 slides' copy ready to paste into Canva with per-slide design directions

### HTML Carousel structure (8 slides)
| Slide | Content |
|---|---|
| 1 | Hook — big bold pain statement, nothing else |
| 2 | Data — hard stat with attribution |
| 3–6 | One error per slide + its fix, left-aligned |
| 7 | Social proof — anonymous result or screenshot |
| 8 | CTA — one action, one destination |

### Anti-slop design rules
- No gradients on buttons (solid color only)
- No white background with bright colors (default: `#0a0f1e` navy dark or black)
- No colored-circle icons as feature markers
- No fully centered layout (body text left-aligned)
- No two ideas on the same slide (each slide has ONE job)
- Default colors: background `#0a0f1e`, text `#FFFFFF`, accent `#FFD700`

### Required inputs before generating anything
- Format — which of the 5 output types
- Service/product — what is being advertised (specific)
- Target persona — one human, their situation and current frustration
- Hook type — result, question, contrarian, curiosity, or negative/loss
- Platform — Instagram feed 4:5, Stories 9:16, Facebook feed 1:1, etc.
- Language — Spanish by default
- Brand inputs — colors, font, logo or name

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
