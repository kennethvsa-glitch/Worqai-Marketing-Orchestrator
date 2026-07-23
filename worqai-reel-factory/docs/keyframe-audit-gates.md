# Keyframe Audit Gates — Video Adaptation of the Hallmark Slop Test

Run against 6–8 full-resolution still frames plus the contact sheet at the
still-frame review gate, and against the full draft before human approval.
Every answer must be **no**. Any *yes* is a rejection with the gate number cited.

Source: `nutlope/hallmark` `references/slop-test.md` (58 web gates), translated
to video; project-specific gates from `docs/CESAR_REEL_PIPELINE_V2_PLAN.md` §7.
Deterministic source-level checks live in `scripts/lint_reel_source.py`; this
list is for eyes on rendered frames.

## A. Timeline gates (check once per reel, against the timeline JSON + draft)

- **A1.** Do the first 3–5 seconds show anything other than Cesar full-frame?
- **A2.** Does real footage (person / real screens / real documents / sourced stills) cover less than 75% of the runtime?
- **A3.** Is there any cutaway that cannot be mapped to the exact transcript sentence under it?
- **A4.** Does Cesar ever appear as a persistent corner picture-in-picture?
- **A5.** Does the reel end on anything other than Cesar full-frame (without an approved product-screen CTA)?
- **A6.** Do two or more designed overlays compete on screen at the same moment?
- **A7.** Is any private datum visible — notification, account email, real applicant data, unapproved company or person name?

## B. Frame composition gates (check on every audited still)

- **B1.** Could this frame pass for a generic SaaS promo (card grid, dashboard, floating UI, decorative diagram)?
- **B2.** Is there any gradient — background, panel, or text?
- **B3.** Is there a glow, neon edge, or glowing status dot?
- **B4.** Is there a pill-shaped designed chip or badge?
- **B5.** Is any fake or invented product UI visible (anything not a real WorqAI capture)?
- **B6.** Is re-drawn chrome visible — fake browser bar, fake phone frame, fake terminal?
- **B7.** Is there a decorative element with no anchor in the spoken sentence (floating shapes, ornaments, unrelated animation)?
- **B8.** Is everything centered on one axis with equal weight (no hierarchy)?
- **B9.** Does the accent (lime) cover more than ~8% of the frame area?
- **B10.** Is a surface pure `#000` or pure `#fff`?
- **B11.** Is any color visibly off-token (gold, red, purple, improvised navy panels)?

## C. Typography gates

- **C1.** Is Inter (or any non-Archivo face) used at display size?
- **C2.** Is any display text italic?
- **C3.** Does a caption beat exceed 2 lines or ~5 words?
- **C4.** Are more than two type families visible in the frame?
- **C5.** Is an emoji used as an icon or bullet?
- **C6.** Does caption text fail 4.5:1 contrast against its computed background (busy footage without a sufficient scrim)?
- **C7.** Is there a designed text element using a banned phrase from `.claude/rules/anti-slop.md`?
- **C8.** Does any on-screen number lack a source (not spoken by Cesar, not visible in a cited screenshot)?

## D. Motion gates (check on the rendered draft, not stills)

- **D1.** Does any designed element loop, pulse, or idle while Cesar talks?
- **D2.** Is any easing a bounce/overshoot on a designed element?
- **D3.** Does a push-in on Cesar exceed ~5% scale, or feel faster than the speech?
- **D4.** Are two document highlights animating at once?
- **D5.** Does any enter/exit ignore the duration buckets (micro 120 / short 220 / long 420 ms, exits at 75%)?
- **D6.** Does motion continue through a hard cut (smearing the edit)?

## E. Evidence gates

- **E1.** Is a news still missing its publication name and date label?
- **E2.** Is a generated image used where a real capture exists?
- **E3.** Does a generated image contain readable text, a logo, or a fake product screen?
- **E4.** Is the excluded rejection-inbox screenshot present in any form?

## Recording results

For each audited frame: `frame_id, gates_failed[], verdict`. A still-frame
review passes only when every audited frame passes every gate. Write results to
the job's QA evidence JSON next to the contact sheet, with the six pre-emit
self-critique scores from `VIDEO_DESIGN.md` §8.
