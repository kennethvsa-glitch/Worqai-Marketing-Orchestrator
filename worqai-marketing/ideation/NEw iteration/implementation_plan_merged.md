# IMPLEMENTATION PLAN — MERGED
## Visual Taxonomy + ChatGPT Architecture + Enforcement + Your System

---

## CAN YOUR SYSTEM HANDLE THIS? YES.

Your architecture is already at the right level:
- JSON spec → Python render → HTML → PNG export
- Layer system (blobs, geo layers, decoratives)
- 48 design systems with personalities
- 18-check preflight validator
- Visual richness scorer

**What you need:** New templates, new layer types, and 2 new abstractions (background engine + continuity system). **Not** a rewrite.

---

## THE MERGED PLAN — 4 PHASES

### PHASE 1: ENFORCEMENT (Kimi's best work — prevents bad output)
**Goal:** Make it impossible to ship the same blob 18 times or a badge overlapping text.
**Files to modify:** `preflight.py`, `visual_richness_check.py`
**Time:** 1 session

| # | Rule | File | Implementation |
|---|------|------|---------------|
| 1 | **Blob overuse FAIL** — same blob variant >2× per carousel | `visual_richness_check.py` | Count occurrences of each `svg-blob-*` class in rendered HTML. If any count > 2, FAIL. |
| 2 | **Glow-orb cap** — glow-orb on >50% of slides = FAIL | `visual_richness_check.py` | Count slides with `glow-orb` in layers. If count > slides × 0.5, FAIL. |
| 3 | **Identical layer combos FAIL** — >50% slides share exact same layers array | `visual_richness_check.py` | Hash each slide's `layers` array. If any hash appears on >50% of slides, FAIL. |
| 4 | **Badge collision detection** — chrome-badge-stamp within 150px of headline | `preflight.py` | Check: if slide has `chrome-badge-stamp` AND any `.display-headline` or `.headline` element with `right` position < 200px, FAIL. |
| 5 | **Shape diversity cap** — any single decorative appears on >4 slides total | `preflight.py` | Count each decorative ID across all slides. If any appears > 4 times, FAIL. |
| 6 | **"Show don't tell" rule** — every carousel must have ≥1 data viz or demo layout | `preflight.py` | Check: at least one slide uses `slide-waffle-chart`, `slide-donut-chart`, `slide-input-output`, or `slide-before-after`. If none, FAIL. |
| 7 | **Decoration purpose statement** — every decorative layer must have purpose | `build_carousel.py` | If any layer lacks a `purpose` field (or purpose is "visual interest"), WARN. |

**Code sketch for Rule 1 (blob overuse):**
```python
# visual_richness_check.py
def check_blob_overuse(rendered_html, slide_count):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(rendered_html, 'html.parser')
    blob_counts = {}
    for blob_class in ['svg-blob-tr', 'svg-blob-bl', 'svg-blob-center', 
                       'svg-blob-asymmetric', 'svg-blob-scattered']:
        count = len(soup.find_all(class_=blob_class))
        if count > 0:
            blob_counts[blob_class] = count
    
    failures = []
    for blob, count in blob_counts.items():
        if count > 2:
            failures.append(f"Blob '{blob}' used {count} times (max: 2)")
    
    # Total soft-circle check
    glow_orb_count = len(soup.find_all(class_='glow-orb'))
    vol_light_count = len(soup.find_all(class_='vol-light'))
    total_soft = sum(blob_counts.values()) + glow_orb_count + vol_light_count
    max_soft = int(slide_count * 1.2)
    if total_soft > max_soft:
        failures.append(f"Total soft circles: {total_soft} (max: {max_soft})")
    
    return len(failures) == 0, failures
```

---

### PHASE 2: NEW LAYOUTS (The missing pieces)
**Goal:** Add demonstration and data visualization layouts.
**Files to add:** `templates/slides/slide-*.html` (5 new files)
**Files to modify:** `render_carousel.py` (add to layout registry)
**Time:** 1-2 sessions

#### Layout 1: `slide-waffle-chart` — Visual Proportion Grid
**What:** 10×10 grid. N squares filled. Shows "73%" as 73 lit squares.
**Screenshot ref:** `image.png` (your beyond-elite carousel)
**Beat types:** `data`, `shock`, `proof`

