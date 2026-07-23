# Batch 3 v2 — Carousel Reframe Specification

## Counter-Attack Creative Direction (READ FIRST)

**WorqAI is not a generic resume startup. It is the counter-attack against an automated hiring system that rejects you before a human ever sees you.**

An ATS bot screens the CV, keyword filters discard it, AI recruiters score it — all before a person is involved. Most people read their silence as "I'm not good enough." The truth is an algorithm threw them out in seconds. WorqAI arms the candidate: AI that reads the CV the way the filter does, tells the truth about what's broken, and rebuilds it to pass. David vs Goliath. The system vs you. We hand you the weapon.

Tone: provocative, system-calling-out, a little defiant. Then every carousel pivots from the callout into a constructive, honest fix.

**Honesty guardrail (non-negotiable):** never promise a job or interview. The ATS score is a *diagnosis, not a verdict*. "Hackear" means speaking the filter's language, not cheating it. Every claim stays true.

## Slide 1 (HOOK) — system callout, not generic startup

Open on the system, not on WorqAI. Two lines max, big type. The rest of the carousel (Data → Errors → Fix → Proof) turns the callout into the practical fix, following the approved `personaliza-cv` reference structure:

S1 Hook → S2 Data → S3/S4 Error → S5 Fix → S6 Proof → S7 CTA

## CTA Slide (FINAL) — NEW unified limited-time design, ALL carousels

Replace any old CTA card. The change: **both free offers, stated as limited-time.**

Headline above card (pick assigned option per carousel):
- **Option A:** "Contraatacá el filtro."
- **Option B:** "¿Querés ver qué ve el ATS cuando abre tu CV?"

Card content, in order:
1. Lime badge at top of card: `POR TIEMPO LIMITADO`
2. Lime line: `Puntuación ATS de tu CV — gratis`
3. Lime line: `CV reconstruido, listo para descargar — gratis`
4. Sub: `Las dos cosas gratis, por tiempo limitado. Sin tarjeta.`
5. URL box: `WORQAI.IO` (42px, weight 900, lime, dashed lime border)
6. Closing: `Subí tu CV a worqai.io. Te decimos qué ve el ATS, qué falla, y te devolvemos el CV listo para pasar el filtro. En español o en inglés.`
7. Honest microline (small): `Tu puntuación es un diagnóstico, no un veredicto.`

Keep all dark/light card color rules and the glow orb from BATCH2_V2_SPEC.md.

## Source Files & Output Mapping

Source location: `production/Carousels to remake/priority 1/batch 3/`
Output location: `production/Carousels to remake/priority 1/batch 3/reframed/`

Theme split: 8 dark / 5 light.

