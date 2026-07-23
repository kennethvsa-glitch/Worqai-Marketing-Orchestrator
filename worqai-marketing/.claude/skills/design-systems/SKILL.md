---
name: design-systems
description: >
  DEPRECATED — all system data has moved to html-carousel-builder/tokens.md.
  Load tokens.md directly for all carousel builds.
metadata:
  author: kenneth-valverde
  version: 5.0
  updated: 2026-05-11
---

# Design Systems Index v5

**This file is deprecated.** All 48 systems, selection logic, and tokens are now in:

```
.claude/skills/html-carousel-builder/tokens.md
```

## Migration Notes

- `tokens/system_*.md` — all 48 files consolidated into `tokens.md`
- `selection-intelligence.md` — selection logic merged into `tokens.md`
- `geo-modules-core.md` — GEO modules moved to `html-carousel-builder/techniques.md`
- `geo-modules-advanced.md` — moved to `techniques.md` (on-demand)
- `textures.md` — texture recipes moved to `techniques.md`
- `blobs.md` — blob shapes moved to `techniques.md`
- `continuity-engine.md` — continuity rules merged into `workflow.md`

## New Workflow

1. Load `carousel-matrix.yaml` (root) for presets
2. Load `html-carousel-builder/tokens.md` for system data
3. Load `html-carousel-builder/build.md` for layouts, voice, templates
4. Load `html-carousel-builder/techniques.md` on-demand for effects

See `html-carousel-builder/SKILL.md` for full instructions.
