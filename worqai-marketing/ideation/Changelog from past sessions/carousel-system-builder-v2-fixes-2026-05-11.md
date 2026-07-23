# Changelog: Carousel System Builder v2 Fixes + Scripts

**Date:** 2026-05-11  
**Session type:** Plan execution (5 fixes + 2 scripts)  
**Based on:** User feedback from a previous chat about improving the carousel builder system

---

## 1. What We Built or Changed

### Files created or modified

| File | Action | What changed |
|------|--------|-------------|
| `templates/carousel-shell.html` | **Rewritten** | Inlined all base CSS (~94 lines), grain CSS, nav JS (~31 lines), and ZIP export JS (~55 lines) that previously lived in `build.md`. Now uses `VAR_*` placeholders throughout. The agent copies the shell and replaces tokens instead of copy-pasting CSS/JS blocks. |
| `.claude/skills/html-carousel-builder/build.md` | **Trimmed** | Dropped from ~490 lines to ~290 lines. Removed CSS template, JS navigation, ZIP export code blocks, and grain CSS template. Kept only decision logic: layouts, hook patterns, voice DNA, copy frameworks, anti-slop, ship gate, platform deltas, localization, aspect ratio overrides, and visual continuity rules. |
| `.claude/skills/html-carousel-builder/workflow.md` | **Rewritten Step 4** | Added explicit copy-paste-replace instructions. Lists every `VAR_*` token with what value to substitute (e.g. `VAR_FONT_STACK` → font-family stack, `VAR_GRAIN_OPACITY` → grain value from compact matrix). Also lists all structural placeholders (`{{TITLE}}`, `{{SLIDES_HTML}}`, `{{DOTS_HTML}}`, etc.). |
| `.claude/agents/ads-agent.md` | **Rewritten** | Updated from old design-systems skill references to new 3-tier system. Removed all deprecated sub-modules (`layouts-a.md`, `layouts-b.md`, `rl-core.md`, `type-architecture.md`, `motion-effects.md`, etc.). Added build modes (`fast`/`standard`/`verbose`). Added references to new scripts (`apply_tokens.py`, `build_orchestrator.py`). |
| `carousel-matrix.yaml` | **Updated to v2.1** | Added `custom_build` fallback section, `build_mode: "standard"` to all 12 presets, `techniques_required: true/false` to all presets. Auto-populated production index with **47 entries** scanned from `production/*.html`. |
| `scripts/apply_tokens.py` | **Created** | Post-process script. Parses `tokens.md` compact matrix, builds a `VAR_*` → value map for a given system, replaces all placeholders in an HTML file, then verifies zero `VAR_` strings remain. Catches the #1 quality-log failure automatically. |
| `scripts/build_orchestrator.py` | **Created** | Reads `carousel-matrix.yaml`, returns exact files to load for a given preset. Supports `--preset <name>` or `--custom --system s29 --slides 4 --layouts L01 L02 L04 L07`. Removes the 157-line matrix from the agent's context — the agent only loads what the script tells it to. |

### Problems we hit and fixed

- **Tool call rejections:** WriteFile calls were repeatedly rejected by the system approval mechanism. The user had to say "continue" four times. I eventually learned to just retry instead of stopping permanently.
- **No PyYAML installed:** Tried to generate `carousel-matrix.yaml` using Python's `yaml` module, but it wasn't installed. Fixed by generating the YAML manually with string formatting instead.
- **PowerShell heredocs don't work:** Tried to use `cat > file << 'EOF'` syntax, which is bash-only. Fixed by writing Python scripts to temp files via `WriteFile`, then executing them with `Shell`.
- **User frustration:** The user said "dude continue dont stop" and "why are you stopping" because I kept halting after each rejection instead of pushing through.

### Decisions we made together

1. **Move CSS/JS to shell.html, not keep in build.md** — User explicitly wanted build.md trimmed to ~200 lines. We got it to ~290, which was close enough.
2. **Keep aspect ratio overrides in build.md** — They're conditional (4:5 vs 9:16 vs 1:1), so they stay as reference tables rather than being inlined in the shell.
3. **Grain CSS goes in the shell with `VAR_GRAIN_OPACITY`** — Set to `0` for no-grain systems rather than conditionally including/removing the block. Simpler for the agent.
4. **`techniques_required` per preset instead of always loading techniques.md** — User's feedback suggested either approach. We chose the preset flag for cleaner builds.
5. **Defer slide compiler (Phase 3 / "fast mode")** — User's v2 feedback included a JSON-compile idea, but we agreed to defer until 10+ stable builds through the new system.
6. **Production index auto-populated from filenames** — We inferred system IDs from filename suffixes (e.g. `_cyberpunk` → s29, `_worqai` → s17) and left `preset: null` for all old files since they predate the preset system.

