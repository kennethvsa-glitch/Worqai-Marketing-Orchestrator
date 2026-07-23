# WMI Next Level — Roadmap

**Date:** 2026-07-13
**Status:** engineering workstreams implemented 2026-07-13 (see `audit/AUDIT-2026-07-13-NEXT-LEVEL.md`); operational workstreams pending real execution.
**Scope:** the WMI system itself (this repo) plus its connections to the four production workspaces. This is a systems plan, not a content calendar.

## Implementation status (2026-07-13)

- **Done (code):** WS0 hygiene incl. memory.db relocation out of OneDrive; WS1 two-tier validation (hard gates + judge packet, score demoted to advisory) with golden fixtures; WS2 UTM builder + `record-performance`/`utm` bridge commands; WS3 `OPERATIONS.md`; WS4 create/contrarian/judge passes in `SKILL.md`. 95 tests pass.
- **Pending (operational, cannot be coded):** running three real weekly cadences; live Metricool/GSC/conversion ingestion; shipping the first WMI-briefed SEO page (WS5).
- **Correction:** the bridge "triplication" was really one source + two `runpy` shims (guard test added); the two `SKILL.md` variants differ on purpose (Claude vs Codex).

## Where the system stands

WMI already has the right skeleton: markdown brand sources, JSON routing/capabilities, Python context compilation, Claude creation, SQLite memory, human-gated production handoffs into `cv-tailored`, `worqai-marketing`, `motion-studio`, and `worqai-launch`. It has shipped real output (the 2026-07-13 SEO growth plan now driving the cv-tailored `Google-SEO` branch, staged patches, a rendered carousel).

The honest weaknesses, from the 2026-07-13 audit:

1. **Validation is theater.** `taste_judge.py` scores "specificity" as *contains "ats" or a digit*, CTA as *contains "try"/"use"*, Spanish as *an accent mark or two signal words*. It passes mediocre copy and can flag good copy. Only the banned-phrase and risky-claim checks have real teeth.
2. **The learning loop is manual.** Pattern re-ranking on performance events is the system's entire long-term edge, and it currently depends on the operator remembering to paste metrics back. If that habit lapses, memory decays into a static prompt library.
3. **The ten agents are labels.** `agents.json` provides routing tags and framing, not distinct judgment passes. One brain, ten hats.
4. **Triplication.** `wmi_bridge.py` and `SKILL.md` exist in three copies (root `scripts/`, `.claude/skills/`, `integrations/` Codex plugin). They will drift.
5. **Housekeeping.** Git "dubious ownership" (repo created under the `CodexSandboxOffline` user), stray `.pnpm-store/` and `.pytest_cache/`, and the whole repo — including `.wmi/memory.db`, a live SQLite file — sits inside a OneDrive-synced folder.

"Next level" means: **close the performance loop automatically, make validation real, and run the system on a weekly operating cadence — before adding any new engines or asset types.**

---

## Workstream 0 — Hygiene (half a day, do first)

