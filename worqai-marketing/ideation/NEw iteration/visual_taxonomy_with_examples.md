# VISUAL TAXONOMY FOR CAROUSEL BUILDER
## Complete Reference: 20 Visual Systems with Screenshot Examples
### For Kimi/Claude Implementation — JSON → Python → HTML Pipeline

---

> **How to read this document:**
> Each system has: (1) a technical name, (2) what it looks like, (3) which screenshot shows it, (4) how to implement it in your existing pipeline, (5) a ready-to-use code snippet, (6) feasibility rating for your current architecture.

---

## TIER S — IMPLEMENT NOW (Works in current pipeline, no new abstractions)

These can be added as new `layers`, `decoratives`, or `layout` templates. They use SVG + CSS only. No new architecture needed.

---

### S1. WAFFLE CHART — Visual Proportion Grid

**What it is:** A 10×10 grid of squares. N squares filled with accent color. The rest are faint. More persuasive than text saying "73%."

**Screenshot example:**
- `image.png` — "De cada 100 CVs, solo 25 sobreviven el filtro" — 25 of 100 squares lit in cyan
- This is YOUR existing beyond-elite carousel. You already have this in production.

**Implementation:** New `layout: slide-waffle-chart` OR decorative `layer: waffle-chart-overlay`

**JSON spec usage:**
```json
{
  "layout": "slide-waffle-chart",
  "copy": {
    "stat_number": "73%",
    "filled": 73,
    "headline": "de CVs eliminados antes de revision humana",
    "context": "El ATS filtra automaticamente"
  }
}
```

**HTML implementation:**
```html
<div class="waffle-grid">
  <!-- 100 divs, first N get .filled class -->
  {% for i in range(100) %}
    <div class="waffle-cell {% if i < filled %}filled{% endif %}"></div>
  {% endfor %}
</div>
```

```css
.waffle-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 3px;
  width: 220px;
  height: 220px;
}
.waffle-cell {
  background: rgba(var(--accent-rgb), 0.06);
  border: 1px solid rgba(var(--accent-rgb), 0.1);
  border-radius: 1px;
}
.waffle-cell.filled {
  background: var(--accent);
  box-shadow: 0 0 4px rgba(var(--accent-rgb), 0.4);
}
```

**Feasibility:** EASY. Pure CSS Grid. Add to render engine as new layout template.

---

### S2. DONUT CHART — Circular Progress Ring

**What it is:** A circle with a stroke that fills to show a percentage. Center has the number label. Glowing variant available.

**Screenshot example:**
- `image.png` — "75% RECHAZADOS" with glowing cyan ring on dark background

**Implementation:** New `layout: slide-donut-chart` OR inline SVG in any layout

**JSON spec usage:**
```json
{
  "copy": { "stat_number": "75%", "label": "RECHAZADOS", "fill_pct": 0.75 }
}
```

**HTML implementation:**
```svg
<svg viewBox="0 0 120 120" class="donut-chart">
  <circle cx="60" cy="60" r="50" fill="none"
    stroke="rgba(255,255,255,0.08)" stroke-width="10"/>
  <circle cx="60" cy="60" r="50" fill="none"
    stroke="var(--accent)" stroke-width="10"
    stroke-dasharray="314" stroke-dashoffset="78.5"
    stroke-linecap="round" transform="rotate(-90 60 60)"/>
  <text x="60" y="58" text-anchor="middle" fill="white" font-size="28" font-weight="900">75%</text>
  <text x="60" y="72" text-anchor="middle" fill="#888" font-size="8" letter-spacing="0.2em">RECHAZADOS</text>
</svg>
```

**Feasibility:** EASY. SVG circles with stroke-dasharray. Add to templates.

---

### S3. GLASSMORPHISM PANEL — Frosted Glass Card

**What it is:** Semi-transparent panel with `backdrop-filter: blur()`, light border, subtle inner shadow. Content behind is visible but blurred. Premium depth.

