# Cesar Reel Pipeline V2 — Plan Only

Status: creative direction approved for a 45–55 second R01; implementation remains gated behind asset/privacy and storyboard review.

Date: 2026-07-17

## 1. Reset and scope

- The previous concept, storyboard, scene system, and render approvals are invalidated.
- All 93 generated video files from the rejected output were permanently deleted. The 13 original source videos in `inbox/` remain intact.
- The next production scope is **R01 only**. The other five reels wait until R01 establishes the visual language and is approved.
- Previous code and production notes remain temporarily for audit and comparison. They should be archived or removed only after this plan is approved.
- This document plans the rebuild; it does not authorize a render, package update, repository installation, or account access.

## 2. Creative rule: Cesar first, evidence second

The reel must feel like a person explaining something, supported by real evidence—not like a software promo template.

### Required

- Start with Cesar full-frame for at least the first 3–5 seconds.
- Keep Cesar, real screen recordings, real documents, or sourced evidence on screen for at least 75% of the runtime.
- Use the strongest original Cesar take as the visual and audio spine.
- Every cutaway must support the exact sentence being spoken.
- Use real WorqAI screens and real/staged application actions. Do not invent product UI.
- Keep captions short: two lines maximum and generally 2–5 words per beat.
- Use editorial source labels and dates when showing news screenshots.
- End on Cesar full-frame unless the approved call to action specifically requires the real product screen.

### Banned from the new composition

- Persistent top-right picture-in-picture or a permanently cropped Cesar.
- Dashboard/card grids, generic SaaS panels, fake analytics, floating UI, or decorative diagrams.
- Purple/blue gradients, neon glows, glowing status dots, and unrelated looping animation.
- Generic three-column layouts, the old dark-card scene system, and Inter as the default design decision.
- Generated images containing text, logos, CV copy, email copy, or fake product screens.
- Motion that competes with the spoken explanation.

### Motion vocabulary

- Clean cuts and restrained dissolves.
- Subtle 3–5% push-ins or reframes on Cesar.
- Natural cursor movement and scrolling in screen recordings.
- One marker underline, crop, or document highlight at a time.
- Slow Ken Burns movement on a sourced still when a still must be used.
- Simple email-row scrolling/highlighting for the rejection sequence.

## 3. Proposed R01 editorial storyboard

Source runtime: approximately 71 seconds. The approved final target is 45–55 seconds, using a tightened transcript edit rather than speeding up Cesar.

| Target time | Picture | Purpose |
|---|---|---|
| 00:00–00:05 | Cesar full-frame; subtle push-in only | Establish the person and hook: “Secreto número 1…” |
| 00:05–00:09 | Cesar, then a brief 2–3 second Expansión headline cutaway with source/date | Support the mention of layoffs and unemployment without turning the reel into a news montage |
| 00:09–00:13 | Cesar full-frame | Deliver “conseguir trabajo ahora es una fórmula” directly |
| 00:13–00:19 | Full-screen real/staged application workflow: job post and CV upload | Show the system comparison Cesar describes; no corner portrait |
| 00:19–00:28 | Cesar full-frame | Explain the required CV format |
| 00:28–00:34 | Real CV/document B-roll with one highlight at a time: “claro”, “fácil”, “sin tablas” | Make the advice tangible without a fake dashboard |
| 00:34–00:40 | Cesar full-frame | Explain adapting the CV to every job |
| 00:40–00:44 | Staged repeated-application actions or neutral documentary B-roll | Show repetition without using the rejection-inbox screenshot |
| 00:44–00:48 | Cesar full-frame | Transition into the solution |
| 00:48–00:53 | Full-screen real WorqAI recording: paste job description → adapt CV → inspect result | Demonstrate the actual workflow; no fake UI and no picture-in-picture |
| 00:53–00:55 | Cesar full-frame | Close on the recruiter/callback benefit and a restrained CTA |

The rejection-inbox screenshot is excluded from R01 and must not be altered or used. The Forbes education headline does not support R01’s claim closely enough; preserve it for a later reel about education, competition, or the changing labor market rather than forcing it into this story.

## 4. Assets to gather before editing

### Essential

