# Motion Studio

Branded motion graphics pipeline. Outputs MP4 videos for Instagram Reels, Meta ads, and social content. Started as a mirror of the worqai-marketing carousel builder (JSON spec → render → export, but video instead of static PNGs). It is now **two pipelines sharing one deterministic recorder** (Playwright frame-step → ffmpeg stdin → MP4):

1. **Spec pipeline** — JSON spec (copy only) → `render_motion.py` → `motion_exporter.py`. Generates the template scenes (stat-reveal, text-poster, list-reveal, quote-card). Built, proven, stable.
2. **Film pipeline** — hand-authored narrative scenes (`templates/scenes/scene-launch-*.html`, shared runtime `templates/motion-lib.js`) orchestrated by `scripts/make_film.py` from a manifest in `films/`. **This is where current work happens.** A new narrative video is a copy of `scene-launch-honest.html` with new copy, re-sequenced beats, and recolored primitives — never a from-scratch build, and never spec-generated. See the Production Effect Library in `.claude/skills/motion-builder/SKILL.md`.

## Status (2026-06-20)

The frame-stepper and both production lanes are proven. Determinism is enforced by the 9 locks (`.claude/rules/motion-determinism.md`) plus `golden_frames.py` regression hashes. Narrative films support SFX, voiceover, music, captions, and cutdowns. `Ideation/villain-v6-plan.md` is the latest active version plan; completed v3/v4 plans are historical material under `docs/archive/plans/`.

## Quantum Routing

Quantum is the control plane, not a creative agent and not the Oracle. Claude is
the execution provider; this repository's skills define Motion production.

Run Quantum from this repository so workers receive this `CLAUDE.md`, the Motion
skills, and the repository's deterministic tools:

```powershell
$q = "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\quantum-v4\.venv\Scripts\q.exe"

# Produce a bounded video through the local Motion skill.
& $q new "Use the local produce-motion-video skill to produce: <brief>" --profile production

# Change shared Motion code, manifests, rendering, or architecture.
& $q new "Engineering change: <describe pipeline change>" --profile engineering
```

Use `production` for a video made through the existing pipeline. The Quantum
worker must follow `.claude/skills/produce-motion-video/SKILL.md`, its approval
gates, and bounded scene paths. If the work requires changing shared scripts,
dependencies, schemas, or render architecture, stop the Production run and open
an Engineering run.

Do not start Quantum merely to make a tiny copy correction or rerun an existing
export; use the repository tools directly. Quantum currently controls one target
repository per run. It does not yet coordinate atomic changes across Motion and
WorqAI in one multi-repository transaction.

## Architecture

Spec pipeline (template scenes):

```
JSON spec (copy only)
    ↓
render_motion.py          → animated HTML (GSAP timeline baked in)
    ↓
motion_preflight.py       → validate before export
    ↓
motion_exporter.py        → frame-step → ffmpeg stdin → MP4
    ↓
motion_contact_sheet.py   → QA frame grid (runs alongside exporter)
    ↓
export-video/             → final MP4 + contact sheet PNG
```

Film pipeline (narrative scenes):

```
films/{name}.json          ← manifest: scene, sounds, voiceover, music, cutdowns, captions
    ↓
make_film.py
  1. motion_exporter.py    → silent master
  2. add_sounds.py         → SFX placed at MOTION_LABELS times
  3. split_voiceover.py    → one continuous TTS take, auto-split, placed per label
  4. music bed             → ducked under VO windows
  5. loudnorm              → -14 LUFS
  6. burned captions       → {master}_captions.mp4 (brand-styled .ass)
  7. cutdowns              → label-range stream-copy slices
    ↓
export-video/video_{name}_{YYYY-MM-DD}.mp4 (+ _captions.mp4, + cutdown mp4s)
```

Everything timing-related hangs off `window.MOTION_LABELS` emitted by the scene: SFX, VO placement, music ducking, captions, and cutdowns all resolve label times live from the rendered HTML. Missing manifest assets are WARN-skipped, not fatal — read the `make_film` output.

## Tech Stack

- **GSAP** (free, all plugins; CustomEase palette `snap/luxe/settle/mech/verdict` in `templates/motion-lib.js`)
- **Playwright** (Python) — headless frame capture + label resolution
- **ffmpeg / ffprobe** — encoding, audio mixing, ducking, loudnorm, caption burn, cutdowns. Paths resolve via `scripts/_config.py` (PATH → `MOTION_FFMPEG`/`MOTION_FFPROBE` env → WinGet fallback)
- **ElevenLabs** (external) — VO takes and SFX assets, stored in `Ideation/Sound effects/`
- CSS design tokens — same system as worqai-marketing carousels
- No Three.js, no WebGL, no shaders

