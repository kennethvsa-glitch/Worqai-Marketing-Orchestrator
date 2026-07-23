---
name: "source-command-ads-brief"
description: "Generate a structured Meta ad brief for WorqAI or Profile Pro LATAM."
---

# source-command-ads-brief

Use this skill when the user asks to run the migrated source command `ads-brief`.

## Command Template

1. Ask which brand (if not specified)
2. Collect: product/service, audience, objective, budget range
3. Route to ads-agent, load `meta-ads-specialist` + brand context
4. Output structured brief:
   - Campaign objective + funnel stage
   - Audience definition (demo + psycho + behavioral)
   - 3 hook angles
   - Ad copy: primary text, headline, description
   - Visual direction + image prompt (no stock photo language)
   - CTA button + placement recommendation
5. Save to `production/brief_{brand}_{topic}_{date}.md`