1. A safe WorqAI demo recording using a test account, test CV, and public/sample job description.
2. A staged application recording that stops before submitting any real application.
3. One clean, readable sample CV and matching job description with no personal data.
4. Confirmation that the two news screenshots may be used, with their publication name and date visible or credited. The rejection-email screenshot is excluded and must remain untouched.

### Capture specification

- Record product/application screens at 1920×1080 or higher, with a calm cursor and deliberate pauses.
- Avoid notifications, browser bookmarks, autofill data, account email addresses, and customer information.
- Capture 5–10 seconds of handles before and after each action so the edit can breathe.
- The final composition is 1080×1920; keep important screen content near the center so it survives a vertical crop.
- If the user records the material, provide three separate clips: application/job post, WorqAI input, and WorqAI output/download.

## 5. Optional AI-image prompts

Generated images are optional documentary cutaways, not substitutes for the real product or real evidence. Do not ask the image model to render readable text.

### Repeated applications

> Documentary editorial photograph, over-the-shoulder view of a Latin American job seeker applying to several roles on a laptop in a modest home office, natural daylight, candid and emotionally restrained, authentic skin and hands, screen content intentionally unreadable, no logos, no readable text, no glossy corporate-stock look, vertical 9:16, negative space for captions.

### CV versus job description

> Close editorial photograph of human hands comparing a printed one-page CV with a printed job description, a yellow highlighter marking matching experience, realistic paper texture and desk clutter, soft window light, documentary newsroom photography, no company names, no logos, no readable personal data, vertical 9:16.

### Application fatigue

> Naturalistic late-night photograph of a job-search desk, laptop with several intentionally blurred and unreadable application tabs, coffee cup, handwritten notes and printed CV, quiet fatigue rather than melodrama, restrained neutral color palette, realistic documentary photography, no logos or readable text, vertical 9:16.

### Prepared CV

> Credible daylight editorial photograph of hands reviewing a clean one-page CV beside a laptop, calm and organized workspace, authentic paper and screen reflections, understated optimism, not a commercial stock photo, no generated UI, no logos, no readable text, vertical 9:16.

All accurate text, product UI, captions, and source labels should be overlaid from real assets in Remotion.

## 6. Pipeline V2 architecture

### A. Content and evidence gate

- Lock the transcript and claims before visual design.
- Maintain an asset registry containing source, usage permission, privacy/redaction status, crop notes, and the exact transcript line supported.
- Reject any cutaway that does not directly support the spoken sentence.

### B. Restricted editorial timeline

The new JSON timeline should expose only these scene types:

- `talking_head`
- `screen_recording`
- `still_evidence`
- `document_highlight`
- `inbox_montage`
- `caption`
- `simple_title`

### C. Remotion as the primary compositor

Build a separate `FootageFirstReel` composition with small, explicit components:

- `TalkingHead`
- `EvidenceCutaway`
- `RealScreenRecording`
- `DocumentHighlight`
- `InboxMontage`
- `Captions`

The new path must not import the old `Pip`, dark-panel `Wordmark`, dashboard, card-grid, scan, competition, or fake-product scene primitives. Remotion controls timing, crops, captions, source labels, and deterministic rendering.

### D. Motion Studio as an optional specialist

Motion Studio is not the main renderer for this series. It may be used only for an approved 0.5–2 second transparent overlay, restrained title accent, or one-off graphic that cannot be expressed cleanly in Remotion. It must never create a persistent layout around Cesar.

### E. FFmpeg finishing and QA

- Loudness normalization and audio integrity.
- H.264, `yuv420p`, correct 1080×1920 dimensions and frame rate.
- Black-frame, freeze-frame, duration, clipping, and stream checks.
- Contact sheet and selected full-resolution stills before human approval.

## 7. Anti-slop repository strategy

Do not clone every topic result into the production repository. Topic pages are discovery surfaces, not dependencies. Every adopted tool must be inspected, license-checked, commit-pinned, and recorded in a small vendor lock file.

### Adopt or evaluate