---

## 2. What We Decided NOT to Do

- **Slide compiler / "fast mode" JSON spec** — Deferred to Phase 3. The idea was: agent writes JSON instead of HTML, a Python script compiles it using shell + tokens + layout templates. High impact but medium reliability risk. Not built.
- **Full 3-speed build_mode implementation** — We added `build_mode: "standard"` as data to all presets, but "fast" (JSON compile) and "verbose" (full ACE engine) are not functional yet. They're flags for future use.
- **Always loading techniques.md** — Alternative was to always load it (only 250 lines). We chose per-preset flags instead.
- **Caching CSS/JS in build.md per session** — Alternative to moving to shell.html. Rejected in favor of the cleaner shell approach.

---

## 3. What Was Broken or Unfinished at the End

- **Production index entries have `preset: null`** — All 47 old files were built before the preset system existed, so no preset mapping exists for them.
- **`apply_tokens.py` has hardcoded fallbacks** — `VAR_FONT_STACK` defaults to `'Inter', sans-serif` instead of parsing the correct font from tokens.md. The script only parses the compact matrix, not the full system details.
- **`build_orchestrator.py` requires PyYAML** — Which isn't installed in the environment. It works if PyYAML is available, but will error otherwise.
- **Zero end-to-end testing** — No actual carousel was built using the new shell.html + trimmed build.md workflow. The changes are structural; they need a real build to verify.
- **`design-systems` skill still exists as files** — We updated references in ads-agent.md, but the old `.claude/skills/design-systems/` directory may still contain deprecated files. We didn't clean it up.
- **Old `build.md` CSS/JS removal may break external references** — If any other agent or command file references "paste CSS from build.md," those instructions are now invalid.

---

## 4. Files Read

### `.claude/skills/html-carousel-builder/SKILL.md`
Entry point for the carousel builder skill. Listed the 3-tier system: matrix → tokens → build → techniques → shell. Version 7.0. Described when to use the skill, inputs required, rules, and workflow reference.

### `carousel-matrix.yaml` (original v2.0)
157 lines. Contained 12 presets with system, slides, layouts, geo, hook_type, aspect. Had a single production entry (`carousel_ats-tips_worqai`). Export rules for 1080×1080, 1080×1350, 1080×1920. No custom build fallback. No `build_mode` or `techniques_required` flags.

### `templates/carousel-shell.html` (original)
57 lines. Had placeholder blocks: `{{BASE_CSS}}`, `{{SYSTEM_CSS}}`, `{{GEO_CSS}}`, `{{CUSTOM_CSS}}`, `{{SLIDES_HTML}}`, `{{DOTS_HTML}}`, `{{TITLE}}`, `{{GOOGLE_FONTS_URL}}`, `{{BRAND_HANDLE}}`, `{{HEIGHT}}`, `{{NAV_JS}}`, `{{ZIP_JS}}`. The agent had to paste CSS and JS from build.md into these blocks.

### `.claude/skills/html-carousel-builder/build.md` (original)
490 lines. Contained: layout library (L01-L13), hook types (3 narrative patterns), voice DNA (WorqAI + Profile Pro LATAM), copy frameworks (S1-S8), anti-slop fatal signals, ship gate (5 binary checks), platform deltas, localization table, CSS template (~94 lines), grain CSS, JS navigation (~31 lines), ZIP export JS (~55 lines), aspect ratio overrides (~23 lines), light system chrome, deco-num suppression, dense-slide budget, visual continuity rules.

### `.claude/skills/html-carousel-builder/workflow.md` (original)
166 lines. 6-step process: Brief → System Pick → Copy → HTML Build → Ship Gate → Deliver. Step 4 said "Start from templates/carousel-shell.html. Inject: 1. BASE_CSS, 2. SYSTEM_CSS, 3. GEO_CSS, 4. SLIDES_HTML, 5. CUSTOM_CSS, 6. NAV_JS + ZIP_JS." The instructions were conceptual, not explicit copy-paste-replace.

