---
name: "source-command-weekly-content"
description: "Generate a week of social media content for WorqAI and/or Profile Pro LATAM."
---

# source-command-weekly-content

Use this skill when the user asks to run the migrated source command `weekly-content`.

## Command Template

1. Ask which brand(s) this calendar is for
2. Route to content-agent, load `social-growth` + brand context
3. Generate 7-day calendar:
   - Day × platform × format (Reel, carousel, static, story) × pillar × hook × caption × hashtags
4. Pillar balance: 40% education, 20% authority, 15% social proof, 15% BTS, 10% product
5. Flag carousel posts for `/project:ads-carousel` follow-up
6. Save to `production/content_{brand}_{week-date}.md`
