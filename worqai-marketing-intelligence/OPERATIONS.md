# WMI Weekly Operating Cadence

**Status:** active playbook (introduced 2026-07-13)
**Audience:** the operator running WMI through Claude, plus Claude itself.

WMI becomes a marketing *operation* when it runs on a rhythm, not when it grows
more engines. This is a three-touch week. Every external action (posting,
writing into another workspace) stays behind explicit human approval — the
cadence never removes a gate, it just makes the loop turn.

The whole point is the **performance loop**: published assets earn metrics,
metrics re-rank patterns, better patterns produce the next assets. Nothing here
matters if performance data never comes back, so Friday is the load-bearing day.

---

## Monday — Pipeline (compile the week)

Ask Claude, in ordinary language:

> "Give me this week's WMI pipeline: what performed last week, what patterns got
> promoted, and the next 3–5 assets to make."

Under the hood this reads from memory, not from memory-of-conversation:

- Recent performance events: `wmi history` and the `performance_events` table
  (via `MemoryStore.list_performance_events`).
- Promoted patterns: `MemoryStore.rank_benchmark_examples` — examples whose IDs
  have linked outcome events, outcomes weighted above reach.
- The SEO backlog from `production/2026-07-13/worqai-seo-growth-plan.md`.

**Output:** 3–5 assets for the week, each with a one-line brief and channel.
Throughput floor is 3. Stage briefs now so midweek is production, not deciding.

## Midweek — Production batch (make and stage)

For each asset, run the full skill loop (see `SKILL.md`): compile context →
create → contrarian pass → judge pass → repair blocked gates → revalidate.

- Stage handoffs to the capability workspaces (`config/workspace-capabilities.json`).
  A route is not approval; state the target and intended writes and wait for a yes.
- For anything that will be published, generate the tracked link up front:

  ```text
  python scripts/wmi_bridge.py utm --asset-id <id> --url <public-url> \
    --source <network> --medium <social|email|referral> --campaign <name>
  ```

  The asset ID rides in `utm_content`, which is what lets Friday match clicks and
  signups back to the exact asset.
- Scheduling social posts (e.g. via the Metricool connector) is fine to *prepare*,
  but publishing waits for explicit approval.

## Friday — Retro (close the loop)

This is the day that compounds. For every asset published this week:

1. Pull its metrics (Metricool for social, Search Console for SEO pages, product
   analytics for signups) and record them against the asset ID:

   ```text
   python scripts/wmi_bridge.py record-performance --asset-id <id> \
     --asset-type <type> --channel <channel> --metrics-json '{"saves": 42, "signups": 8}'
   # or, from a natural-language note:
   python scripts/wmi_bridge.py record-performance --asset-id <id> \
     --asset-type <type> --channel <channel> --text "42 guardados y 8 registros"
   ```

2. For assets worth learning from, save the winning pattern as a benchmark
   example **using the same ID** (`wmi remember-example`) so ranking can promote
   it. A performance event only influences future work once it is tied to a saved
   example of that ID.
3. Write a five-line dated retro to `production/reviews/YYYY-MM-DD.md`: what
   shipped, what moved, what got promoted/retired, and next week's single focus.

**KPI to watch:** share of published assets that end the week with a linked
performance event. Target > 80%. If it slips, the loop is open and the pattern
library is filling with unmeasured guesses.

---

## What stays manual on purpose

- Publishing to any external channel.
- Writing into another workspace or invoking its production skill.
- Promoting a pattern as a "measured winner" — it must have a real, linked event.

## When to automate

Only after three weeks have actually run this way. Then the Monday compile and
Friday ingestion are the first candidates for a scheduled routine; production and
approval stay human. Don't automate a cadence you haven't proven by hand.
