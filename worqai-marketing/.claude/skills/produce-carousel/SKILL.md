---
name: produce-carousel
description: Produce original WorqAI carousels through art direction, standalone HTML/CSS slide previews, hash-bound human approval, deterministic assembly, taste review, technical QA, and export. Use for new or revised carousel production; do not use for changing shared pipeline architecture.
---

# Produce Carousel

Use the existing renderer, templates, components, preflight, visual-richness, and exporter as the rendering kernel.

1. Create a brief and run `py scripts/creative_job.py new BRIEF`.
2. Create an art-direction and visual-language contract using `config/taste-policy.json`.
3. Validate it with `py scripts/taste_gate.py contract CONTRACT`. Run deterministic HTML checks before one lean Taste Director review across the relevant dimensions. Findings must match `config/taste-finding.schema.json`.
4. Obtain human concept approval with `approve-concept` before production.
5. Give each worker one slide and one isolated directory. Workers must create standalone HTML/CSS and cannot edit the assembled carousel.
6. Render and check each slide, then register source, render, and report with `submit-slide`.
7. Open each candidate for human review and record acceptance with `approve-slide`. Any file change invalidates approval.
8. Run `ready`; only then may one integration owner assemble the carousel.
9. Review hook, progression, CTA, hierarchy, and continuity. Repair bounded findings only, maximum two rounds.
10. Run preflight, visual-richness, Playwright export, and final human approval.

Do not invoke one critic per taste dimension by default. Use a specialist only for a major or low-confidence finding.
