# WorqAI Marketing — Carousel Builder System

WorqAI is an AI-powered resume builder SaaS for LATAM and US Hispanic job seekers. Kenneth runs marketing; the cofounder builds the product. This workspace has two roles: (1) the carousel builder system — producing agency-quality HTML carousels for Instagram, Facebook, and LinkedIn; (2) WorqAI marketing strategy — roadmaps, GTM, content, and paid ads.

## Tech Stack

Python 3.11+, Playwright, Pillow, numpy. Platforms: Meta Ads, Instagram, Facebook, LinkedIn. The active skill library lives in `.claude/skills/`; do not hardcode its count because skills evolve.

## Structure

```
.claude/
  agents/     — 2 specialized subagents (worqai-creative-agent, worqai-growth-agent)
  skills/     — reusable skills, including gated carousel production
  rules/      — Global guardrails (anti-slop, brand-voice, output conventions, changelog)
  commands/   — Slash commands for common workflows
  hooks/      — Lifecycle scripts (registered in settings.json)

scripts/      — All Python tooling (24 scripts total, see Scripts section below)
templates/
  carousel-shell.html   — Base HTML shell for all carousels
  slides/               — 52 slide layout templates
brand/
  generated-bg/         — AI background variants + manifest.json (manifest-driven pipeline)
  (logo, colors, other visual assets)
ideation/
  ai-backgrounds/       — Source AI-generated background PNGs
    panels/             — Drop multi-panel grid images here for panel_extractor.py
gallery/      — Component gallery (246 component HTML files + INDEX.html)
production/   — WIP carousels and JSON specs
export/       — Final deliverables only (PNGs + ZIPs ready to post)
roadmap/      — Strategy docs, sprint plans, OKRs
distribution/ — Scheduled content with posting dates
```

## Conventions

- Client-facing Spanish for LATAM; English only when targeting US or for bilingual content.
- Files: kebab-case `.md`, snake_case `.py`.
- Carousels: 1080×1080px. Always use a design system from `html-carousel-builder` skill tokens.
- Final deliverables always land in `export/`.
- See @.claude/rules/anti-slop.md and @.claude/rules/brand-voice.md before writing anything.

## Scripts

Core build pipeline:
```bash
# Full build (render + preflight + visual_richness in one command)
py scripts/build_carousel.py production/my-spec.json
py scripts/build_carousel.py production/spec1.json production/spec2.json   # batch

# Export to PNGs + ZIP + contact sheet (default: saves to export/)
py scripts/carousel_exporter.py --input production/carousel.html --output export/
py scripts/carousel_exporter.py --input production/carousel.html             # auto-routes to export/
py scripts/carousel_exporter.py --input production/carousel.html --no-contact-sheet  # skip sheet

# Individual steps (debugging)
py scripts/render_carousel.py production/spec.json --output production/carousel.html
py scripts/preflight.py production/carousel.html
py scripts/visual_richness_check.py production/carousel.html
```

AI background pipeline:
```bash
# Extract panels from a grid image, color-adapt to design systems, update manifest
py scripts/panel_extractor.py --file grid.png --panels 5 --name "My Scene"
py scripts/panel_extractor.py --file grid.png --panels 5 --preview        # preview crop zones FIRST (mandatory)
py scripts/panel_extractor.py --file grid.png --panels 5 --compare        # generate kit comparison grid

# Gutter trimming — ALWAYS use --trim-gutters 3 when extracting from ChatGPT grids
# ChatGPT adds white canvas margins and gutters that ruin slide backgrounds without trimming
py scripts/panel_extractor.py --file grid.png --panels 8 --name "My Scene" --trim-gutters 3

# Fix already-extracted kits that have white borders baked in (post-hoc trim)
py scripts/panel_extractor.py --fix-kit brand/generated-bg/my-kit-name --trim-gutters 3

# Flat single-image color adaptation (older approach, still valid)
py scripts/adapt_image_bg.py --file bubbles.png --name "Bubbles 01" --hue 180

# Algorithmic slide-to-slide transformations (8 recipes: glow_bloom, deep_zoom, etc.)
py scripts/transform_bg_v2.py bubbles.png --recipe glow_bloom --slides 5
```

**AI background extraction rules (2026-05-27):**
- ALWAYS use `--preview` before extraction to verify crop zones
- ALWAYS use `--trim-gutters 3` when source image is a ChatGPT grid (removes canvas margins)
- NEVER use `--panels N` where N = slide count — always use N = actual panel count in image
- ChatGPT prompting for grid images: *"Create exactly 8 separate square panels in a strict 2×4 grid. No gutters, no white borders, no frames, no spacing between panels. Each panel must touch the next panel edge-to-edge."*
- Irregular grids (e.g. 4 panels top row + 2 wide panels bottom row) are NOT extractable — reject and regenerate

**Per-slide `density` field (required on AI-bg carousels):**
```json
{ "density": "heavy" }   // hook/stat/pull-quote/CTA slides — strong dark scrim
{ "density": "demo" }    // terminal/input-output/waffle slides — lighter scrim
{ "density": "cta" }     // CTA slide — high contrast scrim
```
Omitting `density` defaults to medium scrim — NOT acceptable for hook/stat/CTA slides.

