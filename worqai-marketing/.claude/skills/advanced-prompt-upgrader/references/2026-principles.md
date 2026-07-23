# 2026 Prompting Principles

Load in Step 5 of the advanced-prompt-upgrader workflow.
Apply these as a final filter before writing variants.

---

## The Core Shift

Prompt engineering used to be about finding the magic phrase. Now it's about:

**Context > Wording.** What you give the model to work with matters more than how you
phrase the instruction. A mediocre instruction with rich, relevant context beats a
beautifully crafted instruction with none.

**Workflow > Mega-prompt.** Breaking a task into focused stages produces better output
than stuffing everything into one prompt. Each stage can be evaluated and redirected.

**Constraints > Encouragement.** Telling the model what it cannot do narrows the solution
space into quality. Telling it to "be creative" or "be thorough" does almost nothing.

**Verification > Trust.** The model that checks its own output before delivering it
produces better final results than the model that outputs and moves on.

---

## What Consistently Works in 2026

| Technique | Why It Works |
|---|---|
| Specific context | Removes ambiguity — the model can't fill gaps with generics |
| System / user separation | Persistent rules stay salient; task input stays clean |
| 2–5 concrete examples | Pattern transfer is more reliable than description |
| Testable constraints | Binary pass/fail forces precision ("≤80 words" not "concise") |
| Self-critique steps | Models catch their own drift when given criteria to check against |
| Chain decomposition | Each stage gets focused attention without cross-contamination |
| Negative prompting | Avoidance is faster and more reliable than positive specification |
| Step-back before answering | Principle-first reasoning outperforms immediate pattern-match |

---

## What's Getting Weaker

### "Act as an expert with 20 years of experience"
Why it underperforms: The model's knowledge doesn't expand with the claim. A specific
role framing (domain + specialization + priorities) does more work than seniority language.

### "Think step by step" on reasoning models
Why it underperforms: Claude with extended thinking, o3, and similar reasoning models do
this automatically. Adding the instruction is redundant and adds latency without benefit.

### More than 5 few-shot examples
Why it underperforms: Few-shot collapse is documented across multiple models. At 8+ examples,
Gemini Flash dropped from 64% to 33% accuracy on a benchmark. More examples can override
the task instruction.

### Mega-prompts on top-tier models
Why it underperforms: Prompting Inversion — on GPT-5, Claude Opus, and similar advanced
models, excessive instruction can actually degrade reasoning quality. The model burns
capacity parsing your structure instead of thinking about your problem.

### Emotional appeals ("please", "I'll tip you")
Why it underperforms: No consistent effect confirmed across modern models in controlled
research settings (Wharton, 2025). Don't bother.

---

## The Model Tier Rule

The more capable the model, the cleaner and more direct your prompt should be.

| Model Tier | Prompting Style |
|---|---|
| Haiku / Flash / smaller models | More explicit instruction, more examples, more hand-holding |
| Sonnet / GPT-4o-mini tier | Balanced — role + constraints + clear format |
| Opus / GPT-4o / top-tier | Shorter, cleaner, trust the model — add context not rules |

If you're prompting Claude Opus and your prompt is 800+ words of rules, you've likely
over-instructed. Cut 30–40% and trust the model to fill the gaps correctly.

---

## The Practical Stack (Ranked by Impact)

For most tasks, this order of investment produces the best returns:

1. **Role + specific context** — who is answering and what do they know
2. **Constraints (what not to do)** — narrow the solution space
3. **Format specification** — exact shape of the output
4. **2–3 examples** — pattern transfer
5. **Decomposition** — stages if the task is multi-phase
6. **Verification step** — self-audit before delivering
7. **Chain of thought** — only if model won't reason well without it
8. **Retrieval grounding** — only if training knowledge isn't reliable enough

Context engineering and workflow design first. Clever wording last.
