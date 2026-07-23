# Motion Studio — Locked Phase 1 Plan

## What This Is

A deterministic pipeline for rendering branded motion graphics to MP4. Architecture mirrors worqai-marketing carousel builder. The core difference: animated HTML gets frame-stepped through ffmpeg instead of screenshotted to PNG.

## What Was Settled (Do Not Revisit)

**Recording pipeline:** Frame-stepping only. GSAP `pause()` at load + `.time(t)` per frame + screenshot piped to ffmpeg stdin. No Playwright native video recording (variable framerate, double encoding, dropped frames). No intermediate frame files written to disk.

**Timing:** Absolute per-element timing in the scene template. JSON spec carries copy only — no sequence, no stagger, no easing. The AI never authors timing, same as the carousel render engine never accepts raw CSS.

**Audio:** Export silent. Audio added in-app after upload. Baking audio = legal trap + no algorithmic benefit.

**Geo layers in video (Option A):** Freeze animated CSS geo layers at a settled pose via `animation-play-state: paused; animation-delay: -Ns`. Background motion comes in Phase 3 when GSAP-driven animated backgrounds are added. Phase 1 backgrounds are static/frozen.

**One design system first (s01):** Lock the motion language on s01 before porting to others. Motion pacing is part of brand feel — it doesn't theme-swap as cleanly as color.

**Scope from doc 4:** Only motion tokens + safe zones added to Phase 1. Layers, transitions, performance budgets deferred.

## The 9 Implementation Locks

All in `.claude/rules/motion-determinism.md`. Summary:

1. `gsap.ticker.lagSmoothing(0)` at init — non-negotiable
2. `gsap.globalTimeline.time(t)` per frame, not `.pause(t)` in a loop
3. Effects animate via `gsap.to()` — never CSS class + transition
4. `counter` = GSAP proxy tween with `onUpdate` writing `innerText`
5. Encode: `-crf 18`, dithering for dark gradient banding
6. Safe-zone check in exporter, after page load, as FAIL
7. Exporter scans for running CSS animations before frame loop
8. Geo layers freeze at settled pose (`animation-delay: -Ns`), not t=0
9. Duration check excludes `repeat: -1` tweens

## The Effect Library (Phase 1)

7 effects: `fade`, `slide`, `text-reveal`, `counter`, `scale`, `reveal`, `blur`

Every effect has a `direction` parameter (in/out), even if Phase 1 only uses `in`.

`draw` (SVG stroke) deferred to Phase 1.5 — SVG-specific, higher effort.

## Phase 1 Scope — Exactly This, Nothing More

| Deliverable | Description |
|---|---|
| `spikes/recorder-spike/` | Minimal pipeline proof: 2s clip, one box, one tween. Build first. |
| `templates/motion-shell.html` | GSAP + 7 effects + seeded PRNG + safe zone CSS vars + video mode flag |
| `motion/tokens/motion-tokens.json` | s01 preset: duration_unit, ease, stagger values |
| `scripts/render_motion.py` | spec JSON + tokens → animated HTML |
| `scripts/motion_exporter.py` | frame-step + ffmpeg stdin pipe → MP4 |
| `scripts/motion_contact_sheet.py` | 5-frame QA grid (0/25/50/75/100%) — built before first real scene |
| `scripts/motion_preflight.py` | 8 checks (see SKILL.md) |
| `templates/scenes/scene-stat-reveal.html` | Absolute GSAP timeline, copy slots, s01 only |
| `templates/scenes/scene-text-poster.html` | Absolute GSAP timeline, copy slots, s01 only |

**Build order is strict:** recorder spike → shell → render → exporter → contact sheet → preflight → scene-stat-reveal → scene-text-poster. Do not skip ahead.

## Quality Gate Before Phase 2

Both scene outputs must look good enough to post on Instagram Reels without additional work. Not "functional." Not "the timing is roughly right." Actually good. Watch the MP4, not just the contact sheet.

## Phase 2+ (Deferred — Do Not Build Until Phase 1 Gate Passes)

- Additional scene templates (beyond the first 2)
- Additional design systems (beyond s01)
- GSAP-driven animated geo backgrounds (replaces frozen-at-pose approach)
- Three.js / WebGL / shaders
- Scroll-triggered animations
- draw effect (SVG stroke)
- Lottie integration
- Video generation AI hybrid (bg gen + HTML composite)
- Multi-scene specs (more than one scene per video)

## What "Recorder Spike Pass" Looks Like

See `spikes/recorder-spike/README.md`. Short version: a 2-second 1080×1920 clip with one box that fades in, rendered twice, producing bit-for-bit identical output. No stuttering. No banding on a dark (#080a10) background. ffmpeg stdin pipe confirmed working.

## Lessons From the Carousel Builder

- Volume without quality control creates a mess you spend weeks cleaning up
- Build one thing, validate it looks good, then add the next
- The recording pipeline is the highest-risk piece — prove it before building anything on top
- QA tooling (contact sheet) built alongside the first deliverable, not after
- Generic critiques miss system-specific failure modes — the 9 locks above all came from knowing the carousel system
