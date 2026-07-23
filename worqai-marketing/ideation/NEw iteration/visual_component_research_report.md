# VISUAL COMPONENT RESEARCH REPORT
## What's Missing From Your Carousel System — Named, Catalogued, Implementation-Ready

---

## EXECUTIVE SUMMARY

I analyzed 14 screenshots (6 template gallery references + 4 existing WorqAI carousels + 3 new uploads) and researched implementation techniques. I found **23 distinct visual components** that professional carousels use. Your current system has **4 of them**. **19 are missing.**

The biggest gaps: **no data visualization**, **no glassmorphism**, **no texture overlays**, **no demonstration layouts**, and **no 3D geometric backgrounds**.

---

## PART 1: EVERY VISUAL TECHNIQUE IN YOUR SCREENSHOTS — NAMED & IDENTIFIED

### A. From image(8) — Yellow Social Media Carousel

| # | Visual Element | Technical Name | What It Is |
|---|---------------|----------------|------------|
| 1 | **Large yellow flowing shape** | **SVG Organic Morph / Blob Transition** | A single organic S-curve shape that is repositioned (not reshaped) across slides to create visual continuity. Same path, different translate/rotate per slide. |
| 2 | **Small dot clusters** | **Dot Grid Pattern** | 4x4 or 5x5 grids of small circles used as decorative texture. Creates a "digital/confetti" feel. |
| 3 | **Arrow between slides** | **Slide Connector Arrow** | Thin arrow lines connecting slide content visually. Indicates sequence/flow. |
| 4 | **Curved photo mask** | **Organic Clip-Path Mask** | Photo is not rectangular — it's masked by an organic/blob shape. Creates softness. |
| 5 | **Numbered steps with # prefix** | **Decorative Number Prefix** | Numbers like #1, #2 with a decorative hash/number sign treated as a design element, not just text. |

### B. From image(9) — Yellow Carousel (Phone Mockup)

| # | Visual Element | Technical Name | What It Is |
|---|---------------|----------------|------------|
| 6 | **Circular photo frames** | **Circle Mask Portrait** | Photos masked to perfect circles. Clean, modern, approachable. |
| 7 | **Floating bubble dots** | **Floating Orb Clusters** | Various-sized circles scattered like bubbles. Different opacities create depth. |

### C. From image(10) — Dark Teal Carousel

| # | Visual Element | Technical Name | What It Is |
|---|---------------|----------------|------------|
| 8 | **Large flowing ribbon** | **SVG Ribbon Wave** | A wide, flowing ribbon-like shape that snakes through all slides. Dark teal on black. Creates elegance and movement. |
| 9 | **Pagination progress dots** | **Progress Indicator Dots** | Row of circles at bottom showing current slide position (filled vs empty). Creates "this is part of a sequence" context. |
| 10 | **Profile avatar circle** | **Avatar Badge** | Small circle with photo/initials at top-left of each slide. Creates authorship/brand consistency. |

### D. From image(11) — THE KEY REFERENCE (9 Tech Slides)

This is the most visually sophisticated set. Every single slide uses a different technique:

| # | Visual Element | Technical Name | What It Is |
|---|---------------|----------------|------------|
| 11 | **Flowing parallel curved lines** | **Topographic Contour Lines / Isohypses** | Parallel curved lines that flow across the slide like a topographic map. Each line follows the same path at different offsets. Pure SVG paths with varying stroke-opacity. |
| 12 | **Diagonal grid with depth** | **3D Perspective Wireframe Grid** | A grid of lines that appear to recede into 3D space (perspective transform). Lines get closer together toward a vanishing point. Creates "entering the matrix" feel. |
| 13 | **Glowing neon circle ring** | **Neon Aura Ring / Glowing Torus** | A circular ring with inner and outer glow (feGaussianBlur SVG filter). The center is hollow, creating a portal/portal effect. Green/cyan on dark. |
| 14 | **Hexagonal grid pattern** | **Hexagonal Tessellation / Honeycomb Mesh** | Repeating hexagonal grid that looks like molecular structure or graphene. Can be rendered as lines or filled cells. SVG pattern or CSS clip-path. |
| 15 | **Curved parallel wave lines** | **Flowing Wave Lines / Sound Wave Pattern** | Parallel lines that curve in a wave pattern. Like a fingerprint or sound wave visualization. SVG paths with consistent amplitude. |
| 16 | **Glowing dots with connections** | **Particle Constellation Network** | Small dots connected by thin lines. Distance-based: dots within X px connect. Creates a "neural network" or "constellation" effect. Canvas or SVG. |

