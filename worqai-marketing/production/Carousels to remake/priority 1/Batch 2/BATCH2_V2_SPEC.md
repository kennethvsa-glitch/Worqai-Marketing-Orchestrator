# Batch 2 v2 — Carousel Reframe Specification

## Source Files
Location: `production/Carousels to remake/priority 1/Batch 2/`

| # | File | Current Brand | Theme | Topic / Notes |
|---|------|---------------|-------|---------------|
| 1 | `carousel_ats-te-elimino_cyberpunk.html` | WorqAI | 🌙 **DARK** | El ATS te eliminó antes de que un humano te vea |
| 2 | `carousel_ats-tips_worqai.html` | WorqAI | ☀️ **LIGHT** | Tips para que tu CV pase el ATS |
| 3 | `carousel_consejo-cv-esta-mal_brutalist.html` | WorqAI (rewrite) | 🌙 **DARK** | El consejo que te dieron sobre tu CV está mal |
| 4 | `carousel_cv-no-entrevistas_worqai.html` | WorqAI | ☀️ **LIGHT** | Por qué tu CV no genera entrevistas |
| 5 | `carousel_cv-silencio-reclutadores_glass.html` | WorqAI (rewrite) | 🌙 **DARK** | El silencio de los reclutadores: por qué no responden |
| 6 | `carousel_linkedin-fantasma_aurora.html` | WorqAI (rewrite) | 🌙 **DARK** | LinkedIn fantasma: por qué no te contactan |
| 7 | `carousel_linkedin-optimizado_boutique.html` | WorqAI (rewrite) | ☀️ **LIGHT** | Perfil de LinkedIn optimizado |
| 8 | `carousel_mentiras-reclutadores_crimson.html` | WorqAI (rewrite) | 🌙 **DARK** | Mentiras que los reclutadores te dicen |
| 9 | `carousel_mismo-cv_s26.html` | WorqAI (rewrite) | 🌙 **DARK** | Por qué enviar el mismo CV a todas las vacantes no funciona |
| 10 | `carousel_negociacion-salarial_terra.html` | WorqAI (rewrite) | 🌙 **DARK** | Errores en la negociación salarial |

## Output Location
`production/Carousels to remake/priority 1/Batch 2/reframed/`

## Dark Theme (Carousels 1, 3, 5, 6, 8, 9, 10)

### Backgrounds
- `#0A0A0A` (near-black) — body, deepest layers
- `#111111` — slide base, card backgrounds
- `#141414` — gradients, elevated surfaces
- Gradient pattern: `linear-gradient(145deg, #111111, #0A0A0A)` or similar
- NEVER use pure white (`#FFFFFF`) as background or slide base

### Text
- `#FFFFFF` — primary headings, important text
- `#E5E5E5` — body text, secondary content
- `#A0A0A0` — muted labels, meta text, captions
- `rgba(255,255,255,0.78)` — descriptive paragraphs
- `rgba(255,255,255,0.55)` — subtle labels, disabled states
- `rgba(255,255,255,0.35)` — very faint labels, watermark text

### Accent
- `#C7FF3A` — lime, primary accent (CTA titles, highlights, brand marks, URL box, progress indicators)
- `#9AE600` — darker lime, secondary accent (gradients, subtle highlights)
- Lime glow orbs: `radial-gradient(circle, rgba(199,255,58,0.15), transparent 65%)`
- Geo grids: `rgba(199,255,58,0.04)` — very subtle

### Cards & Containers
- Background: `rgba(255,255,255,0.04)` or `#111111`
- Border: `1px solid rgba(255,255,255,0.1)` or `rgba(255,255,255,0.07)`
- NEVER use light backgrounds for cards in dark theme

## Light Theme (Carousels 2, 4, 7)

### ⚠️ CRITICAL: READABILITY MANDATE
Light theme was attempted before and FAILED. Text was barely readable. These rules prevent that:

### Backgrounds
- `#FFFFFF` or `#FAFAFA` — slide backgrounds, primary surface
- `#F5F5F5` — secondary surfaces, card backgrounds, elevated areas
- `#E8E8E8` or `#ECECEC` — tertiary, subtle differentiation
- Gradient: `linear-gradient(148deg, #FFFFFF 0%, #F5F5F5 100%)` or similar
- NEVER use dark grey (`#0A0A0A`, `#111111`) as background in light theme

### Text — MUST BE DARK ENOUGH TO READ
- `#0A0A0A` or `#111111` — primary headings, important text (NOT `#333333` which is too light for headings)
- `#222222` or `#1A1A1A` — secondary headings
- `#333333` — body text (minimum acceptable darkness for body)
- `#444444` — secondary body text
- `#666666` or `rgba(0,0,0,0.6)` — muted labels, meta text (never lighter than this)
- `rgba(0,0,0,0.78)` — descriptive paragraphs (NEVER use `rgba(0,0,0,0.35)` or `0.45` for body text)
- `rgba(0,0,0,0.55)` — subtle labels, minimum opacity for readable text
- `rgba(0,0,0,0.35)` — ONLY for decorative watermarks, NEVER for functional text

### ⚠️ CONTRAST CHECK
- All body text must be at minimum `#444444` or `rgba(0,0,0,0.65)`
- All headings must be at minimum `#222222` or `rgba(0,0,0,0.85)`
- Muted labels ("Sin tarjeta. Sin costo."): minimum `rgba(0,0,0,0.55)` or `#666666`
- Any text smaller than 18px: minimum `#333333` or `rgba(0,0,0,0.7)`
- No text on light backgrounds should use opacity below 0.35 unless it's a decorative watermark

### Accent
- `#C7FF3A` — lime, primary accent (keep identical to dark theme)
- `#9AE600` — darker lime, secondary accent
- Lime elements are MORE prominent on light backgrounds, so REDUCE opacity of glow effects:
  - Glow orbs: `radial-gradient(circle, rgba(199,255,58,0.10), transparent 65%)` (was 0.15-0.18 in dark)
  - Geo grids: `rgba(199,255,58,0.03)` (was 0.04 in dark)
  - Band/background tints: `rgba(199,255,58,0.04)` (was 0.07 in dark)

### Cards & Containers
- Background: `#FFFFFF` or `#F5F5F5` (NOT `rgba(0,0,0,0.04)`)
- Border: `1px solid rgba(0,0,0,0.1)` or `#E0E0E0` or `rgba(0,0,0,0.15)`
- Border must be VISIBLE — `rgba(0,0,0,0.03)` is invisible on light backgrounds, use at least 0.1
- Card shadow: `0 4px 24px rgba(0,0,0,0.08)` for subtle elevation

### Grain Texture
- Dark theme: opacity 0.06-0.07
- Light theme: opacity 0.02-0.03 (reduced, or use darker grain instead of light grain)
- If using SVG noise filter: change the `feColorMatrix` to output dark values instead of light

## CTA Design (Final Slide — ALL CAROUSELS)

### CTA Headline (above the card)
Two options, assigned per carousel:
- **Option A:** "¿Tu CV está pasando el filtro?"
- **Option B:** "¿Querés ver qué ve el ATS cuando abre tu CV?"

Style: `font-size: 48px-56px; font-weight: 800; color: #FFFFFF` (dark) or `#0A0A0A` (light); `margin-bottom: 24px; line-height: 1.1; position: relative; z-index: 2;`

