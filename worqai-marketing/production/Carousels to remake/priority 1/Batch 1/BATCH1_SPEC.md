# Batch 1 — Carousel Reframe Specification

## Objective
Reframe 10 existing carousel HTML files into unified WorqAI-branded carousels with consistent dark lime identity, updated CTAs, and educational content about WorqAI's mission, product, and value proposition.

## Source Files
Location: `C:\Users\kenne\OneDrive\Documentos\worqai-marketing\production\Carousels to remake\priority 1\Batch 1`

| # | File | Current Topic | Current Brand | Current Colors | New Topic | Agent Pair |
|---|------|---------------|-------------|----------------|-----------|------------|
| 1 | `carousel_0-a-4-entrevistas_crimson.html` | 0→4 interviews case study | WorqAI | Crimson `#e05a7a` | **WorqAI case study** — why tailoring works, how we help | Pair A |
| 2 | `carousel_0a4-entrevistas_beyond-elite.html` | 0→4 interviews educational | WorqAI | Crimson `#e8455f` | **WorqAI educational** — the cheat code, why more opportunities | Pair A |
| 3 | `carousel_0a4-entrevistas_clean-saas.html` | 0→4 interviews clean SaaS | WorqAI | Blue `#3b82f6` | **WorqAI educational** — how we were born, what we offer | Pair B |
| 4 | `carousel_amby-cr-demo_agency-pain.html` | Agency services pitch | **amby (not WorqAI)** | Cream/periwinkle/gold | **FULL REWRITE** — Why WorqAI was born, what we do, how we help | Pair B |
| 5 | `carousel_aplicar-usa-latam_worqai.html` | Apply to USA from LATAM | WorqAI | Lime `#C7FF3A` + coral | **WorqAI** — LATAM→US tailoring, why we exist | Pair C |
| 6 | `carousel_ats-cv_worqai-verde.html` | ATS and CV errors | WorqAI | Lime `#C7FF3A` + coral | **WorqAI** — what we do, how tailoring fixes ATS | Pair C |
| 7 | `carousel_ats-data-dashboard_beyond-elite.html` | ATS data dashboard | WorqAI | Cyan `#00ffc8` | **WorqAI** — data-driven proof of why tailoring matters | Pair D |
| 8 | `carousel_ats-espanol-bombas_worqai.html` | Spanish ATS errors | WorqAI | Lime `#C7FF3A` + coral | **WorqAI** — bilingual moat, how we help LATAM | Pair D |
| 9 | `carousel_ats-latam_worqai-verde.html` | ATS LATAM "nunca leído" | WorqAI | Lime `#C7FF3A` + coral | **WorqAI** — the problem we solve, why we do it | Pair E |
| 10 | `carousel_ats-rechaza-sin-leer_s29.html` | ATS rejects without reading | WorqAI | Neon green `#00ff9c` | **WorqAI** — the diagnosis, how we fix it | Pair E |

## Color Mandate (Applies to ALL 10)

**Primary accent:** `#C7FF3A` (WorqAI lime green)
**Secondary accent:** `#9AE600` (darker lime for depth)
**Backgrounds:** 
- Dark: `#0A0A0A`, `#111111`, `#141414` (greys, not pure black)
- Gradient: `linear-gradient(145deg, #111111, #0A0A0A)` or similar
**Text:** `#FFFFFF` (white), `#E5E5E5` (light grey), `#A0A0A0` (muted grey)
**Bad/error states:** `#FF4444` (red, only for warnings/errors, never as accent)
**Good states:** `#C7FF3A` (lime, same as accent)

**What to REMOVE from all files:**
- Crimson (`#e05a7a`, `#e8455f`, `#dc3c50`)
- Coral (`#FF5C3C`)
- Blue (`#3b82f6`, `#00a8ff`)
- Cyan (`#00ffc8`, `#00e6b8`, `#00ff9c`)
- Periwinkle (`#C9CEE8`)
- Gold (`#D8A64A`)
- Cream paper backgrounds (`#F3F2EF`)
- Any brown/chocolate (`#3B170E`)

**What to ADD:**
- Lime glow orbs (`radial-gradient(circle, rgba(199,255,58,0.15) 0%, transparent 65%)`)
- Lime progress bars/dots
- Lime brand marks
- Lime CTA buttons
- Grey geo grids at very low opacity (`rgba(199,255,58,0.04)`)

## CTA Mandate (Every Carousel Must Have)

Every final slide (CTA slide) must include **both** of these calls-to-action clearly visible:

1. **"CV mejorado gratis — listo para descargar"** (or EN: "Free CV upgrade — ready to download")
   - Sub-line: "Sin tarjeta. Sin costo." (or EN: "No card needed. No cost.")

2. **"Puntuación ATS para tu CV gratis"** (or EN: "Free ATS score for your resume")
   - Sub-line: "Sin tarjeta. Sin costo." (or EN: "No card needed. No cost.")

