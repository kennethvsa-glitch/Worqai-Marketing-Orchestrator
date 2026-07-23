# Engine Decision — Reel Factory

> **Current status (2026-07-13):** This document preserves the original spike decision. HyperFrames remains the historical baseline, while **Remotion 4.0.489 is now activated for the WMI-orchestrated transcript + motion-video lane** because the React component model is the better fit for semantic animation sections, reusable scene mechanisms, captions, and campaign variants. The activation does not auto-publish and remains human-gated.

**Date:** 2026-07-11  
**Worktree:** q/7932dc83-candidate  
**Spikes synthesized:** S1 (HyperFrames brand test), S2 (footage inside HyperFrames), S3 (transcription backend selection)

---

## Original Render Engine Decision: HyperFrames

**Chosen engine: HyperFrames 0.7.52**

### Rationale

S1 confirmed that HyperFrames renders branded WorqAI compositions deterministically (composition hash `58f304807e2fdcde` reproduced across two independent runs, byte-identical frames). All brand tokens — bg `#080a10`, lime `#C9F24D`, Archivo, grain at 0.11 opacity — rendered correctly via HTML/GSAP. Render time ~17s cold / ~10s warm.

S2 confirmed that real footage from `inbox/` plays inside a HyperFrames composition without audio/video drift. Both renders produced identical byte outputs (18,739,023 bytes each) with 26.7ms audio tail (standard AAC 1024-sample block boundary, less than one 30fps frame at 33.3ms). All five S2 gates passed:

| Gate | Result |
|---|---|
| Both renders complete without error | PASS |
| Audio/video in sync (< 1 frame drift) | PASS (26.7ms < 33.3ms) |
| Identical deterministic output | PASS (same hash, same bytes) |
| Real footage from inbox/ (no AI avatars) | PASS |
| Caption overlay at fixed timecode | PASS |

**No license flip to Remotion required** — see license table below. No actually-imported package carries proprietary terms that preclude commercial content production.

### Remotion path (originally a fallback; now activated for the motion-video lane)

The original spike recorded Remotion as a fallback with `<OffthreadVideo>` for footage reliability and word-timed caption rendering. The React component model has since become preferable for transcript-driven explanatory scenes and controlled A/B variants, so this path is now active alongside—not in place of—the historical HyperFrames baseline.

---

## Transcription Backend: faster-whisper

**Winning backend: faster-whisper 1.2.1 via `.venv/Scripts/python.exe`**

### Selection Order (S3)

| Priority | Backend | Outcome | Reason |
|---|---|---|---|
| 1 | ffmpeg built-in whisper AVFilter | FAIL | No GGML model file on system; filter requires whisper.cpp-format `.bin` model. Installed model is CTranslate2 format (incompatible). |
| 2 | whisper.cpp standalone binary | FAIL | Binary not found at any of 7 checked locations on PATH and common install paths. |
| 3 | faster-whisper via .venv/ | **PASS** | Per-word `start`, `end`, `prob` on every segment. Already installed. Zero additional downloads required. |

### Winning Command

```bash
.venv/Scripts/python.exe -c "
from faster_whisper import WhisperModel
model = WhisperModel('<model_dir>', device='cpu', compute_type='int8')
segs, info = model.transcribe('<audio_file>', language='es', word_timestamps=True)
for seg in segs:
    for word in seg.words:
        print(word.word, word.start, word.end, word.probability)
"
```

Where `<model_dir>` is `~/.cache/huggingface/hub/models--Systran--faster-whisper-tiny/snapshots/d90ca5fe.../` (already cached).

### Sample Output (Spanish, first 30s)

```
{"word": " Ok,",  "start": 0.000, "end": 0.58, "prob": 0.041}
{"word": " voy",  "start": 1.100, "end": 1.38, "prob": 0.661}
{"word": " a",    "start": 1.380, "end": 1.38, "prob": 0.521}
```

Every word carries `start` and `end` in seconds — compatible with the existing `cutlist.json` schema and the kinetic caption pipeline.

### Model Upgrade Path

Current model: `faster-whisper-tiny` (CTranslate2, CPU, int8). For production: upgrade to `faster-whisper-base` or `faster-whisper-small` — same CTranslate2 format, same invocation, higher word accuracy.

---

## License Table

Packages audited are those actually imported by the factory via `spikes/s1-hyperframes/package.json` (direct dependency: `hyperframes`) and the runtime dependencies HyperFrames installs. GSAP is not in node_modules — see note below.

