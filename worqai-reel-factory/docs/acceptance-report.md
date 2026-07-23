# Acceptance Report — 2026-07-12 Repair

The 2026-07-11 report is superseded. It checked file presence and did not validate captions or editorial continuity.

## Current outcome

Two release candidates were produced from explicit storyboards:

| Recipe | Storyboard | Clips | Duration | Result |
|---|---|---|---:|---|
| `H04-B09-C00` | `ats-direct` | S004 + S009 + CTA | 29.0 s | automated QA pass |
| `H04-B06-B09-C00` | `ats-context` | S004 + S006 + S009 + CTA | 34.6 s | automated QA pass |

Both contain corrected burned-in Spanish captions, local Archivo/Inter fonts, WorqAI grain and CTA branding, one video stream, one audio stream, 1080×1920 output, program loudness near −14.2 LUFS, and true peak below −1.5 dBTP.

## Editorial correction

The rejected B13 and B14 combinations were removed because their source sentences begin with context-dependent discourse markers (“pero” and “entonces”). The repaired batch renderer no longer creates combinations from duration and broad tags. Every render must reference an explicit storyboard with a written narrative.

## Evidence

- Contact sheets and caption inventories: `out/release-candidates/`
- Technical and visual evidence: `.visual-production/jobs/reel-factory-repair-20260712/evidence/qa-report.json`
- Reproducible storyboard definitions: `scripts/storyboards.json`
- Reviewed caption tokens: `scripts/caption-corrections.json`

## Remaining gate

Status is **candidate awaiting human creative approval**. Kenneth or Cesar must watch each complete MP4 and use `scripts/approve_release.py` to bind approval to the QA-verified SHA-256 hash. No candidate is represented as published or founder-approved before that step.
