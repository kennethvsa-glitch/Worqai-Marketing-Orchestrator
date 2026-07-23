# Motion WorqAI Premium Output Plan

Session directive: Implement the proposed plan from the prior Codex thread, and write/track it at this path first.

Source plan: `Ideation/villain-v6-plan.md` (`WorqAI Launch Video - v6 Plan`, rev 2 green-world rebuild).

## Execution Status

- [x] Create this tracking plan before implementation.
- [x] Confirm existing v6 scaffold: `templates/scenes/scene-launch-villain-v6.html` is a Pilot A scene, not the full film.
- [x] Pilot A: validate and repair Scene 1 green-world system.
- [x] Pilot A: render draft/contact sheet for Scene 1.
- [x] Pilot A: verify determinism/safe-zone/text glitch/cursor checks.
- [x] Human gate: approve Pilot A before expanding to 1b/3/8/full film.
- [x] If approved: build 1b, 3, 8 reuse of green-world system.
- [x] If approved: integrate Scene 2 red HUD, Scene 7 pill, reduced tailor Pilot B, and CTA.
- [x] If approved: add `films/launch-villain-v6.json`, run full render, captions, cutdowns, and golden baseline.

## Current Implementation Notes

- The existing v6 pilot already includes the static lime SVG glow filter, background grid, dot clusters, hollow squares, anchor line, wave cluster, cursor hidden at init, and separate `#s1-nada` node to avoid the SplitText/morph collision.
- Repaired the question beat in `templates/scenes/scene-launch-villain-v6.css` so it reads at phone scale: larger type, two-line wrapping, stronger badge, and subtle glow.
- Removed the visible left vertical anchor line per human feedback while keeping the surrounding dot, clusters, glow, and wave system.
- Pilot A approved by Kenneth on 2026-07-07 after the no-left-line contact sheet.
- Current scope may now expand beyond Pilot A; continue through the v6 staging order without changing the approved Scene 1 look except where required for scene transitions.
- Green-world expansion pass added:
  - Scene 3 turn: corner brackets, target icon, white-to-lime copy, underline draw, and `turn` / `turn-human` / `turn-underline` labels.
  - Scene 8 human close: left manifesto copy, right flow path, node pops, checklist panel, and `human_close` / `human_checklist` labels.
  - `data-duration` is now `24`, `data-name` is `villain-v6-green-pass`.
  - Infinite tweens are explicitly killed before the green pass exits.
- Scene 2 first red HUD pass was rejected by Kenneth on 2026-07-08 because the CV looked worse than the already-shipped version.
- Scene 2 repair pass rebuilt the CV beat as a premium ATS diagnosis system:
  - Compact red glass diagnostic header.
  - Larger inspectable CV card with contact row, meta tags, scan sweep, highlighted phrases, warning chips, reject stamp, skills, three concrete experience rows, and lower ATS meters.
  - Score component moved below the CV into a bottom diagnostic deck inspired by the v3 quantum reference instead of a detached floating widget.
  - Deterministic red particle layer driven and killed by GSAP timeline.
  - Score ring now reveals from empty instead of starting at the final value.
  - July 8 quantum-reference repair used `export-video/video_villain-v3-quantum-v2_2026-06-25.mp4` and `templates/scenes/scene-launch-villain-v3-quantum.html` as taste references for density, bullets, and bottom score placement.
  - Human gate: Kenneth approved the quantum-reference Scene 2 repair on 2026-07-08.
- Pilot B extension after Scene 2 approval added:
  - Reduced tailor pass before the human-close scene, showing original CV vs. adapted CV with bullets, keywords, and a 92/100 ATS score deck below the documents.
  - Scene 7 success pill as a short celebratory overlay on the transformed CV.
  - CTA scene with WorqAI branding, "El filtro ya existe.", "Ahora ponelo de tu lado.", and "Analiza mi CV gratis".
  - `data-duration` is now `46`, `data-name` is `villain-v6-pilot-b`.
  - `scene_lint.py`, `orthography_check.py`, and draft export/preflight pass on the Pilot B build.
