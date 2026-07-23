# Agents & Skills Breakdown

## Routing

```
User Request → CLAUDE.md (router)
  ├─ strategy / roadmap / positioning / launches  → strategy-agent (opus, effort:high, memory:project)
  ├─ paid ads / Meta / carousel ads               → ads-agent (opus, effort:high)
  ├─ social / blog / SEO / content calendars      → content-agent (sonnet, effort:medium, memory:project)
  └─ sales / objections / Reddit / job hunting    → growth-agent (sonnet, effort:medium, memory:user)
```

---

## Strategy Agent

**Triggers:** strategy, roadmap, GTM, positioning, ICP, pricing, launches, OKRs, KPIs, marketing plan

**Skills:** worqai-brand-context, saas-gtm-playbook, launch-playbook, analytics-kpi, human-voice-writer

**Model:** opus | **Effort:** high | **Memory:** project | **Tools:** Read, Write, Edit, Glob, Grep

**Output:** Strategy docs, roadmaps, positioning statements, launch plans → `roadmap/`

---

## Ads Agent

**Triggers:** ads, campaign, Meta, Facebook ads, Instagram ads, ad copy, carousel ad, image prompt, ad brief

**Skills:** worqai-brand-context, meta-ads-specialist, html-carousel-builder, carousel-to-zip-exporter

**Scripts:** `carousel_exporter.py`, `render_carousel.py`

**Model:** current | **Effort:** high | **Tools:** Read, Write, Edit, Bash, Glob, Grep

**Output:** Ad briefs, copy, HTML carousels, PNGs, ZIPs → `export/`

---

## Content Agent

**Triggers:** content calendar, blog post, SEO, Reel, caption, hashtags, DM funnel, newsletter, social media

**Skills:** worqai-brand-context, human-voice-writer, social-growth, seo-content-strategy, email-marketing, html-carousel-builder, carousel-to-zip-exporter

**Scripts:** `carousel_exporter.py`, `render_carousel.py`

**Model:** sonnet | **Effort:** medium | **Memory:** project | **Tools:** Read, Write, Edit, Bash, Glob, Grep

**Output:** Calendars, captions, blog posts, newsletters, organic carousels → `production/`, `export/`, `distribution/`

---

## Growth Agent

**Triggers:** sales, close, objection, WhatsApp, pricing question, Reddit post, cold outreach, job hunting, follow-up

**Skills:** worqai-brand-context, sales-mastery-expert, human-voice-writer, reddit-job-posting, job-hunter, email-marketing

**Model:** sonnet | **Effort:** medium | **Memory:** user (cross-project) | **Tools:** Read, Write, Glob, Grep

**Output:** Sales replies, objection counters, Reddit posts, cold outreach, job applications

---

## Outreach Agent

**Triggers:** cold outreach, prospect DMs, IG outreach, personalized carousel demo sequence

**Skills:** worqai-brand-context, human-voice-writer, html-carousel-builder

**Model:** sonnet | **Effort:** medium | **Tools:** Read, Write, Glob, Grep

**Output:** Personalized Day 1 / Day 3 / Day 7 DM sequences → conversation context

---

## Skills Directory (19 total)

### Brand Context
| Skill | Primary Agents |
|---|---|
| worqai-brand-context | ALL |

### Strategy & Planning
| Skill | Primary Agents |
|---|---|
| saas-gtm-playbook | Strategy |
| launch-playbook | Strategy |
| analytics-kpi | Strategy |
| customer-interviews | Strategy |
| pricing-experiments | Strategy |
| referral-program | Strategy, Growth |

### Content & SEO
| Skill | Primary Agents |
|---|---|
| seo-content-strategy | Content |
| social-growth | Content |
| human-voice-writer | Content, Growth |
| email-marketing | Content, Growth |
| landing-page-cro | Content, Strategy |

### Ads & Creative
| Skill | Primary Agents |
|---|---|
| meta-ads-specialist | Ads |
| html-carousel-builder | Ads, Content |
| carousel-to-zip-exporter | Ads, Content |

**v2 carousel primitives (2026-05-17):** Ads and Content agents have access to the v2 SVG primitive library — 21 inline icons, 5 SVG bezier blobs, 3 SVG starbursts, 3 text treatments (gradient/glow/stroke), 3 drop-shadow filters, upgraded SVG grain. All html2canvas-safe by SVG-first design. Spec adds `copy.text_treatment` and slide-level `effects` field. Playwright (`carousel_exporter.py`) is the canonical export pipeline. See `roadmap/visual-primitives-v2-spec.md`.

### Sales & Outreach
| Skill | Primary Agents |
|---|---|
| sales-mastery-expert | Growth |
| reddit-job-posting | Growth |
| job-hunter | Growth |

### Meta
| Skill | Primary Agents |
|---|---|
| skill-creator | Used to build new skills |
| advanced-prompt-upgrader | ALL — use before any prompt is sent to a model |

---

## Shared Rules (apply to ALL agents)

- `.claude/rules/anti-slop.md` — Banned words and voice checks
- `.claude/rules/brand-voice.md` — Voice guide for WorqAI
- `.claude/rules/output-conventions.md` — File naming and destinations
- `.claude/rules/carousel-layout-checks.md` — Pre-export checks for every carousel slide

## Scripts

### Core carousel pipeline
| Script | Used By | Purpose |
|---|---|---|
| `build_carousel.py` | Ads, Content | One-command build: render + preflight + visual_richness |
| `render_carousel.py` | Ads, Content | JSON spec → HTML carousel |
| `carousel_exporter.py` | Ads, Content | HTML carousel → numbered PNGs → ZIP |
| `preflight.py` | Ads, Content | 22-check validation before export |
| `visual_richness_check.py` | Ads, Content | Visual quality gate (blob overuse, layer combos) |
| `stat_source_validator.py` | Ads, Content | Catch fabricated stat citations |

### AI background pipeline
| Script | Used By | Purpose |
|---|---|---|
| `panel_extractor.py` | Ads, Content | Grid image → N panels → color-adapt to systems → manifest |
| `adapt_image_bg.py` | Ads, Content | Single image → flat color variants per system |
| `transform_bg_v2.py` | Ads, Content | Algorithmic slide-to-slide transformations (8 recipes) |

### Gallery & tooling
| Script | Used By | Purpose |
|---|---|---|
| `build_gallery.py` | Dev | Rebuild gallery/INDEX.html from component files |
| `inline_assets.py` | Ads, Content | Embed external assets for self-contained export |
| `screenshot_carousels.py` | Dev | Batch screenshots of production carousels |
