# Reel Matrix Factory — Execution Plan for Quantum

Turn Cesar's recorded WorqAI reels into a permutation machine: a library of transcribed hook/body/CTA clips that an agent can edit, caption, animate, and recombine into dozens of distinct publishable variants. Two lanes: an **editor lane** (one rough video in → one branded edited reel out, the HyperFrames workflow) and a **matrix lane** (hook × body × CTA permutations at volume).

**Relationship to existing plans:** This supersedes the *engine choice* of `remotion-content-factory-plan.md` (HyperFrames replaces Remotion as primary — reasons in M0) but inherits its discipline wholesale: binary spike gates, brand-token sync from motion-studio, the anti-slop/spelling FAIL gate, the kinetic-captions brand bar ("if it looks like a generic TikTok template, the spike FAILS"), and the 2-week falsifier that Cesar measures. The artisanal motion-studio pipeline (villain films, golden hashes, Locks) is NOT touched by this plan in any way.

## Where this runs

- **New repo**: `C:\Users\kenne\worqai-reel-factory` (sibling of motion-studio, per the "repo NUEVO" rule in the remotion plan).
- Session needs read access to `C:\Users\kenne\motion-studio` for brand tokens (`motion/tokens/`) and `Ideation/Sound effects/`.
- Execute milestones in order. Every milestone has a binary exit gate. Report gate results with evidence (rendered files, screenshots, hashes), not assertions.

## Scope fence (violating this is failure)

- No auto-posting to any platform. Output is MP4s + a tracking CSV.
- No AI-generated avatars or synthetic footage of people. Real recorded footage only.
- Do not modify anything inside `C:\Users\kenne\motion-studio` except ADDING a token-export script if one doesn't exist (M4) — never touch scenes, locks, or golden hashes.
- CapCut MCP is an optional handoff target, never a dependency. If its spike fails, the pipeline must work without it.
- No new product features. This is a content pipeline, not an app.

---

## Reference stack (study these, in this order, before S1)

- **HyperFrames** — https://github.com/heygen-com/hyperframes — primary engine candidate. HTML/GSAP-native (our idiom), deterministic by principle, agent-friendly CLI, 21 agent skills, registry blocks for captions/transitions. Apache 2.0.
- **Remotion** — https://github.com/remotion-dev/remotion — reference AND fallback. Even if HyperFrames wins the spikes, study Remotion's `@remotion/captions` package (word-timing data model, caption grouping) and its Whisper integration patterns before building M2 captions — it is the most mature open implementation of exactly that problem. If S2 fails, Remotion's `<OffthreadVideo>` becomes the editor-lane engine (license: free ≤3 employees, per LICENSE.md — we qualify; re-verify if the team grows).
- **motion-studio** (read-only) — the artisanal pipeline's `motion/tokens/`, house eases, and determinism locks are the house style this factory inherits.

## M0 — Spikes (all binary; half a day each, max)

Run these before building anything. The engine decision comes out of S1–S2, not out of preference.

**S1 — HyperFrames brand render.** `npx hyperframes init`, build a 2-second 1080×1920 comp using WorqAI tokens (bg `#080a10`, lime `#C9F24D`, Archivo, grain — pull real values from `motion-studio/motion/tokens/`). Render twice.
*Gate:* both renders complete, outputs are pixel-identical or visually indistinguishable, and the comp uses GSAP with the house eases (port `worq-luxe` if the tokens file defines it).

**S2 — Footage in composition (THE critical spike).** Put a real recorded clip (any WorqAI take Cesar has) inside a HyperFrames comp: trim to a sub-range, overlay one caption word synced to speech, render 10 seconds.
*Gate:* audio/video stay in sync frame-accurately and the render is reliable across two runs. **If S2 fails, the editor lane falls back to Remotion** (`<OffthreadVideo>` is proven; license free ≤3 people per the remotion plan — re-verify on team growth) and HyperFrames keeps only the motion-graphics duties. If both fail: captions via ffmpeg subtitle burn, assembly via ffmpeg only. Record the decision in the repo README.

**S3 — Transcription.** Whisper (faster-whisper local, or API if a key exists in env) on one Spanish clip and one English clip → word-level timestamps JSON.
*Gate:* word timings accurate enough to drive word-by-word captions without manual fixing.