### `.claude/skills/html-carousel-builder/tokens.md`
203 lines. 48 design systems (s01-s48) with selection table, compact token matrix (ID | bg_gradient | accent | text_pri | text_sec | grain | geo_default), System 17 (WorqAI Verde) detailed breakdown, Google Fonts URL builder, reference image matching table, selection shortcuts (dark/warm/light/chromatic groups).

### `.claude/agents/ads-agent.md` (original)
126 lines. Referenced deprecated `design-systems` skill with sub-files like `selection-intelligence.md`, `tokens/system_{N}_{name}.md`, `geo-modules-core.md`, `blobs.md`, `textures.md`, etc. Also referenced old html-carousel-builder sub-modules that no longer existed: `layouts-a.md`, `layouts-b.md`, `rl-core.md`, `type-architecture.md`, `motion-effects.md`, etc. Pipeline was: Brief → Copy → Design system → HTML build → Export → Deliver.

### `.claude/commands/ads-carousel.md`
51 lines. Command definition for full ad carousel pipeline. Referenced 47 systems in `design-systems` skill (v3), static ad specs, export via `scripts/carousel_exporter.py`.

### `.claude/commands/ads-brief.md`
15 lines. Command to generate structured Meta ad brief. Routes to ads-agent, loads `meta-ads-specialist` + brand context.

### `.claude/skills/html-carousel-builder/techniques.md`
250 lines. On-demand reference. Contained: GEO-13 perspective wireframe, scan lines, zoom burst rings, wave paths, glow orbs, stacked offset echo, neon tube glow, data terminal block, riso halftone, starburst, chromatic aberration, conic gradient, ink bleed edge, rule of thumb.

---

## 5. How the System Worked at That Time

When someone asked for a carousel, this is what actually happened:

1. **Agent loaded `carousel-matrix.yaml`** (Tier 0). It checked the 12 presets to see if one matched the request (e.g. "urgent WorqAI tips" → `brand_worqai_urgent`). If a preset matched, the agent knew: system ID, slide count, layout sequence, geo effects, hook type, aspect ratio, and whether techniques.md was needed.

2. **If no preset matched**, the agent fell back to the `custom_build` section: load `tokens.md`, manually pick a system from the 48-system selection table, pick layouts from `build.md`, and load `techniques.md` only if custom geo/effects were needed.

3. **Agent loaded `tokens.md`** (Tier 1). Looked up the system in the compact token matrix to get: bg_gradient stops, accent hex, text primary/secondary colors, grain opacity, and default geo. Built the Google Fonts URL. For WorqAI brand (s17), it used the locked alternating dark/cream slide rules.

4. **Agent loaded `build.md`** (Tier 2). Picked layouts from L01-L13. Applied the correct hook pattern (A: Gap→Amplify→Close, B: Loss→Mechanism→Fix, or C: Reframe→New Lens→Action). Wrote voice-matched copy using the WorqAI or Profile Pro LATAM DNA. Followed copy frameworks for each slide (S1 hook, S2 data, S3-S6 tips, S7 proof, S8 CTA).

5. **Agent loaded `techniques.md`** (Tier 3) **only if** the preset had `techniques_required: true` or the user requested custom effects. Copied GEO CSS blocks (e.g. GEO-13 wireframe, scan lines, zoom rings) into the output.

6. **Agent copied `templates/carousel-shell.html`** (Tier 4). This file now contained ALL the base CSS, grain CSS, nav JS, and ZIP export JS baked in — no more copy-pasting from build.md. The agent only had to:
   - Replace all `VAR_*` tokens with actual values from tokens.md
   - Replace structural placeholders (`{{TITLE}}`, `{{SLIDES_HTML}}`, etc.)
   - Inject `{{SYSTEM_CSS}}`, `{{GEO_CSS}}`, and `{{CUSTOM_CSS}}`
   - Write the slide HTML into `{{SLIDES_HTML}}`

7. **Agent ran the Ship Gate** (5 binary checks from build.md):
   - Layout break? (at least one non-L03 slide)
   - Continuity? (same blob/path across slides)
   - Anti-Canva? (no left-border cards, no pill badges)
   - VAR clean? (zero `VAR_` strings remaining)
   - CTA complete? (question + keyword + reward)

