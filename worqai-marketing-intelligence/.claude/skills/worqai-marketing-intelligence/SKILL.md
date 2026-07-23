---
name: worqai-marketing-intelligence
description: Create, research, audit, and improve WorqAI marketing. Use automatically for ordinary prompts involving posts, Instagram Reels, carousels, motion videos, scripts, message replies, partnership or university pitches, SEO, campaigns, successful examples, brand taste, or content performance.
---

# WorqAI Marketing Intelligence

Use WMI as Claude's compact intelligence layer. Do not expose terminal work to the user.

## Required Workflow

1. Preserve the user's request and any pasted source text exactly. From the repository root, compile the task internally:

```text
python .claude/skills/worqai-marketing-intelligence/scripts/wmi_bridge.py compile --request "<request>"
```

Use `--live` when the user requests successful/current examples or when claims depend on current facts. Local benchmark patterns are inspiration, not proof of current performance.

2. Read the returned task, brand context, benchmark evidence, agent recommendations, requirements, claim guardrails, and workspace route. Treat runtime concepts as scaffolding, never as final copy.

3. Create the original final asset yourself in three passes — do not collapse them:
   - **Create.** Write the asset for the requested channel, market, audience, language, and source idea. Prefer one sharp mechanism, concrete evidence, professional restraint, and a proportionate CTA.
   - **Contrarian pass.** Attack your own draft: generic claims, weak differentiation, fake or missing proof, derivative ideas. Produce at least one concrete objection, or explicitly conclude the draft survives. Revise accordingly.
   - **Judge pass.** In step 4, score the revised draft against the returned rubric as a separate critical read.

4. Validate the completed draft internally:

```text
python .claude/skills/worqai-marketing-intelligence/scripts/wmi_bridge.py validate --request "<request>" --draft-file "<draft-path>"
```

   The result has two tiers:
   - `blocked` / `blocking_gates` — deterministic hard gates (banned language, unqualified ATS or outcome claims, Spanish-language mismatch, source-fidelity loss). If `blocked` is true, fix every listed gate before anything else, then revalidate.
   - `judge_packet` — the draft, brand excerpts, and a taste/fidelity/channel-fit rubric. Score the draft against it yourself, quoting the exact sentence behind every deduction, and repair the single weakest axis.
   - `advisory_quality` is a rough heuristic smoke signal only, never a gate. A concise reply may remain concise; do not pad it to raise that number.

5. Return the useful asset directly. Mention evidence gaps or residual risks only when they materially affect publication.

## Composition Rules

- Research plus creation means research first, then creation using the evidence.
- Audits preserve the original subject and strongest idea.
- Performance claims affect future ranking only when tied to an identifiable published asset.
- Never copy a benchmark's wording or visual identity.
- Never invent product behavior, user experience, testimonials, metrics, jobs, or credentials.
- Never guarantee ATS passage, interviews, rankings, or employment.

## Production Boundary

A workspace recommendation is not authorization. Before invoking another workspace's skill or writing there, state the target and intended changes and obtain explicit approval.