**S4 — CapCut MCP inventory.** Check `claude mcp list` in the session. If a CapCut MCP is registered: list its tools, then smoke-test — create a draft with 2 clips and a text layer, find the export path.
*Gate (informational, can't fail the plan):* verdict recorded in README — CapCut is (a) a usable programmatic assembler, (b) a manual-polish handoff (we generate drafts, Cesar finishes), or (c) dropped. If no CapCut MCP is registered in the session, note it and move on — do not install random community servers without flagging to Kenneth first.

## M1 — Clip library + manifest (the memory of the system)

```
worqai-reel-factory/
  CLAUDE.md                ← style memory: tokens, voice, anti-slop (inherited), engine decision
  library/
    hooks/  bodies/  ctas/  broll/
  refs/                    ← reference-creator notes (see M2)
  inbox/                   ← raw drops before ingest
  scripts/                 ← CLI tools
  out/                     ← rendered variants + manifest.csv
  manifest.json
```

**Two ingest modes — raw mode is the primary one.** Input reality: Cesar records 5–6 minute continuous takes with retakes left in. Nobody cuts them by hand; segmentation is the pipeline's job.

`ingest --raw <file>`: full Whisper transcript with word timestamps → the agent proposes a **cut list** from the transcript alone: segment boundaries at silences (>1.2s) and sentence breaks; **retake detection** by fuzzy-matching near-duplicate sentences (keep the LAST take of any repeated phrase — people re-record until they nail it); a suggested slot (hook/body/cta) and topic tags per segment based on content. The cut list is written to `inbox/{file}.cutlist.md` as a human-readable table (segment, timecodes, transcript excerpt, proposed slot, keep/drop + why). Kenneth or Cesar reviews the table — approving is editing text, not video — then `ingest --apply` slices the approved segments with ffmpeg (stream-copy where keyframes allow, re-encode otherwise) into `library/{slot}/` named `H01`, `B03`, `C02`…

`ingest <file> --slot hook`: direct mode for pre-cut clips, same downstream path.

Both modes end in the same manifest entry:

```json
{ "id": "H03", "slot": "hook", "file": "library/hooks/H03.mp4",
  "duration_s": 2.8, "lang": "es", "transcript": "…", "words": [...],
  "tags": ["ats", "callback-pain"], "energy": "high",
  "ingested": "2026-07-06", "status": "active" }
```

The manifest is the answer to "the AI knows the transcript of every clip we have." Every downstream step reads it; nothing reads raw files directly.
*Gate:* one real 5–6 minute raw recording goes through `--raw`: the cut list correctly flags the obvious retakes and silences (spot-checked against the actual video), and after approval the library holds 6+ usable clips across slots; manifest validates (unique ids, no missing transcripts); a `library` CLI command prints a readable inventory table.

## M2 — Editor lane (the HyperFrames workflow from the reel)

One rough-cut video in → one branded, captioned, animated reel out. This is the creator's workflow from the saved IG reel, with our discipline instead of "bypass permissions, of course."

1. `edit <file>` prepares a session brief: transcript + word timings + the style contract.
2. The agent builds a HyperFrames comp: cuts/punch-ins on beat, kinetic captions word-by-word (**brand style: lime on dark, Archivo, mask-reveal — explicitly NOT default TikTok yellow**), SFX from `motion-studio/Ideation/Sound effects/` (whooshes on transitions, ticks on UI beats), branded CTA end-card.
3. **Reference-creator protocol:** `refs/{creator}.md` files describe editing *patterns* in words (cut rhythm, caption style, zoom cadence) extracted from watching reference reels. Patterns are imitated; assets are never copied. Start with one ref file for the @mrpink-style fast-caption edit described in the saved reel.
4. Brand gate before any file is "done": contact-sheet screenshots reviewed against the anti-slop + brand rules. Generic-template look = FAIL = iterate captions/timing, same as the remotion plan's gate 3.

*Gate:* one real rough-cut goes in, one publishable branded reel comes out, and Kenneth/Cesar approve it visually. Time budget once built: under 30 minutes per video.

## M3 — Matrix lane (the multiplier)

`combine` CLI reads the manifest and generates permutations:

- **Rules:** total duration 20–40s; language consistency (no ES hook into EN body); topic-tag compatibility (configurable allow/deny pairs); no contradictory claims (tag-driven); max N variants per run.
- **Assembly:** normalize all segments (1080×1920, 30fps, loudness ≈ -14 LUFS), concat via the engine chosen in M0 (ffmpeg concat is the default fast path for pure footage joins; rendered CTA end-cards from M2 templates append as the final segment).
- **Recipe naming:** `H02-B01-C03.mp4` — the filename IS the experiment record.
- `out/manifest.csv`: one row per variant (recipe, duration, lang, created, posted?, platform, notes) — Cesar's posting log. Metricool wiring is a later session; leave the columns ready.

*Gate:* from 3 hooks × 2 bodies × 2 CTAs in the library, 12 valid variants render in one command; spot-check 3 for sync/loudness/branding; recipes and CSV correct.

## M4 — Token sync + docs

- Token export: generate the factory's tokens from `motion-studio/motion/tokens/` via script (the remotion plan's regla de oro: brand changes once, both factories inherit). If motion-studio lacks an export script, add ONLY that script there, additive.
- `CLAUDE.md` in the new repo: engine decision + rationale, the style contract, how to ingest/edit/combine, the brand gate, the scope fence.
- README: spike results, CapCut verdict, falsifier date.

*Gate:* a fresh Claude session in the repo can run `ingest → edit → combine` end-to-end using only the docs.

## The falsifier (inherited, Cesar measures)

Two weeks of posting matrix variants. If they don't beat the existing approach (film recortes / hand-edited reels) on reach/retention, the matrix lane freezes — volume is only justified by volume that works. The editor lane (M2) survives regardless if it cuts editing time below 30 min/video.
