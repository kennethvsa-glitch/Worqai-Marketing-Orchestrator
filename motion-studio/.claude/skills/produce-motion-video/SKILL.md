---
name: produce-motion-video
description: Produce a Motion Studio video through a human-gated, multi-role workflow instead of a single prompt. Use when Codex must turn a creative brief into an approved concept, storyboard, HTML/CSS/SVG scene, audio plan, deterministic draft render, contact sheet, visual QA, technical QA, repair iterations, and final release candidate in a compatible Motion Studio repository.
---

# Produce Motion Video

Use the existing Motion Studio render kernel. Coordinate creative work around it.

## Required Inputs

- Creative brief with audience, objective, offer, platform, duration, language,
  assets, constraints, and call to action.
- Clean Motion Studio Git repository.
- A local production packet created by `scripts/create_job.py`.

## Roles And Gates

1. `creative-director`: convert the brief into one concept and a visual-language contract. Validate it with `scripts/taste_gate.py contract`. Stop for concept approval.
2. `taste-director`: review the concept using `config/taste-policy.json`. Produce bounded findings matching `config/taste-finding.schema.json`; do not edit scenes.
3. `storyboard-editor`: define beats, timestamps, copy, transitions, and evidence frames. Run the storyboard taste gate, then stop for approval.
4. `copy-editor`: verify hierarchy, brevity, orthography, and CTA.
5. `motion-scene-engineer`: implement only the approved scene files and labels.
6. `media-engineer`: map SFX, voiceover, music policy, captions, and cutdowns.
7. `render-controller`: run validate-only, preflight, draft export, and contact sheet.
8. `taste-director`: review rendered scene samples before assembly, then the assembled draft for continuity. Use one integrated review; call a specialist only for major or low-confidence findings.
9. `visual-verifier`: review sampled frames, safe zones, hierarchy, pacing, and
   visual continuity without reading the implementer's rationale.
10. `media-verifier`: check streams, duration, loudness policy, clipping, captions,
   and required outputs.
11. Repair only bounded findings, then rerun the relevant check, maximum two rounds.
12. Stop for human creative approval before final export or golden replacement.

## Execution

Read `references/motion-contract.md`, then run:

`py .claude/skills/produce-motion-video/scripts/create_job.py BRIEF --duration SECONDS`

Validate the emitted packet with
`py .claude/skills/produce-motion-video/scripts/check_packet.py PACKET`. Follow the
packet DAG in order. Use the commands already documented by Motion Studio; do not
invent a second renderer.

Record each human gate with `scripts/approve_gate.py PACKET GATE ARTIFACTS...`.
Run the same command with `--verify` before a dependent stage starts. Changed
artifact bytes invalidate the approval.

Store evidence under `.visual-production/jobs/JOB_ID/evidence/`. Every finding must
name the artifact, frame or timestamp, severity, and requested correction.

## Limits

- Maximum two creative repair rounds by default.
- Run deterministic checks before model-based taste review.
- Do not silently change an approved concept or storyboard.
- Do not bake platform-native or unlicensed music into a master.
- Golden hashes detect change; humans judge whether the change is good.
- Never merge or publish without explicit human signoff.