**Screenshot examples:**
- `image(1).png` — "Antes vs. Despues" — two frosted glass panels stacked, one red-tinted, one cyan-tinted
- `image(2).png` — Testimonial card with frosted glass background + gradient avatar circle
- `image(13).png` — Green webinar template with rounded glass panels over gradient

**Implementation:** New CSS class `.glass-panel` usable in any layout

**JSON spec usage:**
```json
{
  "layers": ["glassmorphism-bg"],
  "copy": { "glass_tint": "accent" }
}
```

**HTML implementation:**
```css
.glass-panel {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(40px) saturate(120%);
  -webkit-backdrop-filter: blur(40px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}
/* Fallback for html2canvas (no backdrop-filter support) */
.glass-panel-fallback {
  background: linear-gradient(135deg,
    rgba(255,255,255,0.1) 0%,
    rgba(255,255,255,0.03) 50%,
    rgba(var(--accent-rgb), 0.05) 100%);
  border: 1px solid rgba(255,255,255,0.15);
}
```

**Feasibility:** EASY. Pure CSS. Add to carousel-shell.html. NOTE: html2canvas does NOT support backdrop-filter. Use the gradient fallback for html2canvas exports.

---

### S4. INPUT/OUTPUT COMPARISON — "What You Wrote vs What the ATS Sees"

**What it is:** Two panels side by side. Left = clean human-readable text (green border, checkmark). Right = garbled ATS output (red border, monospace, X mark). Central arrow. Instantly demonstrates the WorqAI problem.

**Screenshot example:**
- `image(3).png` — "El ATS lee de izquierda a derecha" — columns vs garbled text demo

**Implementation:** New `layout: slide-input-output`

**JSON spec usage:**
```json
{
  "layout": "slide-input-output",
  "copy": {
    "input_label": "LO QUE ESCRIBISTE",
    "input_text": "EXPERIENCIA | SKILLS | Ingeniera de Datos | Python - SQL - AWS",
    "output_label": "LO QUE VE EL ATS",
    "output_text": "EXPERIENCIASKILLSIngenieradeDatosPythonSQLAWSBancoNacional2022-2025"
  }
}
```

**HTML implementation:**
```html
<div class="io-comparison">
  <div class="io-panel io-human">
    <div class="io-label">{{ input_label }}</div>
    <div class="io-content">{{ input_text }}</div>
    <div class="io-icon io-check">&#10003;</div>
  </div>
  <div class="io-arrow">&#8594;</div>
  <div class="io-panel io-ats">
    <div class="io-label">{{ output_label }}</div>
    <div class="io-content">{{ output_text }}</div>
    <div class="io-icon io-x">&#10007;</div>
  </div>
</div>
```

```css
.io-panel { padding: 20px; border-radius: 12px; flex: 1; }
.io-human { border: 1px solid rgba(0,255,150,0.3); background: rgba(0,255,150,0.05); }
.io-ats { border: 1px solid rgba(255,50,50,0.3); background: rgba(255,50,50,0.05); font-family: monospace; }
.io-arrow { font-size: 36px; color: var(--accent); align-self: center; }
```

**Feasibility:** EASY. Flexbox + CSS. Add as new layout template.

---

### S5. BEFORE/AFTER PANELS — Transformation Comparison

**What it is:** Two stacked panels. Top = before (problem, muted). Bottom = after (solution, accent). "VS" badge overlapping the boundary. Progress bars inside each.

**Screenshot example:**
- `image(1).png` — "Antes vs. Despues" — CV con columnas (3% legible) vs CV optimizado (98% legible) with animated progress bars

**Implementation:** New `layout: slide-before-after`

**JSON spec usage:**
```json
{
  "layout": "slide-before-after",
  "copy": {
    "before_label": "CV CON COLUMNAS",
    "before_text": "El ATS ve caos estructural...",
    "before_pct": 3,
    "after_label": "CV OPTIMIZADO ATS PURO",
    "after_text": "Texto plano, estructura estandar...",
    "after_pct": 98
  }
}
```