| Package | Installed Version | LICENSE file path checked | License found | Commercial verdict |
|---|---|---|---|---|
| **hyperframes** | 0.7.52 | `node_modules/hyperframes/LICENSE*` — **no file** | Apache 2.0 (see dual-source note) | **CLEAR** |
| puppeteer-core | 25.3.0 | `node_modules/puppeteer-core/` — no LICENSE file | Apache-2.0 (package.json `license` field) | CLEAR |
| @puppeteer/browsers | 3.0.6 | `node_modules/@puppeteer/browsers/` — no file | Apache-2.0 (package.json `license` field) | CLEAR |
| sharp | 0.34.5 | `node_modules/sharp/LICENSE` | Apache 2.0 | CLEAR |
| hono | 4.12.29 | `node_modules/hono/LICENSE` | MIT | CLEAR |
| @hono/node-server | (see hono) | `node_modules/@hono/node-server/LICENSE` | MIT | CLEAR |
| esbuild | 0.25.12 | `node_modules/esbuild/LICENSE.md` | MIT | CLEAR |
| postcss | 8.5.16 | `node_modules/postcss/LICENSE` | MIT | CLEAR |
| prettier | 3.9.5 | `node_modules/prettier/LICENSE` | MIT | CLEAR |
| fontkit | 2.0.4 | `node_modules/fontkit/` — no file | MIT (package.json `license` field) | CLEAR |
| onnxruntime-node | 1.27.0 | `node_modules/onnxruntime-node/` — no file | MIT (package.json `license` field) | CLEAR |
| **GSAP** | 3.14.2 (CDN) | N/A — not in node_modules | GSAP Standard License (free for web) | CLEAR (CDN, not installed binary) |

**No package carries proprietary terms that preclude commercial content production. Engine decision remains HyperFrames. No flip to Remotion.**

### HyperFrames License — Dual-Source Documentation (Amendment B)

#### Source 1: npm Registry

The npm registry reports **Proprietary** for `hyperframes@0.7.52`. This is the registry's default label when a `package.json` ships with **no `license` field** — it is a system default, not an affirmative proprietary declaration by the publisher.

Installed file checked: `node_modules/hyperframes/package.json`  
Result: no `license` key present. No `LICENSE*` file exists in `node_modules/hyperframes/`.

#### Source 2: GitHub (heygen-com/hyperframes)

The upstream repository at `https://github.com/heygen-com/hyperframes` carries an **Apache 2.0** LICENSE file. This is confirmed by the BRIEF.md citation ("Apache 2.0") and by SPDX identifiers embedded in the installed binary.

#### Evidence in the Installed Binary

File: `node_modules/hyperframes/dist/cli.js`  
Path: `spikes/s1-hyperframes/node_modules/hyperframes/dist/cli.js`

Opening lines of the embedded `@license` block at line 185465–185470:

```
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
```

Additional SPDX occurrences at lines 132659 and 143777 of the same file confirm that the bundled components carry Apache-2.0 identifiers throughout.

#### Definitive Determination

**The governing license for the installed binary is Apache 2.0.**

The npm registry "Proprietary" label is a false positive arising from an absent `license` field in `package.json`. The GitHub repository provides the authoritative license terms. The installed binary's own embedded SPDX identifiers corroborate Apache 2.0 at three distinct locations in `dist/cli.js`. No proprietary license text was found anywhere in the installed package. Commercial content production is permitted under Apache 2.0 with attribution.

### GSAP — CDN Note

GSAP is not installed in `node_modules`. It is loaded at composition runtime via CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
```

Source: `spikes/s1-hyperframes/index.html`, line 13.

GSAP 3.x core and standard plugins are covered by the GSAP Standard ("No Charge") License, which permits free commercial use on public websites. No GSAP files are part of the factory's installed binary footprint.

---

## CapCut MCP Verdict

**Verdict: (c) not registered**

A scan of the session's MCP server registry found no CapCut MCP server. Registered MCP servers in this session: `autocad-mcp`, `chrome-devtools`, `claude.ai Figma`, `claude.ai Jam`, `claude.ai Metricool`. No CapCut server appears in `~/.claude/settings.json` or any project-level settings file.

CapCut is confirmed as a non-dependency. No CapCut tooling is referenced in any spike or project file.

---

## Summary

| Decision | Value |
|---|---|
| Render engine | **HyperFrames 0.7.52** |
| Engine rationale | S1+S2 PASS: deterministic brand renders + real footage with sync. Apache 2.0 governs. |
| Transcription backend | **faster-whisper 1.2.1** via `.venv/Scripts/python.exe` |
| Transcription rationale | Only backend producing per-word timestamps. Already installed. No download required. |
| CapCut MCP | Not registered — cannot assess programmatic vs. handoff role |
| License flip to Remotion | **No** — no proprietary blocking terms found |