### E. From image(12) — Tech Carousel (9 Slides)

| # | Visual Element | Technical Name | What It Is |
|---|---------------|----------------|------------|
| 17 | **Circuit traces with nodes** | **Circuit Board Trace Pattern** | Lines that branch and connect at glowing nodes/vertices. Like a PCB circuit board. SVG paths with circle nodes at intersections. |
| 18 | **Bokeh light spots** | **Bokeh / Lens Blur Orbs** | Soft, out-of-focus light circles of various sizes. CSS radial-gradient with heavy blur. Creates depth and atmosphere. |
| 19 | **Diagonal light rays** | **Light Ray / Lens Flare Beams** | Diagonal beams of light emanating from a corner. CSS linear-gradient at an angle with transparency. |
| 20 | **Wave grid overlay** | **Deformed Grid / Warped Mesh** | A grid where lines curve/warp as if viewed through a lens or flowing water. SVG paths with mathematical curve functions. |

### F. From image(13) — Green Webinar Template

| # | Visual Element | Technical Name | What It Is |
|---|---------------|----------------|------------|
| 21 | **Frosted glass panels** | **Glassmorphism Cards** | Semi-transparent panels with backdrop-filter: blur(), light border (rgba white), and subtle shadow. Content behind is visible but blurred. |
| 22 | **Large glossy 3D blob** | **Liquid Gradient Blob / Glossy Morph** | A large organic shape with a glossy highlight (white streak at top) and gradient depth. Looks like a 3D rendered liquid drop. SVG gradient + feSpecularLighting filter. |
| 23 | **Thin curved connector lines** | **Arc Connector Lines** | Thin lines that arc between elements, suggesting flow or connection. SVG quadratic bezier curves. |

---

## PART 2: WHAT YOUR EXISTING WORQAI CAROUSELS HAVE

From image.png through image(3).png — the carousels you said have better elements:

| Element | Present? | Where |
|---------|----------|-------|
| Waffle chart (100-square grid) | Yes | image.png — 25/100 squares lit |
| Donut chart with glow | Yes | image.png — 75% glowing ring |
| Horizontal stacked bars | Yes | image.png — 3 bars with % labels |
| Glassmorphism panels | Yes | image(1).png, image(2).png — frosted cards |
| Before/after comparison | Yes | image(1).png — two panels with "vs" badge |
| Progress bar with fill | Yes | image(1).png — 3% vs 98% bars |
| Corner frames (L-brackets) | Yes | All 4 screenshots — consistent system element |
| Testimonial card with avatar | Yes | image(2).png — glass card + gradient circle |
| Rotated stamp badge | Yes | image(2).png — "CASO REAL" rotated circle |
| Input/output demo blocks | Yes | image(3).png — columns vs garbled text |
| Pill tag | Yes | image(3).png — "BOMBA 02 - COLUMNAS" |
| Highlighted text span | Yes | image(3).png — "derecha" in green highlight |
| Watermark letter | Yes | image(3).png — "W" in background |

**These 12 elements are in your reference carousels but MISSING from Claude's latest 3 carousels.** This is the gap — the system CAN do these (they're in the reference HTMLs), but Claude didn't use them.

---

## PART 3: WHAT CLAUDE'S 3 CAROUSELS ACTUALLY USED

From the 15 slides analyzed:

| Element | Count | Assessment |
|---------|-------|------------|
| Blob (svg-blob, 5 positions) | 8 instances | OVERUSED — same shape, different position |
| Glow orb | 10 instances | OVERUSED — on every slide of s01 and s04 |
| Starburst decorative | 6 instances | Fine — varied per slide |
| Corner frame | 3 instances | Underused — should be consistent system element |
| Terminal component | 3 instances | Fine — purposeful, content-driven |
| Chrome badge stamp | 3 instances | BUG — overlaps text on 2 slides |
| Text treatment (gradient/stroke/glow) | 4 instances | Fine — varied per slide |
| Watermark number | 1 instance | Underused — should reinforce key stat |
| Data visualization | **0** | MISSING |
| Glassmorphism panels | **0** | MISSING |
| Demonstration blocks | **0** | MISSING |
| Texture overlays | **0** | MISSING |
| 3D geometric backgrounds | **0** | MISSING |
| Progress indicator | **0** | MISSING |

---

## PART 4: ABOUT THAT "3D STUFF" YOU MENTIONED

You asked: *"did we did any 3d stuff i swear we talked about it maybe it got lost"*

**Looking at the handoff memory (WORQAI_HANDOFF_MEMORY.md):**

Section 10 "WHAT TO DO NEXT" lists under Medium Term:
> "11. Asymmetric editorial layouts — full-bleed image + text overlay"
> "10. Add photography support — image_asset field in spec, duotone filters"

There is **NO mention of 3D**, wireframe grids, perspective transforms, or geometric backgrounds in the entire handoff memory. You may have discussed it in a conversation that didn't get persisted, OR you're remembering the reference carousels (beyond-elite) which use 3D perspective wireframe grids — and you wanted that capability added.

**Either way, it didn't get implemented.** Your system currently has ZERO 3D visual capabilities. The `geo-topo-lines` layer exists but it's basic — just a few curved lines, not the sophisticated topographic contour patterns from image(11).

---

## PART 5: IMPLEMENTATION GUIDE — HOW TO ADD EACH COMPONENT

### PRIORITY A — Data Visualization (Biggest Gap)

These are what make carousels persuasive. Text says "73% are rejected." A waffle chart SHOWS it.

#### A1. Waffle Chart (10x10 Grid)
**What:** 100 squares in a grid. N squares are filled with accent color. Rest are faint.
**Implementation:** CSS Grid, 10x10, 10px gaps. Each cell is a div. Fill first N cells with `background: var(--accent)`. Rest get `background: var(--accent)` at 8% opacity + 1px border.
**SVG Alternative:** Single SVG with 100 rect elements. More compact, scales better.
**Best for:** `data`, `shock`, `proof` beats.

```css
.waffle-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 3px;
  width: 200px;
  height: 200px;
}
.waffle-cell {
  background: rgba(var(--accent-rgb), 0.08);
  border: 1px solid rgba(var(--accent-rgb), 0.12);
  border-radius: 1px;
}
.waffle-cell.filled {
  background: var(--accent);
}
```

#### A2. Donut Chart (Circular Progress)
**What:** Circle with stroke-dashoffset showing percentage. Center has number label.
**Implementation:** SVG circle with `stroke-dasharray` and `stroke-dashoffset`. Two circles: background track + filled arc.
**Best for:** `data`, `proof`, `diagnostic` beats.

```svg
<svg viewBox="0 0 120 120">
  <!-- Background track -->
  <circle cx="60" cy="60" r="50" fill="none" 
    stroke="rgba(255,255,255,0.1)" stroke-width="10"/>
  <!-- Filled arc -->
  <circle cx="60" cy="60" r="50" fill="none" 
    stroke="var(--accent)" stroke-width="10"
    stroke-dasharray="314" stroke-dashoffset="78.5"
    stroke-linecap="round" transform="rotate(-90 60 60)"/>
</svg>
```
(78.5 = 314 * 0.25, so 75% filled)

#### A3. Horizontal Stacked Bars
**What:** Bars with labels and percentage fills. Like image.png shows.
**Implementation:** CSS flex row. Background bar (full width, faint) + foreground bar (filled %, accent color).
**Best for:** `data`, `comparison`, `proof` beats.

```css
.bar-track {
  width: 100%;
  height: 8px;
  background: rgba(255,255,255,0.08);
  border-radius: 4px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-light));
  border-radius: 4px;
  width: var(--fill-pct);
}
```

