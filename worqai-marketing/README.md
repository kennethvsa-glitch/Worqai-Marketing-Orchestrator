# WorqAI Marketing

AI-assisted marketing operations for **WorqAI** (AI resume builder SaaS for LATAM) and **Profile Pro LATAM** (done-for-you CV/LinkedIn service).

Built for use with [Claude Code](https://code.claude.com). Two specialized agents handle creative production and growth strategy, backed by reusable skills and a Python scripts library.

## Quick Start

```bash
# 1. Install dependencies
pip install reportlab python-docx playwright Pillow
playwright install chromium

# 2. Open in VS Code with Claude Code
code .

# 3. Claude reads CLAUDE.md automatically. Try:
#    "Create an ad brief for WorqAI targeting LATAM remote workers"
#    "Audit this CV" + upload a PDF
#    "Plan next week's content calendar for both brands"
#    "Draft a sales reply for this WhatsApp thread"
```

See `SETUP.md` for full setup. See `AGENTS_BREAKDOWN.md` for agent capabilities. See `ROADMAP.md` for the 90-day marketing plan.

## Project Layout

```
.claude/
  agents/    2 specialized subagents (creative production and growth)
  skills/    reusable skills, including gated carousel production
  commands/  project commands for repeatable marketing workflows
  rules/     anti-slop, brand-voice, output-conventions
  hooks/     format-check, bash-guard (registered in settings.json)
scripts/     resume_builder.py, linkedin_report.py, carousel_exporter.py
config/      machine-readable production and taste policies
brand/       WorqAI visual identity
clients/     Per-client folders (Profile Pro LATAM)
production/  WIP files
export/      Final deliverables
distribution/ Scheduled content
ideation/    Brainstorms
roadmap/     Strategy docs, OKRs, launch plans
```

## Carousel Production

Carousel workers build standalone HTML/CSS slides first. A human approves the
exact source, render, and comparison evidence before one integration owner may
assemble the final carousel. See `.claude/skills/produce-carousel/SKILL.md`.

## Two Brands, One Repo

- **WorqAI** is the primary SaaS product — marketing goal is sign-ups and paid conversions.
- **Profile Pro LATAM** is Kenneth's service business — marketing goal is qualified leads via Reddit/Instagram/Facebook → free audit → paid rewrite.

They share workflows (content, carousels) but have separate brand voices, ICPs, and funnels. Agents route to the right brand context automatically.

## License

Private. Not for redistribution.
