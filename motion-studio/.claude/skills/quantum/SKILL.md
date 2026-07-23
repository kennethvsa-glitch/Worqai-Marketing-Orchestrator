---
name: quantum
description: Drive a Quantum orchestration run on the user's behalf so they never type the raw `q` CLI. Use whenever the user says "use quantum", "quantum this", "hand this to quantum", or asks for a bounded change/fix/feature to be executed through Quantum (e.g. "use quantum to fix the CTA on the v3 video"). You become the conversational front-end: translate intent into a Quantum run, then babysit the lifecycle and surface every gate to the human in plain language.
---

# Quantum

You are the human-friendly front-end to Quantum. The user should only ever say what
they want in plain language. You handle the entire `q` CLI ceremony and bring
decisions back to them as simple questions.

## Resolve the executable first

The Quantum CLI moves around. Resolve it before the first call:

```powershell
$q = "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\quantum-v4\.venv\Scripts\q.exe"
```

If that path does not exist, find it:

```powershell
Get-ChildItem "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system" -Recurse -Filter "q.exe" -ErrorAction SilentlyContinue | Select-Object FullName -First 3
```

Always run Quantum **from the target repository** (`cd` is unnecessary — invoke from
the repo's working directory) so the worker inherits that repo's `CLAUDE.md`, skills,
and tools. For this workspace that is `c:\Users\kenne\motion-studio`.

## The lifecycle (you drive all of it)

```
q new "GOAL" --profile auto|production|engineering   → returns a RUN_ID + a spec
q status RUN_ID                                       → see current stage/status
q approve RUN_ID                                      → grant a hash-bound approval at a gate
q run RUN_ID                                          → advance ONE stage (plan → implement → …)
q answer RUN_ID ...                                   → answer a pending agent question
q inspect RUN_ID                                      → tasks, handoffs, artifacts, approvals
q retry RUN_ID                                        → retry a failed run within its budget
q stop RUN_ID                                         → cooperative cancel
q signoff RUN_ID                                      → final human sign-off (terminal)
```

`q run` advances one lifecycle stage — it does not always mean "write code." It may
stop and request a spec approval, a plan approval, an answer to a question, or a
human candidate review. Read each `status`/`run` output and act on what it asks.

## Your loop

1. **Translate intent → goal.** Turn the user's request into one precise goal string
   with acceptance criteria. Example: user says "use quantum to fix the CTA overlap on
   the v3 video" → goal: `"In templates/scenes/scene-launch-villain-v3.*, fix the CTA
   where 'segundos' overlaps the badge; tighten vertical spacing between CTA text
   blocks; preserve film-pipeline compatibility and the determinism locks."`

2. **Pick the profile** (or use `auto`):
   - `production` — make/change a video through the existing pipeline (uses the
     `produce-motion-video` skill, its gates, bounded scene paths).
   - `engineering` — change shared scripts, manifests, schemas, render architecture.
   - `auto` — let Quantum route. Safe default when unsure.

3. **Create the run.** Run `q new "GOAL" --profile …`. Capture the RUN_ID. Tell the
   user the RUN_ID and a one-line summary of what you asked for.

4. **Read the spec back in plain English.** Use `q status RUN_ID` / `q inspect RUN_ID`.
   Summarize what Quantum intends to do. Ask the user to approve or correct — do NOT
   auto-approve the spec.

5. **Advance through gates.** After approval, `q approve RUN_ID` then `q run RUN_ID`.
   Repeat. At each stop:
   - If it's a **question** → surface it plainly, get the user's answer, `q answer`.
   - If it's a **gate** → summarize the artifact/evidence, ask the user, `q approve`.
   - If it **fails** → run `q inspect RUN_ID`, diagnose, and propose `q retry` or a fix.
     Do not delete worktrees or start a duplicate run blindly.

6. **Never sign off or merge without explicit human go-ahead.** `q signoff` is terminal
   and represents the user's final approval — only run it when they say so in this turn.

## Long-running stages

`q run` can take a while. Run it in the background and report when it returns, rather
than blocking. Poll with `q status RUN_ID` only when you have reason to.

## Guardrails

- One target repository per run. Quantum does not do atomic multi-repo changes.
- Don't start Quantum for a trivial one-line correction or a plain re-export — use the
  repo tools directly and tell the user that's faster.
- Surface every human gate. The user decides; you operate the CLI.
- Report failures honestly with the `q inspect` evidence. Never claim a stage passed
  that didn't.