```html
<!-- templates/slides/slide-waffle-chart.html -->
<div class="slide waffle-slide">
  <div class="waffle-content">
    <div class="waffle-stat">
      <span class="waffle-number">{{ copy.stat_number }}</span>
      <span class="waffle-label">{{ copy.label }}</span>
    </div>
    <div class="waffle-grid">
      {% for i in range(100) %}
        <div class="waffle-cell {% if i < copy.filled %}filled{% endif %}"></div>
      {% endfor %}
    </div>
  </div>
  <h2 class="waffle-headline">{{ copy.headline }}</h2>
  <p class="waffle-context">{{ copy.context }}</p>
</div>
```

```css
.waffle-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 3px;
  width: 240px;
  height: 240px;
}
.waffle-cell {
  background: rgba(var(--accent-rgb), 0.06);
  border: 1px solid rgba(var(--accent-rgb), 0.08);
  border-radius: 1px;
}
.waffle-cell.filled {
  background: var(--accent);
  box-shadow: 0 0 6px rgba(var(--accent-rgb), 0.35);
}
```

#### Layout 2: `slide-input-output` — ATS Demo
**What:** Two panels. Left = human-readable. Right = ATS garbled. Arrow in middle.
**Screenshot ref:** `image(3).png` (your bombas carousel)
**Beat types:** `diagnostic`, `shock`, `myth`

```html
<div class="slide io-slide">
  <div class="io-header">
    <span class="io-kicker">{{ copy.kicker }}</span>
    <h2>{{ copy.headline }}</h2>
  </div>
  <div class="io-comparison">
    <div class="io-panel io-human">
      <div class="io-panel-label">{{ copy.input_label }}</div>
      <div class="io-panel-content">{{ copy.input_text }}</div>
      <div class="io-check">&#10003;</div>
    </div>
    <div class="io-arrow">&#8594;</div>
    <div class="io-panel io-ats">
      <div class="io-panel-label">{{ copy.output_label }}</div>
      <div class="io-panel-content">{{ copy.output_text }}</div>
      <div class="io-x">&#10007;</div>
    </div>
  </div>
</div>
```

```css
.io-panel { padding: 24px; border-radius: 14px; flex: 1; position: relative; }
.io-human { 
  border: 1px solid rgba(0,255,150,0.25); 
  background: linear-gradient(135deg, rgba(0,255,150,0.06), rgba(0,255,150,0.02));
}
.io-ats { 
  border: 1px solid rgba(255,60,60,0.25); 
  background: linear-gradient(135deg, rgba(255,60,60,0.06), rgba(255,60,60,0.02));
  font-family: 'Courier New', monospace;
  font-size: 13px;
  letter-spacing: -0.5px;
  line-height: 1.4;
}
.io-arrow { font-size: 42px; color: var(--accent); align-self: center; margin: 0 16px; }
.io-check { color: #00ff96; font-size: 24px; position: absolute; top: 16px; right: 16px; }
.io-x { color: #ff4444; font-size: 24px; position: absolute; top: 16px; right: 16px; }
```

#### Layout 3: `slide-before-after` — Transformation Proof
**What:** Two stacked panels with "VS" badge. Progress bars inside each.
**Screenshot ref:** `image(1).png` (your bombas carousel)
**Beat types:** `transformation`, `proof`, `solution`

```html
<div class="slide ba-slide">
  <h2>{{ copy.headline }}</h2>
  <div class="ba-panels">
    <div class="ba-panel ba-before">
      <div class="ba-label">{{ copy.before_label }}</div>
      <div class="ba-text">{{ copy.before_text }}</div>
      <div class="ba-bar">
        <div class="ba-bar-track">
          <div class="ba-bar-fill ba-red" style="width: {{ copy.before_pct }}%"></div>
        </div>
        <span class="ba-pct">{{ copy.before_pct }}%</span>
      </div>
    </div>
    <div class="ba-vs">VS</div>
    <div class="ba-panel ba-after">
      <div class="ba-label">{{ copy.after_label }}</div>
      <div class="ba-text">{{ copy.after_text }}</div>
      <div class="ba-bar">
        <div class="ba-bar-track">
          <div class="ba-bar-fill ba-green" style="width: {{ copy.after_pct }}%"></div>
        </div>
        <span class="ba-pct">{{ copy.after_pct }}%</span>
      </div>
    </div>
  </div>
</div>
```