### PRIORITY B — Demonstration Layouts (Show Don't Tell)

#### B1. Input/Output Comparison
**What:** Two panels side by side. Left = human-readable. Right = garbled ATS output. Central arrow.
**Implementation:** Two flex containers. Left has clean text + green border + check icon. Right has monospace garbled text + red border + X icon. Center has large arrow.
**Best for:** `diagnostic`, `shock`, `myth` beats.
**Reference:** image(3).png — "El ATS lee de izquierda a derecha" slide.

```css
.demo-panel-human {
  border: 1px solid rgba(0,255,100,0.3);
  background: rgba(0,255,100,0.05);
  font-family: var(--font-body);
}
.demo-panel-ats {
  border: 1px solid rgba(255,50,50,0.3);
  background: rgba(255,50,50,0.05);
  font-family: 'Courier New', monospace;
  letter-spacing: -0.5px;
}
```

#### B2. Before/After Panels
**What:** Two stacked panels. Top = before (problem). Bottom = after (solution). "vs" badge in center.
**Implementation:** Two glassmorphism cards stacked vertically. Top has muted/reduced styling. Bottom has accent styling. Center has circular "vs" badge overlapping the boundary.
**Best for:** `transformation`, `proof`, `solution` beats.
**Reference:** image(1).png — "Antes vs. Despues" slide.

### PRIORITY C — Glassmorphism (Premium Feel)

#### C1. Glassmorphism Card Container
**What:** Semi-transparent panel with backdrop blur, light border, subtle shadow.
**Implementation:** CSS backdrop-filter. Key properties:

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}
```

**Note:** backdrop-filter does NOT work in html2canvas export. Must use Playwright export only. Or: pre-render the blur as a static gradient overlay for html2canvas compatibility.

**Fallback for html2canvas:**
```css
.glass-panel-fallback {
  background: linear-gradient(135deg, 
    rgba(255,255,255,0.08) 0%, 
    rgba(255,255,255,0.02) 100%);
  border: 1px solid rgba(255, 255, 255, 0.15);
  /* No backdrop-filter — static gradient simulates glass */
}
```

#### C2. Liquid Glass Blob
**What:** A glossy 3D-looking blob with highlight streak and gradient depth.
**Implementation:** SVG with feSpecularLighting filter for the glossy highlight + linearGradient for depth.

```svg
<svg viewBox="0 0 400 400">
  <defs>
    <linearGradient id="blobGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ade80"/>
      <stop offset="100%" stop-color="#16a34a"/>
    </linearGradient>
    <filter id="gloss">
      <feGaussianBlur in="SourceAlpha" stdDeviation="4"/>
      <feSpecularLighting surfaceScale="5" specularConstant="1" 
        specularExponent="20" lighting-color="white">
        <fePointLight x="100" y="-100" z="200"/>
      </feSpecularLighting>
      <feComposite in="SourceGraphic" operator="in"/>
    </filter>
  </defs>
  <path d="M200,50 Q350,50 350,200 Q350,350 200,350 Q50,350 50,200 Q50,50 200,50" 
    fill="url(#blobGrad)" filter="url(#gloss)"/>
</svg>
```

### PRIORITY D — Texture Overlays (Background Depth)

These go IN FRONT of the solid background but BEHIND content. They add visual interest without competing with text.

#### D1. Topographic Contour Lines
**What:** Parallel curved lines flowing across the slide like a topographic map.
**Implementation:** 8-12 SVG paths with the same base curve but different Y-offsets. Stroke-opacity decreases with distance from center.

```svg
<svg viewBox="0 0 1080 1080" opacity="0.15">
  <path d="M0,200 Q270,100 540,200 Q810,300 1080,200" 
    stroke="var(--accent)" fill="none" stroke-width="1"/>
  <path d="M0,250 Q270,150 540,250 Q810,350 1080,250" 
    stroke="var(--accent)" fill="none" stroke-width="1" opacity="0.8"/>
  <path d="M0,300 Q270,200 540,300 Q810,400 1080,300" 
    stroke="var(--accent)" fill="none" stroke-width="1" opacity="0.6"/>
  <!-- 5-10 more lines -->