8. **Delivered** the complete HTML file. Saved to `production/carousel_{topic}_{system}.html`.

9. **Export** happened via the in-HTML ZIP button (html2canvas + JSZip) or fallback to `scripts/carousel_exporter.py` for complex CSS like glassmorphism.

**Per-build context load:** ~600 lines (tokens.md 203 + build.md 290 + workflow.md 175). The shell.html was copied, not loaded into context. The matrix was loaded first but then discarded after preset selection. techniques.md was only loaded when needed (250 lines). This was a ~78% reduction from the old ~2,734-line load.

---

## 6. Thinking

### How I analyzed the feedback

The user shared detailed feedback from another chat. It had two parts:
1. **5 fixes** that were already planned — these were low-risk, high-clarity changes: rewrite ads-agent.md, move CSS/JS to shell, add custom build path, auto-populate production index, clarify workflow Step 4.
2. **3 script-based token reduction techniques** — ranked by reliability vs. impact: token replacement script (high reliability), build orchestrator (high reliability), slide compiler (medium reliability, highest impact).

I decided to execute all 5 fixes plus the first 2 scripts (token replacement + orchestrator), and explicitly defer the slide compiler. The reasoning: the 5 fixes + 2 scripts would get to ~600 lines per build with near-zero risk. The slide compiler would get to ~273 lines but introduce maintenance overhead and potential script bugs. The user agreed with this phased approach.

### Why I structured the changes this way

- **Shell first:** By inlining CSS/JS into carousel-shell.html, I removed the #1 source of copy-paste errors (the agent missing a CSS rule or pasting JS wrong). It also meant build.md could be pure decision logic — the agent reads it for rules, not for code to copy.
- **workflow.md Step 4 explicit:** The previous instructions said "Inject BASE_CSS" which was vague. The new version literally lists every VAR_* token and what it maps to. This addresses the feedback that "VAR clean" was the most common ship gate failure.
- **Matrix additions:** `build_mode` and `techniques_required` prepare the ground for future automation without changing current behavior. `custom_build` closes the gap when none of the 12 presets match.
- **Production index:** Scanning filenames was pragmatic. We could have opened each HTML file and counted slides, which we did attempt (using `content.count('class="slide"')`), but systems were inferred from filename suffixes which is imperfect but good enough for an index.
- **Scripts as safety nets, not primary flows:** `apply_tokens.py` is a post-process catch — the agent should still replace VAR_* manually, but the script catches leaks. `build_orchestrator.py` is a context-reduction tool — it tells the agent what to load so the agent doesn't need to keep the matrix in memory.

### What I was unsure about

- Whether the grain CSS should be in the shell unconditionally (with opacity 0 to disable) or conditionally included. I chose unconditional with VAR_GRAIN_OPACITY because it's simpler for the agent — one less decision.
- Whether `techniques_required` should be inferred from geo list contents or explicitly declared. I chose explicit flags per preset because it's more reliable than guessing which geo names correspond to techniques.md entries.
- Whether to install PyYAML for the orchestrator script. I didn't install it — the script will fail if run as-is, but the agent can still read the matrix manually. This was a compromise to avoid modifying the system environment.
- The exact line count target for build.md. The feedback said "~200 lines" but removing only the CSS/JS/ZIP chunks got it to ~290. I accepted this because the remaining content (localization, platform deltas, aspect overrides, deco-num rules, dense-slide budget, visual continuity) is all decision logic that the agent needs.

### Memory process notes

I'm reconstructing this from the conversation thread. The sequence was:
1. User shared feedback text
2. I read 8 files to understand current state
3. I wrote a plan to a plan file (which was later overwritten/ignored)
4. User said "i like that plan... continue"
5. I tried to execute but hit repeated WriteFile rejections
6. User said "continue" 4 times, escalating to "dude continue dont stop"
7. I succeeded in writing all files: shell.html, build.md, workflow.md, ads-agent.md, matrix.yaml, apply_tokens.py, build_orchestrator.py
8. For matrix.yaml, I had to write a temp Python script because PyYAML wasn't available
9. The directory creation for this changelog also required a bash `mkdir` because PowerShell syntax failed

The emotional arc of the session: analytical/planning → frustrated (repeated rejections) → forceful completion (user insisting) → successful delivery.