**Feasibility:** EASY. Two divs + progress bar CSS. Add as new layout template.

---

### S6. TOPOGRAPHIC CONTOUR LINES — Flowing Terrain Lines

**What it is:** Parallel curved lines flowing across the slide like a topographic map. Creates depth and sophistication without chaos.

**Screenshot examples:**
- `image(11).png` — "Technology of Tomorrow" and "Technology & Innovation" slides — flowing curved contour lines on dark teal
- `image(10).png` — Dark carousel — flowing ribbon-like contour lines

**Implementation:** New `layer: geo-contour-lines`

**HTML implementation:**
```svg
<svg viewBox="0 0 1080 1080" class="geo-contour" preserveAspectRatio="none">
  {% for offset in range(-5, 6) %}
    {% set alpha = 0.5 - (offset|abs) * 0.08 %}
    <path d="M0,{{ 540 + offset * 60 }}
      Q{{ 135 }} {{ 440 + offset * 50 + loop.index * 20 }}
      {{ 270 }} {{ 540 + offset * 60 }}
      Q{{ 405 }} {{ 640 + offset * 50 - loop.index * 15 }}
      {{ 540 }} {{ 540 + offset * 60 }}
      Q{{ 675 }} {{ 440 + offset * 50 + loop.index * 10 }}
      {{ 810 }} {{ 540 + offset * 60 }}
      Q{{ 945 }} {{ 640 + offset * 50 - loop.index * 5 }}
      {{ 1080 }} {{ 540 + offset * 60 }}"
      fill="none" stroke="var(--accent)" stroke-width="1"
      opacity="{{ max(0.03, alpha) }}"/>
  {% endfor %}
</svg>
```

```css
.geo-contour {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}
.geo-contour path { vector-effect: non-scaling-stroke; }
```

**Feasibility:** EASY. SVG paths with quadratic bezier curves. Add to LAYER_HTML in render engine. Parameter: `density` (3-15 lines), `curve_strength` (0-100).

---

### S7. HORIZONTAL STACKED BARS — Data Bars with Labels

**What it is:** Horizontal bars with percentage fills, labels, and accent colors. Like image.png shows for "STARTUPS 62%, CORPORATIVO 89%, REMOTO US 94%."

**Screenshot example:**
- `image.png` — Three horizontal bars on right side with colored fills and percentage labels

**Implementation:** New `layout: slide-data-bars` OR component usable in any layout

**HTML implementation:**
```html
<div class="data-bar-item">
  <div class="data-bar-label">STARTUPS</div>
  <div class="data-bar-track">
    <div class="data-bar-fill" style="width: 62%"></div>
  </div>
  <div class="data-bar-pct">62%</div>
</div>
```

```css
.data-bar-track { width: 100%; height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; }
.data-bar-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-light)); border-radius: 4px; }
```

**Feasibility:** EASY. CSS only. Add to carousel-shell.html.

---

## TIER A — IMPLEMENT WITH MODERATE EFFORT (New layer types, some engine changes)

These need new abstractions in the render engine but don't require architectural changes.

---

### A1. NEON AURA RING — Glowing Portal Effect

**What it is:** A circular ring with multiple glow layers (inner, mid, outer). Creates a portal/gateway feel. Center can hold text.

**Screenshot examples:**
- `image(11).png` — "The Future Is Now" slide — glowing green ring on dark background, text inside
- `image(12).png` — Top-right slide — neon ring effect around text

**Implementation:** New `layer: geo-neon-ring` OR `decorative: neon-aura`

