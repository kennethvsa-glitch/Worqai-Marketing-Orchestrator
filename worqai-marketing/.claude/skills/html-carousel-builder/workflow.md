---
LOAD WHEN: Every carousel build
---

# CAROUSEL WORKFLOW — 6 Steps

> **RENDER ENGINE ACTIVE (as of 2026-05-16)**
> Step 4 is now JSON spec → `render_carousel.py`. Do NOT write raw HTML.
> Full pipeline: write spec → `py scripts/render_carousel.py spec.json --output production/name.html` → `py scripts/preflight.py production/name.html`
> Schema: `scripts/carousel-spec.schema.json` · Available layouts: `templates/slides/` · Available layers: see `render_carousel.py` LAYER_HTML dict
> Python path on Kenneth's machine: `py` resolves correctly in PowerShell.

---

## MANDATORY PRE-WORK — Before Step 1

### Reference Study (every build, no exceptions)
Open and read at least ONE reference carousel before touching any spec:

| If your system is... | Study this file |
|---------------------|-----------------|
| Dark (s01, s08–s17, s20–s28, s30–s32) | `production/carousel_consejo-cv-esta-mal_brutalist.html` |
| Warm / Crimson (s04) | `production/carousel_0-a-4-entrevistas_crimson.html` |
| WorqAI Verde (s17) | `production/carousel_pdf-ats-error_worqai-verde.html` |
| Light / Editorial (s48) | `production/carousel_amby-cr-demo_agency-pain.html` |
| Cyberpunk (s29) | `production/carousel_consejo-cv-esta-mal_brutalist.html` |

Note in chat: "Read `[filename]`. Key techniques I will borrow: [list 2]."

### Batch Rules (when building ≥2 carousels in one session)
1. Each carousel MUST use a different system family (dark / light / warm / brutalist / cyberpunk).
2. Write the PRE-BUILD PLAN GATE block (from build.md) for ALL carousels first. Review them side by side. If two visual signatures rhyme — fix the plan.
3. Run `py scripts/visual_richness_check.py production/carousel_1.html production/carousel_2.html` after rendering both. Cross-carousel diversity check must pass.

---

## Step 1 — Brief

Write one paragraph before touching any design or copy:
- Who is the viewer? Age, city, what they were doing before seeing this.
- What are they feeling right now? Be specific.
- What shift does this carousel promise by the last slide?

---

## Step 2 — System + Technique Pick

Load `tokens.md`. Pick a system from the selection table. State in one line:

```
System: s29 CYBERPUNK ALLEY · Accent: #00ff9c · Fonts: Space Grotesk / JetBrains Mono
```

Then pick techniques (bullet list, no justification):
```
- Background: gradient + GEO-13 wireframe + scan lines
- Effect: zoom burst rings on S2
- Layouts: L01 Poster → L02 Big Number → L04 Terminal → L07 CTA
```

Default technique stack:
- Dark systems: gradient + GEO-13 wireframe + grain
- Warm systems: gradient + blob + grain
- Light systems: gradient + parametric grid (subtle)

---

## Step 3 — Copy

Load `build.md`. Reference hook pattern + voice DNA.

Write copy for all slides BEFORE designing:

```
S1 HOOK      — pain headline (max 8 words) + intensifier + swipe pill
S2 DATA      — oversized stat + 2-line context + source tag (or Myth vs Reality)
S3–S6 TIPS   — label + headline + problem block + fix block + progress dots
S7 PROOF     — city + number + timeframe (or Myth vs Reality if no proof)
S8 CTA       — question + keyword to DM + reward copy
```

Rules:
- Headline: max 8 words, weight 700+, no filler
- Body: max 18 words, weight 300, conversational
- Label: max 4 words, uppercase, tracking 0.2em
- One idea per slide. Never two.

---

## Step 4 — JSON Spec + Render Engine

**Do NOT write raw HTML. Output a JSON spec and run the render engine.**

