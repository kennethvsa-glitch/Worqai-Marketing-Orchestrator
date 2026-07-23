---
date: 2026-07-09
workspace: C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence
verdict: DRIFT
findings: 6
ships: yes
status: fixed-in-this-pass
---

# What this workspace actually is

WorqAI Marketing Intelligence is now a prompt-routed Python marketing runtime.
It can create briefs, audit scripts, reframe social posts, generate fast replies,
build SEO plans, assemble campaign packages, create deep research plans, define
feedback loops, and prepare Motion Studio handoffs. The largest remaining
boundary is external execution: writing real website pages or Motion Studio
scene files still requires explicit approval for those workspaces.

# What is working - do not touch

- The `run` prompt dispatcher is the right activation surface.
- The Markdown/JSON/Python split is still compact and Quantum-like.
- Lightweight reply/social engines should stay before the full orchestrator.
- SQLite memory is the correct place for benchmark and performance history.

# Findings

## F1 - Simple replies loaded too much machinery - WASTES - REWRITE

**Evidence**: Fast reply routing now happens at
`src/worqai_marketing_intel/prompt_runtime.py:41`, before the full orchestrator
is created. The reply renderer is at `src/worqai_marketing_intel/cli.py:300`.
**Cost**: A tiny reply prompt could feel slow and route through generic brief
generation.
**Falsifier checked**: A pre-orchestrator fast path would disprove this. It now
exists and smoke-tested as `message_reply`.
**Fix**: Added `message_reply_engine.py` and lazy-loaded the orchestrator only
for heavy workflows.

## F2 - SEO was advice, not an engine - BREAKS - ADD

**Evidence**: SEO routing is now at
`src/worqai_marketing_intel/prompt_runtime.py:93`, and the engine starts at
`src/worqai_marketing_intel/seo_engine.py:45`. Docs list it at `README.md:193`.
**Cost**: WMI could talk about ranking for `cv con ia`, but could not output a
repeatable SEO page map.
**Falsifier checked**: A callable SEO plan with keyword pages, metadata, schema,
internal links, and 90-day plan would disprove this. It now exists.
**Fix**: Added the SEO engine and route support for `seo_page`.

## F3 - No single campaign package existed - MISLEADS - ADD

**Evidence**: Campaign package routing is at
`src/worqai_marketing_intel/prompt_runtime.py:59`, and the engine starts at
`src/worqai_marketing_intel/campaign_package_engine.py:14`.
**Cost**: The user had to ask for reels, carousel, SEO, motion, and pitch assets
one at a time, which defeated the orchestrator idea.
**Falsifier checked**: A full package containing reels, carousel, SEO, social,
motion handoff, partnership pitch, and distribution plan would disprove this.
It now exists.
**Fix**: Added campaign package engine and asset classification.

## F4 - Deep research was too shallow for competitor/SERP work - MISLEADS - ADD

**Evidence**: Deep research routing is at
`src/worqai_marketing_intel/prompt_runtime.py:83`, and the plan engine starts at
`src/worqai_marketing_intel/deep_research_engine.py:6`.
**Cost**: WMI could fetch examples, but did not define source sets, extraction
fields, or pattern outputs for serious research.
**Falsifier checked**: A deterministic source-set and extraction-plan output
would disprove this. It now exists.
**Fix**: Added the deep research engine for SERP, social, ad, and landing-page
pattern extraction.

## F5 - Feedback loop had no storage support - BREAKS - ADD

**Evidence**: `PerformanceEvent` is defined at
`src/worqai_marketing_intel/models.py:133`; `performance_events` storage is
created at `src/worqai_marketing_intel/memory_store.py:313`; tests start at
`tests/test_orchestrator.py:286`.
**Cost**: WMI could not remember which assets actually performed, so it could
not improve from reality.
**Falsifier checked**: SQLite-backed event storage would disprove this. It now
exists.
**Fix**: Added performance event storage and feedback-loop engine output.

## F6 - SQLite connections stayed open on Windows - BREAKS - REWRITE

**Evidence**: `_connect` now closes connections at
`src/worqai_marketing_intel/memory_store.py:261`.
**Cost**: Temporary databases could stay locked and fail cleanup on Windows.
**Falsifier checked**: A smoke test using `TemporaryDirectory` and performance
events would disprove this. It now passes.
**Fix**: Replaced raw sqlite connection context use with a closing context
manager.

# What was considered and rejected

- Direct writes into `worqai-launch` and `motion-studio` were rejected because
  those external workspaces require explicit approval.
- Full live SERP scraping was rejected because network access is restricted in
  this runtime; the engine now produces source sets and extraction rules.
- Installing pytest was rejected because the bundled runtime does not include
  it and adding dependencies was not necessary for this pass.

# Escalation path

When WMI has 25 stored performance events, add a calibration command that ranks
hook patterns by channel and adjusts future output scoring.
