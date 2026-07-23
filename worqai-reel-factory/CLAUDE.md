# WorqAI Reel Factory — Source of Truth

This file supersedes the pre-repair workflow documentation.

## Scope

The factory turns real vertical recordings into local, captioned WorqAI release candidates. Humans review and publish them. The system never posts automatically and never generates synthetic people.

`C:\Users\kenne\motion-studio` is a read-only source for WorqAI tokens, fonts, GSAP, and SFX.

## Production architecture

1. `ingest.py` proposes transcript-based cuts for human review.
2. Approved clips are stored in `library/` and indexed by `manifest.json`.
3. Production captions require reviewed tokens in `scripts/caption-corrections.json`.
4. Editorial ordering is explicit in `scripts/storyboards.json`.
5. `render_storyboard.py` concatenates normalized real clips, offsets word timings, and renders the complete sequence through HyperFrames.
6. `combine.py` batches approved storyboards only. It does not invent semantic combinations.
7. `qa_release.py` verifies the encoded release candidate and records hashes/evidence.
8. `approve_release.py` records human approval against the exact verified hash.

## Brand contract

- Background: `#080a10`
- Accent: `#C9F24D`
- Display/captions: local Archivo Black
- Supporting text: local Inter
- Grain: 0.11 opacity
- Captions: burned-in, transcript-timed mask reveal, no generic yellow preset
- CTA: WorqAI wordmark plus operator-written copy
- Audio: approximately −14 LUFS; true peak must not exceed −1.5 dBTP

## Editorial contract

- Language, duration, or a broad topic tag do not prove two sentences connect.
- A production storyboard must name its exact ordered clips and explain its narrative.
- Clips beginning with dependent markers such as “pero” or “entonces” require their antecedent in the same storyboard.
- Machine transcripts are drafts. Production rendering is blocked without reviewed caption corrections.
- A contact sheet is evidence, not proof that the entire video was watched.

## Commands

See `docs/operator-guide.md` for the exact implemented CLI. The production commands are:

```powershell
python scripts/render_storyboard.py ats-direct --force
python scripts/combine.py --force
python scripts/qa_release.py
```

## Release state

`out/release-candidates/` is the only current output source. `out/variants/` contains rejected legacy renders and must not be posted.

Passing automated QA does not equal creative approval. Watch the complete candidate and record human approval with `scripts/approve_release.py` before promotion, merge, or publication.