#### Layout 4: `slide-donut-chart` — Circular Progress
**What:** SVG donut with percentage fill. Optional glow.
**Screenshot ref:** `image.png` (your beyond-elite carousel)
**Beat types:** `data`, `proof`

```html
<div class="slide donut-slide">
  <svg viewBox="0 0 200 200" class="donut-chart">
    <circle cx="100" cy="100" r="80" fill="none" 
      stroke="rgba(255,255,255,0.06)" stroke-width="16"/>
    <circle cx="100" cy="100" r="80" fill="none" 
      stroke="var(--accent)" stroke-width="16"
      stroke-dasharray="502" stroke-dashoffset="{{ 502 * (1 - copy.fill_pct) }}"
      stroke-linecap="round" transform="rotate(-90 100 100)"
      filter="url(#glow-accent)"/>
    <text x="100" y="95" text-anchor="middle" fill="white" 
      font-size="32" font-weight="900">{{ copy.stat_number }}</text>
    <text x="100" y="115" text-anchor="middle" fill="#888" 
      font-size="8" letter-spacing="0.15em">{{ copy.label }}</text>
  </svg>
</div>
```

#### Layout 5: `slide-data-bars` — Horizontal Bars
**What:** Multiple horizontal bars with labels and percentage fills.
**Screenshot ref:** `image.png` (your beyond-elite carousel)
**Beat types:** `data`, `comparison`

```html
<div class="slide bars-slide">
  <div class="bars-list">
    {% for bar in copy.bars %}
    <div class="bar-item">
      <div class="bar-header">
        <span class="bar-label">{{ bar.label }}</span>
        <span class="bar-pct">{{ bar.pct }}%</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill" style="width: {{ bar.pct }}%"></div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
```

```css
.bar-track { width: 100%; height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; margin-top: 8px; }
.bar-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-light)); border-radius: 4px; transition: width 0.6s ease; }
.bar-item { margin-bottom: 20px; }
.bar-header { display: flex; justify-content: space-between; font-size: 13px; }
```

---

### PHASE 3: NEW VISUAL LAYERS (The backgrounds you're missing)
**Goal:** Add 8 new geo layers for texture and atmosphere.
**Files to modify:** `render_carousel.py` (LAYER_HTML), `carousel-shell.html` (CSS)
**Time:** 2 sessions

#### Layer additions to `LAYER_HTML` in `render_carousel.py`:

