# Image → SVG Component Pipeline

**Use case:** Generate AI image assets for carousel components, trace them to SVG, and inject them into slides as replacement or enhancement for CSS-only components.

**Last updated:** 2026-05-21

## Prompt Template (Copy-Paste Ready)


A flat vector graphic design element for a dark-mode Instagram carousel slide.
1080×1080 square composition, [COMPONENT_TYPE] positioned [POSITION].

ELEMENT DESCRIPTION:
[Describe the component: shape, style, complexity. Be specific.]

VISUAL STYLE:
[Choose one: minimalist / brutalist / cyberpunk / editorial magazine / risograph print / Swiss modern / Y2K chrome / organic hand-drawn / Art Deco]

COLOR RULES (STRICT):
- Background: transparent / pure black (#0a0a12)
- Primary accent: [HEX_ACCENT, e.g. #C7FF3A]
- Secondary: [SECONDARY_HEX or "none"]
- NO gradients. Use flat solid colors only.
- NO blur, NO glow effects, NO shadows, NO depth of field.

TECHNICAL REQUIREMENTS:
- Clean hard edges, no anti-aliasing softness
- Simplified shapes, low node count (easy to vectorize)
- No text, no letters, no numbers, no typography
- No photographic textures, no noise, no grain
- Single isolated element on transparent background
- Symmetrical or balanced composition
- Max 4 colors total including background

MOOD REFERENCES:
[Optional: 2-3 reference descriptors, e.g. "NASA mission patch", "1980s technical manual illustration", "Muji minimalism"]

NEGATIVE PROMPT / AVOID:
text, typography, letters, numbers, words, blur, bokeh, gradient, shadow, glow, photographic, realistic, 3D render, depth of field, noise, grain, texture, watermark, frame, border, vignette, people, faces, hands
```

---

## Component-Specific Prompt Examples

### Example 1: Decorative Starburst (for stamp/badge area)
```
A flat vector 12-point starburst badge shape. Centered composition.
Sharp triangular rays radiating from a solid circular center.
Flat solid colors only: center fill #C7FF3A, rays #C7FF3A at 60% opacity.
Brutalist editorial style. Clean hard edges. Transparent background.
No text. No gradients. No shadows. Low node count.
```

### Example 2: Organic Blob (for background layer replacement)
```
A single amorphous organic blob shape, off-center to the top-right.
Flat fill #C7FF3A at 15% opacity. Soft but vector-clean edges.
Inspired by 1970s Swiss poster design meets liquid motion.
Transparent background. No gradients. No blur. No texture.
Simplified bezier curves, easy to trace to SVG.
```

### Example 3: Tech Icon (for icon-grid or bento card)
```
A flat vector icon of a document with a checkmark badge.
Minimalist line-art style, 2px strokes, rounded caps.
Color: #C7FF3A on transparent background.
No fill, only strokes. Geometric, grid-aligned.
No text. No shadows. 48×48px visual density.
```

### Example 4: Wax Seal / Stamp (for chrome-badge-stamp)
```
A flat vector circular wax seal stamp with jagged outer edge.
Center: solid #C7FF3A. Outer ring: #C7FF3A at 40% opacity.
Two concentric circle guidelines visible (thin stroke).
Brutalist editorial style. Centered. Transparent background.
No text. No gradients. No shadows.
```

---


## Integration into the Carousel System

### Option A: Replace an existing geo layer
Use the SVG as a background layer inside `.slide`:
```html
<div class="slide">
  <svg class="geo-ai-blob" viewBox="0 0 1080 1080" preserveAspectRatio="xMaxYMin slice">
    <path fill="var(--accent)" fill-opacity="0.12" d="[your path data]"/>
  </svg>
  <!-- rest of slide -->
</div>
```

### Option B: Decorative inline component
Inject via `extras` in the spec:
```json
{
  "layout": "slide-hook-lockup",
  "extras": "<svg class='deco-ai-starburst' style='position:absolute;top:40px;right:40px;width:80px;height:80px'>...</svg>"
}
```

### Option C: New template component
Add to `templates/slides/` as a proper layout:
```html
<div class="slide">
  <svg class="hero-illustration" viewBox="0 0 1080 1080">...</svg>
  <div class="hook-wrap">...</div>
</div>
```

---

## Quality Checklist Before Ship

- [ ] SVG file size under 30KB
- [ ] No embedded raster images inside the SVG
- [ ] Only 1-4 colors used
- [ ] `viewBox="0 0 1080 1080"` for full-slide elements, `viewBox="0 0 100 100"` for icons
- [ ] Tested in both dark (s01) and light (s05) systems
- [ ] Renders correctly through html2canvas (test the ZIP export button)
- [ ] No `clip-path` or `mask` if targeting html2canvas (use simple paths instead)
- [ ] `fill="currentColor"` applied if theming is needed

---

## Quick-Start: Your First AI Component

1. Pick a component from the gallery that feels "too CSS" (e.g., `sub-stamp-circle` or `geo-blob-tr`)
2. Copy the prompt template above, fill in the brackets
3. Generate 4 variants in Recraft (or Midjourney/Flux)
4. Pick the best one, trace to SVG (or use Recraft's native SVG)
5. Open `gallery/XX-[component]-component.html` in a text editor
6. Find the existing component markup, replace with your SVG
7. Test the ZIP export — if it renders clean, you're golden
8. Add the new SVG path data to `scripts/build_gallery.py` as a new demo if you want it in the gallery permanently
