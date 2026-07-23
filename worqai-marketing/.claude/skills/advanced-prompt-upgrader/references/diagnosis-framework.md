# Prompt Diagnosis Framework

Load this in Step 2 of the advanced-prompt-upgrader workflow.
Run through every failure mode before selecting techniques.

---

## The 8 Common Failure Modes

### 1. Missing Role or Wrong Role
**What it looks like:** No persona defined, or a generic one ("act as an expert").  
**Why it fails:** The model has no frame of reference for the expertise level, voice, or
perspective required. "Expert" is meaningless — it doesn't tell the model *which* expert,
*what they prioritize*, or *how they think*.  
**Fix:** Replace with a specific, domain-anchored role.  
Bad: `Act as an expert copywriter.`  
Good: `You are a direct-response copywriter who specializes in Meta ads for SaaS products.
You write short, punchy, benefit-first copy that converts cold audiences. You never use
passive voice or vague adjectives.`

---

### 2. Weak or Missing Context
**What it looks like:** No background on the situation, audience, product, or prior work.  
**Why it fails:** The model fills gaps with generic assumptions. A resume-writing prompt with
no mention of the target role, country, or industry will produce a template, not a strategy.  
**Fix:** Add the minimum context that changes what "good" looks like. Usually: who the end
reader is, what constraints apply, and what the prior state is.

---

### 3. No Output Format Specified
**What it looks like:** The prompt asks for a result but doesn't say what shape it should take.  
**Why it fails:** The model guesses — sometimes correctly, often not. Prose when you wanted
bullets. JSON when you wanted a table. A 2,000-word essay when you wanted 3 options.  
**Fix:** Specify format explicitly. Word count, structure, example of what one "unit" looks like,
any schema if output is parsed downstream.

---

### 4. No Examples (When Pattern Matters)
**What it looks like:** The prompt describes a pattern but gives no instances of it.  
**Why it fails:** "Write like the brand" without examples produces generic brand voice.
"Extract in this format" without a sample produces inconsistent extraction.  
**Fix:** Add 1–3 examples of the target output. For rewriting: before/after pairs. For
classification: correctly labeled samples. For format: one fully worked example.  
**Limit:** Stop at 5 examples. More can cause few-shot collapse on some models.

---

### 5. No Verification Step
**What it looks like:** The prompt asks for output with no quality gate.  
**Why it fails:** The model outputs whatever it generates first. Errors, hallucinations, and
lazy choices go unchecked.  
**Fix:** Add an explicit self-audit step. "Before outputting, check: does this meet criteria
X, Y, Z?" or "After drafting, identify the 3 weakest sentences and rewrite them."

---

### 6. Over-Instruction on Advanced Models
**What it looks like:** A 500-word prompt stuffed with every rule the writer could think of.  
**Why it fails:** Prompting Inversion — on GPT-4o, Claude Opus, and similar advanced models,
excessive instruction can degrade reasoning quality. The model spends effort parsing your
structure instead of thinking about your problem.  
**Fix:** Cut to the essential constraints. If a capable model can infer something from context,
don't spell it out. Save long rulebooks for weaker or more specialized models.

---

### 7. Unclear Success Criteria
**What it looks like:** The prompt has a goal but no way to know if it was achieved.  
**Why it fails:** "Write a good summary" — good by whose standard? The model optimizes for
plausible-sounding output, not your actual success criteria.  
**Fix:** State what "done" looks like. Measurable where possible: "under 80 words", "hits all
5 key points from the brief", "would make a CS director approve it without edits."

---

### 8. Task Too Large for One Prompt
**What it looks like:** A single prompt trying to research, analyze, write, and format.  
**Why it fails:** Quality degrades in each stage because the model is splitting attention.
Research prompts need broad exploration. Writing prompts need focused execution.  
**Fix:** Break into a chain. Stage 1 researches and extracts. Stage 2 plans. Stage 3 writes.
Stage 4 refines. Each stage gets a focused prompt with the previous stage's output as context.

---

## Rapid Diagnosis Table

| Symptom | Most Likely Cause | Primary Fix |
|---|---|---|
| Output sounds generic | Weak role + no context | Specific role + background |
| Format is unpredictable | No format spec | Explicit structure + example |
| Answers are vague or safe | No success criteria | Add testable criteria |
| Output ignores key requirements | Buried constraints | Move to top, make them salient |
| Model hallucinates | No grounding | Add evidence source or RAG |
| Different runs = different quality | No verification | Add self-audit step |
| Output is too long / too short | No length constraint | Explicit word/item count |
| Reasoning is shallow | No decomposition | Add CoT or break into chain |
| Good model producing worse output | Over-instruction | Cut 40%, trust the model |
| Tone is off | No voice examples | Add 2–3 tone references |
