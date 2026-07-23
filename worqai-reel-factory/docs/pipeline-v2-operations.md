# Pipeline V2 Operations — Markdown decides, Python enforces

The architecture rule for this repository:

- **Markdown (.md) holds judgment and taste.** Brand voice, creative
  principles, quality standards, storyboards, approval records. Humans read
  and approve Markdown. Examples: `CLAUDE.md`, `docs/VIDEO_DESIGN.md`,
  `docs/keyframe-audit-gates.md`, `docs/R01-storyboard-v2.md`.
- **Python (.py) executes and enforces.** Scripts read the decisions the
  Markdown records, build production artifacts from them, validate every
  claim and constraint, and write evidence. Python never invents creative
  decisions and never marks a human gate as passed.

The bridge is `scripts/v2_contract.py`: a machine-readable mirror of
`docs/VIDEO_DESIGN.md`. Any change to the design contract updates both files
in the same commit.

## The enforcement chain

| Stage | Script | Reads (judgment) | Enforces / produces |
|---|---|---|---|
| Source lint | `lint_reel_source.py` | VIDEO_DESIGN.md tokens + bans | Blocks off-token colors, gradients, glows, Inter-as-display, banned copy in `remotion/src` |
| Timeline build | `build_timeline.py` | `<reel>-cutlist.json` (mirror of the approved storyboard), words.json, caption corrections | Spine ffmpeg plan, `timeline.json`, caption beats grouped to contract limits |
| Timeline validation | `validate_timeline.py` | VIDEO_DESIGN.md §2/§5/§10, `docs/asset-registry.json` | Gates A1–A7: opening/closing on Cesar, ≥75% real footage, every cutaway asset registered + privacy-cleared + transcript-mapped, excluded assets blocked, caption limits, unreviewed captions blocked |
| Frame audit | `audit_keyframes.py` | keyframe-audit-gates.md deterministic subset | numpy pixel checks on renders: accent ≤8%/frame, black frames, pure-#000/#fff dominance, caption-zone contrast ≥4.5:1 |
| Orchestrator | `run_v2_gates.py` | all of the above | Runs the chain, stops at first block, writes `out/v2/<REEL>/gate-evidence.json` with human gates recorded as `pending` |

## Commands

```powershell
# Full automated gate run for a reel (dry: no media written)
python scripts/run_v2_gates.py R01

# After gate-2 approval: also build the audio-video spine
python scripts/build_timeline.py R01 --execute

# After a render exists: include the pixel audit
python scripts/run_v2_gates.py R01 --render out/v2/R01/render.mp4

# Individual stages
python scripts/lint_reel_source.py remotion/src --strict
python scripts/validate_timeline.py out/v2/R01/timeline.json
python scripts/audit_keyframes.py out/v2/R01/render.mp4 --frames 12
```

Use the repo venv: `.venv/Scripts/python.exe` (Python 3.11, numpy available).
All script output is ASCII-only to survive Windows cp1252 consoles.

## What Python can never do here

- Approve a storyboard, a still-frame review, or a final video.
- Mark `human_gates` as anything but `pending` in evidence files.
- Use an asset whose registry entry is not `privacy_status: "cleared"`.
- Render captions whose corrections are not marked `reviewed: true`.
- Post or schedule anything, anywhere.

## Per-reel data files (execution mirrors of approved Markdown)

- `scripts/<reel>-cutlist.json` — keeps/trims + picture track. Mirror of the
  storyboard MD; the MD remains the human-readable source of judgment.
- `scripts/<reel>-caption-corrections.json` — phrase fixes with
  `"reviewed": true` set only by a human after checking against audio.

Adding a reel = write its storyboard MD (with assembled-transcript section),
mirror it into a cutlist JSON, register its assets, then `run_v2_gates.py`.
