# Output Conventions

## Destinations

- `spikes/` — Pipeline proof-of-concept tests. Never production. Delete after spike passes.
- `motion/specs/` — JSON spec files (copy only, no timing). WIP.
- `templates/scenes/` — Scene template HTML files. Versioned, never edited after passing QA.
- `export-video/` — Final MP4 outputs + contact sheet PNGs. Ready to post. Never edit what's here.

## Production Workflow

```
Spec (JSON)                  Rendered HTML               Export
motion/specs/       →    templates/scenes/output.html  →  export-video/
  spec_*.json              (preflight passes)              video_*.mp4
                                                           video_*_contact.png
```

**Gate at each stage:**
- `specs/ → render`: `motion_preflight.py` passes all checks
- `render → export`: safe-zone check passes in exporter (FAIL aborts)
- `export-video/`: only ship to export after watching the contact sheet

## Naming Conventions

- Specs: `spec_{topic}_{system}.json` → `spec_cv-stat-73pct_s01.json`
- SFX placement specs: `sounds_{film}.json` · VO beat specs: `vo_{film}.json`
- VO audio takes: `export-video/vo_{film}.mp3`
- Exported videos: `video_{topic}_{system}_{YYYY-MM-DD}.mp4` → `video_cv-stat-73pct_s01_2026-06-01.mp4`
- Film masters (from `make_film.py`): `video_{name}_{YYYY-MM-DD}.mp4`, captions variant `..._captions.mp4`, cutdowns `..._{cutdown-name}.mp4`
- Contact sheets: `{video-stem}_contact.png`
- Scene templates: `scene-{name}.html` → `scene-stat-reveal.html`
- Film manifests: `films/{name}.json`
- Superseded exports move to `export-video/archive/`

## Audio

The exporter always produces a **silent master** first. Audio is baked only by `make_film.py` from a film manifest, and only from sources we own or license:

- **Own voiceover (ElevenLabs)** — safe to bake. Placed per GSAP label via `split_voiceover.py`.
- **Own/licensed SFX** — safe to bake. Placed per label via `add_sounds.py`.
- **Licensed music bed** — bake via the manifest's `music` block (ducked under VO, loudnorm to -14 LUFS), or skip it and add platform-native music in-app after upload (platform audio earns algorithmic boost).
- **Platform or copyrighted audio** — never baked. Strikes.

## Aspect Ratios

- Instagram Reels / TikTok / Stories: 9:16 → 1080×1920
- Instagram Feed square: 1:1 → 1080×1080
- Instagram Feed portrait: 4:5 → 1080×1350

Phase 1 builds 9:16 only. Other ratios added after Phase 1 is proven.