**HTML implementation:**
```svg
<svg viewBox="0 0 400 400" class="neon-aura">
  <defs>
    <filter id="neonGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="20" result="blur1"/>
      <feGaussianBlur stdDeviation="40" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <!-- Outer glow -->
  <circle cx="200" cy="200" r="160" fill="none" stroke="var(--accent)" stroke-width="30"
    opacity="0.08" filter="url(#neonGlow)"/>
  <!-- Mid glow -->
  <circle cx="200" cy="200" r="150" fill="none" stroke="var(--accent)" stroke-width="12"
    opacity="0.2" filter="url(#neonGlow)"/>
  <!-- Main ring -->
  <circle cx="200" cy="200" r="140" fill="none" stroke="var(--accent)" stroke-width="4"
    opacity="0.9" filter="url(#neonGlow)"/>
  <!-- Inner edge -->
  <circle cx="200" cy="200" r="130" fill="none" stroke="var(--accent)" stroke-width="1"
    opacity="0.3"/>
</svg>
```

**Feasibility:** MEDIUM. SVG filters work in both Playwright and html2canvas. Add to DECORATIVE_HTML.

---

### A2. PARTICLE CONSTELLATION NETWORK — Connected Dots

**What it is:** Small dots connected by thin lines. Like a neural network or star constellation. Distance-based connections.

**Screenshot examples:**
- `image(11).png` — "Machine Learning" slide — dots connected by lines, network pattern
- `image(12).png` — "Advanced Technology" top-right — constellation of connected nodes

**Implementation:** New `layer: geo-constellation`

**HTML implementation:**
```svg
<svg viewBox="0 0 1080 1080" class="geo-constellation">
  <!-- Pre-generated nodes and connections -->
  <g stroke="var(--accent)" stroke-width="0.5" opacity="0.25">
    <line x1="100" y1="200" x2="250" y2="180"/>
    <line x1="250" y1="180" x2="400" y2="300"/>
    <line x1="400" y1="300" x2="550" y2="250"/>
    <!-- 20-30 more connections -->
  </g>
  <g fill="var(--accent)">
    <circle cx="100" cy="200" r="3" opacity="0.8"/>
    <circle cx="250" cy="180" r="4" opacity="0.9"/>
    <circle cx="400" cy="300" r="3" opacity="0.7"/>
    <!-- 20-30 more nodes -->
  </g>
</svg>
```

**Feasibility:** MEDIUM. Best as pre-generated SVG (not runtime Canvas) since carousels are static exports. Add `seed` parameter for reproducible patterns. Generate 20-30 nodes with distance-based connections.

---

### A3. HEXAGONAL TESSELLATION — Molecular Grid

**What it is:** Repeating hexagonal grid. Looks like molecular structure, graphene, or honeycomb.

**Screenshot examples:**
- `image(11).png` — "Advanced Technology" bottom-right — hexagonal grid pattern
- `image(12).png` — "Cloud Network" bottom-right — hexagonal pattern with glow

**Implementation:** New `layer: geo-hex-mesh`

**HTML implementation:**
```svg
<svg viewBox="0 0 1080 1080" class="geo-hex-mesh" preserveAspectRatio="none">
  <defs>
    <pattern id="hexPattern" x="0" y="0" width="52" height="90" patternUnits="userSpaceOnUse">
      <path d="M26,0 L52,15 L52,45 L26,60 L0,45 L0,15 Z"
        fill="none" stroke="var(--accent)" stroke-width="0.5" opacity="0.15"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#hexPattern)"/>
</svg>
```

**Feasibility:** MEDIUM. SVG pattern. Add to LAYER_HTML. Parameter: `scale` (30-80px hex size), `opacity` (0.05-0.3).

---

### A4. 3D PERSPECTIVE WIREFRAME GRID — Depth Lines

**What it is:** Grid lines that recede toward a vanishing point. Creates "entering the matrix" depth.

**Screenshot examples:**
- `image(11).png` — "Technology & Innovation" slide — diagonal grid receding into depth
- `image(11).png` — "Welcome to the Metaverse" — 3D grid effect

**Implementation:** New `layer: geo-perspective-grid`

