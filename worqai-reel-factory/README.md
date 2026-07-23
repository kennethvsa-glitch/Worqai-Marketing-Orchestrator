# WorqAI Reel Factory

Content factory for WorqAI reels: raw talking-head recordings in → branded edited reels + hook×body×CTA variant matrix out. The goal and guardrails live in `BRIEF.md`; the build plan is written by **Quantum V4** (the orchestration control plane), not by hand.

## To build it with Quantum

`q` is installed globally (shim → quantum-v4's venv). Each repo gets its own control DB at `.quantum/control.db`, created on first use.

1. Drop Cesar's raw recordings into `inbox/` **as-is** — 5–6 minute takes with retakes are exactly what the factory is designed to eat.
2. Open Claude Code **in this folder**, with the brand workspace attached:
   ```
   claude --add-dir C:\Users\kenne\motion-studio
   ```
3. Say:
   > Start a Quantum run to build the reel factory described in BRIEF.md.
4. Quantum walks its gates — you're needed exactly three times:
   - **Approve the spec** (what it understood the job to be)
   - **Approve the plan** (the step-by-step it wrote — this is where Quantum improves on the brief)
   - **Sign off** (watch the rendered evidence, then promote)

Slash commands (`/q-status`, `/q-approve`, `/q-signoff`…) are available user-wide; plain English works too ("show me my Quantum runs").

## Notes

- CapCut MCP: not registered in any tested session — confirmed non-dependency. See [`docs/engine-decision.md`](docs/engine-decision.md) for verdict.
- Ideation record (superseded by BRIEF.md but kept for reference): `C:\Users\kenne\motion-studio\Ideation\reel-matrix-factory-plan.md`.

## Current State (2026-07-12 repair)

The legacy duration/tag permutation renderer and its uncaptained `out/variants/` files are rejected. Production now uses explicit storyboards, reviewed caption corrections, a captioned multi-clip HyperFrames renderer, deterministic QA evidence, and hash-bound human approval.

Current review candidates are in `out/release-candidates/`. Run `python scripts/qa_release.py` to verify them. See [`docs/operator-guide.md`](docs/operator-guide.md) for the implemented commands and [`docs/acceptance-report.md`](docs/acceptance-report.md) for the current gate state.

### Historical engine decision

Spikes S1, S2, S3 complete. Engine and transcription backend selected.

| Decision | Outcome |
|---|---|
| Render engine | **HyperFrames 0.7.52** — HTML/GSAP → deterministic MP4 via headless Chrome + ffmpeg. S1+S2 PASS. Apache 2.0 governs. |
| Transcription | **faster-whisper 1.2.1** (`.venv/Scripts/python.exe`). Per-word timestamps, already installed, no download required. |
| CapCut MCP | Not registered — confirmed non-dependency. Factory does not depend on it. |
| Remotion | **Activated** for transcript-driven footage + motion compositions. Official packages `remotion` and `@remotion/cli` are pinned together by `package-lock.json`. |

Full spike evidence: [`docs/engine-decision.md`](docs/engine-decision.md)

Operator guide for running the factory day-to-day: [`docs/operator-guide.md`](docs/operator-guide.md)

## WMI-orchestrated Remotion pipeline

`worqai-marketing-intelligence` now acts as the brief, brand, audience, claim, and workspace-routing control plane. A validated JSON handoff in `remotion/specs/` selects real manifest clips, reviewed caption corrections, deterministic scene types, evidence frames, and a human-gated CTA.

One command builds upright render proxies, compiles Remotion props, renders the MP4, performs two-pass dialogue normalization, creates a contact sheet, probes media, scans unexpected black segments, and writes hash-bound QA:

```powershell
python scripts/render_remotion_pipeline.py remotion/specs/cesar-500-applications-wmi.json --output out/remotion-candidates/cesar-500-applications.mp4
```

The output is always a review candidate. The pipeline never auto-posts or silently promotes it.

For the curated Cesar campaign, the factory validates the semantic catalog before rendering: hook/body compatibility, six distinct master signatures, meaningful A/B hooks, caption-review coverage, one CTA, duration limits, guarded claims, and duplicate rejection. Generate or resume all 12 candidates with:

```powershell
python scripts/render_cesar_batch.py --resume
```

Campaign candidates, individual QA reports, contact sheets, and the campaign manifest are written to `NEW_OUTPUTS/CESAR_BATCH_12/`.
