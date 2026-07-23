---
name: advanced-prompt-upgrader
description: >
  Diagnoses any raw or underperforming prompt, selects the right architecture and techniques
  for the task, and returns 2–4 production-ready upgraded variants — copy-paste ready for
  chat, Claude Code, API, agents, or RAG systems. Use when the user shares a draft prompt
  and wants a significantly stronger, more reliable version. Also use when the user says
  "make this prompt better", "upgrade this", "this isn't working", or pastes a prompt and
  asks for help.
metadata:
  author: kenneth-valverde
  version: 2.1
  domain: prompt-engineering
  tags: [prompt-engineering, context-engineering, workflow-design, prompt-optimization]
---

## What This Skill Does

Takes any weak, vague, or inconsistent prompt and upgrades it into production-ready
variants using techniques selected specifically for the task — not randomly stacked.

The process is diagnosis-first: understand what the prompt is actually trying to do,
find its failure modes, pick the right architecture, apply only the techniques that earn
their place, then verify before delivering.

Output is always copy-paste ready. No advice about prompts — actual prompts.

---

## When to Use This Skill

- User pastes a prompt and says it's weak, generic, or not working
- User wants a prompt "100x better" or "production ready"
- User needs a system prompt, agent prompt, or workflow prompt upgraded
- User has a rough idea they want turned into a structured, reliable prompt
- User wants variants for different environments (chat, API, Claude Code, RAG)

---

## Inputs Required

Collect or infer before rewriting:

1. **Raw prompt** — exact original or rough draft
2. **Primary goal** — what success looks like in plain language
3. **Task type** — writing, code, strategy, research, design, extraction, agent workflow
4. **Target environment** — Claude chat, Claude Code, API, RAG system, multi-agent
5. **Output type** — paragraph, JSON, markdown, HTML, plan, code, table
6. **Hard constraints** — things that must never change (language, tone, length, schema)
7. **Available context** — files, examples, docs, style guides, prior outputs, tools

If inputs 1–3 are missing, ask before proceeding. One message, all gaps.

---

## Step-by-Step Workflow

1. **Ingest and classify** — read the raw prompt; identify task category and real objective
2. **Diagnose failure modes** — load `references/diagnosis-framework.md` and identify what's broken
3. **Select architecture** — load `references/architecture-guide.md`; choose single, chain, RAG, or agent
4. **Load techniques** — load `references/techniques-library.md`; select only what fits this task
5. **Load 2026 principles** — load `references/2026-principles.md`; apply before writing
6. **Apply the 6-core stack** — Role · Goal · Context · Format · Examples · Constraints
7. **Write 2–4 variants**:
   - **v1** — Production single-shot (recommended for most cases; always include this)
   - **v2** — Multi-step workflow version (include when task has stages)
   - **v3** — RAG / tools / agent version (include only if environment supports it)
   - **v4** — Minimal high-signal version (include when user wants fast iteration)
8. **Run verification pass** — check against quality checklist below
9. **Deliver** — labeled code blocks, brief note on which variant to use and why

---

## Output Format

```markdown
## What Was Wrong With the Original
[2–4 bullets naming the specific failure modes — no vague praise or criticism]

---

## Prompt v1 — Production Single-Shot
[full prompt, copy-paste ready]

---

## Prompt v2 — Multi-Step Workflow
[full prompt]

---

## Prompt v3 — RAG / Tools Version  ← skip if not applicable
[full prompt]

---

## Prompt v4 — Minimal High-Signal  ← skip if not needed
[full prompt]

---

## Which Variant to Use
[1–2 sentences: when to use each, based on the user's environment]
```

Always start with the "What Was Wrong" section. It shows the upgrade is intentional, not arbitrary.

---

## Quality Checklist

Before delivering any variant, verify:

- [ ] Original intent is preserved — the goal didn't shift during rewriting
- [ ] Six core elements present where relevant (Role, Goal, Context, Format, Examples, Constraints)
- [ ] Techniques match the task — not randomly stacked to look thorough
- [ ] Hard constraints from the original are explicit and testable
- [ ] At least one verification step included (self-critique, reflection, checklist, red-team)
- [ ] Complex tasks decomposed into stages or separate variants
- [ ] Retrieval/tool instructions are operationally clear if environment supports them
- [ ] No unresolved placeholders (`[INSERT X]` that the user needs to fill before using)
- [ ] Prompt Inversion avoided — over-instruction removed from advanced-model variants

---

## Rules

1. Never rewrite without diagnosing the real failure modes first — the fix follows the diagnosis
2. Never add techniques that don't earn their place for this specific task
3. Never drop hard constraints from the original prompt
4. Prefer better context and decomposition over clever wording
5. If the task has clear stages, propose a chain instead of one giant prompt
6. Keep all variants copy-paste ready
7. Separate system instructions from task-specific user input when it improves consistency
8. On advanced models (Opus, GPT-4o): shorter and cleaner beats longer and over-structured