```python
LAYER_HTML.update({
    # Topographic contour lines — flowing terrain
    "geo-contour-flow": """
        <svg viewBox="0 0 1080 1080" class="geo-layer geo-contour" preserveAspectRatio="none">
            <g opacity="{{ opacity | default(0.12) }}">
                <path d="M0,200 Q270,100 540,200 Q810,300 1080,200" 
                    fill="none" stroke="var(--accent)" stroke-width="1"/>
                <path d="M0,280 Q270,180 540,280 Q810,380 1080,280" 
                    fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.7"/>
                <path d="M0,360 Q270,260 540,360 Q810,460 1080,360" 
                    fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.5"/>
                <path d="M0,440 Q270,340 540,440 Q810,540 1080,440" 
                    fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.35"/>
                <path d="M0,520 Q270,420 540,520 Q810,620 1080,520" 
                    fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.2"/>
                <path d="M0,600 Q270,500 540,600 Q810,700 1080,600" 
                    fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.1"/>
            </g>
        </svg>
    """,
    
    # Perspective wireframe grid
    "geo-perspective-grid": """
        <div class="geo-layer perspective-grid"></div>
    """,
    
    # Hexagonal tessellation
    "geo-hex-mesh": """
        <svg viewBox="0 0 1080 1080" class="geo-layer geo-hex" preserveAspectRatio="none">
            <defs>
                <pattern id="hexPattern" x="0" y="0" width="52" height="90" 
                    patternUnits="userSpaceOnUse">
                    <path d="M26,0 L52,15 L52,45 L26,60 L0,45 L0,15 Z" 
                        fill="none" stroke="var(--accent)" stroke-width="0.5" opacity="0.12"/>
                </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#hexPattern)"/>
        </svg>
    """,
    
    # Particle constellation (pre-generated static SVG)
    "geo-constellation": """
        <svg viewBox="0 0 1080 1080" class="geo-layer geo-constellation">
            <g stroke="var(--accent)" stroke-width="0.5" opacity="0.2">
                <line x1="100" y1="200" x2="250" y2="180"/>
                <line x1="250" y1="180" x2="400" y2="300"/>
                <line x1="400" y1="300" x2="550" y2="250"/>
                <line x1="550" y1="250" x2="700" y2="350"/>
                <line x1="700" y1="350" x2="850" y2="280"/>
                <line x1="200" y1="400" x2="350" y2="380"/>
                <line x1="350" y1="380" x2="500" y2="480"/>
                <line x1="500" y1="480" x2="650" y2="420"/>
                <line x1="150" y1="600" x2="300" y2="580"/>
                <line x1="300" y1="580" x2="450" y2="650"/>
            </g>
            <g fill="var(--accent)">
                <circle cx="100" cy="200" r="3" opacity="0.7"/>
                <circle cx="250" cy="180" r="4" opacity="0.9"/>
                <circle cx="400" cy="300" r="3" opacity="0.6"/>
                <circle cx="550" cy="250" r="4" opacity="0.8"/>
                <circle cx="700" cy="350" r="3" opacity="0.7"/>
                <circle cx="850" cy="280" r="3.5" opacity="0.8"/>
                <circle cx="200" cy="400" r="3" opacity="0.6"/>
                <circle cx="350" cy="380" r="4" opacity="0.9"/>
                <circle cx="500" cy="480" r="3" opacity="0.7"/>
                <circle cx="650" cy="420" r="3.5" opacity="0.8"/>
                <circle cx="150" cy="600" r="3" opacity="0.6"/>
                <circle cx="300" cy="580" r="4" opacity="0.9"/>
                <circle cx="450" cy="650" r="3" opacity="0.7"/>
            </g>
        </svg>
    """,
    
    # Neon aura ring
    "geo-neon-ring": """
        <svg viewBox="0 0 400 400" class="geo-layer geo-neon-ring">
            <circle cx="200" cy="200" r="160" fill="none" 
                stroke="var(--accent)" stroke-width="24" opacity="0.06"/>
            <circle cx="200" cy="200" r="150" fill="none" 
                stroke="var(--accent)" stroke-width="10" opacity="0.15"/>
            <circle cx="200" cy="200" r="140" fill="none" 
                stroke="var(--accent)" stroke-width="3" opacity="0.8"/>
            <circle cx="200" cy="200" r="130" fill="none" 
                stroke="var(--accent)" stroke-width="1" opacity="0.25"/>
        </svg>
    """,
    
    # Scan lines overlay
    "geo-scan-lines": """
        <div class="geo-layer scan-lines"></div>
    """,
    
    # Bokeh field
    "geo-bokeh": """
        <div class="geo-layer bokeh-container">
            <div class="bokeh-orb" style="width:220px;height:220px;top:8%;left:12%"></div>
            <div class="bokeh-orb" style="width:320px;height:320px;top:45%;left:55%"></div>
            <div class="bokeh-orb" style="width:160px;height:160px;top:70%;left:18%"></div>
            <div class="bokeh-orb" style="width:200px;height:200px;top:25%;left:75%"></div>
        </div>
    """,
    
    # Typographic field
    "geo-text-field": """
        <svg viewBox="0 0 1080 1080" class="geo-layer geo-text-field" preserveAspectRatio="none">
            <defs>
                <pattern id="textPattern" x="0" y="0" width="180" height="28" 
                    patternUnits="userSpaceOnUse">
                    <text x="0" y="18" fill="var(--accent)" opacity="0.04"
                        font-size="12" font-family="monospace" letter-spacing="0.25em">
                        WORQAI ATS CV OPTIMIZE
                    </text>
                </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#textPattern)"/>
        </svg>
    """,
})
```

