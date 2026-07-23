# Changelog

## 2026-06-15 — villain-v5 visual redesign — source files complete

### New film: scene-launch-villain-v5.html + scene-launch-villain-v5.css + films/launch-villain-v5.json

Premium visual redesign over v3. Same narrative arc and timing spine (`SCAN_START=11.9`, three tailors, same CTA block). v3 stays untouched.

**Design system changes (scene-launch-villain-v5.css):**

- New palette: `--navy-deep: #02060C`, `--navy-mid: #0B0F14` (deeper than v3's `#080a10`)
- Font swap: Inter Variable replaces Archivo for all hero/UI text (unlocks `weightShift`); JetBrains Mono stays for CV body text
- Fake glass utilities: `--glass-bg`, `--glass-red-bg`, `--glass-lime-bg` — `rgba()` fill + 1px border + layered `box-shadow`, zero `backdrop-filter` (Lock 10, determinism-safe)
- Vignette increased to 0.22 soft edge for "room in the dark" feel

**Scene-level additions over v3:**

- Scene 1: `#s1-deco` SVG node + descending draw-line; three-layer SVG wave drift (repeat:-1, killed at 10.3s); `#s1-glow` breathe (repeat:-1, killed at 10.3s); `particleField` seed "v5-s1"; `blurInChars` on all intro lines
- Scene 2: `#s2-header` glass-red panel (warn icon + title + sub); `#s2-rechazado-panel` floating dark-red stamp panel; `#s2-radar-svg` full-body radar with arm rotation (repeat:-1, killed at 17.6s)
- Scene 3 — complete redesign: `#s3-frame` with `#s3-corners` SVG draw-in (4 corner L-marks staggered); `#s3-target` crosshair (outer/inner rings + lines + person silhouette, repeat:-1 pulse killed at 23.45s); `#s3-content` with white/lime headline blocks via `blurInChars` y-offset; `#s3-check-row` blur-reveal; `#s3-underline` draw + `bloomPulse`
- Scenes 4-6: `#s4-header` glass-lime panel (radar widget + stat text + status row with dot + job chip + scanning label); `#s4-radar-arm` rotation (repeat:-1, killed at t3end); same three-tailor morph cycle
- Scene 7: `#s7-banner` replaces `#s7-texts` — circle draw (`#s7-circle`) + tick draw (`#s7-tick`) + `#s7-si` blur-reveal; `bloomPulse` on fan-out
- Scene 8 — two-column layout: `#s8-left` (4 manifesto lines staggered slide-up) + `#s8-right` (flow diagram: `#s8-flow-path` draw 1.4s, `#s8-node-building`/`#s8-node-robot` pop-in, `#s8-x-node` pulse repeat:-1, `#s8-profile-card` blur-reveal, `#s8-worqai-panel` with 3 sequential circle+tick draws); `#_post-bloom` breathe (repeat:-1, killed with `killTweensOf` at ctaT)
- Scene 9 (CTA): ported unchanged from v3

**Determinism checklist (§7, all PASS before render):**

- No `backdrop-filter` (grep clean)
- All repeat:-1 loops killed/faded at scene boundaries (7 loops traced)
- `particleField` uses seeded PRNG: seed "v5-s1" / "v5-cta" (Lock 10)
- No CSS `@keyframes` or SMIL (grep clean)
- No CDN references (grep clean)
- All `[data-copy]` elements inside safe-zone CSS vars by construction

**Next steps:**

```bash
# Draft render to QA
py scripts/make_film.py --film films/launch-villain-v5.json --draft

# After visual QA passes, generate golden baseline
py scripts/golden_frames.py --html templates/scenes/scene-launch-villain-v5.html --write

# Full export
py scripts/make_film.py --film films/launch-villain-v5.json
```

---

## 2026-06-12 — villain-v4 "El Loop Cerrado" — complete build

### New film: scene-launch-villain-v4.html (50s, 60fps, 1080×1920)

Narrative arc: 3 copy-paste rejection notifs → ATS stamp (23 red) → cheat code reveal →
3 tailored CVs (92/94/93 lime) → human callback notif → CTA with watermark travel.

**Scene-level additions over v3:**

- `#notif-stack` — 3 mechanical rejection notifs with identical body text, sequential entrance at 0.4/1.2/1.8s (`mech` ease).
- `#intro-group` — 5-line proof block with `morphSection` ("Y tú empezaste..." → "No eres tú." lime) + `weightShift(500→900)` at turn.
- Red `scan-sparks` during ATS scan; `caFlash()` on stamp impact; vignette 0.06→0.12 across Scene 2.
- Score hesitation in tailor 3: ring holds at 68, `worq-breathe` wiggle, then resolves to 93.
- `#notif-callback` (lime-edged) — Scene 8 callback with human close line "Solo dejaste de ser invisible."
- `#s7-stat` stat bar in fan-out panel: "x10.6 más entrevistas · dato interno WorqAI · 2025".
- Watermark travel: `#watermark` tweens to `#cta-wordmark` slot at CTA (`luxe`), stays visible as the wordmark.
- `ember-rise` canvas inside `#cta-group` (Lock 10 compliant).
- `initPostLayer()` active throughout; dust canvas at 0.25/0.15/0.30 per scene.
- CTA origin line: "Hecho por gente que también fue rechazada por un filtro."

**Pipeline:**

- Golden frames baseline written (15 frames, strict mode PASSED — particles + post-processing deterministic).
- Orthography check clean.
- Full quality export: `video_villain_v4_2026-06-12.mp4` (5.1 MB, SFX + music, -14 LUFS).
- Captions: `_captions.mp4` burned from VO script (VO audio pending).
- Cutdowns: `_hook-6s.mp4` (0.8 MB), `_15s-cut.mp4` (1.2 MB).

### make_film.py extensions

- `make_multiseg_cutdown()` — re-encodes each segment to temp, concatenates via concat demuxer. Enables non-contiguous cutdowns from a single master.
- `music.extra_duck` — array of `{label, offset_s, dur_s}` duck windows added to VO ducking before `mix_music`. Used to silence music during the tailor-3 hesitation beat.
- `burn_captions()` — fixed Windows path escaping: now uses `cwd=tmp` + relative `ass=captions.ass` instead of `C\:/...` in filter string (drive-letter colon broke `original_size` option parsing in ffmpeg 8.1).

### Spec files

- `motion/specs/vo_villain_v4.json` — 11-beat VO script (audio pending: `export-video/vo_villain_v4.mp3`).
- `motion/specs/sounds_villain_v4.json` — 10 SFX events: notifs ×3, stamp, CA-flash, lime scans ×3, score burst, callback chime.
- `films/launch-villain-v4.json` — film manifest with music, extra_duck, captions, hook-6s + 15s-cut cutdowns.

### Pending (unblocked by VO)

Generate ElevenLabs take from `Ideation/villain-v4-callback-plan.md` voiceover section → save to `export-video/vo_villain_v4.mp3` → `py scripts/make_film.py --film films/launch-villain-v4.json --skip-export` to add VO + final captions.

---

## 2026-06-12 — Expansion Plan gap closure: P1b chip overshoot, particle spike PASSED, Gate B

### Phase 1b — chip overshoot wired (previously stubbed)

- `landWith()` was incomplete — entrance tween existed but settle bounce was missing.
  Fixed: now uses `fromTo` (explicit from/to, unambiguous on timeline) + two-tween y micro-bounce
  (overshoot settlePx then return with `worq-settle`). Default settlePx = 4.
- villain-v3 `#job-chip` entrance replaced: `tl.to` with `ease:"luxe"` → `landWith()`.
  Chip now overshoots 4px on y after sliding in, then springs back. Matches plan spec.

### Phase 2 — Particle spike PASSED (canvas determinism confirmed)

Three bugs found and fixed; gate now open:

1. **`ctx.arc()` GPU-dependent antialiasing** — replaced with `fillRect` at integer-snapped
   positions in all four `drawParticles` presets. No antialiasing = hardware-independent.
2. **`drawParticles` wrongly owned `clearRect`** — moved to caller (`canvasParticles` +
   spike `onUpdate`). Two presets can now composite on the same canvas correctly.
3. **Canvas→screenshot pipeline gap** — Chrome's GPU-accelerated canvas composites
   asynchronously; screenshot captured stale frame. Fix: `getContext("2d", { willReadFrequently: true })`
   forces a CPU-backed canvas (synchronous flush). Applied to `canvasParticles` in motion-lib.js
   and spike.html. **Spike PASSED: both exports hash-identical (`36b1ada5c1c87f4b…`).**
- `spike_render.py` fixed: path resolution now uses glob pattern `video_{stem}_*.mp4` to match
  the exporter's `video_{name}_{date}.mp4` naming convention.

### Gate B + P0.6 — contact sheet watched

- Draft render (`--draft` 15fps/540p) of villain-v3 produced and watched.
- Contact sheet confirms Phase 1 changes visible: RECHAZADO stamp decay, chip landing,
  scan sweep, score reveal, CTA sequence. Output is production-ready.

### Lottie spike

- Remains PENDING: requires `test.json` (MIT/CC0 Lottie from lottiefiles.com).
- README updated: `willReadFrequently: true` note added for canvas-renderer Lottie files.

---

## 2026-06-12 — Expansion Plan Phases 0–3 infrastructure

### Phase 0 — Vendor infrastructure

- **vendor/gsap/** — all GSAP scripts vendored locally; no CDN at render time.
  - Pinned 3.12.5 first (exact CDN match → Gate A: all 13 villain-v3 golden frames matched).
  - Bumped to 3.15.0 (all plugins free since 3.13): CustomEase, CustomBounce, CustomWiggle,
    MotionPathPlugin, SplitText, MorphSVGPlugin, DrawSVGPlugin, ScrambleTextPlugin, Physics2DPlugin.
  - villain-v3 goldens re-baselined after version bump.
- **vendor/lottie/** — lottie-web 5.12.2 vendored (Phase 3 ready).
- **vendor/fonts/** — Inter Variable latin woff2 vendored (Phase 1c ready).
- **vendor/VERSIONS.md** — version, source URL, sha256 for every vendored file.
- All 9 scene source HTML files + `motion-shell.html`: CDN → vendor paths.
- **motion_preflight.py**: WARN on CDN script src; FAIL on Lottie `autoplay:true`; WARN on vendor file not in VERSIONS.md.
- **motion-determinism.md**: Lock 10 added (pure function of `(t, seed)`); Phase 4–5 shader/three.js spike protocols documented.

### Phase 1 — Expensive pass (motion-lib.js additions)

- **1a house eases**: `worq-settle` (CustomBounce, preferred landing ease), `worq-breathe` (CustomWiggle, held oscillation). Added to `T` token object and `motion-tokens.json`.
- **1b secondary motion**: `landWith(tl, sel, t, props)`. `stamp()` updated with 1° post-impact rotation decay.
- **1c variable font**: Inter Variable @font-face auto-injected on load. `weightShift(tl, sel, t, fromW, toW, dur)` tweens font wght axis.
- **1d post-processing**: `initPostLayer()` creates vignette + CA filter + bloom. `vignetteUp()`, `caFlash()`, `bloomPulse()`.
- **1e curved cursor**: `cursorPress()` upgraded with MotionPathPlugin bezier arc + 2-frame hover decel. Falls back to linear if plugin not loaded.
- **1f SplitText**: `splitChars()` wraps SplitText. `blurInChars()` for per-char blur-in. Legacy `splitWords()` kept.
- scene-launch-villain-v3.html, scene-launch-honest.html: Phase 1 plugin scripts added to `<head>`.
- motion-tokens.json: `lime`, `font_var`, `eases` map, `ease_usage` map added.
- villain-v3 golden frames re-baselined after Phase 1.

### Phase 2 — Particle layer (spike pending)

- `particleField()` — DOM particles ≤120, seeded PRNG, timeline-native.
- `drawParticles(ctx, t, seed, preset)` — canvas, analytic positions `f(seed, t)` (Lock 10).
- `canvasParticles()` — wires proxy tween to canvas.
- Presets: `ambient-dust`, `scan-sparks`, `score-burst`, `ember-rise`.
- **spikes/particle-spike/** — spike.html, spike_render.py, README. **Gate: PENDING**.

### Phase 3 — Lottie lane (spike pending, vendor ready)

- `lottieSeek(tl, anim, t, dur, fromFrame, toFrame)` — goToAndStop proxy pattern (Lock 4/10).
- **spikes/lottie-spike/** — spike.html, spike_render.py, README; requires test.json download. **Gate: PENDING**.
- **motion/lottie/CREDITS.md** — license tracking file created.

### Docs

- **SKILL.md**: "Expensive Layer" section added (house eases, secondary motion, variable font, post-processing, particles, Lottie) with crib patterns. Preflight table updated with 3 new checks.

---

## 2026-06-12

### Changed
- `CLAUDE.md` — rewritten to reflect two-pipeline architecture (spec pipeline + film pipeline). Status section updated; removed stale Phase 1 build order and recorder-spike references.
- `AGENTS.md` — condensed to a single-screen pointer to `CLAUDE.md` and the rules/skills/agents files.
- `.claude/rules/output-conventions.md` — Audio section rewritten to cover the film pipeline's owned/licensed audio sources. Naming conventions expanded with `sounds_*.json`, `vo_*.json`, VO audio takes, film masters, cutdown variants, and `export-video/archive/`.
- `films/launch-villain-v3.json` — Fixed: `name` changed to `villain_v3` (matches existing exports), music filename corrected to the file that exists, cutdown labels replaced with labels present in the scene (`wound`, `cheat_code`).
- `Ideation/worqai-voiceover-script.md` — Moved from root; updated to 46s/three-tailor cut with correct beat labels, times, and ElevenLabs settings.

### Added
- `motion/specs/vo_villain_v3.json` — VO beat spec for `scene-launch-villain-v3.html`: 7 entries keyed to `MOTION_LABELS`.
- `CHANGELOG.md` — this file.

### Removed
- `scripts/verify_palette.py` — dead script, no callers.
- `spikes/recorder-spike/` — proof-of-concept folder; recorder is proven, folder deleted per output conventions.
- `.gitignore` line for `spikes/recorder-spike/spike_output*.mp4`.
- `worqai-voiceover-script.md` (root) — replaced by `Ideation/worqai-voiceover-script.md`.

---

## 2026-06-11

### Added
- Film pipeline scripts: `make_film.py`, `add_sounds.py`, `split_voiceover.py`, `golden_frames.py`, `orthography_check.py`, `_config.py`.
- Shared film runtime: `templates/motion-lib.js`.
- Narrative scenes: `scene-launch-honest.html` (22s), `scene-launch-villain-v3.html` (46s) + CSS.
- Template scenes: `scene-list-reveal.html`, `scene-quote-card.html`, `scene-story.html`.
- Film manifests: `films/launch-villain-v3.json`.
- SFX placement specs: `motion/specs/sounds_*.json`.
- VO beat specs: `motion/specs/voiceover_*.json`.
- Agent definitions: `.claude/agents/worqai-creative-agent.md`, `.claude/agents/worqai-growth-agent.md`.
- Workspace audit skill: `.claude/skills/workspace-audit/SKILL.md`.
- Audit documents: `audit/AUDIT-2026-06-11.md`, `audit/PLAN-2026-06-11.md`.
- `Ideation/` — briefs, plans, sound/music assets.
- `export-video/archive/` — superseded exports.

---

## 2026-06-01

### Added
- Initial scaffold: Motion Studio architecture, rules, skill, plan, stubs.
- Recorder proven: frame-stepper produces clean, deterministic output.
- Spec pipeline complete: `render_motion.py`, `motion_exporter.py`, `motion_preflight.py`, `motion_contact_sheet.py`.
- Template scenes: `scene-stat-reveal.html`, `scene-text-poster.html`.
- Base template: `templates/motion-shell.html`.
- Encode settings locked: `-crf 18 -preset slow -pix_fmt yuv420p`.