Other scripts (rarely called directly): `build_gallery.py`, `stat_source_validator.py`, `inline_assets.py`, `screenshot_carousels.py`.

## Carousel Build Reference

Read `.claude/skills/html-carousel-builder/carousel-master-ref.md` before writing any spec.
It contains all 48 systems, 52 layouts, 25+ geo layers, 12 decoratives, copy budgets, ship gate,
v2 SVG primitive library (icons, blobs, starbursts, text treatments, drop-shadows), and a
copy-paste JSON template. One file instead of 17.

For new carousel production, follow `.claude/skills/produce-carousel/SKILL.md`.
Slides are built and approved as standalone HTML/CSS artifacts before one owner
integrates them. Shared renderer or architecture changes require Quantum's
Engineering profile; routine carousel production uses the Production profile.

## Quantum Routing

Quantum is the control plane, not a marketing agent and not the Oracle. Claude is
the execution provider; this repository's skills define carousel production.

Run Quantum from this repository:

```powershell
$q = "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\quantum-v4\.venv\Scripts\q.exe"

# Produce a bounded carousel through the local production skill.
& $q new "Use the local produce-carousel skill to produce: <brief>" --profile production

# Change the shared builder, renderer, schemas, components, or architecture.
& $q new "Engineering change: <describe carousel pipeline change>" --profile engineering
```

Use `production` for a carousel made through the existing factory. Workers must
build standalone slides, obtain hash-bound approvals, and leave shared pipeline
code unchanged. If shared scripts, dependencies, schemas, or architecture must
change, stop and create an Engineering run.

Do not use Quantum for a one-line caption correction or a deterministic export
rerun. Quantum currently controls one target repository per run; it is not yet a
transactional multi-repository orchestrator.

**v2 visual primitives (2026-05-17):** Carousels auto-load a 21-icon SVG sprite + 3 drop-shadow filters. Opt into gradient/glow/stroke text via `copy.text_treatment`. Opt into SVG organic blobs via `layers: ["svg-blob-tr"]` (with optional `{"animate":true}` drift). Opt into SVG starbursts via `decoratives: ["svg-starburst-burst"]`. Old `blob-bg` and `ornament*` keep working — soft warned in preflight, never blocked. See `roadmap/visual-primitives-v2-spec.md` for the full design.

**Pipeline policy:** `carousel_exporter.py` (Playwright) is canonical. In-HTML html2canvas button = quick preview only. CSS `background-clip:text`, `box-shadow`, `backdrop-filter`, `mix-blend-mode`, and `filter:blur()` are broken in html2canvas — SVG primitives bridge the gap. Mark Playwright-only slides with `effects.requires_playwright_export: true`.

## AI Background System (2026-05-25)

AI-generated images can be used as carousel backgrounds. The system is manifest-driven — `brand/generated-bg/manifest.json` is the registry. The render pipeline reads it automatically via `resolve_ai_bg()`.

**How to add a new background:**
1. Generate a grid image in ChatGPT with N panels (e.g. "5 panels in a 2×3 grid, continuous scene")
2. Drop PNG in `ideation/ai-backgrounds/panels/`
3. Run: `py scripts/panel_extractor.py --file grid.png --panels 5 --name "My Scene"`
4. Manifest is updated with `recipe_variants["extracted"]` — one path per panel per system

**How to use in a spec:**
```json
{
  "meta": { "system": "s17", "bg_recipe": "extracted" },
  "slides": [
    { "layers": ["my-scene"], "layout": "slide-hook-lockup", ... }
  ]
}
```
Each slide gets the matching panel automatically (slide 1 → panel_01, slide 2 → panel_02, etc.).

**Available background IDs** (check `brand/generated-bg/manifest.json` for current list):
- `ai-bubbles-01` — floating iridescent bubbles, supports: `glow_bloom`, `deep_zoom`, `phase_distort`
- `vector-field-distortion` — vector field distortion, 5 panels, supports: `extracted`

**Supported `bg_recipe` values:** `extracted` (panel grid), `glow_bloom`, `deep_zoom`, `phase_distort` (algorithmic). Use `extracted` for real visual continuity; algorithmic recipes for subtle per-slide variation.

## Agent Routing

Two agents. Everything routes to one of them.

- **Any writing, creative output, or content** → @agent worqai-creative-agent
  Covers: ad copy, motion design scripts, social posts, captions, landing page copy,
  video scripts, carousel briefs, LinkedIn posts, Reddit posts, animation text.
  Also covers: what copy angle to use, which language version, how to frame the
  anti-ChatGPT claim, how to write ES and EN natively.

- **Strategy, GTM, outreach, or sales** → @agent worqai-growth-agent
  Covers: roadmap decisions, channel prioritization, launch sequencing, Reddit warm
  lead DM sequences, LinkedIn growth, objection handling, WhatsApp closes, what to
  do next to move the business forward.
  Also covers: funnel principles, content strategy direction, pre-conversion flow.

For the marketing roadmap, see @ROADMAP.md