| # | Source file | Theme | Topic | Output filename | Slide-1 hook (headline / subline) | CTA headline option |
|---|-------------|-------|-------|-----------------|-----------------------------------|---------------------|
| 1 | `carousel_nexus-workflow-test.html` | 🌙 **DARK** | El sistema se automatizó contra vos | `reframed_carousel_sistema-automatizado-contra-vos_worqai-lime.html` | **"Aplicás. Silencio."** / No es personal. Es un filtro automático que te bota antes del humano. | A |
| 2 | `carousel_noema_portfolio.html` | ☀️ **LIGHT** | 7 segundos | `reframed_carousel_7-segundos_worqai-lime.html` | **"7 segundos."** / Eso tarda el ATS en decidir si tu CV existe o no. | B |
| 3 | `carousel_pdf-ats-error_worqai-verde.html` | 🌙 **DARK** | Tu PDF llega roto al ATS | `reframed_carousel_tu-pdf-llega-roto-al-ats_worqai-lime.html` | **"Tu PDF se ve perfecto."** / Del otro lado, el ATS lo lee como basura y te descarta. | B |
| 4 | `carousel_personaliza-cv_s26.html` | ☀️ **LIGHT** | Personalizá o el bot te baja | `reframed_carousel_personaliza-o-el-bot-te-baja_worqai-lime.html` | **"Mandás el mismo CV a todo."** / El bot lo nota, baja tu score y ni llegás a la lista. | A |
| 5 | `carousel_portfolio_02.html` | 🌙 **DARK** | Hackeá tu CV para más entrevistas | `reframed_carousel_hackea-tu-cv-para-mas-entrevistas_worqai-lime.html` | **"Hackeá tu CV."** / No es trampa: es hablar el idioma exacto del filtro que te lee. | A |
| 6 | `carousel_portfolio_04.html` | ☀️ **LIGHT** | No es ChatGPT | `reframed_carousel_no-es-chatgpt_worqai-lime.html` | **"ChatGPT no sabe de ATS."** / Por eso tu CV sigue sin pasar, aunque suene lindo. | B |
| 7 | `carousel_portfolio_07_cyberpunk.html` | 🌙 **DARK** | Una máquina te filtró, otra te pasa | `reframed_carousel_una-maquina-te-filtro-otra-te-pasa_worqai-lime.html` | **"Una máquina te filtró."** / Otra máquina, de tu lado, te va a hacer pasar. | A |
| 8 | `carousel_portfolio_08_terra-cotta.html` | ☀️ **LIGHT** | No sos vos, es tu formato | `reframed_carousel_no-sos-vos-es-tu-formato_worqai-lime.html` | **"No es tu experiencia."** / Es un formato que el bot no puede leer, y te cuesta el puesto. | B |
| 9 | `carousel_portfolio_abyss_deepsea.html` | 🌙 **DARK** | El agujero negro de las aplicaciones | `reframed_carousel_el-agujero-negro-de-las-aplicaciones_worqai-lime.html` | **"Tu aplicación cae a un agujero negro."** / Un algoritmo la traga antes de que un humano la vea. | A |
| 10 | `carousel_portfolio_iris_holographic_v2.html` | 🌙 **DARK** | Lo que el ATS ve | `reframed_carousel_lo-que-el-ats-ve_worqai-lime.html` | **"Esto es lo que ve el ATS cuando abre tu CV."** / No es lo que ves vos. Por eso te rechaza. | B |
| 11 | `carousel_portfolio_kinetic_brutalist.html` | 🌙 **DARK** | Contraataque en 3 movidas | `reframed_carousel_contraataque-en-3-movidas_worqai-lime.html` | **"El sistema juega sucio."** / Acá están tus 3 contraataques para pasar el filtro. | A |
| 12 | `carousel_resultados_s25.html` | ☀️ **LIGHT** | Resultado real | `reframed_carousel_resultado-real_worqai-lime.html` | **"4 meses sin respuesta."** / 3 entrevistas en 8 días. Mismo perfil, otro CV. | B |
| 13 | `carousel_tu-cv-nunca-fue-leido_worqai.html` | 🌙 **DARK** | Tu CV nunca fue leído | `reframed_carousel_tu-cv-nunca-fue-leido_worqai-lime.html` | **"Tu CV nunca fue leído por un ser humano."** / Un bot decidió por vos. Cambiemos eso. | A |

**Scope note:** The 3 Batch 2 leftovers (aura, crest, nexa) already have approved reframes and are NOT in scope for this run.

## Dark Theme (Carousels 1, 3, 5, 7, 9, 10, 11, 13)

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

## Light Theme (Carousels 2, 4, 6, 8, 12)

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
- Muted labels ("Sin tarjeta."): minimum `rgba(0,0,0,0.55)` or `#666666`
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
Two options, assigned per carousel in the table above:
- **Option A:** "Contraatacá el filtro."
- **Option B:** "¿Querés ver qué ve el ATS cuando abre tu CV?"

Style: `font-size: 48px-56px; font-weight: 800; color: #FFFFFF` (dark) or `#0A0A0A` (light); `margin-bottom: 24px; line-height: 1.1; position: relative; z-index: 2;`

### CTA Card
```
┌────────────────────────────────────────────────────────┐
│  [POR TIEMPO LIMITADO]                                 │
│                                                        │
│  Puntuación ATS de tu CV — gratis                      │
│  CV reconstruido, listo para descargar — gratis        │
│  Las dos cosas gratis, por tiempo limitado. Sin tarjeta.│
│                                                        │
│  ┌──────────────────────────────┐                      │
│  │         WORQAI.IO            │                      │
│  └──────────────────────────────┘                      │
│                                                        │
│  Subí tu CV a worqai.io. Te decimos qué ve el ATS,    │
│  qué falla, y te devolvemos el CV listo para pasar    │
│  el filtro. En español o en inglés.                   │
│                                                        │
│  Tu puntuación es un diagnóstico, no un veredicto.    │
└────────────────────────────────────────────────────────┘
```