**HTML implementation:**
```css
.perspective-grid {
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  background-image:
    linear-gradient(var(--accent) 1px, transparent 1px),
    linear-gradient(90deg, var(--accent) 1px, transparent 1px);
  background-size: 60px 60px;
  opacity: 0.08;
  transform: perspective(600px) rotateX(55deg);
  transform-origin: center center;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 70%);
}
```

**Feasibility:** MEDIUM. CSS transforms. The `perspective()` and `rotateX()` may have edge cases in html2canvas — test before deploying. Add as CSS class in carousel-shell.html.

---

### A5. FLOWING BLOB CONTINUITY — Visual Echo Across Slides

**What it is:** The SAME organic shape placed at different positions on each slide. Creates the illusion of flow when swiping. NOT one continuous element (impossible on Instagram) — it's the same SVG path with different transforms.

**Screenshot examples:**
- `image(8).png` — Yellow carousel — large yellow S-curve shape repositioned across 5 slides
- `image(10).png` — Dark carousel — ribbon wave flows through all slides

**Implementation:** New `layer: flow-blob` with `position` and `transform` parameters

**JSON spec usage:**
```json
{
  "meta": { "continuity_shape": "flow-wave" },
  "slides": [
    { "layers": [{"id": "flow-wave", "position": "br", "transform": "rotate(-20deg) scale(1.2)"}] },
    { "layers": [{"id": "flow-wave", "position": "center", "transform": "rotate(15deg) scale(1.5)"}] },
    { "layers": [{"id": "flow-wave", "position": "tl", "transform": "rotate(50deg) scale(0.9)"}] }
  ]
}
```

**HTML implementation:**
```svg
<svg class="flow-blob" style="position:absolute; {{ position_css }}; {{ transform }};">
  <!-- SAME path on every slide, only position/rotation changes -->
  <path d="M200,100 Q400,0 500,200 Q600,400 400,500 Q200,600 100,400 Q0,200 200,100"
    fill="var(--accent)" opacity="0.12"/>
</svg>
```

**Feasibility:** MEDIUM. Requires render engine to recognize `meta.continuity_shape` and inject the same path with different transforms per slide. This is the KEY to making carousels feel premium on Instagram.

---

### A6. LIQUID GLASS BLOB — Glossy 3D Drop

**What it is:** A large organic shape with a glossy highlight streak and gradient depth. Looks like a 3D rendered liquid drop or glass form.

**Screenshot example:**
- `image(13).png` — Green webinar — large glossy green blob with white highlight, looks 3D

**Implementation:** New `layer: geo-liquid-blob` with SVG filters

**HTML implementation:**
```svg
<svg viewBox="0 0 400 400">
  <defs>
    <linearGradient id="liquidGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="var(--accent-light)"/>
      <stop offset="100%" stop-color="var(--accent)"/>
    </linearGradient>
    <filter id="specular">
      <feGaussianBlur in="SourceAlpha" stdDeviation="4"/>
      <feSpecularLighting surfaceScale="6" specularConstant="1.2"
        specularExponent="25" lighting-color="white">
        <fePointLight x="80" y="-100" z="200"/>
      </feSpecularLighting>
      <feComposite in2="SourceAlpha" operator="in"/>
    </filter>
  </defs>
  <path d="M200,40 Q360,40 360,200 Q360,360 200,360 Q40,360 40,200 Q40,40 200,40"
    fill="url(#liquidGrad)" opacity="0.3"/>
  <!-- Highlight streak -->
  <ellipse cx="140" cy="120" rx="80" ry="30"
    fill="white" opacity="0.15" transform="rotate(-25 140 120)"/>
</svg>
```

**Feasibility:** MEDIUM. SVG `feSpecularLighting` filter. Works in Playwright, test in html2canvas.

---

### A7. BOKEH / LENS BLUR ORBS — Atmospheric Depth

**What it is:** Soft, out-of-focus light circles of various sizes scattered across the background. Creates depth and atmosphere.

**Screenshot example:**
- `image(12).png` — "Global Connection" slide — soft blue/purple bokeh orbs in background

