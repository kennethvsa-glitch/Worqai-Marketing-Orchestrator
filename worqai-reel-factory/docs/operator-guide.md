# WorqAI Reel Factory — Operator Guide

This guide documents the implemented commands as of the 2026-07-12 repair.

## Safety and release rules

- Source footage must be real footage from `inbox/`.
- The factory writes local files only. It never posts or schedules content.
- `C:\Users\kenne\motion-studio` is read-only.
- `out/variants/` contains rejected legacy renders and is not a release source.
- New renders remain release candidates until a human watches and approves their exact QA hash.

## 1. Ingest footage

```powershell
python scripts/ingest.py --raw inbox/recording.mp4 --lang es
```

This transcribes the recording and writes:

- `inbox/recording.cutlist.md` — editable human review table.
- `inbox/recording.cutlist.json` — timed-word sidecar.

Review the Markdown table. Correct `keep`, slot labels, and cut boundaries, then apply it:

```powershell
python scripts/ingest.py --apply inbox/recording.cutlist.md
```

List the resulting library:

```powershell
python scripts/ingest.py --list
```

Slot classification is only a proposal. Recording position is never treated as semantic evidence.

## 2. Review captions

Machine transcripts are drafts. Any clip used in a production storyboard must have a reviewed, one-to-one token correction in:

```text
scripts/caption-corrections.json
```

The renderer blocks a clip with missing corrections or mismatched word counts. This prevents tiny-Whisper errors from becoming published captions.

## 3. Define a coherent storyboard

Add a record to `scripts/storyboards.json` containing:

- a stable storyboard ID and recipe name;
- an explicit ordered clip list;
- a written narrative explaining why those sentences connect;
- evidence timestamps;
- `status: approved_for_repair` only after editorial review.

Do not restore duration/tag-only permutations. Broad tags such as `general` are insufficient to establish sentence continuity.

## 4. Render

Render one reviewed storyboard:

```powershell
python scripts/render_storyboard.py ats-direct --force
```

Render every approved storyboard and rebuild the tracking manifest:

```powershell
python scripts/combine.py --force
```

Use `--storyboards ats-direct ats-context` to select specific storyboards. Use `--max-variants N` to cap the approved list.

Outputs land in `out/release-candidates/`:

- `<recipe>.mp4` — captioned reel;
- `<recipe>-contact.jpg` — twelve-frame visual review sheet;
- `<recipe>.captions.json` — caption/clip inventory;
- `<recipe>.storyboard.json` — exact storyboard snapshot;
- `manifest.csv` — batch tracking record.

## 5. QA

```powershell
python scripts/qa_release.py
```

The gate verifies streams, resolution, duration, caption inventory, sampled burned-in caption pixels, non-black footage, loudness, true peak, and SHA-256 hashes. Evidence is written to:

```text
.visual-production/jobs/reel-factory-repair-20260712/evidence/qa-report.json
```

## 6. Human approval

Watch the complete MP4, not only its contact sheet. If it is acceptable, record approval against the verified hash:

```powershell
python scripts/approve_release.py H04-B09-C00 --reviewer "Kenneth" --verdict approved --notes "Watched complete video"
```

If the bytes change after approval, rerun QA and approve the new hash again.

## Legacy single-clip diagnostic

`python scripts/edit.py S004` still renders a one-clip caption test. It is a diagnostic, not a complete production reel.

## 7. WMI → Remotion motion-video lane

Use this lane when Cesar's transcript benefits from explanatory animation rather than only footage editing.

1. Compile and validate the marketing request through `worqai-marketing-intelligence`.
2. Create a JSON handoff in `remotion/specs/`. The contract is documented in `remotion/specs/README.md`.
3. Keep all on-screen claims supported by the selected transcript. Global reviewed corrections live in `scripts/caption-corrections.json`; use `caption_overrides` only for a spec-specific final repair.
4. Render and QA in one command:

```powershell
python scripts/render_remotion_pipeline.py remotion/specs/cesar-500-applications-wmi.json --output out/remotion-candidates/cesar-500-applications.mp4
```

The controller performs these bounded stages:

- validate WMI routing and claim guards;
- trim and normalize real footage into upright 1080×1920 proxies;
- compile manifest word timing and reviewed caption overrides;
- render the generic `SpecDrivenCesarReel` Remotion composition;
- normalize dialogue to approximately −14 LUFS with true-peak headroom;
- create a six-frame contact sheet;
- verify H.264/AAC streams, 30 fps, resolution, loudness, true peak, black frames, and SHA-256;
- leave `human_review: pending` in the QA report.

Supported deterministic scene types are `hook`, `competition`, `dual_reader`, `scan`, `system_variants`, `proof_map`, `role_focus`, `application_stack`, `mismatch`, `alignment`, `relevance`, and `cta`. Add new scene types only when they represent a reusable transcript mechanism, not decorative B-roll.

### Curated 12-video campaign

The Cesar batch is controlled by `scripts/cesar-campaign-catalog.json`. Validate it before spending render time:

```powershell
python scripts/generate_cesar_batch.py --validate-only
```

The validator rejects missing caption review, incompatible hook/body topics, identical A/B hooks, duplicate master signatures, extra CTAs, unsupported source trims, unsafe claims, and variants outside the 18–32 second taste window.

Render or resume all candidates:

```powershell
python scripts/render_cesar_batch.py --resume
```

The campaign controller requires 12 passing media reports, six master stories, and 12 unique output hashes before campaign QA can pass. The final human-review gate remains open until the user watches the outputs.