3. **URL:** `worqai.io` — visible on every slide, bottom-left or bottom-center

## Content Direction (Per Pair)

### Pair A (Carousels 1-2): The Case Study + The Cheat Code
- Carousel 1: Keep the case study structure but reframe as "why tailoring works." Lead with the result (0→4 interviews), then explain it was WorqAI's tailoring that made it happen. End with CTAs.
- Carousel 2: Educational — "El problema no es tu experiencia. Es tu CV." Teach the cheat code (tailoring per posting = 10.6x more interviews per Jobscan research). Explain WorqAI does this in 30 seconds.

### Pair B (Carousels 3-4): The Origin Story + The Full Rewrite
- Carousel 3: "Why WorqAI was born." Tell the story: Kenneth and Cesar built this because they were tired of seeing capable people feel invisible. The 6-stage pipeline. The honest guardrail (facts stay yours).
- Carousel 4: **FULL REWRITE** — This was an amby agency carousel. Rewrite completely for WorqAI: "What WorqAI does and how we help." Cover all 6 stages, the bilingual moat, the not-ChatGPT proof.

### Pair C (Carousels 5-6): LATAM→US + The ATS Fix
- Carousel 5: Keep the LATAM→US angle but reframe through WorqAI. "We built this because LATAM job seekers need a tool that understands both markets." The bilingual moat.
- Carousel 6: "What WorqAI does." The 6-stage deterministic pipeline. How AI writes + real software builds. Why ChatGPT can't do this. The ATS-safe output.

### Pair D (Carousels 7-8): Data Proof + The Bilingual Moat
- Carousel 7: Data-driven educational. Use the stats (73% rejected by ATS, 10.6x more interviews from tailoring) but reframe as "why WorqAI exists." The data is the proof that the problem is real.
- Carousel 8: "Why WorqAI is different." Spanish-specific ATS errors, the bilingual advantage, auto-language detection. No English-first competitor serves this lane.

### Pair E (Carousels 9-10): The Problem + The Solution
- Carousel 9: "Why we do this." The emotional core: people feel invisible after 40 rejections. The self-doubt. WorqAI was built to fix that — not with fake promises, but with real software.
- Carousel 10: "How WorqAI fixes it." The diagnosis (free ATS score) + the solution (free CV upgrade + tailoring). The 30-second fix.

## Language
- All carousels are **Spanish (es-LATAM)** unless the original is bilingual
- Register: tú, natural LATAM. Banned: "usted", "potencia", "empoderarte", "transforma", "en el mundo de hoy"
- If the original has English content, keep it in Spanish

## Technical Requirements
- Maintain 1080×1080 canvas
- Keep all html2canvas-safe CSS (no `mix-blend-mode` on text, no `backdrop-filter` on elements with text)
- Keep slide navigation (prev/next arrows, track transform)
- Keep ZIP export button functionality
- Keep grain texture via SVG noise filter
- Output to: `C:\Users\kenne\OneDrive\Documentos\worqai-marketing\production\Carousels to remake\priority 1\Batch 1\reframed\`

## Quality Checklist
- [ ] All crimson/coral/blue/cyan colors replaced with lime/grey/white
- [ ] Both CTAs present on final slide (free CV upgrade + free ATS score + worqai.io)
- [ ] Every slide has `worqai.io` visible
- [ ] Content passes the "paste test" — could this line go on Jobscan/Teal/Rezi without changing a word? If yes, rewrite.
- [ ] No banned words: unlock, unleash, elevate, leverage, game-changer, cutting-edge, seamless, potencia, empoderarte, transforma
- [ ] The score is framed as a "diagnosis, not a verdict"
- [ ] Honest guardrail: "Your facts stay yours — companies, dates, schools"

## Execution Profile
- **Profile:** production
- **Agents:** 5 (1 per 2 carousels)
- **Parallel tasks:** max 4 (production profile default)
- **Repair budget:** 1 round per task
- **Critic:** not required (production skips critic for speed)
- **Verifier:** 1 independent verifier per pair

## Output Naming
Reframed files should be named:
- `reframed_carousel_0-a-4-entrevistas_worqai-lime.html`
- `reframed_carousel_0a4-entrevistas_worqai-lime.html`
- `reframed_carousel_0a4-entrevistas-origin_worqai-lime.html`
- `reframed_carousel_worqai-origin-what-we-do.html`
- `reframed_carousel_aplicar-usa-latam_worqai-lime.html`
- `reframed_carousel_ats-cv_worqai-lime.html`
- `reframed_carousel_ats-data_worqai-lime.html`
- `reframed_carousel_ats-espanol_worqai-lime.html`
- `reframed_carousel_ats-latam_worqai-lime.html`
- `reframed_carousel_ats-rechaza_worqai-lime.html`
