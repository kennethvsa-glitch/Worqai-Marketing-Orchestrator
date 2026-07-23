# design-core — the shared WorqAI anti-slop engine

One brand contract, enforced across every lane: **reels, carousels, single
pictures, motion.** Before design-core, the anti-slop rules lived only in the
reel factory; carousels and images kept shipping generic gradient/glass/Inter
slop because nothing checked them. design-core fixes that by making the taste
one package that every builder imports.

## The principle (same as WMI and the reel factory)

- **Markdown / JSON hold taste.** `brand/tokens.json`, `brand/motion.json`,
  `brand/banned.json`, and this file. Humans edit these.
- **Python enforces it.** `src/design_core/` reads the brand data and blocks
  anything that violates it. Python never invents taste and never approves.

Edit the brand JSON once and every lane's gate reconfigures.

## What's inside

| Module | Enforces | Consumed by |
|---|---|---|
| `contract.py` | Loads tokens/motion/banned; thresholds; `GateFailure` | everything |
| `lint_source.py` | Off-token color, gradients, glass, glow, pills, Inter-as-display, banned copy, emoji — in **.tsx/.ts** (reels, motion) **and .html/.css/.svg** (carousels, pictures) | build gate of each lane |
| `audit_frames.py` | numpy pixel audit of any rendered frame or video: accent ≤8%, black frames, pure #000/#fff, text-band contrast ≥4.5:1 | after render/export |
| `critique.py` | Pre-emit six-axis score (philosophy/hierarchy/execution/specificity/restraint/variety); any axis <3 blocks | before human review |

## The locked brand (brand/tokens.json)

- `bg #080a10` · `ink #F5F7F2` · `muted #8D96A8` · `lime #C9F24D`
- display **Archivo Black**; body **Inter** (never display size)
- accent ≤ 8% of any frame; no pure #000/#fff surface; neutrals tint toward bg

## The motion language (brand/motion.json)

- durations 120 / 220 / 420 ms; exits at 75% of enter
- easings easeOut `(0.16,1,0.3,1)`, easeIn `(0.7,0,0.84,0)`, easeInOut `(0.65,0,0.35,1)`
- animate only transform + opacity; one orchestrated moment; no bounce on UI

## Run it

```powershell
# lint any lane's source (HTML carousels, TSX reels, SVG pictures)
python -m design_core.lint_source <path> --strict

# audit a rendered slide, post image, reel, or motion video
python -m design_core.audit_frames <image-or-video> --frames 12

# check a pre-emit critique score file
python -m design_core.critique scores.json
```

Set `PYTHONPATH=src` (or `pip install -e .`). ASCII-only output for Windows
consoles; `--json` writes proper UTF-8 evidence.

## Provenance

The rules are fused from repos inspected and pinned (see `README.md`):
`nutlope/hallmark` (slop gates + motion language), `Laith0003/ux-skill`
(152-entry anti-pattern catalog), `rohitg00/awesome-claude-design` (reference).
Nothing from those repos is installed or executed — only their rules were
translated into the brand JSON above.