</svg>
```

#### D2. 3D Perspective Wireframe Grid
**What:** Grid lines that recede toward a vanishing point, creating depth.
**Implementation:** CSS transform: perspective() + rotateX(). Or SVG paths manually drawn with perspective math.

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
  opacity: 0.1;
  transform: perspective(500px) rotateX(60deg);
  transform-origin: center center;
}
```

#### D3. Hexagonal Tessellation
**What:** Repeating hexagonal grid.
**Implementation:** SVG pattern with hexagon path, repeated. Or CSS clip-path on repeated elements.

```svg
<svg width="100%" height="100%">
  <defs>
    <pattern id="hex" x="0" y="0" width="56" height="100" patternUnits="userSpaceOnUse">
      <path d="M28,0 L56,16 L56,48 L28,64 L0,48 L0,16 Z" 
        fill="none" stroke="var(--accent)" stroke-width="0.5" opacity="0.2"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#hex)"/>
</svg>
```

#### D4. Particle Constellation Network
**What:** Dots connected by lines. Neural network / constellation feel.
**Implementation:** Canvas (for randomness) or pre-generated SVG. 30-50 circle elements + line elements connecting nearby circles.

**For static export (no animation needed):**
```svg
<svg viewBox="0 0 1080 1080">
  <g opacity="0.3" stroke="var(--accent)" stroke-width="0.5">
    <line x1="100" y1="200" x2="250" y2="180"/>
    <line x1="250" y1="180" x2="400" y2="300"/>
    <!-- Pre-generated connections -->
  </g>
  <g fill="var(--accent)">
    <circle cx="100" cy="200" r="2"/>
    <circle cx="250" cy="180" r="3"/>
    <circle cx="400" cy="300" r="2"/>
    <!-- Pre-generated nodes -->
  </g>
</svg>
```

#### D5. Scan Lines / CRT Effect
**What:** Horizontal lines across the entire slide. Retro/digital feel.
**Implementation:** CSS repeating-linear-gradient.

```css
.scan-lines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.03) 2px,
    rgba(0, 0, 0, 0.03) 4px
  );
  pointer-events: none;
  z-index: 5;
}
```

#### D6. Bokeh / Lens Blur Orbs
**What:** Soft out-of-focus light circles.
**Implementation:** CSS radial-gradient positioned absolutely.

```css
.bokeh-orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, 
    rgba(var(--accent-rgb), 0.3) 0%, 
    rgba(var(--accent-rgb), 0) 70%);
  filter: blur(20px);
}
```

### PRIORITY E — "Flowing Through Slides" Effect

You asked about *"this big figure that goes smoothly through the slides"* — from image(8) and image(10).

**What this actually is:** It's NOT one continuous shape across slides. Instagram carousels are separate images. The effect is achieved by:

1. **Same SVG path** on every slide
2. **Different transform** (translate/rotate) per slide
3. **Consistent color** so it "reads" as the same element

**Implementation:**

```svg
<!-- Slide 1: Blob enters from bottom-right -->
<svg class="flow-blob" style="position:absolute; right:-100px; bottom:-150px; transform: rotate(-20deg);">
  <path d="M200,100 Q350,0 400,150 Q450,300 300,350 Q150,400 100,250 Q50,100 200,100" 
    fill="var(--accent)" opacity="0.15"/>
</svg>

<!-- Slide 2: Same blob, repositioned -->
<svg class="flow-blob" style="position:absolute; left:-50px; top:-100px; transform: rotate(45deg) scale(1.2);">
  <path d="M200,100 Q350,0 400,150 Q450,300 300,350 Q150,400 100,250 Q50,100 200,100" 
    fill="var(--accent)" opacity="0.15"/>
</svg>

<!-- Slide 3: Same blob, different position again -->
<!-- etc. -->
```

**Key insight:** The shape is identical. Only position, rotation, and scale change. The human brain connects them visually when swiping. This is called **visual continuity through repetition with transformation** — a classic graphic design principle.

### PRIORITY F — Small Polish Elements