**Dark theme card:**
- Background: `#111111` or `rgba(255,255,255,0.04)`
- Border: `2px solid rgba(199,255,58,0.25)` or `1px solid rgba(255,255,255,0.1)`
- Badge background: `#C7FF3A`; badge text: `#0A0A0A` (or lime text on dark badge)
- Lime offer lines: `#C7FF3A`
- Subtext: `color: rgba(255,255,255,0.55)` ("Las dos cosas gratis...")
- Closing text: `color: rgba(255,255,255,0.78)` ("Subí tu CV...")
- Honest microline: `color: rgba(255,255,255,0.45)`

**Light theme card:**
- Background: `#FFFFFF` or `#F5F5F5`
- Border: `2px solid rgba(199,255,58,0.35)` or `1px solid rgba(0,0,0,0.15)`
- Badge background: `#C7FF3A`; badge text: `#0A0A0A`
- Lime offer lines: `#C7FF3A`
- Subtext: `color: rgba(0,0,0,0.55)` ("Las dos cosas gratis...") — MUST be dark enough
- Closing text: `color: rgba(0,0,0,0.78)` ("Subí tu CV...") — MUST be dark enough
- Honest microline: `color: rgba(0,0,0,0.45)`

**URL Box:**
```html
<div style="display:inline-flex;align-items:center;justify-content:center;padding:18px 28px;border:2px dashed #C7FF3A;border-radius:14px;margin-top:20px;margin-bottom:20px;">
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
- Position: bottom-left, bottom-center, or integrated into brand anchor
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
Spanish (es-LATAM), register tú. No "usted". Costa Rican voseo is fine in hooks where natural (subí, hablale, contraatacá) — keep it consistent within each carousel.

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

## Output Naming (Explicit List)
- `reframed_carousel_sistema-automatizado-contra-vos_worqai-lime.html`
- `reframed_carousel_7-segundos_worqai-lime.html`
- `reframed_carousel_tu-pdf-llega-roto-al-ats_worqai-lime.html`
- `reframed_carousel_personaliza-o-el-bot-te-baja_worqai-lime.html`
- `reframed_carousel_hackea-tu-cv-para-mas-entrevistas_worqai-lime.html`
- `reframed_carousel_no-es-chatgpt_worqai-lime.html`
- `reframed_carousel_una-maquina-te-filtro-otra-te-pasa_worqai-lime.html`
- `reframed_carousel_no-sos-vos-es-tu-formato_worqai-lime.html`
- `reframed_carousel_el-agujero-negro-de-las-aplicaciones_worqai-lime.html`
- `reframed_carousel_lo-que-el-ats-ve_worqai-lime.html`
- `reframed_carousel_contraataque-en-3-movidas_worqai-lime.html`
- `reframed_carousel_resultado-real_worqai-lime.html`
- `reframed_carousel_tu-cv-nunca-fue-leido_worqai-lime.html`

## Quality Checklist (Verifier Must Check)
- [ ] Counter-attack hook on slide 1 matches assigned headline/subline
- [ ] Dark theme: background is `#0A0A0A`-`#141414`, text is `#FFFFFF`-`#E5E5E5`
- [ ] Light theme: background is `#FFFFFF`-`#F5F5F5`, text is `#0A0A0A`-`#333333` (minimum)
- [ ] No text in light theme uses opacity below 0.35 for functional content
- [ ] Accent `#C7FF3A` used everywhere required (offers, URL box, highlights)
- [ ] CTA card does NOT overflow the slide bottom
- [ ] CTA card has `margin-top: auto` and `margin-bottom: 60px`
- [ ] Track has `width: auto` (not `100%`)
- [ ] All slides have `width: 1080px; height: 1080px`
- [ ] Final slide has `POR TIEMPO LIMITADO` badge
- [ ] Final slide has BOTH free offers (ATS score + reconstructed CV)
- [ ] Final slide has honest microline: "Tu puntuación es un diagnóstico, no un veredicto."
- [ ] `worqai.io` on every slide
- [ ] URL box is prominent (42px, weight 900, lime, dashed border)
- [ ] No overlapping elements
- [ ] No banned words
- [ ] Content is WorqAI-focused
- [ ] Never promises a job or interview
- [ ] Navigation works (arrow keys, buttons)
- [ ] html2canvas-safe (no mix-blend-mode on text, no backdrop-filter on text)