1. Write a `production/{topic}-spec.json` following `scripts/carousel-spec.schema.json`.
   - Pick layouts from `templates/slides/` (slide-hook-lockup, slide-terminal, slide-before-after, slide-tip-blocks, slide-checklist, slide-cta, slide-pull-quote, slide-big-number, slide-list-numbered, slide-typeset-poster, slide-myth-vs-fact, slide-bento-grid, slide-comparison-table, etc.)
   - Pick layers from the LAYER_HTML dict in `render_carousel.py` (blob-bg, vol-light, pw-grid, glow-orb, geo-topo-lines, geo-ribbon-flow, geo-halftone, geo-circuit-trace, etc.)
   - Write all copy inside `copy:` per slide — headline, body, kicker, output_lines, before_items/after_items, tips, cta_keyword, reward, etc.
2. Run the render engine:
   ```
   py scripts/render_carousel.py production/{topic}-spec.json --output production/carousel_{topic}_{system}.html
   ```
3. Run QA chain (all three must pass):
   ```
   py scripts/stat_source_validator.py production/carousel_{topic}_{system}.html
   py scripts/preflight.py production/carousel_{topic}_{system}.html
   py scripts/visual_richness_check.py production/carousel_{topic}_{system}.html
   ```
   For batch builds, run richness check with all files at once for cross-carousel diversity:
   ```
   py scripts/visual_richness_check.py production/c1.html production/c2.html production/c3.html
   ```
4. Fix any failures, re-render. **preflight.py = Technical Compliance. visual_richness_check.py = Creative Quality. Both must pass.**

**Example minimal spec:**
```json
{
  "meta": { "system": "s17", "brand": "WorqAI", "slides": 4 },
  "slides": [
    { "layout": "slide-hook-lockup", "layers": ["blob-bg","vol-light"], "copy": { "headline": "Tu CV nunca llegó a un reclutador", "body": "Lo filtró un algoritmo antes de que nadie lo viera." } },
    { "layout": "slide-terminal", "layers": ["blob-bg"], "copy": { "headline": "Así funciona el filtro", "command": "parse --cv candidato.pdf", "output_lines": [{"type":"warn","text":"Multi-column layout detected"},{"type":"err","text":"FILTERED OUT — score 0/100"}] } },
    { "layout": "slide-tip-blocks", "layers": ["blob-bg","vol-light"], "copy": { "kicker": "La solución", "headline": "Un formato. Sin tablas. Sin columnas.", "tips": [{"problem":"Diseño con columnas y tablas — el ATS lo ve como basura","fix":"Un bloque de texto corrido, PDF estándar, keywords en texto plano"}] } },
    { "layout": "slide-cta", "layers": ["blob-bg","vol-light"], "copy": { "question": "¿Tu CV llega donde tiene que llegar?", "cta_keyword": "ANALIZA", "reward": "Te mandamos el diagnóstico ATS gratis en 48hs." } }
  ]
}
```

---

## Step 5.5 — Subtraction Gate (MANDATORY)

Before running the Ship Gate, perform forced subtraction:

1. Count every decorative element (ornament, stamp, watermark, frame, badge, glow orb, zoom ring, scan line layer).
2. Remove exactly 25% of them (round down). Priority removal order:
   - Watermarks that overlap text zones
   - Duplicate technique types (e.g., second glow orb, third zoom ring)
   - Ornaments near the slide edge (clipping risk)
   - Any element whose removal you do not immediately notice
3. If the slide still communicates its single idea, the removal is permanent.
4. If a slide becomes worse, restore ONLY that element. Do not restore others.

## Step 6 — Ship Gate

Run all checks. All must be TRUE:

- [ ] **Rhythm arc:** Carousel has tension, silence, impact, and release beats
- [ ] **Technique budget:** Max 4 techniques per slide, min 1 per slide. Average across carousel ≤3.
- [ ] **Subtraction gate:** 25% of decorative elements removed without breaking any slide
- [ ] **Bespoke CSS:** Every slide has custom `.sN-` prefixed CSS, no generic L01-L07 classes
- [ ] **Fixed canvas:** Viewer is 1080px wide, not responsive max-width/clamp
- [ ] **Layout break:** At least one slide uses a non-standard layout rhythm
- [ ] **Continuity:** Same geo effect across all slides (only rotation/translation changes)
- [ ] **Anti-Canva:** Zero colored left-border cards. Zero pill badges.
- [ ] **VAR clean:** Zero `VAR_` strings anywhere in the output HTML
- [ ] **CTA complete:** Final slide contains question + single keyword + reward
- [ ] **File size:** 35–55 KB ideal. If >55 KB, list 3 removal candidates.
- [ ] **Fonts:** 3–4 typefaces loaded (display + body + accent + optional script)
- [ ] **Mock UI:** At least one slide contains a simulated interface (terminal, CV mock, checklist)
- [ ] **html2canvas safe:** No `conic-gradient()`. `backdrop-filter` has `-webkit-` fallback and passed export test.
- [ ] **Stat source clean:** Every stat citation is either from the VERIFIED ALLOW-LIST or uses `Dato interno WorqAI · base de datos 2025`. Zero fabricated report titles. `<!-- STAT_REVIEW_REQUIRED -->` present on any external source.
- [ ] **Quality bar:** Would this carousel sit next to `carousel_0-a-4-entrevistas_crimson.html` without looking cheap?

Any FALSE → fix that section, re-check.

---

## Step 7 — Deliver

One complete `<!DOCTYPE html>...</html>` block in a code fence.

State in one line: system, font, hook type.

```
System: s29 CYBERPUNK ALLEY
Font: Space Grotesk / JetBrains Mono
Hook: negative
Aspect: 1:1
File: production/carousel_{topic}_cyberpunk.html
```

If the carousel has photo slots, also output IMAGE BRIEF block below delivery card with one prompt per slot.

---

## ASPECT RATIO NOTES

- **1:1 (1080×1080)** — default
- **4:5 (1080×1350)** — change `.wrap { aspect-ratio: 4/5 }`, `.viewer { max-width: 432px }`, apply 4:5 font overrides from build.md
- **9:16 (1080×1920)** — Stories format. Change `.wrap { aspect-ratio: 9/16 }`, `.viewer { max-width: 320px }`, padding-top 180px, padding-bottom 220px

## LIGHT SYSTEM UI CHROME

For systems with cream/white background (s05, s18, s19, s23, s25, s26, s39, s47, s48):
Add `class="light-system"` to `<body>` or `<html>`. The shell already includes the chrome override rule.

## DECO-NUM SUPPRESSION

```css
.deco-num { display: none; }
```

Exceptions (set `display: block`):
- s07 BRUTALIST: opacity 0.10
- s25 SWISS BRUT ACCENT: opacity 0.85
- s31 NEOBRUT COLOR BLOCKS: opacity 0.90
- s32 MAXIMALIST COLLAGE: visible as collage element
- s44 ACADEMIC CHALKBOARD: opacity 0.40
- s46 BLUEPRINT SYSTEMS: visible as technical drawing reference

## DENSE-SLIDE CONTENT BUDGET

Available vertical space = 1080 − 96 (top) − 140 (bottom safe-zone) = 844px.

```
headline:    font-size 68px (NOT 78px for 3-line slides)
block pad:   24px 28px (NOT 32px 36px)
blk-text:    font-size 25px (NOT 30px)
why-row:     font-size 21px, margin-top 18px
inline margin-top between headline and blocks: 28–32px
```

## VISUAL CONTINUITY RULES

1. Same blob/path on every slide — only rotate/translate changes
2. Brand anchor locked — handle + counter identical position
3. Label style frozen — same font, weight, tracking, color
4. Gradient angle constant — do not change angle per slide
5. Background element always present — blob, glow, or texture
6. Progress dots always same position — only active dot shifts
7. Swipe pill on slide 1 only
8. Accent color used max 3× per slide — label, active dot, one highlight word
