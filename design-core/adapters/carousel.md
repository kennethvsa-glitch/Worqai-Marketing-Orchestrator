# Adapter: carousel lane (worqai-marketing)

How design-core wires into the carousel builder. **This is the first-pass
integration.** Nothing here has been applied to `worqai-marketing` yet — it is
the instruction for that step, to run once the workspace is idle and approved.

## Current carousel flow (from WMI workspace-capabilities.json)

```
py scripts/creative_job.py new {source}
py scripts/build_carousel.py {source}         -> production/carousel_{slug}_s17.html
py scripts/carousel_exporter.py --input ...html --output export/{slug}.zip
```

## Where design-core inserts (two hard gates)

1. **Source gate — before export.** After `build_carousel.py` writes the slide
   HTML, run the linter on it. Block the export on any BLOCK finding.

   ```powershell
   python -m design_core.lint_source production/carousel_{slug}_s17.html --strict
   ```

   This catches the exact slop the linter flagged in testing: `linear-gradient`
   panels, glass `backdrop-filter` blocks, glow shadows, pill radii, off-token
   hexes, and Inter used at headline size — before a single slide is exported.

2. **Frame gate — after render.** When slides are rasterized to PNG, audit each:

   ```powershell
   python -m design_core.audit_frames export/{slug}/slide-03.png
   ```

   Blocks lime over 8% of a slide, weak text contrast, and near-black slides.

3. **Critique — before human review.** Record the six-axis score in the job's
   QA record; `design_core.critique` blocks if any axis < 3.

## Integration options for worqai-marketing

- **Minimal:** add the two commands to the carousel capability's
  `verification_commands` in WMI's `config/workspace-capabilities.json`, so the
  gate runs as part of the produce-carousel workflow.
- **Native:** import `design_core.lint_source` inside `carousel_exporter.py`
  and refuse to write the ZIP when findings block. Same enforcement philosophy
  as the reel factory's caption-corrections block.

## Migration note

The carousel templates predate this gate and will fail it at first (the
last worqai-marketing commit was about glass-block backgrounds — glass is a
BLOCK). Expect a repair pass: swap gradients/glass for flat brand-token
surfaces, move Inter off display sizes to Archivo Black, replace emoji icons.
Run the linter in report mode first to size the cleanup before turning on
`--strict`.
