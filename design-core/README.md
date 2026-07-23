# design-core

Shared WorqAI anti-slop enforcement for every content lane — reels, carousels,
single pictures, motion. See [DESIGN_CORE.md](DESIGN_CORE.md) for the full
contract.

Part of the WorqAI umbrella (`C:\Users\kenne\worqai\`), consumed by the
production workspaces and orchestrated by `worqai-marketing-intelligence`.

## Layout

```
design-core/
  brand/          tokens.json · motion.json · banned.json   (taste, editable)
  src/design_core/  contract · lint_source · audit_frames · critique  (enforcement)
  gates/          keyframe-audit-gates.md                   (human checklist)
  adapters/       carousel.md · (remotion.md, image.md to come)
  tests/
```

## Install

```powershell
python -m pip install -e .
# or run in place:
$env:PYTHONPATH = "src"; python -m design_core.lint_source <path> --strict
```

Requires numpy (frame audit) and ffmpeg/ffprobe on PATH (decode). Both are
already present in the reel-factory venv.

## Vendored knowledge (inspected, pinned, never installed)

| Repo | Commit | License | Used for |
|---|---|---|---|
| nutlope/hallmark | aeb42fb | MIT | slop-test gates, motion language |
| Laith0003/ux-skill | 98dad81 | MIT | 152-entry anti-pattern catalog (regex subset) |
| rohitg00/awesome-claude-design | 7f60ee5 | MIT | reference patterns |

Only the rules were translated into `brand/*.json`; no third-party code runs.
