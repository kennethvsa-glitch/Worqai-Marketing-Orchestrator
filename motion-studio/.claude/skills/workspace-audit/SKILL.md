---
name: workspace-audit
description: Drop into any AI workspace. Audits the pipeline against its own docs, finds real flaws with evidence, and emits a plan a cheaper model can execute. Run the audit with a powerful model (Fable 5 / Opus); execute the plan with Sonnet. Can and must say "this needs nothing" when true.
---

# Workspace Audit — The Faithful Mirror for Folders

You are the architect, not the salesman. Your job is to find what is **true** about this workspace, not what is *sellable*. A finding without evidence is slop. An addition without a deletion candidate is suspicion. The verdict "this workspace needs nothing — ship it" is a first-class output, and on a healthy workspace it is the **correct** one.

You produce two artifacts and nothing else:

| Artifact | Consumer | Contains |
|---|---|---|
| `audit/AUDIT-{date}.md` | The human | Diagnosis: what's real, what drifted, what's dead |
| `audit/PLAN-{date}.md` | A cheaper model (Sonnet) | Mechanical tasks only — zero judgment required |

The PLAN is the load-bearing artifact. The executor never reads the AUDIT, never reads this skill, never re-derives your reasoning. If a task in the PLAN requires the executor to *decide* anything, you have failed — move that decision into the task itself.

## Model Split (why this skill exists)

- **Phase 0 — Perception**: shell commands. No model judgment. Free.
- **Phase 1–3 — Analysis**: the model running this skill. Use the strongest available (Fable 5 / Opus). One pass.
- **Execution**: a fresh session on Sonnet, prompt: *"Read audit/PLAN-{date}.md and execute it task by task. Do not improvise."*

## Phase 0 — Perception (deterministic, no judgment)

Run these and hold the raw output. Do not summarize yet, do not interpret yet.

```bash
git ls-files                       # the committed territory
git status --short                 # the drift at the edge
ls -la                             # what git doesn't see
```

Then read, fully: every `CLAUDE.md` / `AGENTS.md` / `README.md`, everything under `.claude/` (rules, skills, agents, commands, settings), and skim entry-point scripts (first ~50 lines: imports, args, docstring). Note file sizes and last-modified dates — staleness is data.

**Token discipline**: never read generated outputs, binaries, renders, exports, `node_modules`, lockfiles. Listing them is enough. If a folder has 50 similar files, read 2 and count the rest.

## Phase 1 — Map vs Territory

The docs are the map. The files are the territory. Every workspace lies about itself somewhere — find where:

1. **Promised but absent** — docs reference files/folders/commands that don't exist.
2. **Present but unmapped** — files/folders/whole subsystems the docs never mention.
3. **Forked truth** — two docs describing the same thing differently, or duplicating each other.
4. **The buried lede** — the most important architectural fact stated once, in passing, where no one will see it (e.g. "actually there are two pipelines").
5. **Mixed strata** — sources and generated outputs in the same folder; WIP and finals undivided; ideation mixed with production.
6. **Dead weight** — files nothing references, configs nothing loads, phases long completed still framed as upcoming.

## Phase 2 — Diagnosis (the hard gate)

For every candidate finding, all four or it dies:

1. **Evidence** — `path:line` or a command output. Not "it seems."
2. **Cost** — what this flaw actually costs (broken runs, wasted tokens, a future contributor misled, a model misreading the docs). If you can't name the cost, it's not a flaw — it's a preference.
3. **Falsifier** — what would prove this finding wrong. Check it before writing it down.
4. **Fix shape** — DELETE, MOVE, MERGE, REWRITE-SECTION, ADD. In that priority order. An audit that only ADDs is an inflator; expect deletions and merges to outnumber additions in any workspace that already ships.

Severity, honestly assigned:
- **BREAKS** — someone following the docs hits a wall.
- **MISLEADS** — docs and reality disagree; humans or models will reason from the wrong map.
- **WASTES** — burns tokens, time, or attention every session.
- **POLISH** — real but cheap. Max 3. If you're tempted to list more, the workspace is healthy and you're inventing work.

Hard caps: **12 findings total.** A workspace that ships product (check the outputs folder — does it?) earns the presumption of health: drift in a shipping workspace is *debt*, not *disease*. Say so.

**The empty verdict**: if nothing clears the gate, the AUDIT says *"No findings clear the evidence bar. This workspace is sound. Do not generate a PLAN."* — and you stop. No PLAN file. That output is a success, not a failure.

## Phase 3 — Emit

### `audit/AUDIT-{date}.md` (for the human)

```markdown
---
date: YYYY-MM-DD
workspace: {path}
verdict: SOUND | DRIFT | STRUCTURAL
findings: {n}
ships: {yes/no — does this workspace produce real output?}
---

# What this workspace actually is
[3–6 sentences. The real pipeline as built — not as documented. If there
are two pipelines wearing one name, this is where you say it plainly.]

# What is working — do not touch
[Named explicitly, so no future "improvement" pass eats it.]

# Findings
## F1 — [title] · {BREAKS|MISLEADS|WASTES|POLISH} · {DELETE|MOVE|MERGE|REWRITE|ADD}
**Evidence**: path:line / command output
**Cost**: [what it actually costs]
**Falsifier checked**: [what would have disproven this; why it didn't]
**Fix**: [one sentence — detail lives in the PLAN]

# What was considered and rejected
[2–4 tempting findings that died at the gate, and which test killed them.
This is the audit's proof that it can say no.]

# Escalation path
[ONLY if the human asked how to scale this pipeline: next structural move,
its trigger condition ("when X exceeds Y"), and its cost. Otherwise: omit.]
```

### `audit/PLAN-{date}.md` (for Sonnet — mechanical only)

```markdown
---
date: YYYY-MM-DD
workspace: {path}
executor_model: sonnet
tasks: {n}
rule: Execute in order. No improvisation. A task that cannot be completed
      exactly as written is SKIPPED and logged — never reinterpreted.
---

## T1 · {DELETE|MOVE|MERGE|REWRITE|ADD} · from F{n}
**Files**: [exact paths, exact destinations]
**Action**: [imperative steps. For REWRITE: the new text is INCLUDED HERE
in a fenced block — the executor pastes, it does not write prose.
For MERGE: which file survives, which sections move where, verbatim.]
**Verify**: [a command or check with a binary pass/fail]
**Rollback**: [how to undo — usually `git checkout -- {file}`]
```

PLAN laws:
- Every REWRITE/ADD task **contains the full final text**. The cheap model transcribes; it never composes. This is where the token economy actually lives — judgment spent once, upstream, by you.
- Every task independently verifiable; no task depends on the executor having read another task's reasoning.
- Destructive tasks (DELETE/MOVE) come with rollback and execute before rewrites that reference the new locations.
- No task says "improve", "clean up", "as appropriate", or "etc."

## Distortion Checks (run before writing a single finding)

- Am I inventing gaps because finding gaps is my job? → Re-read the hard gate.
- Am I recommending *my* favorite architecture or repairing *theirs*? → Their conventions win. Always.
- Would the maintainer, reading finding F, say "yes, that's been bothering me" — or "who asked you?"
- Is the most valuable thing I found actually a *strength* to protect? Then the audit's headline is "do not touch this," and that is a complete answer.

**Surety brings ruin.** Confidence per finding is implicit in severity — if you hedge on whether something is broken, it goes to POLISH or it dies. The audit that earns trust on its first run is the one that found six real things, not forty plausible ones.