## Folder Structure

```
.claude/
  rules/                    ← determinism locks, anti-slop, output conventions
  skills/motion-builder/    ← spec format and production effect library
  skills/produce-motion-video/ ← gated brief-to-video orchestration and QA
  agents/                   ← worqai creative + growth agents

templates/
  motion-shell.html         ← spec-pipeline base: GSAP + tokens + 7 effects + seeded PRNG
  motion-lib.js             ← film-pipeline shared runtime: eases, scanSweep, stamp, cursor,
                              fanOut, morphSection, makeScoreRing, signalReady, splitWords…
  scenes/                   ← scene templates (sources) + output*.html (generated, gitignored)

films/                      ← film manifests for make_film.py
motion/
  tokens/                   ← canonical s01 design and timing tokens
  specs/                    ← spec_* (copy), sounds_* (SFX placement), vo_*/voiceover_* (VO beats)

scripts/
  render_motion.py          ← spec → animated HTML
  motion_preflight.py       ← pre-render gates
  motion_exporter.py        ← frame-step → ffmpeg → MP4 (safe-zone + CSS-animation gates)
  motion_contact_sheet.py   ← 5-frame QA grid
  make_film.py              ← film orchestrator (7 stages above)
  add_sounds.py             ← SFX mixing at labels/offsets
  split_voiceover.py        ← split one TTS take, place per label
  golden_frames.py          ← deterministic frame-hash regression harness
  orthography_check.py      ← Spanish diacritics scan (run on scenes + VO scripts)
  _config.py                ← ffmpeg/ffprobe resolution

Ideation/                   ← active briefs, current plans, VO scripts, sound/music assets
docs/archive/plans/         ← completed implementation plans; historical, never auto-execute
docs/archive/audits/        ← completed workspace audits and execution plans
export-video/               ← final MP4s + contact sheets (gitignored binaries)
  golden/                   ← per-scene frame hashes (machine-specific, gitignored)
  archive/                  ← superseded exports
```

## Rules (read before every session)

- `.claude/rules/motion-determinism.md` — the 9 implementation locks
- `.claude/rules/anti-slop.md` — copy quality
- `.claude/rules/output-conventions.md` — destinations, naming, audio policy

## Scripts Reference

```bash
# ── Spec pipeline ──────────────────────────────────────────────
py scripts/motion_preflight.py motion/specs/my-spec.json
py scripts/render_motion.py motion/specs/my-spec.json
py scripts/motion_exporter.py --input templates/scenes/output.html --output export-video/
py scripts/motion_contact_sheet.py --input export-video/my-video.mp4

# ── Film pipeline ──────────────────────────────────────────────
py scripts/make_film.py --film films/launch-villain-v3.json            # full build
py scripts/make_film.py --film films/launch-villain-v3.json --draft    # 15fps/540p draft
py scripts/make_film.py --film films/launch-villain-v3.json --skip-export  # reuse last export

# ── QA ─────────────────────────────────────────────────────────
py scripts/scene_lint.py templates/scenes/scene-launch-villain-v3.html           # determinism locks + scene contract gate
py scripts/scene_lint.py templates/scenes/scene-launch-villain-v3.html --strict  # WARN -> FAIL
py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --write   # baseline
py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v3.html --check --strict
py scripts/orthography_check.py templates/scenes/scene-launch-villain-v3.html
```

`scene_lint.py` enforces the determinism locks (1/2/3/4/8/10, no-CDN) and the film
scene contract as a real gate — `make_film.py` runs it before export and aborts on
FAIL (escape hatch: `--skip-lint`). This is the executable version of
`.claude/rules/motion-determinism.md`: the mechanical locks no longer depend on the
model remembering them.

## Quality Gate (before any film ships)

1. `scene_lint.py` passes (determinism locks + scene contract) — runs automatically in `make_film.py`.
2. Preflight / exporter gates pass (safe-zone FAIL, no running CSS animations).
3. Contact sheet watched — actually watched, not glanced.
4. `golden_frames.py --check --strict` passes after any refactor.
5. `orthography_check.py` clean on the scene HTML and the VO script.
6. Output you'd post without touching it. Not "functional." Actually good.
7. Concept, storyboard, rendered scenes, and assembled output pass the lean taste gates in `config/taste-policy.json`; final human creative approval remains mandatory.
