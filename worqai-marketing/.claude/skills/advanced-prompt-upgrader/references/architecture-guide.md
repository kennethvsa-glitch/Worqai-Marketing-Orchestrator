# Prompt Architecture Guide

Load this in Step 3 of the advanced-prompt-upgrader workflow.
Pick one architecture before selecting techniques.

---

## The 4 Architectures

### Architecture 1: Single-Shot Prompt
**What it is:** One prompt → one response. The model does everything in one pass.  
**Use when:**
- Task is self-contained (all needed info fits in the prompt)
- Output is a single artifact (paragraph, code block, list, email)
- Turnaround speed matters more than maximum quality
- The user will iterate manually on the result

**Don't use when:**
- Task requires research AND writing AND refinement
- Context is longer than ~8,000 tokens
- Output quality needs to be consistently excellent at scale

**Template structure:**
```
[Role]
[Goal + success criteria]
[Context / background]
[Constraints]
[Format specification]
[Examples]
[Verification instruction]
```

---

### Architecture 2: Prompt Chain (Multi-Stage)
**What it is:** Multiple focused prompts run in sequence. Output of each stage feeds the next.  
**Use when:**
- Task has distinct phases (research → plan → write → refine)
- You need to check or redirect between stages
- Quality in one stage depends on a clean handoff from the previous

**Don't use when:**
- Task is simple enough for one pass
- Latency is a hard constraint (chains are slower)

**Standard chain pattern:**
```
Stage 1 — Extract / Research
  Input: raw material (document, data, URL)
  Output: structured findings (bullets, schema, key facts)

Stage 2 — Plan / Outline
  Input: Stage 1 output
  Output: structured plan (outline, framework, decision)

Stage 3 — Generate
  Input: Stage 2 output + original goal + constraints
  Output: draft content

Stage 4 — Refine
  Input: Stage 3 draft
  Output: final version with self-audit applied
```

---

### Architecture 3: RAG-Grounded Prompt
**What it is:** A prompt that requires the model to answer based on specific retrieved documents
or data, not its training knowledge.  
**Use when:**
- Answers must be accurate about specific, changing, or private information
- You have documents the model must use as its source of truth
- Hallucination is unacceptable (policy docs, pricing, technical specs)

**Don't use when:**
- General knowledge questions where training data is reliable
- You don't have relevant documents to inject

**Template structure:**
```
[Role]
[Task]
[Source documents — injected as context]
[Explicit instruction: "Answer only from the provided documents.
  If the answer isn't in them, say so."]
[Format specification]
[Citation instruction if needed]
```

**Key technique to pair with this:** Chain of Evidence (CoE) — extract relevant quotes
first, then reason over only those quotes.

---

### Architecture 4: Agent / Tool-Using Prompt
**What it is:** A prompt that instructs a model with tool access to reason, decide which tools
to call, interpret results, and continue — in a loop until the task is done.  
**Use when:**
- Task requires actions in the real world (web search, code execution, file reading, APIs)
- The path to completion isn't linear — the model needs to make decisions mid-task
- You're building a Claude Code agent, a ReAct loop, or an orchestrator

**Don't use when:**
- No tools are available — agent prompting without tools is just verbose instruction
- Task is too simple for a loop (single tool call is fine as a regular prompt)

**Template structure (system prompt):**
```
[Role and primary mission]
[Available tools and when to call each one]
[Decision-making rules: how to choose between tool paths]
[Stopping criteria: when the task is done]
[Output format for final response]
[Hard constraints: what never to do]
```

---

## Architecture Selection Flowchart

```
Is the task fully self-contained with all info in the prompt?
  YES → Single-Shot (Architecture 1)
  NO ↓

Does the task have distinct phases that benefit from staged handoffs?
  YES → Prompt Chain (Architecture 2)
  NO ↓

Does the answer require specific documents, data, or private knowledge?
  YES → RAG-Grounded (Architecture 3)
  NO ↓

Does the task require real-world actions, tool calls, or adaptive decisions?
  YES → Agent / Tool-Using (Architecture 4)
  NO → Default to Single-Shot or Chain
```

---

## System Prompt vs. User Prompt: When to Split

On API and Claude Code, you can separate persistent instructions (system prompt) from
per-task input (user prompt). This matters when:

- The same role and constraints apply across many different tasks
- You want to prevent the model from ignoring rules buried in a long user message
- You're building a reusable agent where the "job description" should never change

**System prompt holds:** Role, operating rules, output format, hard constraints, persona  
**User prompt holds:** The specific task, the input data, the variable content
