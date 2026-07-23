# Output Conventions

## Destinations

- `ideation/` — Rough ideas, research, brainstorms. Not client-facing.
- `production/` — WIP HTML carousels. Three sub-stages:
  - `production/` (root) — active builds in progress
  - `production/drafts/` — spec files (`.json`) being iterated before first render
  - `production/approved/` — carousels that have passed preflight and are staged for export
- `export/` — Final deliverables ONLY. PNGs + ZIPs ready to post. Never edit what's in here.
- `distribution/` — Scheduled content with posting dates.
- `clients/{client-name}/` — Per-client Profile Pro LATAM folders (audit, CV, LinkedIn).
- `brand/` — Logo, colors, visual identity assets.
- `roadmap/` — Strategy docs, sprint plans, OKRs.

## Production Workflow

```
Spec (JSON)                HTML render              Approved              Export
production/drafts/  →  production/ (root)  →  production/approved/  →  export/
  spec_*.json           carousel_*.html          (passed preflight)      slide_NN.png
                                                                          carousel.zip
```

**Gate at each stage:**
- `drafts/ → production/`: render passes with no Jinja2 errors
- `production/ → approved/`: `build_carousel.py` scores ≥ 90/100 (26/26 checks)
- `approved/ → export/`: `carousel_exporter.py` PNG export complete

## Naming Conventions

### WorqAI marketing
- Blog posts: `blog_{slug}.md` → `blog_cv-ats-latam.md`
- Content calendars: `content_{week-date}.md` → `content_2026-W17.md`
- Carousels: `carousel_{topic}_{system}.html` → `carousel_ats-tips_aurora.html`
- Newsletters: `newsletter_{date}.md` → `newsletter_2026-04-22.md`

### Profile Pro LATAM delivery
- Audits: `clients/{client-name}/audit_{date}.md`
- CVs: `{client-name}_cv_{lang}_{date}.pdf` → `carlos-mendez_cv_es_2026-04-22.pdf`
- LinkedIn: `{client-name}_linkedin-report_{date}.docx`
- Delivery note: `clients/{client-name}/delivery-note_{date}.md`

### Ads
- Briefs: `brief_{brand}_{topic}_{date}.md` → `brief_worqai_signup-push_2026-04.md`
- Carousel exports: `slide_01.png`, `slide_02.png`, … + `carousel.zip`

## Language in Filenames

Always English for folders and filenames (`clients/`, `production/`, `export/`). Content inside files follows brand voice decision tree.