#### CSS additions to `carousel-shell.html`:

```css
/* === GEO LAYER: Contour Lines === */
.geo-contour { position: absolute; inset: 0; z-index: 1; pointer-events: none; }
.geo-contour path { vector-effect: non-scaling-stroke; }

/* === GEO LAYER: Perspective Grid === */
.perspective-grid {
  position: absolute; width: 200%; height: 200%; top: -50%; left: -50%;
  background-image: 
    linear-gradient(var(--accent) 1px, transparent 1px),
    linear-gradient(90deg, var(--accent) 1px, transparent 1px);
  background-size: 60px 60px; opacity: 0.06;
  transform: perspective(600px) rotateX(55deg);
  transform-origin: center center;
  mask-image: radial-gradient(ellipse at center, black 25%, transparent 60%);
}

/* === GEO LAYER: Hex Mesh === */
.geo-hex { position: absolute; inset: 0; z-index: 1; pointer-events: none; opacity: 0.7; }

/* === GEO LAYER: Constellation === */
.geo-constellation { position: absolute; inset: 0; z-index: 1; pointer-events: none; }

/* === GEO LAYER: Neon Ring === */
.geo-neon-ring { position: absolute; z-index: 1; pointer-events: none; }

/* === GEO LAYER: Scan Lines === */
.scan-lines {
  position: absolute; inset: 0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 3px, rgba(0,0,0,0.025) 3px, rgba(0,0,0,0.025) 6px
  );
  pointer-events: none; z-index: 5; mix-blend-mode: overlay;
}

/* === GEO LAYER: Bokeh === */
.bokeh-container { position: absolute; inset: 0; overflow: hidden; z-index: 0; }
.bokeh-orb {
  position: absolute; border-radius: 50%;
  background: radial-gradient(circle, rgba(var(--accent-rgb), 0.3) 0%, 
    rgba(var(--accent-rgb), 0.1) 40%, rgba(var(--accent-rgb), 0) 70%);
  filter: blur(35px);
}

/* === GEO LAYER: Text Field === */
.geo-text-field { position: absolute; inset: 0; z-index: 1; pointer-events: none; opacity: 0.6; }

/* === GLASSMORPHISM === */
.glass-panel {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(40px) saturate(120%);
  -webkit-backdrop-filter: blur(40px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.08);
}
.glass-panel-fallback {
  background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, 
    rgba(255,255,255,0.02) 50%, rgba(var(--accent-rgb), 0.04) 100%);
  border: 1px solid rgba(255,255,255,0.15);
}
```

---

### PHASE 4: CONTINUITY SYSTEM (The "flowing through slides" effect)
**Goal:** Same shape, different position per slide.
**Files to modify:** `render_carousel.py`, `build_carousel.py`
**Time:** 1 session

**What it actually is:** NOT one continuous canvas. It's the same SVG path with different CSS transforms on each slide. The brain connects them when swiping.

**JSON spec syntax:**
```json
{
  "meta": {
    "system": "s01",
    "continuity": {
      "shape": "flow-wave",
      "path": "M200,100 Q400,0 500,200 Q600,400 400,500 Q200,600 100,400 Q0,200 200,100",
      "positions": [
        { "slide": 1, "transform": "translate(200px, 400px) rotate(-20deg) scale(1.2)", "opacity": 0.1 },
        { "slide": 2, "transform": "translate(-100px, 200px) rotate(15deg) scale(1.5)", "opacity": 0.12 },
        { "slide": 3, "transform": "translate(300px, -100px) rotate(45deg) scale(0.9)", "opacity": 0.08 },
        { "slide": 4, "transform": "translate(100px, 300px) rotate(-10deg) scale(1.3)", "opacity": 0.1 },
        { "slide": 5, "transform": "translate(-200px, 100px) rotate(60deg) scale(1.1)", "opacity": 0.06 }
      ]
    }
  }
}
```