- Fix git ownership: `git config --global --add safe.directory <this repo>` or re-own the directory under the primary user.
- Add `.pnpm-store/`, `.pytest_cache/`, `__pycache__/` to `.gitignore`; delete the stray stores.
- **Get `memory.db` out of OneDrive sync.** A live SQLite file under OneDrive is a corruption/conflict risk (sync grabbing the file mid-write, `-wal`/`-shm` files syncing separately). Either move the whole repo out of OneDrive, or relocate `.wmi/` to e.g. `%LOCALAPPDATA%\wmi\` via `paths.py` and leave a pointer.
- Kill the triplication: make root `scripts/wmi_bridge.py` and `.claude/skills/.../SKILL.md` the single sources; make `integrations/` (Codex plugin) a generated copy via a tiny `sync_integrations.py`, or delete it if Codex is no longer used. Add a test that asserts the copies are identical so drift fails CI.

**Acceptance:** `git status` works as the normal user; one canonical bridge/skill; memory.db lives outside synced storage.

## Workstream 1 — Make validation real (two-tier judge)

Replace the pretend score with a two-tier design:

**Tier 1 — deterministic hard gates (keep, in Python).** Banned phrases (`anti-slop.md`), risky/absolute ATS claims, language mismatch, source-fidelity floor, required format fields per asset type. These are cheap, testable, and genuinely protective. They return **pass/fail with reasons**, not a 0–10 score.

**Tier 2 — Claude-as-judge (new).** `wmi_bridge.py validate` stops emitting a fake numeric score and instead compiles a **judge packet**: the draft, the task, the relevant `brand/*.md` excerpts, and a rubric with 3 axes — taste (premium/specific/restrained), fidelity (topic + source preserved), and channel fit. The skill workflow then has Claude score the draft against that packet *as a separate pass*, citing the exact sentences that justify each deduction. Repair targets the citations.

- Demote `taste_judge.py` to Tier 1 only; delete the specificity/CTA/word-count heuristics or keep them as advisory warnings, never as score.
- Add **golden fixtures**: `tests/fixtures/` with known-good and known-bad drafts per asset type; unit-test that Tier 1 gates catch the bad ones and pass the good ones. This is the regression net the current regex tests can't provide.

**Acceptance:** validate output contains hard-gate results + a judge packet; no numeric score produced by regex; golden fixtures in CI.

## Workstream 2 — Close the learning loop automatically (the compounding move)

This is the highest-leverage workstream. The goal: **>80% of published assets get a linked performance event without manual pasting.**

1. **Asset registry discipline.** Every asset that leaves WMI gets: an asset ID (already exists), the channel, the publish URL, and a tracked link with `utm_source/medium/campaign` and the **asset ID in `utm_content`**. The bridge should print the ready-made UTM link at handoff time so there is zero friction.
2. **Metricool ingestion.** Metricool is already connected as an MCP in Claude. Add a bridge command `wmi_bridge.py record-performance --asset-id <id> --json <metrics>` (structured path alongside the existing natural-language parser). The weekly workflow (WS3) has Claude pull per-post metrics via Metricool MCP, match posts to asset IDs (by URL/date/first-line hash), and write events through the bridge. Python stores and re-ranks; Claude only ferries data.
3. **Search Console for SEO assets.** The growth plan already mandates GSC setup. Once live, a weekly export (CSV drop into `production/gsc/` or API later) feeds clicks/queries per SEO page into performance events for the SEO briefs that produced them.
4. **Revenue attribution.** The cv-tailored `Google-SEO` branch already adds a marketing-conversions migration and `src/lib/analytics/`. Once merged, signups/checkouts carry UTM attribution in Supabase. A weekly query (manual paste at first, Supabase MCP later) links conversions back to asset IDs — closing the loop all the way to Polar revenue, which is exactly the outcome-over-reach ranking the README promises.

**Acceptance:** one real asset goes publish → Metricool metrics → `performance_events` row → pattern promoted, with no hand-typed metrics.

## Workstream 3 — Weekly operating cadence (run it like a company)

The simulation becomes a company when it has a rhythm, not more staff. One markdown playbook, `OPERATIONS.md`, defining a three-touch week:

- **Monday — pipeline.** Compile a digest: last week's performance events, GSC movers, pattern promotions, and the growth-plan backlog. Output: this week's asset list (3–5 items) with briefs staged.
- **Midweek — production batch.** Run the create→critique→repair→judge loop per asset; stage handoffs to the capability workspaces; schedule approved social posts via Metricool MCP (`createScheduledPost`) — **human approval stays mandatory** before anything external.
- **Friday — retro.** Run WS2 ingestion, promote/demote patterns, write a five-line dated entry to `production/reviews/`. Decide next week's single focus.

Optionally automate the Monday/Friday compile steps as a Claude Code scheduled routine later; start manual to prove the shape.

**Acceptance:** three consecutive weeks executed; retro entries exist; the Monday digest is generated from memory.db data, not memory.

## Workstream 4 — Real judgment passes (not personas)

Don't build ten subagents. Convert the three roles that represent *distinct cognitive stances* into explicit sequential passes inside the skill workflow:

1. **Create** — specialist framing from `agents.json` (as today).
2. **Contrarian pass** — a dedicated critique step with its own instructions ("attack generic claims, weak differentiation, fake proof, derivative ideas") that must produce at least one concrete objection or explicitly concede.
3. **Judge pass** — the WS1 rubric scoring.

Keep the other seven agents as compiled framing. Only reach for actual Claude Code subagents (`.claude/agents/`) if quality plateaus with in-context passes — subagents cost context and cold starts, and the evidence so far doesn't justify them.

**Acceptance:** SKILL.md workflow shows the three passes; a test fixture demonstrates a draft changed by the contrarian pass.

## Workstream 5 — Industrialize the SEO factory (execute, don't re-plan)

The growth plan is the strategy; WMI's job is throughput with quality gates:

- Exercise the `nextjs-website-seo-implementation` capability end-to-end **once**: one role/market page brief staged into `cv-tailored/plans/wmi/`, implemented, verified (`lint/test/build`), shipped. Fix whatever friction appears in the adapter.
- Then batch: the growth plan's free-tool pages and role pages become a brief queue in memory.db, ordered by GSC query data as it arrives (WS2.3).
- Maintain an internal-linking map as a memory artifact so every new page strengthens the cluster instead of standing alone.

**Acceptance:** first WMI-briefed page live in production; queue of next 10 briefs ranked by search evidence.

---

## Sequencing

| When | What |
|---|---|
| Week 1 | WS0 hygiene; WS1 two-tier validation + golden fixtures |
| Weeks 2–3 | WS2 asset registry + Metricool ingestion; WS4 passes wired into SKILL.md |
| Week 4 | WS3 first full operating week (Mon/mid/Fri); WS5 first end-to-end SEO page |
| Weeks 5–12 | Cadence runs; SEO queue executes; GSC + conversion attribution come online as the cv-tailored branch ships |

## KPIs (review monthly)

- % of published assets with a linked performance event (target **>80%**; today ~0% automated)
- Measured-winner patterns in the library (patterns with outcome-linked events, not reach)
- Weekly organic clicks (GSC) — growth-plan base case: 3,000/mo by day 90
- Signups/conversions attributed to WMI assets via UTM
- Assets published per week (throughput floor: 3)

## What NOT to do

- **No new engines or asset types** until the performance loop closes — breadth without feedback is how the library fills with unmeasured guesses.
- **No dashboard/UI.** Markdown digests from memory.db are enough for one operator.
- **No auto-publishing.** Metricool scheduling always behind explicit human approval; the production-boundary rule stands.
- **Don't improve the regex judge.** Its scoring role is being removed, not refined.

## Risks

- **Habit risk (until WS2 lands):** the loop still depends on the operator for 2–3 weeks. Mitigate by doing WS2 early and making the UTM link zero-friction.
- **Metricool coverage:** metric granularity varies by network; verify LinkedIn/Instagram fields before promising per-asset saves/clicks. Fall back to natural-language paste where the API is thin.
- **OneDrive + SQLite:** unresolved until WS0 lands; treat any memory.db anomaly before then as suspect sync, not code.
- **Attribution lag:** GSC and the conversions migration depend on cv-tailored's branch shipping; don't let WS5 batching start before at least directional query data exists.