### CTA Card
```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  CV mejorado gratis — listo para descargar            │
│  Sin tarjeta. Sin costo.                               │
│  ────────────────────────────────────────                │
│  Puntuación ATS para tu CV gratis                      │
│  Sin tarjeta. Sin costo.                               │
│                                                        │
│  ┌──────────────────────────────┐                      │
│  │ URL         WORQAI.IO        │                      │
│  └──────────────────────────────┘                      │
│                                                        │
│  Subí tu CV a worqai.io. Te pasamos el diagnóstico   │
│  completo: qué falla, por qué, y cómo arreglarlo.    │
│  En español o en inglés.                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Dark theme card:**
- Background: `#111111` or `rgba(255,255,255,0.04)`
- Border: `2px solid rgba(199,255,58,0.25)` or `1px solid rgba(255,255,255,0.1)`
- Subtext: `color: rgba(255,255,255,0.55)` ("Sin tarjeta...")
- Closing text: `color: rgba(255,255,255,0.78)` ("Subí tu CV...")

**Light theme card:**
- Background: `#FFFFFF` or `#F5F5F5`
- Border: `2px solid rgba(199,255,58,0.35)` or `1px solid rgba(0,0,0,0.15)`
- Subtext: `color: rgba(0,0,0,0.55)` ("Sin tarjeta...") — MUST be dark enough
- Closing text: `color: rgba(0,0,0,0.78)` ("Subí tu CV...") — MUST be dark enough

**CTA title colors (both themes):**
- "CV mejorado gratis — listo para descargar": `#C7FF3A` (lime)
- "Puntuación ATS para tu CV gratis": `#C7FF3A` (lime)
- These stay lime in BOTH dark and light themes — the accent color must pop

**URL Box:**
```html
<div style="display:inline-flex;align-items:center;gap:14px;padding:18px 28px;border:2px dashed #C7FF3A;border-radius:14px;margin-top:20px;margin-bottom:20px;">
  <span style="font-size:13px;font-weight:800;letter-spacing:0.18em;text-transform:uppercase;color:#C7FF3A;opacity:0.7;">URL</span>
  <span style="font-weight:900;font-size:42px;color:#C7FF3A;letter-spacing:0.06em;">WORQAI.IO</span>
</div>
```
- The URL box must be PROMINENT — large font (42px), bold weight (900), lime color, dashed lime border
- It must NOT be cramped or pushed to the edge
- Minimum padding around it: 20px on all sides

**Glow orb inside card:**
- Dark: `radial-gradient(circle, rgba(199,255,58,0.18), transparent 65%)`
- Light: `radial-gradient(circle, rgba(199,255,58,0.12), transparent 65%)` (reduced)

### worqai.io on Every Slide
Every slide must display `worqai.io` in the bottom area:
- Position: bottom-left or bottom-center
- Font: small (14px-16px), weight 600-700
- Color: `rgba(255,255,255,0.45)` (dark) or `rgba(0,0,0,0.45)` (light)
- Must be visible but not compete with main content

## Content Direction (All Carousels)

Every carousel must be about WorqAI. If the original was for a different brand, rewrite completely.

### What WorqAI Does
- 6-stage deterministic pipeline: Parse → Improve → Tailor → Bullet Shape → Post-Validate → One-Page → Generate
- AI writes; real software builds (ATS-safe layout, length control, document generation)
- Not ChatGPT — ChatGPT doesn't know ATS parsing rules, can't generate DOCX with deterministic layout, has no length enforcement
- Free: ATS score + base CV upgrade
- $4.99: 5 tailorings | $17.99/mo: unlimited
- Bilingual: auto-detects Spanish/English, adapts formatting, knows Mexican CV ≠ US resume
- Honest guardrail: "Tu puntuación es un diagnóstico, no un veredicto."

### Banned Words
unlock, unleash, elevate, leverage, game-changer, cutting-edge, seamless, potencia, empoderarte, transforma, en el mundo de hoy, potencial, el camino, el futuro, el éxito, la clave, el secreto, la magia

### Language
Spanish (es-LATAM), register tú. No "usted".

## ⚠️ OVERLAP PREVENTION MANDATE

**The #1 bug in the previous attempt was elements overlapping or being cut off. Prevent this:**