**Implementation:** New `layer: geo-bokeh`

**HTML implementation:**
```css
.bokeh-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
}
.bokeh-orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle,
    rgba(var(--accent-rgb), 0.35) 0%,
    rgba(var(--accent-rgb), 0.15) 40%,
    rgba(var(--accent-rgb), 0) 70%);
  filter: blur(30px);
}
.bokeh-orb:nth-child(1) { width: 200px; height: 200px; top: 10%; left: 15%; }
.bokeh-orb:nth-child(2) { width: 300px; height: 300px; top: 50%; left: 60%; }
.bokeh-orb:nth-child(3) { width: 150px; height: 150px; top: 70%; left: 20%; }
```

**Feasibility:** MEDIUM. CSS radial-gradient + blur. Add to carousel-shell.html. Use `seed` parameter for reproducible positioning.

---

### A8. SCAN LINES / CRT EFFECT — Digital Texture Overlay

**What it is:** Horizontal lines across the entire slide. Retro/digital feel. Subtle but adds texture.

**Screenshot example:**
- `image(11).png` — Several slides have subtle horizontal scan lines

**Implementation:** New `layer: geo-scan-lines`

**HTML implementation:**
```css
.scan-lines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 3px,
    rgba(0, 0, 0, 0.03) 3px,
    rgba(0, 0, 0, 0.03) 6px
  );
  pointer-events: none;
  z-index: 5;
  mix-blend-mode: overlay;
}
```

**Feasibility:** EASY. Pure CSS. Add to carousel-shell.html. Works in both renderers.

---

## TIER B — IMPLEMENT WITH SIGNIFICANT EFFORT (New architecture needed)

These require new abstractions in the render pipeline. Not just new templates — new concepts.

---

### B1. CROSS-SLIDE MASTER CANVAS — Visual Continuity

**What it is:** Instead of rendering 5 separate 1080×1080 slides, render ONE 5400×1080 canvas and crop it into 5 slides. This enables true visual continuity — shapes that actually flow from slide to slide, not just look like they do.

**Key insight from ChatGPT:** This is how professional carousels achieve that "flowing through slides" effect. It's NOT done by matching shapes across separate images — it's done by slicing one large composition.

**Implementation:** New render mode in `render_carousel.py`

```python
# In render_carousel.py
if spec.get("meta", {}).get("cross_slide_canvas", False):
    # Render one 5400x1080 SVG
    canvas_width = 1080 * len(spec["slides"])
    master_svg = render_master_canvas(spec, canvas_width, 1080)
    # Crop into 5 slides at export time
    for i, slide in enumerate(spec["slides"]):
        x_offset = i * 1080
        cropped = crop_svg(master_svg, x_offset, 0, 1080, 1080)
        save_slide(cropped, i)
else:
    # Current behavior: render each slide independently
    for i, slide in enumerate(spec["slides"]):
        render_single_slide(slide, i)
```

**JSON spec usage:**
```json
{
  "meta": {
    "cross_slide_canvas": true,
    "canvas_width": 5400,
    "continuity_mode": "flowing_shape"
  }
}
```

**Feasibility:** HARD. Requires:
1. New render path in `render_carousel.py`
2. Master canvas SVG generation
3. SVG cropping logic at export time
4. New layout positioning system (positions are now relative to 5400px canvas, not 1080px)

**BUT:** This is the single biggest upgrade for premium feel. All the "flowing through slides" effects in image(8), image(9), image(10) are achieved this way.

---

### B2. VISUAL DNA SYSTEM — Parameterized Background Generation

**What it is:** Instead of picking a background "template," you define a "visual DNA" — parameters that generate a unique procedural background. This prevents template fatigue and enables infinite variation.

**Concept from ChatGPT:**
```json
{
  "visual_dna": {
    "background_family": "flow_field",
    "depth_style": "volumetric",
    "continuity": "cross_slide",
    "motion_energy": 0.7,
    "glow_strength": 0.4,
    "noise_texture": 0.2,
    "geometry_density": 0.5
  }
}
```