- **Hallmark (`nutlope/hallmark`)**: use as a design-audit/study layer against 6–8 static reel keyframes and the contact sheet. It is an audit skill, not a renderer. Translate its relevant tests into video-specific gates.
- **UX Skill (`Laith0003/ux-skill`)**: the current topic listing describes 120 anti-pattern linter rules and 110 brand specifications, not the previously quoted 152-rule count. Evaluate only the deterministic checks applicable to keyframes; pin a reviewed commit before adoption.
- **Nstup Taste**: promising because it explicitly rejects generic SaaS templates, gradient defaults, card grids, and Inter. Its repository must be inspected successfully before installation; do not add it blindly from a topic listing.
- **PencilPlaybook**: use only if Pencil becomes the approved keyframe tool. Otherwise treat its perceptual principles as research, not a runtime dependency.
- **Awesome Claude Design**: use as a reference catalog to derive one project-specific `VIDEO_DESIGN.md`; it is not part of rendering.
- **PeakOSS Anti-Slop**: optional later as pull-request hygiene if this becomes a multi-contributor GitHub workflow. Its 34 PR-quality rules do not judge visual frames, so it is not a core video-quality gate.

### Project-specific automatic gates

Reject a draft if any of these are true:

- Cesar appears in a persistent corner crop.
- The first 3–5 seconds are not Cesar full-frame.
- Real person/product/evidence occupies less than 75% of the runtime.
- A fake dashboard or fake WorqAI screen appears.
- A card grid, generic gradient, glowing dot, or unrelated diagram appears.
- A cutaway cannot be mapped to a specific transcript sentence.
- More than one major designed overlay competes with the footage.
- Any private data, notification, account identifier, or unapproved company/person name is visible.

## 8. Tool-update plan after approval

### Remotion

- The workspace already contains Remotion. The rejected final videos did not use it, and the current Remotion component library also contains the same generic persistent-PIP/card design problems.
- The workspace currently pins `remotion` and `@remotion/cli` at `4.0.489`; the reviewed upstream release is `4.0.490`.
- After approval, update both packages together, keep exact pins, re-check the current Remotion license for WorqAI’s company size/use, and verify one still plus a short test composition before building R01.

### Motion Studio

- Do not update the existing dirty Motion Studio checkout in place.
- After approval, inspect/fetch upstream in a clean clone or worktree, review changes and license, pin a known commit, and preserve all existing user changes.
- Keep Motion Studio optional and subordinate to the footage-first Remotion edit.

### Anti-slop tools

- Install only reviewed project-scoped skills or pinned audit code.
- Record repository URL, commit, license, purpose, and enabled rules in `vendor-lock.json`.
- Do not let third-party skills rewrite production code automatically; first run them in audit/report mode on still frames.

## 9. Human approval gates

1. **Design contract and privacy** — approve this direction, source use, and redactions.
2. **Timestamp storyboard** — approve the final 71-second or shortened transcript/timeline.
3. **Still-frame review** — approve 6–8 full-resolution frames and a contact sheet; no video render yet.
4. **Opening proof** — approve only the first 12–15 seconds rendered in Remotion.
5. **Full R01 draft** — approve picture, captions, sources, audio, and product accuracy.
6. **Release candidate** — run technical QA and export the master.

No later reel enters production until R01 passes the full-draft gate.

## 10. Proposed implementation sequence after approval

1. Create branch `codex/reel-pipeline-v2`.
2. Build the asset registry and perform privacy/source review.
3. Update and pin the approved tool versions in isolation.
4. Create the separate footage-first Remotion composition and remove old primitives from its dependency path.
5. Produce the R01 timestamp storyboard and 6–8 still frames.
6. Run the anti-slop keyframe audit and repair any failures.
7. Render and review only the first 12–15 seconds.
8. Build the full R01 draft only after approval.
9. Complete visual, editorial, privacy, audio, and technical QA.
10. Decide whether the visual language is strong enough to apply to the other five reels.

## 11. Decisions required before implementation

Resolved on 2026-07-17:

1. R01 will be tightened to 45–55 seconds.
2. The rejection-inbox screenshot will not be anonymized, altered, or used.
3. Codex may record a safe signed-in WorqAI test workflow. No real application submission, customer data, or private CV data is authorized.

Still required before implementation: approve the tightened transcript/timestamp storyboard and identify the safe WorqAI test account, sample CV, and sample job description.
