# Advanced Background Transformation Engine v2.0

## What This Is

Not camera movements (pan/zoom) — **real image deformation**. Your bubble image comes alive between slides using fluid dynamics, curl noise, wave propagation, and frequency separation.

## The 8 Recipes

| Recipe | Technique | Visual Effect | Best For |
|--------|-----------|---------------|----------|
| **glow_bloom** | Brightness extraction + additive blur | Bubbles glow brighter each slide | CTA builds, energy |
| **breathe_life** | Sine-wave param modulation | Organic inhale/exhale pulse | Wellness, living brand |
| **deep_zoom** | Frequency layer blending | Progressive detail reveal | Cinematic storytelling |
| **curl_flow** | Curl noise vector field | Bubbles swirl in gentle currents | Fluid, organic feel |
| **liquid_ripple** | Multi-frequency radial waves | Waves pass through the scene | Water, liquid themes |
| **fluid_warp** | Brightness-gradient velocity | Edges create micro-eddies | Dynamic, techy |
| **phase_distort** | Multi-sine coordinate bend | Glass/water refraction | Luxury, abstract |
| **seamless_drift** | Seamless tile + Lissajous path | Infinite curved scroll | Immersive worlds |

## Quick Start

```bash
# One recipe
python transform_bg_v2.py bubbles.png --recipe glow_bloom --slides 5

# All recipes at once
python transform_bg_v2.py bubbles.png --recipe all --slides 5 --size 1080

# List options
python transform_bg_v2.py --list
```

## Output Structure

```
slide_variants_v2/
├── glow_bloom/          slide_01.png → slide_05.png
├── breathe_life/        slide_01.png → slide_05.png
├── deep_zoom/           slide_01.png → slide_05.png
├── curl_flow/           slide_01.png → slide_05.png
├── liquid_ripple/       slide_01.png → slide_05.png
├── fluid_warp/          slide_01.png → slide_05.png
├── phase_distort/       slide_01.png → slide_05.png
└── seamless_drift/      slide_01.png → slide_05.png
```

Each image is 1080x1080, ready for carousel backgrounds.

## Carousel Integration

```yaml
slides:
  - id: s1
    layout: slide-hook-lockup
    bg_image: "slide_variants_v2/glow_bloom/slide_01.png"
    copy: { ... }

  - id: s2
    layout: slide-stat-hero
    bg_image: "slide_variants_v2/glow_bloom/slide_02.png"
    copy: { ... }
```

## Top 3 Picks for Your Bubble Image

1. **glow_bloom** — Bubbles get bioluminescent. Energy builds toward CTA.
2. **breathe_life** — Subtle pulse. The scene feels alive.
3. **deep_zoom** — Starts dreamy-blur, ends razor-sharp. Cinematic arc.

## Technical Details

- **No external deps** beyond numpy + Pillow
- **Fast**: ~3-5 seconds per 5-slide recipe at 1080px
- **Non-destructive**: Source image never modified directly
- **Bilinear advection**: Smooth inverse warping, no pixelation
- **Curl noise**: Divergence-free vector fields (no compression artifacts)

## Requirements

```
pip install numpy Pillow
```