#### F1. Progress Indicator Dots
```html
<div class="progress-dots">
  <span class="dot active"></span>
  <span class="dot"></span>
  <span class="dot"></span>
  <span class="dot"></span>
  <span class="dot"></span>
</div>
```

#### F2. Highlighted Text Span
```css
.text-highlight {
  background: var(--accent);
  color: var(--bg);
  padding: 2px 8px;
  border-radius: 2px;
}
```

#### F3. Organic Photo Mask
```css
.organic-photo-mask {
  clip-path: path('M200,50 Q350,0 380,150 Q410,300 280,380 Q150,460 80,300 Q10,140 200,50');
}
```

---

## PART 6: RECOMMENDED COMPONENT PRIORITY LIST

Ranked by visual impact + implementation effort:

| Priority | Component | Impact | Effort | Instagram-Compatible? |
|----------|-----------|--------|--------|----------------------|
| **P0** | Waffle chart | Very High | Low | Yes |
| **P0** | Glassmorphism card | Very High | Low | Yes (with fallback) |
| **P0** | Input/output comparison | Very High | Medium | Yes |
| **P1** | Donut chart | High | Low | Yes |
| **P1** | Topographic contour lines | High | Medium | Yes |
| **P1** | Before/after panels | High | Medium | Yes |
| **P1** | Horizontal stacked bars | High | Low | Yes |
| **P2** | 3D perspective wireframe grid | High | Medium | Yes |
| **P2** | Hexagonal tessellation | Medium | Medium | Yes |
| **P2** | Particle constellation | Medium | High | Yes |
| **P2** | Flowing blob continuity | Medium | Low | Yes |
| **P3** | Liquid glass blob | Medium | High | Yes |
| **P3** | Bokeh orbs | Low | Low | Yes |
| **P3** | Scan lines | Low | Low | Yes |
| **P3** | Progress indicator dots | Low | Low | Yes |

---

## PART 7: ABOUT CROSS-SLIDE CONTINUITY (THE "FLOWING" EFFECT)

You asked: *"that background it has like this big figure that goes smoothly through the slides what is this"*

**The answer:** It's the same shape (SVG path) placed at different positions on each slide. NOT one continuous element. Each slide is a separate 1080x1080 PNG on Instagram. The "flow" is an illusion created by:

1. **Identical path data** (same shape every time)
2. **Different CSS transform** (different position/rotation/scale per slide)
3. **Same color** (so the brain connects them)
4. **Exit/entry logic** (shape exits one side of slide N, enters from that side on slide N+1)

This is a graphic design technique called **visual echo** or **motif repetition**. It's been used in print editorial for decades. Your system can do this TODAY — just use the same blob SVG with different positioning on each slide. Claude didn't do it because he used different blob positions (tr, bl, center, scattered) rather than a consistent shape with intentional entry/exit flow.

**How to implement in your spec:**

```json
{
  "meta": { "system": "s01", "continuity_shape": "flow-wave" },
  "slides": [
    { "layers": [{"id": "flow-wave", "position": "enter-br", "transform": "rotate(-20deg)" }] },
    { "layers": [{"id": "flow-wave", "position": "center", "transform": "rotate(10deg) scale(1.3)" }] },
    { "layers": [{"id": "flow-wave", "position": "exit-tl", "transform": "rotate(45deg) scale(0.8)" }] }
  ]
}
```

The render engine would use the SAME SVG path but apply different transforms. This is what image(8) and image(10) are doing.

---

## SUMMARY: WHAT TO ADD TO YOUR SYSTEM

**The 6 things that matter most:**

1. **Waffle chart layout** — show data, don't just say it
2. **Glassmorphism card component** — premium depth without blobs
3. **Input/output comparison layout** — demonstrate the ATS problem visually
4. **Topographic contour line layer** — replace blobs with purposeful texture
5. **Visual continuity shape system** — same shape, different position per slide
6. **"Show don't tell" rule** — every carousel must have at least 1 demonstration slide

**The 3 things to remove/reduce:**

1. **Blob usage** — cap at 2 per carousel, require purpose statement
2. **Glow-orb repetition** — max 2 slides per carousel
3. **Text-only data slides** — if a slide has a percentage, it MUST visualize it