**Render engine logic (in `render_carousel.py`):**
```python
def render_slide_with_continuity(slide, slide_index, continuity_config, system):
    """Inject continuity shape into slide with per-slide transform."""
    html = render_slide_base(slide, system)
    
    if continuity_config and slide_index < len(continuity_config.get("positions", [])):
        pos = continuity_config["positions"][slide_index]
        shape_svg = f'''<svg class="continuity-shape" style="position:absolute;
            transform: {pos['transform']};
            opacity: {pos['opacity']};
            z-index: 0; pointer-events: none;">
            <path d="{continuity_config['path']}" 
                fill="var(--accent)" opacity="0.8"/>
        </svg>'''
        # Inject before closing </div> of .slide
        html = html.replace('</div>', shape_svg + '</div>', 1)
    
    return html
```

**Feasibility:** MEDIUM. Requires modifying the slide render loop to check for `meta.continuity` and inject the shape. No new files needed — just new logic in existing render path.

---

## WHAT TO EXPLICITLY NOT IMPLEMENT

Based on the analysis, these ChatGPT suggestions are **not worth doing** for Instagram carousels:

| Suggestion | Why Skip |
|-----------|----------|
| Cross-slide master canvas (5400px) | Instagram slices are not a real canvas. The "flow" illusion works with per-slide transforms (Phase 4 above). The 5400px approach breaks html2canvas export and adds massive complexity for marginal gain. |
| Volumetric light systems | Requires WebGL or complex SVG filters. Effect is lost on 1080×1080 mobile screens. |
| Procedural noise distortion | Requires runtime Canvas generation. Can't pre-render to static SVG. |
| Isometric abstract worlds | Requires illustration assets. Not suitable for text/content carousels. |
| Fractal systems | Visually overwhelming. Better as standalone art. |
| Chromatic light leak | Complex multi-layer filters. Looks like a rendering error if imperfect. |
| 6 new blob shapes (Kimi Tier 3) | The problem is blob OVERUSE, not blob variety. Adding more blob types makes the problem worse. |
| 5 continuity modes (Kimi Tier 4) | Only the "same shape, different position" approach works on Instagram. Wave/data-pipeline/frame-evolution don't translate to separate PNGs. |

---

## RULES UPDATE FOR SKILL.md

Add these rules to prevent future blob disasters:

```markdown
### Visual System Rules (NEW)

1. **MAX 2 soft shapes per carousel** — Any combination of svg-blob-* + glow-orb 
   + vol-light may appear on maximum 2 slides total.

2. **Every geo layer needs a purpose** — Purpose must be one of: frame_headline, 
   create_depth, show_data, demonstrate_problem, guide_eye_flow, connect_slides. 
   "Visual interest" is rejected.

3. **Every carousel must demonstrate visually** — At least one slide must use 
   slide-waffle-chart, slide-donut-chart, slide-input-output, or slide-before-after.
   Text-only data slides are not acceptable.

4. **Systemic primitives, not isolated decorations** — A blob is not a sticker. 
   It must participate in composition flow, create depth, or connect slides. 
   Tiny corner accents are an anti-pattern.

5. **Texture > Blob** — Prefer geo-contour-flow, geo-hex-mesh, geo-scan-lines 
   over svg-blob-* for backgrounds. They add sophistication without competing 
   with content.

6. **Generators, not templates** — Every visual system must accept parameters 
   (opacity, density, scale, seed). No two carousels should have identical 
   backgrounds.
```

---

## SUMMARY: WHAT YOU'RE BUILDING

**Phase 1 (enforcement):** 7 new validation rules → prevents bad output
**Phase 2 (layouts):** 5 new layout templates → demonstrates visually
**Phase 3 (layers):** 8 new geo layers → replaces blob overuse with texture
**Phase 4 (continuity):** 1 new abstraction → flowing shapes across slides

**Total new files:** 5 (layout templates)
**Total modified files:** 3 (preflight.py, visual_richness_check.py, render_carousel.py, carousel-shell.html)
**Total lines of code:** ~400 (enforcement) + ~200 (layouts) + ~300 (layers) + ~50 (continuity) = **~950 lines**

**Time estimate:** 3-4 sessions
**Impact:** Eliminates blob overuse, adds data visualization, enables visual demonstration, creates flowing continuity. Transforms "template engine" into "visual system engine."