**Implementation:** New module `background_engine.py`

```python
# background_engine.py
BACKGROUND_GENERATORS = {
    "flow_field": generate_flow_field,
    "contour": generate_contour_lines,
    "parametric_mesh": generate_parametric_mesh,
    "aurora": generate_aurora_glow,
    "constellation": generate_constellation,
    "perspective_grid": generate_perspective_grid,
    "hex_mesh": generate_hex_mesh,
    "bokeh": generate_bokeh_field,
}

def generate_background(dna, system_colors, slide_index, total_slides):
    family = dna["background_family"]
    generator = BACKGROUND_GENERATORS[family]
    return generator(dna, system_colors, slide_index, total_slides)
```

**Feasibility:** HARD. Requires new abstraction layer. But it's the future — "generators, not templates."

---

### B3. GENERATIVE TYPOGRAPHIC FIELDS — Text as Texture

**What it is:** Typography used as texture/structure. Repeated text, distorted type, layered typography creating a visual field.

**Implementation:** New `layer: geo-text-field`

**HTML implementation:**
```svg
<svg viewBox="0 0 1080 1080" class="geo-text-field">
  <defs>
    <pattern id="textPattern" x="0" y="0" width="200" height="30" patternUnits="userSpaceOnUse">
      <text x="0" y="20" fill="var(--accent)" opacity="0.06"
        font-size="14" font-family="var(--font-mono)" letter-spacing="0.3em">
        WORQAI ATS OPTIMIZE CV
      </text>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#textPattern)"/>
</svg>
```

**Feasibility:** MEDIUM-HARD. SVG pattern with text. Works in both renderers. Add to LAYER_HTML.

---

## TIER C — DEFERRED (High effort, marginal Instagram impact)

These are visually impressive but don't translate well to 1080×1080 static PNGs on Instagram.

---

### C1. VOLUMETRIC LIGHT SYSTEMS — Cinematic Beams

**What it is:** Simulated atmospheric light beams (like fog or lasers). Very cinematic.

**Why deferred:** Requires WebGL or complex SVG gradients. The effect is subtle at 1080×1080 and gets lost on mobile. Better suited for video/animation.

---

### C2. PROCEDURAL NOISE DISTORTION — Turbulence Geometry

**What it is:** Geometry distorted with Perlin/simplex noise. Creates organic, unpredictable patterns.

**Why deferred:** Requires runtime noise generation (Canvas or WebGL). SVG can't do this natively. Could pre-generate static noise textures, but loses the "procedural" advantage.

---

### C3. ISOMETRIC ABSTRACT WORLDS — Pseudo-3D Scenes

**What it is:** Miniature isometric worlds with layered depth.

**Why deferred:** Requires illustration assets or complex CSS 3D transforms. Not suitable for a text/content carousel system.

---

### C4. FRACTAL SYSTEMS — Recursive Geometry

**What it is:** Self-similar repeating mathematical patterns.

**Why deferred:** Visually overwhelming for a content carousel. Better as standalone art, not background.

---

### C5. CHROMATIC LIGHT LEAK — RGB Edge Glow

**What it is:** Lens flare / chromatic aberration effect with RGB color separation at edges.

**Why deferred:** Complex multi-layer SVG filters. The effect is subtle and can look like a rendering error if not done perfectly.

---

## MERGED TAXONOMY — ALL 20 SYSTEMS IN ONE TABLE