1. **Every slide must have explicit dimensions:**
   ```css
   .slide { width: 1080px; min-width: 1080px; height: 1080px; }
   ```
   - NO `min-width: 100%` or `width: 100%` on slides (this breaks the track)
   - NO `height: 100%` on slides

2. **The track must be wide enough:**
   ```css
   .track { display: flex; width: auto; height: 100%; }
   ```
   - `width: auto` (NOT `width: 100%`) — the track must grow to fit all slides
   - `height: 100%` on the track is fine

3. **Slide padding must leave room for bottom elements:**
   - `padding: 68px 64px 148px` (top right bottom left)
   - The `148px` bottom padding MUST be respected — it leaves room for brand mark, URL, counter, progress dots
   - NEVER increase content padding beyond the slide boundaries

4. **CTA card must NOT overflow:**
   - Use `margin-top: auto` on the CTA card to push it to the bottom within the flex container
   - Use `margin-bottom: 60px` to clear the bottom elements (brand mark, URL, counter)
   - If the CTA card is too tall, reduce internal padding: `padding: 36px 32px` instead of `48px 44px`
   - If the headline + CTA card together are too tall, reduce headline font size to 44px or 40px
   - The CTA card + headline + margin-bottom must fit within `1080px - top_padding - bottom_padding` = ~864px max

5. **No element should have negative margins that pull it outside the slide**
6. **No decorative element should be positioned absolutely in a way that covers text**
7. **Z-index stacking:** text and CTAs must be `z-index: 2` or higher; decorations at `z-index: 1` or lower

## Technical Requirements
- 1080×1080 canvas (Instagram square format)
- html2canvas-safe CSS:
  - NO `mix-blend-mode` on text elements
  - NO `backdrop-filter` on elements containing text
  - `backdrop-filter` on empty decorative elements is OK
- Keep slide navigation (prev/next arrows, track transform)
- Keep ZIP export button functionality if present
- Keep grain texture via SVG noise filter if present
- Each slide: `.slide` class with `width: 1080px; height: 1080px;`
- Navigation: `onclick` handlers or event listeners that use `transform: translateX(-N*1080px)` to move the track
- The transform must move the track by EXACTLY `(slide_index * 1080px)` — no percentage-based transforms

## Output Naming
- `reframed_carousel_ats-te-elimino_worqai-lime.html`
- `reframed_carousel_ats-tips_worqai-lime.html`
- `reframed_carousel_consejo-cv_worqai-lime.html`
- `reframed_carousel_cv-no-entrevistas_worqai-lime.html`
- `reframed_carousel_cv-silencio-reclutadores_worqai-lime.html`
- `reframed_carousel_linkedin-fantasma_worqai-lime.html`
- `reframed_carousel_linkedin-optimizado_worqai-lime.html`
- `reframed_carousel_mentiras-reclutadores_worqai-lime.html`
- `reframed_carousel_mismo-cv_worqai-lime.html`
- `reframed_carousel_negociacion-salarial_worqai-lime.html`

## Quality Checklist (Verifier Must Check)
- [ ] Dark theme: background is `#0A0A0A`-`#141414`, text is `#FFFFFF`-`#E5E5E5`
- [ ] Light theme: background is `#FFFFFF`-`#F5F5F5`, text is `#0A0A0A`-`#333333` (minimum)
- [ ] No text in light theme uses opacity below 0.35 for functional content
- [ ] CTA card does NOT overflow the slide bottom
- [ ] CTA card has `margin-top: auto` and `margin-bottom: 60px`
- [ ] Track has `width: auto` (not `100%`)
- [ ] All slides have `width: 1080px; height: 1080px`
- [ ] Both CTAs present on final slide
- [ ] `worqai.io` on every slide
- [ ] URL box is prominent (42px, bold, lime, dashed border)
- [ ] No overlapping elements
- [ ] No banned words
- [ ] Content is WorqAI-focused
- [ ] Navigation works (arrow keys, buttons)
- [ ] html2canvas-safe (no mix-blend-mode on text)
