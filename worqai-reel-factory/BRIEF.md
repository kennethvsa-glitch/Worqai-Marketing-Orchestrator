# Reel Factory — Quantum Brief

You are building a **content factory for WorqAI reels**. This brief gives you the goal, the raw materials, and the guardrails. **The plan is yours.** Where you see a better architecture than anything sketched here, take it — this document is the floor, not the ceiling.

## The idea

Cesar records talking-head videos for WorqAI (the CV/ATS product, worqai.io). Today each reel is edited by hand, one at a time. The factory changes the economics twice over:

1. **Edit lane** — a raw recording goes in; a branded, captioned, animated, publishable reel comes out with minimal human touch. (The inspiration: creators are doing this today by dropping footage into a HyperFrames project and letting Claude edit it against reference styles.)
2. **Matrix lane** — clips are classified as **hooks, bodies, and CTAs**, and the factory recombines them: 3 hooks × 2 bodies × 2 CTAs = 12 distinct videos from 7 pieces of footage. Every published variant is traceable to its recipe so we learn which hook wins and feed that back.

The factory should feel like this to use: drop raw video → approve what the machine proposes → publishable variants appear, on brand, with a paper trail.

## Input reality (design for this, not for the ideal)

- Recordings arrive as **5–6 minute continuous takes with retakes left in**. Nobody pre-cuts them. Segmenting, detecting retakes, and classifying clips is the factory's job; humans should only ever approve/adjust something readable (text, not timelines).
- Footage is Spanish and English, phone-vertical, varying quality.
- Operators are two non-editor founders. Anything requiring manual video editing skill will not be used.

## Study these before you plan

- **HyperFrames** — https://github.com/heygen-com/hyperframes — HTML/CSS/GSAP → deterministic MP4, headless Chrome + ffmpeg, agent-friendly CLI, agent skills, registry blocks (captions, transitions). Apache 2.0. Our existing motion work is HTML/GSAP-native, so this is our home idiom.
- **Remotion** — https://github.com/remotion-dev/remotion — React → MP4, mature ecosystem: `@remotion/captions` (word-timed caption data model), Whisper integrations, `<OffthreadVideo>` for reliable footage-in-composition. License: free for companies ≤3 people (we qualify; re-verify if the team grows).
- **motion-studio** (attached read-only at `C:\Users\kenne\motion-studio`) — the WorqAI brand's motion home: design tokens in `motion/tokens/`, house eases, SFX library in `Ideation/Sound effects/`, and a determinism philosophy worth inheriting.

Choose your engine(s) with evidence — spike before committing, and record the decision and why. Mixing them (one for footage editing, one for motion graphics, ffmpeg for assembly) is a legitimate outcome if the spikes say so.

## Non-negotiables (the only hard walls)

1. **Brand**: outputs must be unmistakably WorqAI — tokens sourced from motion-studio (bg `#080a10`, lime `#C9F24D`, Archivo, grain), kinetic captions in brand style (never default-TikTok yellow), anti-slop copy rules. If a render could pass for a generic template, it fails.
2. **Real footage only** — no AI avatars, no synthetic people.
3. **No auto-posting** — outputs are files plus a tracking record; humans publish.
4. **motion-studio is read-only** (one exception: an additive token-export script if none exists).
5. **CapCut MCP**: if one is registered in the session, inventory it and decide its role with evidence; it may never be a hard dependency. Do not install unvetted community servers without flagging first.

## Ideas from our ideation — adopt, improve, or discard freely

- Transcript-first architecture: Whisper word-level timestamps as the machine's "eyes"; cuts, captions, retake detection, and compatibility checks all computed from the transcript timeline.
- Auto cut-list for raw takes: split at silences/sentence breaks, detect retakes by near-duplicate sentences (keep the last take), propose slot labels; human approves a readable text table, ffmpeg slices.
- A clip library with a manifest (id, slot, transcript, words, lang, tags) as the single source of truth.
- Recipe naming (`H02-B01-C03.mp4`) so the filename is the experiment record, plus a posting CSV ready for later analytics wiring.
- Reference-creator files: editing styles described as patterns in words (cut rhythm, caption behavior, zoom cadence), imitated — never copied assets.
- The falsifier: after two weeks of posting, matrix variants must beat the current hand-edited approach on reach/retention or the matrix lane freezes (Cesar measures). The edit lane earns its keep separately if it cuts editing below ~30 min/video.

## What success looks like (acceptance, not steps)

1. A real 5–6 minute raw take goes in; a correct, human-readable cut proposal comes out; approved clips land in the library transcribed and classified.
2. One command produces an edited, captioned, branded reel from library footage that Kenneth and Cesar approve on sight.
3. One command produces N valid hook×body×CTA variants with recipe names and a tracking record.
4. A fresh Claude session can operate the whole factory from the repo's docs alone.
5. Every claim of "done" is backed by rendered files someone actually watched.

Aim higher than this brief where you see the opportunity. Surprise us.