| ID | System Name | Tier | Effort | Screenshot | Your System Status |
|----|------------|------|--------|------------|-------------------|
| S1 | Waffle Chart | S | Easy | `image.png` | Already in ref, not in Claude's output |
| S2 | Donut Chart | S | Easy | `image.png` | Already in ref, not in Claude's output |
| S3 | Glassmorphism Panel | S | Easy | `image(1).png`, `image(2).png`, `image(13).png` | Already in ref, not in Claude's output |
| S4 | Input/Output Comparison | S | Easy | `image(3).png` | Already in ref, not in Claude's output |
| S5 | Before/After Panels | S | Easy | `image(1).png` | NEW — not in any ref |
| S6 | Topographic Contour Lines | S | Easy | `image(11).png`, `image(10).png` | Has `geo-topo-lines` but basic |
| S7 | Horizontal Data Bars | S | Easy | `image.png` | Already in ref, not in Claude's output |
| A1 | Neon Aura Ring | A | Medium | `image(11).png`, `image(12).png` | NEW |
| A2 | Particle Constellation | A | Medium | `image(11).png`, `image(12).png` | NEW |
| A3 | Hexagonal Tessellation | A | Medium | `image(11).png`, `image(12).png` | NEW |
| A4 | 3D Perspective Grid | A | Medium | `image(11).png` | NEW |
| A5 | Flowing Blob Continuity | A | Medium | `image(8).png`, `image(10).png` | Has blobs, not continuity system |
| A6 | Liquid Glass Blob | A | Medium | `image(13).png` | NEW |
| A7 | Bokeh/Lens Blur Orbs | A | Medium | `image(12).png` | NEW |
| A8 | Scan Lines / CRT | A | Medium | `image(11).png` | NEW |
| B1 | Cross-Slide Master Canvas | B | Hard | `image(8).png`, `image(9).png` | NEW — biggest impact upgrade |
| B2 | Visual DNA Generator | B | Hard | N/A (conceptual) | NEW — future architecture |
| B3 | Typographic Fields | B | Medium-Hard | N/A | NEW |
| C1-C5 | Volumetric, Noise, Isometric, Fractal, Chromatic | C | Very Hard | N/A | DEFERRED — not for static carousels |

---

## IMPLEMENTATION PRIORITY — WHAT TO BUILD FIRST

**Phase 1 (This session):**
1. S1 Waffle Chart — add as new layout
2. S3 Glassmorphism Panel — add as CSS class
3. S4 Input/Output Comparison — add as new layout
4. S6 Topographic Contour Lines — enhance existing `geo-topo-lines`

**Phase 2 (Next session):**
5. S5 Before/After Panels — add as new layout
6. S2 Donut Chart — add as component
7. A5 Flowing Blob Continuity — add continuity system
8. A8 Scan Lines — add as layer

**Phase 3 (Architecture upgrade):**
9. B1 Cross-Slide Master Canvas — new render path
10. A1 Neon Aura Ring — add as decorative
11. A2 Particle Constellation — add as layer
12. A3 Hexagonal Tessellation — add as layer

**Phase 4 (Future):**
13. B2 Visual DNA Generator — new background engine module
14. A4 3D Perspective Grid — CSS transforms
15. A6 Liquid Glass Blob — SVG filters
16. A7 Bokeh Orbs — CSS gradients

---

## CRITICAL RULES FOR IMPLEMENTATION

1. **GENERATORS, NOT TEMPLATES** — Every visual system should accept parameters (seed, density, opacity, scale) so it generates a unique result each time. No two carousels should have identical backgrounds.

2. **SYSTEMIC PRIMITIVES** — Don't add isolated decorative blobs. Add blob SYSTEMS that interact with typography, create depth, and connect across slides. Same primitive, entirely different role.

3. **INSTAGRAM-COMPATIBLE ONLY** — Every effect must work as a 1080×1080 static PNG. No animations, no hover states, no continuous canvas tricks. If it doesn't export to PNG, don't add it.

4. **HTML2CANVAS FALLBACK** — Every effect needs a fallback that works without `backdrop-filter`, `mix-blend-mode`, or WebGL. Test both export paths.

5. **SHOW, DON'T TELL** — Every carousel must have at least one slide that visually demonstrates the problem (waffle chart, input/output, before/after). Text-only data slides are anti-pattern.
