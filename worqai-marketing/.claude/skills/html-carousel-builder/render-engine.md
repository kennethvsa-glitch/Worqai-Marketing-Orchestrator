# Render Engine Reference — render_carousel.py

Pipeline: `JSON spec → render_carousel.py → Jinja2 templates → HTML`

## Commands

```bash
py scripts/render_carousel.py production/my-spec.json
py scripts/render_carousel.py production/my-spec.json --output production/carousel_topic_s17.html
py scripts/render_carousel.py production/my-spec.json --validate-only
```

Default output path (when `--output` is omitted): `production/carousel_{topic}_{system}.html`

Exit codes: `0` = success, `1` = error.

---

## System Types — SYSTEM_TYPES dict

Each system ID maps to a type that controls the default geo layer and certain style behaviors.

| Type | System IDs |
|------|-----------|
| `dark` | s01, s02, s03, s06, s08–s17, s20–s22, s24, s27, s28, s30–s32 |
| `warm` | s04 |
| `light` | s05, s18, s19, s23, s26, s39, s47, s48 |
| `brutalist` | s07, s25 |
| `cyberpunk` | s29 |

`LIGHT_SYSTEMS` set: `{s05, s18, s19, s23, s25, s26, s39, s47, s48}` — adds `class="light-system"` to `<html>`.

---

## Default Geo Layers per System Type — GEO_HTML dict

| Type | Layers injected (when slide has no `layers` override) |
|------|------------------------------------------------------|
| `dark` | `pw-wrap/pw-grid` + `glow-orb` |
| `cyberpunk` | `pw-wrap/pw-grid` + `scan-lines` + `glow-orb` + `zoom-rings` |
| `brutalist` | `grid-bg` |
| `light` | `diag-band` |
| `warm` | `blob-bg` + `vol-light` |

---

## All Available Layers — LAYER_HTML dict

Layers a spec slide can include in its `layers` list to override the system default:

**Core (pre-expansion)**
- `pw-grid` — perspective grid, dark systems
- `scan-lines` — horizontal scan lines, cyberpunk
- `glow-orb` — radial white glow top-right
- `zoom-rings` — 3 concentric accent-color rings
- `grid-bg` — flat dot/line grid, brutalist
- `diag-band` — diagonal accent band top-right, light
- `blob-bg` — ellipse blur top-right, warm
- `vol-light` — large soft radial, warm

**Tier 1 expansion**
- `geo-mesh-noise` — animated mesh gradient blob (warm/light)
- `geo-pixel-grid` — tight dot matrix, top-fades (cyberpunk/dark)
- `geo-conic-rays` — radial sunburst, uses `conic-gradient` (brutalist/warm) — **html2canvas risk if activated**
- `geo-chevron-stripe` — diagonal repeating chevrons (brutalist/dark)
- `geo-iso-grid` — isometric grid (tech/dark)
- `geo-paper-texture` — paper fiber via repeating gradients (light editorial)
- `geo-halftone` — print halftone dot gradient (brutalist/editorial)
- `geo-ribbon-flow` — bezier ribbon sweeps (warm/light)
- `geo-circuit-trace` — PCB traces + nodes (cyberpunk only)
- `geo-topo-lines` — topographic contour lines (dark/brutalist editorial)
- `geo-starfield` — sparse star scatter (dark/cyberpunk)
- `geo-gradient-bands` — horizontal stripe gradient (warm/light editorial)

Layer resolution logic (`resolve_geo`):
```
if slide_spec["layers"] exists → build from LAYER_HTML entries in that list
else → use GEO_HTML[system_type]
```

---

## Google Fonts per System — GOOGLE_FONTS dict

| System | Fonts loaded |
|--------|-------------|
| s04 | Poppins + JetBrains Mono |
| s07 | Space Grotesk + JetBrains Mono |
| s17 | Nunito + JetBrains Mono |
| s25 | Archivo + JetBrains Mono |
| s29 | Space Grotesk + Inter + JetBrains Mono + Cormorant Garamond |
| default | Space Grotesk + Inter + JetBrains Mono |

---

## Token Defaults (fallback when system not in component_data.json)

```
--bg-base: #0a0a12
--bg-mid: #111122
--accent: #00ff9c
--text-primary: #ffffff
--text-secondary: rgba(255,255,255,0.55)
--text-muted: rgba(255,255,255,0.28)
--font-display: 'Space Grotesk', sans-serif
--font-body: 'Inter', sans-serif
--font-mono: 'JetBrains Mono', monospace
--grain-opacity: 0.05
--geo-opacity: 0.08
```

Token data source: `scripts/component_data.json` → `systems[system_id]`
If `--text-muted` is absent from JSON data it's added automatically.

---

## Aspect Ratio CSS — ASPECT_CSS dict

| Aspect | Override CSS applied |
|--------|---------------------|
| `1:1` | none (default) |
| `4:5` | wrap aspect-ratio 4/5, max-width 432px, smaller font clamps, padding-bottom 120px |
| `9:16` | wrap aspect-ratio 9/16, max-width 320px, slide padding-top 180px / padding-bottom 220px |

Text budget multiplier in preflight: `1:1 = 1.0`, `4:5 = 1.15`, `9:16 = 1.3`

---

## Render Flow

1. Read spec JSON
2. `load_tokens(system_id)` → CSS vars string
3. `build_fonts_url(system_id)` → Google Fonts URL
4. For each slide in `spec["slides"]`:
   - Resolve layout template (`templates/slides/{layout}.html`) — falls back to `slide-tip-blocks` if missing
   - `resolve_geo(slide_spec, system_type)` → geo HTML string
   - `is_silence` = `slide.constraints.silence == true` OR pacing beat == `"silence"`
   - Render Jinja2 template with: `copy`, `slide_num`, `total`, `brand`, `is_active` (true only for slide 1), `is_silence`, `beat`, `system_type`, `geo_html`
5. Join slides → inject into `templates/carousel-shell.html`
6. Write output HTML

Variables passed to shell template: `title`, `fonts_url`, `css_vars`, `aspect_css`, `system_id`, `system_type`, `is_light`, `total`, `brand`, `slides_html`

---

## Jinja2 Environment Settings

- `FileSystemLoader` rooted at `templates/`
- `autoescape=False` — HTML is trusted
- `undefined=Undefined` — missing vars silently become empty (no exceptions)

---

## s17 Token Reference (WorqAI VERDE — primary brand system)

```
--bg-base: #1A1A18
--bg-mid: #0F0F12
--accent: #C7FF3A
--text-primary: #FFF8E7
--text-secondary: rgba(255,248,231,0.55)
--font-display: 'Nunito'
--font-body: 'Nunito'
--font-mono: 'JetBrains Mono'
--grain-opacity: 0.05
--geo-opacity: 0.10
```

Default geo for s17 (type=dark): `pw-grid` + `glow-orb`