- Full v6 film assembly added on 2026-07-12:
  - Added `films/launch-villain-v6.json`.
  - Added v6-specific SFX map at `motion/specs/sounds_villain_v6.json`.
  - Added v6-specific caption/VO script at `motion/specs/vo_villain_v6.json`.
  - Full 1080x1920 / 60fps render completed through `make_film.py`.
  - Master includes SFX, licensed music bed, and loudnorm audio.
  - Captions are burned from the v6 script; no spoken VO was mixed because `export-video/vo_villain_v6.mp3` does not exist yet.
  - Cutdowns generated: hook, diagnosis, CTA.
  - Golden baseline refreshed and strict check passes with the pinned cached Chromium fallback.
  - `make_film.py --skip-export` now reuses only exact master exports so it cannot accidentally pick a cutdown/captions file.
- Existing dirty worktree changes in v4 and unrelated scratch files are treated as user-owned and left untouched.
- Fresh Pilot A evidence:
  - Draft: `export-video/video_villain_v6_pilot_a_current_draft_2026-07-07.mp4`
  - Contact sheet: `export-video/video_villain_v6_pilot_a_current_draft_2026-07-07_contact.png`
  - No-left-line draft: `export-video/video_villain_v6_pilot_a_no_left_line_draft_2026-07-07.mp4`
  - No-left-line contact sheet: `export-video/video_villain_v6_pilot_a_no_left_line_draft_2026-07-07_contact.png`
  - Determinism spot-check: in-memory golden-frame capture at labels `s1-start`, `s1-hero`, `s1-question`, `s1-nada` matched across two fresh browser sessions.
  - Approved golden baseline refreshed at `export-video/golden/scene-launch-villain-v6.json`.
  - `golden_frames.py --check --strict` passes after the approved baseline refresh.
  - Green pass draft: `export-video/video_villain_v6_green_pass_draft_2026-07-07.mp4`
  - Green pass contact sheet: `export-video/video_villain_v6_green_pass_draft_2026-07-07_contact.png`
  - Repaired red+green draft: `export-video/video_villain_v6_red_green_pass_draft_2026-07-08.mp4`
  - Repaired red+green contact sheet: `export-video/video_villain_v6_red_green_pass_draft_2026-07-08_contact.png`
  - Repaired Scene 2 reject still: `export-video/villain_v6_scene2_reject_14_20.png`
  - Quantum-reference Scene 2 still: `export-video/villain_v6_scene2_quantum_repair_14_20.png`
  - v3 quantum reference still: `export-video/villain_v3_quantum_reference_14_20.png`
  - Pilot B draft: `export-video/video_villain_v6_pilot_b_draft_2026-07-08.mp4`
  - Pilot B contact sheet: `export-video/video_villain_v6_pilot_b_draft_2026-07-08_contact.png`
  - Pilot B tailor still: `export-video/villain_v6_pilot_b_tailor_25_80.png`
  - Pilot B success pill still: `export-video/villain_v6_pilot_b_success_27_80.png`
  - Pilot B CTA still: `export-video/villain_v6_pilot_b_cta_40_80.png`
  - Full v6 master: `export-video/video_villain_v6_2026-07-12.mp4`
  - Full v6 contact sheet: `export-video/video_villain_v6_2026-07-12_contact.png`
  - Full v6 captions master: `export-video/video_villain_v6_2026-07-12_captions.mp4`
  - Full v6 captions label contact sheet: `export-video/video_villain_v6_2026-07-12_captions_contact.png`
  - Full v6 hook cutdown: `export-video/video_villain_v6_2026-07-12_hook-6s.mp4`
  - Full v6 diagnosis cutdown: `export-video/video_villain_v6_2026-07-12_diagnosis-15s.mp4`
  - Full v6 CTA cutdown: `export-video/video_villain_v6_2026-07-12_cta-9s.mp4`
  - Golden baseline: `export-video/golden/scene-launch-villain-v6.json`

## Pilot A Gate Checklist

- [x] `scene_lint.py` passes on `scene-launch-villain-v6.html`.
- [x] Draft export succeeds.
- [x] Contact sheet exists and is reviewed.
- [x] Safe-zone exporter gate passes.
- [x] No running CSS animations in video mode.
- [x] Cursor is hidden at t=0.
- [x] `Nada.` and following lines do not collide/glitch around 4.7s-6.0s.
- [x] Lime glow/wave cluster reads visibly richer than v5 Scene 1.
- [x] Golden-frame capture is stable in memory; stored baseline remains intentionally stale until human approval.
- [x] Approved baseline written and strict golden check passes.
