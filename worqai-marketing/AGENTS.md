# WorqAI Marketing — Carousel Builder System

WorqAI is an AI-powered resume builder SaaS for LATAM and US Hispanic job seekers. Kenneth runs marketing; the cofounder builds the product. This workspace has two roles: (1) the carousel builder system — producing agency-quality HTML carousels for Instagram, Facebook, and LinkedIn; (2) WorqAI marketing strategy — roadmaps, GTM, content, and paid ads.

## Tech Stack

Python 3.11+, Playwright, Pillow, numpy. Platforms: Meta Ads, Instagram, Facebook, LinkedIn. Main skill library in `.Codex/skills/` (19 skills).

## Structure

```
.Codex/
  agents/     — 5 specialized subagents
  skills/     — 19 skills, each in its own folder with SKILL.md
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
- See @.Codex/rules/anti-slop.md and @.Codex/rules/brand-voice.md before writing anything.

## Scripts

Core build pipeline:
```bash
# Full build (render + preflight + visual_richness in one command)
py scripts/build_carousel.py production/my-spec.json
py scripts/build_carousel.py production/spec1.json production/spec2.json   # batch

# Export to PNGs after build passes
py scripts/carousel_exporter.py --input production/carousel.html --output export/

# Individual steps (debugging)
py scripts/render_carousel.py production/spec.json --output production/carousel.html
py scripts/preflight.py production/carousel.html
py scripts/visual_richness_check.py production/carousel.html
```

AI background pipeline:
```bash
# Extract panels from a grid image, color-adapt to design systems, update manifest
py scripts/panel_extractor.py --file grid.png --panels 5 --name "My Scene"
py scripts/panel_extractor.py --file grid.png --panels 5 --preview        # preview crop zones first
py scripts/panel_extractor.py --file grid.png --panels 5 --compare        # generate kit comparison grid

# Flat single-image color adaptation (older approach, still valid)
py scripts/adapt_image_bg.py --file bubbles.png --name "Bubbles 01" --hue 180

# Algorithmic slide-to-slide transformations (8 recipes: glow_bloom, deep_zoom, etc.)
py scripts/transform_bg_v2.py bubbles.png --recipe glow_bloom --slides 5
```

Other scripts (rarely called directly): `build_gallery.py`, `stat_source_validator.py`, `inline_assets.py`, `screenshot_carousels.py`.

## Carousel Build Reference

Read `.Codex/skills/html-carousel-builder/carousel-master-ref.md` before writing any spec.
It contains all 48 systems, 52 layouts, 25+ geo layers, 12 decoratives, copy budgets, ship gate,
v2 SVG primitive library (icons, blobs, starbursts, text treatments, drop-shadows), and a
copy-paste JSON template. One file instead of 17.

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

- **Strategy / roadmap / positioning / launches / KPIs** → @agent strategy-agent
- **Paid ads / Meta campaigns / carousel ads** → @agent ads-agent
- **Social / blog / SEO / newsletters / content calendars** → @agent content-agent
- **Sales / objections / WhatsApp / Reddit / job hunting** → @agent growth-agent

For the full capability map, see @AGENTS_BREAKDOWN.md
For the marketing roadmap, see @ROADMAP.md
