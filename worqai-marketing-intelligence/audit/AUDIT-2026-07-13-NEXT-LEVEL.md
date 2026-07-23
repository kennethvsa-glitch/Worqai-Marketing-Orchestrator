---
date: 2026-07-13
workspace: C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence
verdict: IMPLEMENTED
findings: 0
ships: yes
status: engineering-complete-operational-pending
source_plan: PLAN-2026-07-13-NEXT-LEVEL.md
---

# What changed

Implemented the engineering workstreams of the next-level plan. The operational
workstreams (running the weekly cadence for real, live Metricool/GSC ingestion,
shipping SEO pages) are deliberately left to execution over weeks — they cannot
be "coded."

## WS0 — Hygiene

- Fixed git dubious-ownership (`safe.directory`) so git works as the primary user.
  Note: this branch (`codex/wmi-real-intelligence`) still has zero commits — the
  whole tree is uncommitted working state, pre-existing and untouched here.
- `.gitignore` already covered `.wmi/`, `__pycache__/`, `.pytest_cache/`,
  `.pnpm-store/`. Removed the stray `.pnpm-store/`.
- **Relocated the SQLite memory DB out of OneDrive.** `paths.py` now resolves a
  per-user `data_home()` (`WMI_HOME` → `%LOCALAPPDATA%\wmi` → XDG), and
  `MemoryStore` defaults there. Existing in-repo `.wmi/memory.db` is migrated once
  via SQLite's backup API into a staging file then atomically renamed; on any
  failure it falls back to the legacy path so no data is lost.

## WS1 — Real validation (two tiers)

- New `text_signals.py` is the single home for the shared heuristic detectors;
  `taste_judge.py` now imports them. Behavior is byte-for-byte identical — the
  existing taste/score tests still pass — but the regexes are no longer duplicated.
- New `validation.py`: `evaluate_hard_gates` returns deterministic pass/fail gates.
  Only banned language, unqualified ATS/outcome claims, Spanish-language mismatch,
  and source-fidelity loss **block**; format completeness is advisory. `build_judge_packet`
  hands the operator the draft, brand excerpts, and a taste/fidelity/channel-fit
  rubric to score against — WMI no longer fabricates a numeric taste score at the
  validation boundary.
- The bridge `validate` command now leads with `blocked` / `blocking_gates` /
  `judge_packet` and demotes the old score to `advisory_quality`.

## WS2 — Performance-loop plumbing

- New `utm.py` (`build_utm_url`, `asset_id_from_utm_content`): tracked links carry
  the asset ID in `utm_content` so metrics can be matched back to the asset.
- Bridge gained `record-performance` (structured `--metrics-json` or NL `--text`)
  and `utm` commands; the CLI gained a `record-performance` parity command.

## WS3 / WS4 — Cadence and passes

- `OPERATIONS.md`: a Monday-pipeline / midweek-production / Friday-retro weekly
  cadence, with the performance loop as the load-bearing Friday step.
- The Claude-facing `SKILL.md` now specifies three judgment passes (create →
  contrarian → judge) and the two-tier validate output.

## Verification

- `py -m pytest -q` → **95 passed** (73 pre-existing + 22 new; pre-existing
  `tmp_path` tests need `--basetemp` redirected out of the restricted temp dir).
- Smoke-tested `utm`, `record-performance`, and `validate` bridge commands
  end-to-end; `validate` correctly blocks an unqualified-guarantee draft on the
  `absolute_claims` gate and exposes the three judge axes.

# Not done (operational, by design)

- Running three real weekly cadences (WS3 execution).
- Live Metricool / Search Console / conversion ingestion (needs live connectors
  and published assets).
- Shipping the first WMI-briefed SEO page to `cv-tailored` (WS5).

# Notes for the shim/dedup finding

The "triplicated bridge" concern in the plan was partly wrong on inspection: the
`.claude` and `integrations` bridges are thin `runpy` shims of the root
`scripts/wmi_bridge.py`, not logic copies. Added `tests/test_bridge_shims.py` to
keep them thin. The two `SKILL.md` variants differ on purpose (Claude vs Codex
paths); only the Claude-facing one was updated.
