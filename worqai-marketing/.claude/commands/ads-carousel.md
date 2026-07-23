---
description: Full ad carousel pipeline — brief → copy → HTML → design system → PNG → ZIP.
---

1. Ask which brand: WorqAI (product signup) or Profile Pro LATAM (service consult)
2. Ask for: topic, target audience, offer, objective
3. Route to ads-agent and execute the full pipeline:

## Brief
   - Define hook type (result / question / contrarian / curiosity / negative)
   - Write Customer Moment Brief (who, what they feel, what shift this carousel promises)
   - Complete the Style DNA checklist before touching any code:
     ```
     system_name / archetype / background / texture / layout_variation
     typography / accent_hex / density / temperature / trust_signal
     anti_ai_check: no left-border cards, no deco-nums, no pill badges, layout varies
     ```

## Copy
   - Slide-by-slide copy (7-8 slides) following narrative arc:
     Hook → Data → Tip/Error × 3-4 → Proof → CTA
   - At least ONE slide must use a non-standard layout (bento, big-number, pull-quote, comparison, or checklist) — not the default badge+blocks structure

## Design System
   - Select from 47 systems in `design-systems` skill (v3)
   - State: system number + name, blob or texture, fonts (3–4: display + body + accent + optional script), grain opacity, hook type
   - Verify the 4 anti-AI tells are absent before building:
     1. No colored left-border cards (replace with tinted fill or no border)
     2. No large decorative background numbers at 0.05 opacity
     3. No pill/badge labels at top of slides
     4. At least one slide breaks the layout rhythm

## HTML Build
   - Self-contained single file, 1080×1080px or 1080×1350px → `production/carousel_{topic}_{system}.html`
   - Bespoke CSS per slide (`.s1-`, `.s2-` prefixed class names). Do NOT use L01-L07 templates.
   - Minimum 3 visual techniques per slide. Elite tier: 5+ layers (geo + grain + type + depth + decorative)
   - Reference `carousel_portfolio_07_cyberpunk.html` for base structure, `carousel_amby-cr-demo_agency-pain.html` for editorial layouts, `carousel_aura-cr-demo_services.html` for typography mixing, `carousel_portfolio_04.html` for glassmorphism + stat cards
   - Fixed 1080px canvas, not responsive clamp
   - Preview-cage media query guard: transform only inside `@media (min-width:1200px)`
   - Content padding-bottom minimum 140px for brand anchor clearance
   - Run Anti-Slop Sweep and Quality Checklist before saving

## Export
   - PNG + ZIP via `scripts/carousel_exporter.py`:
     ```
     "C:\Users\kenne\AppData\Local\Programs\Python\Python311\python.exe" scripts/carousel_exporter.py --html production/carousel_X.html --output export/carousel_X.zip --width 1080 --height 1080
     ```
   - Confirm: ZIP opens, slides are 1080×1080, in order, no blank frames

## Final Check
   - ZIP opens cleanly, all slides present
   - No AI slop in copy (run anti-slop sweep from `.claude/rules/anti-slop.md`)
   - At least one layout break confirmed
   - Brand handle + counter visible on every slide
   - CTA slide has exactly ONE keyword
   - File size 55+ KB (under 45 KB = add more techniques/decoratives)
   - At least one mock UI component (terminal, CV mock, checklist)
   - 2+ decorative elements per slide (ornament, stamp, watermark, frame)
