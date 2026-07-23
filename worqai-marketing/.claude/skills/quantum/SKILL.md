---
name: quantum
description: Drive a Quantum orchestration run on the user's behalf so they never type the raw `q` CLI. Use whenever the user says "use quantum", "quantum this", "hand this to quantum", or asks for a bounded carousel change/fix/new-carousel to be executed through Quantum (e.g. "use quantum to fix slide 3" or "use quantum to build a carousel from this brief"). You become the conversational front-end: translate intent into a Quantum run, then babysit the lifecycle and surface every gate to the human in plain language.
---

# Quantum

You are the human-friendly front-end to Quantum. The user only says what they want in
plain language. You handle the entire `q` CLI ceremony and bring decisions back as
simple questions.

## Resolve the executable first

The Quantum CLI moves around. Resolve it before the first call:

```powershell
$q = "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\quantum-v4\.venv\Scripts\q.exe"
```

If that path does not exist, find it:

```powershell
Get-ChildItem "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system" -Recurse -Filter "q.exe" -ErrorAction SilentlyContinue | Select-Object FullName -First 3
```

Always run Quantum **from this carousel repository** (`C:\Users\kenne\OneDrive\Documentos\worqai-marketing`)
so the worker inherits this repo's `CLAUDE.md`, skills, and tools.

## The lifecycle (you drive all of it)

```
q new "GOAL" --profile auto|production|engineering   → returns a RUN_ID + a spec
q status RUN_ID                                       → see current stage/status
q approve RUN_ID                                      → grant a hash-bound approval at a gate
q run RUN_ID                                          → advance ONE stage
q answer RUN_ID ...                                   → answer a pending agent question
q inspect RUN_ID                                      → tasks, handoffs, artifacts, approvals
q retry RUN_ID                                        → retry a failed run within its budget
q stop RUN_ID                                         → cooperative cancel
q signoff RUN_ID                                      → final human sign-off (terminal)
```

`q run` advances one lifecycle stage — it does not always mean "write code." It may
stop for a spec approval, plan approval, a question, or a human candidate review.

## Your loop

1. **Translate intent → goal.** Turn the request into one precise goal with acceptance
   criteria. Examples:
   - "use quantum to fix the CTA on slide 5" → `"In the slide-5 standalone HTML, fix
     the CTA per produce-carousel conventions; preserve slide dimensions, safe zones,
     editable text, and standalone rendering."`
   - "use quantum to turn this screenshot into a slide" → `"Use the reconstruct-visual
     skill (carousel mode) to rebuild REFERENCE.png as an editable standalone carousel
     slide at 1080x1350, measure-correct loop to >=92% similarity, stop for human
     approval."`

2. **Pick the profile** (or use `auto`):
   - `production` — make/revise a carousel through the existing factory (uses the
     `produce-carousel` skill, its gates, standalone slides).
   - `engineering` — change the shared builder, renderer, schemas, components, or
     architecture.
   - `auto` — let Quantum route. Safe default when unsure.

3. **Create the run.** `q new "GOAL" --profile …`. Capture and report the RUN_ID.

4. **Read the spec back in plain English.** `q status` / `q inspect`. Summarize the
   plan and ask the user to approve or correct — do NOT auto-approve the spec.

5. **Advance through gates.** `q approve` then `q run`, repeat. At each stop:
   - **Question** → surface it plainly, get the answer, `q answer`.
   - **Gate** → summarize the artifact/evidence, ask, `q approve`.
   - **Failure** → `q inspect`, diagnose, propose `q retry` or a fix. Never delete
     worktrees or start a duplicate run blindly.

6. **Never sign off or merge without explicit human go-ahead.** `q signoff` is terminal.

## Image → carousel slide

For "interpret this image as a slide" work, the goal should direct the worker to the
`reconstruct-visual` skill in carousel mode.

**Resolve the Visual Production Agent first — do not trust the path blindly** (it moves;
the sibling Quantum repo already got renamed once). Primary location:

```powershell
$visualRepo = "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\Visual-Production-Agent"
```

If `$visualRepo\skills\reconstruct-visual\SKILL.md` does not exist, find it:

```powershell
Get-ChildItem "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system" -Recurse -Filter "SKILL.md" -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -match "reconstruct-visual" } | Select-Object -First 1 -ExpandProperty FullName
```

Then derive the repo root from that (two levels up from `skills\reconstruct-visual\`)
and use its `.venv\Scripts\python.exe`.

- SKILL: `$visualRepo\skills\reconstruct-visual\SKILL.md`
- Scripts python: `$visualRepo\.venv\Scripts\python.exe`
- Carousel canvas: 1080x1350 (4:5). Render at TRUE size — never screenshot a scaled
  preview, or the similarity score is fake.

## Guardrails

- One target repository per run.
- Don't start Quantum for a one-line caption fix or a plain re-export — use repo tools
  directly and say that's faster.
- Surface every human gate. The user decides; you operate the CLI.
- Report failures honestly with `q inspect` evidence.
