---
name: html-carousel-builder
description: >
  Builds production-ready, agency-level HTML carousel files for Instagram/Facebook/TikTok/LinkedIn
  (1080x1080, 1080x1350, 1080x1920). Outputs a single self-contained .html file.
metadata:
  author: kenneth-valverde
  version: 9.0
  domain: ad-creative-production
  language: es-CR / es-LATAM / en
  updated: 2026-05-17
---

# html-carousel-builder v8

**v9 (2026-05-18):** Enforcement upgrade + visual continuity. New preflight checks: blob overuse cap, badge/text collision detection, shape diversity limit, decorative repetition guard, and mandatory demonstration layout rule. 6 new non-circular blob shapes (angular, crystal, wave, arch, splatter, ribbon). 3 cross-slide flow layers (wave, arrow, data). 3 new demonstration layouts: `slide-input-output` (what you write vs what ATS sees), `slide-waffle-chart` (10×10 visual proportion grid), `slide-cross-slide-connector` (continuity anchor). Cross-slide continuity modes: `wave`, `data-pipeline`, `corner-frame-evolution`, `number-escalator`, plus dict-based custom path continuity. Glassmorphism panel component (`sub-glass-panel`). 10 new geo layers: `geo-contour-flow`, `geo-perspective-grid`, `geo-hex-mesh`, `geo-constellation`, `geo-neon-ring`, `geo-bokeh`, `geo-scan-lines`, `geo-chromatic-edge`, `geo-data-streaks`, `geo-liquid-morph`. See `carousel-master-ref.md` for full reference.

## WHEN TO USE

- "hazme un carousel" / "crea slides" / "genera el HTML"
- "quiero un carousel para Instagram / Facebook / LinkedIn"
- "dame algo estilo agencia / premium / diseñado"
- "nueva variante" / "mismo contenido, otro color"

## INPUTS REQUIRED

1. **Topic / copy** — what problem does this carousel address?
2. **Style system** — which of the 48 systems? (or say "pick for me")
3. **Slides** — default 8
4. **Language** — default Spanish CR/LATAM
5. **Brand handle** — default "@worqai"
6. **Hook type** — result / question / contrarian / curiosity / negative / identity / transformation
7. **Source facts (optional)** — verified stat + source for Slide 2
8. **Proof case (optional)** — real client result for Slide 7

Never generate with placeholder content. If topic is missing, ask once and wait.

## RENDER ENGINE (ACTIVE — use this, not raw HTML)

**Pipeline:** JSON spec → `scripts/render_carousel.py` → HTML. Never write raw carousel HTML.

```
py scripts/render_carousel.py production/my-spec.json --output production/carousel_topic_s17.html
py scripts/stat_source_validator.py production/carousel_topic_s17.html
py scripts/preflight.py production/carousel_topic_s17.html
```

Schema: `scripts/carousel-spec.schema.json` · Layouts: `templates/slides/` · Layers: `render_carousel.py` LAYER_HTML dict

## FAST PATH (default for all builds)

Read **one file**: `carousel-master-ref.md` — covers all 48 systems, 51 layouts, 29 geo layers,
9 decoratives, copy budgets, ship gate, anti-slop, continuity modes, and a full JSON spec template.
Then write spec → run `py scripts/build_carousel.py production/your-spec.json`.

## 3-TIER BUILD SYSTEM (deep reference — use when master-ref isn't enough)

| Tier | File | When to load | Content |
|------|------|-------------|---------|
| 1 | `tokens.md` | Need full gradient/token hex values | 48 systems, compact token matrix |
| 2 | `build.md` | Need elite reference index or pre-build plan gate | Layouts, voice, copy rules, anti-slop |
| 3 | `workflow.md` | Need full 6-step process detail | Render engine, batch rules, ship gate |

## RULES

1. Always write a 1-paragraph brief before generating anything.
2. Never use flat backgrounds. Gradient + geo effect on every slide.
3. Never put more than one idea per slide.
4. Never change blob/path between slides. Only rotation/translation.
5. If system not specified, pick from the selection table in tokens.md.
6. If topic not specified, ask ONE time and wait.
7. Output a JSON spec + run render engine. Not raw HTML. Not pseudocode.
8. Default language: Spanish (CR/LATAM). English only if explicitly requested.
9. State system, layouts chosen, hook type before writing the spec.
10. Run preflight.py after every render. Fix failures before delivering.
11. **Every decorative layer needs a one-sentence purpose.** "Add visual interest" is rejected. Acceptable: "frame the headline," "show data proportion," "create depth behind terminal."
12. **Max 2 uses of any single shape per carousel.** If `svg-blob-tr` appears on slide 1, it may appear on ONE other slide maximum. Prefer different blob variants for each slide.
13. **At least one slide must be a demonstration layout.** Show the problem visually — don't just describe it in text. Demonstration layouts: `slide-input-output`, `slide-waffle-chart`, `slide-before-after`, `slide-data-viz-donut`, `slide-progress-bars`, `slide-myth-vs-fact`, `slide-comparison-table`.
14. **Before designing, review 2+ reference carousels** from the `production/` directory and note which visual elements to adapt.
15. **Prefer non-circular shapes.** The blob is not a default. Use `geo-circuit-trace`, `geo-topo-lines`, `geo-starfield`, `svg-blob-angular`, `svg-blob-crystal` for visual variety.

## WORKFLOW

Load `workflow.md` for the full 6-step build process.
