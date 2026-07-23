# Techniques Library

Reference for `advanced-prompt-upgrader`. Load in Step 4 — after architecture is selected.
Pick only techniques that earn their place for the specific task.

---

## How to Use This File

For each candidate technique, ask: "Would removing this change the output quality in a
meaningful way?" If no → don't add it. Stacking techniques for thoroughness is a trap.

---

## A. Core Structuring Techniques

### Role Prompting
**What it does:** Gives the model a specific perspective, expertise level, and set of priorities
to reason from. Not a costume — a cognitive frame that changes what the model notices, what it
flags as important, and how it communicates.  
**Use when:** Any task where the expertise, voice, or decision-making lens matters.  
**Skip when:** The task is purely mechanical (reformatting, extracting, summarizing known facts).  
**How to write a good role:**
- Include domain + specialization + what they care about
- `You are a senior growth marketer specializing in B2B SaaS PLG models. You think in
  acquisition funnels, activation metrics, and cohort behavior.`
- NOT: `Act as a marketing expert.`

---

### Persona + Goal + Constraints (WHO/WHAT/LIMITS)
**What it does:** The full professional briefing. Who you are, what you're trying to accomplish,
and what you're not allowed to do. Replaces vague instruction with a bounded operating space.  
**Use when:** Strategy, branding, consulting, design — anything with creative latitude that
could go in many directions.  
**Structure:**
```
WHO: [Role with specific framing]
WHAT: [Goal + what success looks like]
LIMITS: [What to avoid, what's off-brand, what can't change]
```

---

### Negative Prompting
**What it does:** Tells the model what NOT to produce. More effective than positive instruction
for avoiding generic or unwanted outputs because models default toward common patterns.  
**Use when:** Brand tone control, avoiding clichés, preventing hallucination of specific types.  
**Examples:**
- `Do not use: "unlock", "leverage", "game-changer", or any corporate-speak.`
- `Do not invent statistics. If you need a data point, write [DATA NEEDED] instead.`
- `Do not use passive voice.`

---

### Output Formatting Constraints
**What it does:** Specifies exactly what shape the response should take before the model starts
generating. Models that know the format produce cleaner, more consistent outputs.  
**Use when:** Always — if you have a format in mind, state it.  
**Common specifications:** word count, section headers, JSON schema, number of items, bullet vs.
paragraph, one-example-per-idea, table structure.

---

### XML Tag / Delimiter Prompting
**What it does:** Uses tags like `<context>`, `<task>`, `<examples>` to separate distinct
sections of a long prompt. Prevents the model from mixing up instructions with content.  
**Use when:** Prompt is long (>500 words) with multiple distinct sections. Especially useful
for RAG prompts where document content must not bleed into instructions.  
**Example structure:**
```xml
<role>You are a...</role>
<context>The user is trying to...</context>
<document>{{injected_content}}</document>
<task>Based only on the document above, produce...</task>
```

---

### Few-Shot / In-Context Learning
**What it does:** Shows the model 2–5 examples of the target output before asking it to
produce one. The model learns the pattern from the examples rather than from description.  
**Use when:** Consistency matters — formatting, classification, tone, extraction patterns.  
**Key rules:**
- 2–5 examples is the sweet spot. More than 5 causes few-shot collapse on some models.
- Examples must be high quality — bad examples teach bad patterns.
- Use before/after format for rewrites, labeled format for classification.

---

### Constraint Saturation
**What it does:** Stacks multiple specific constraints until the solution space is narrow
enough that what's left must be high quality. Works like design constraints: every
limitation forces creativity.  
**Use when:** Premium output requiring tight aesthetic, quality, or brand control.  
**Example:** `Write a 60-word Instagram caption. No hashtags. No emoji. No rhetorical
questions. No sentences longer than 10 words. The first sentence must name a specific
problem. The last sentence must be an action, not a claim.`

---

### Reference Injection / Style Transfer
**What it does:** You provide examples of a style, voice, or aesthetic — and instruct the
model to match it. More accurate than describing style in words.  
**Use when:** You want to match a specific person's writing style, a brand's existing content,
or blend multiple reference aesthetics.  
**How to use:** Paste 2–3 examples of the target style, then: `Write in the voice demonstrated
by the examples above. Prioritize: [3 specific traits you want to preserve].`

---

### System Prompt Simulation
**What it does:** Sets a persistent operating mode that the model carries across a long session
or an agent's lifetime. Unlike a user message, the system prompt establishes the model's
standing instructions — role, constraints, output rules.  
**Use when:** Reusable agents, Claude Code tools, API products where behavior must be consistent.  
**Note:** In the API and Claude Code, this goes in the `system` parameter, not the user message.

---

## B. Reasoning and Decomposition Techniques

### Chain of Thought (CoT)
**What it does:** Instructs the model to show its reasoning step by step before giving the
final answer. Forces deliberate reasoning instead of pattern-matched recall.  
**Use when:** Math, planning, debugging, complex analysis — tasks where the reasoning process
matters and can go wrong silently.  
**Skip when:** Using extended-thinking models (Claude Opus with extended thinking, o3) — they
do this automatically. Adding "think step by step" wastes tokens.  
**How to invoke:** `Before answering, walk through your reasoning. Then give the final answer.`

---

### Tree of Thoughts (ToT)
**What it does:** The model explores multiple distinct reasoning paths or solution branches
simultaneously, evaluates each, then synthesizes or selects the best.  
**Use when:** Strategy, architecture decisions, creative direction — situations with no single
right answer where exploring branches improves the final choice.  
**How to invoke:** `Generate 3 distinct approaches to this problem. For each, identify its key
assumption, its main risk, and where it breaks down. Then recommend one and explain why.`

---

### Step-Back Prompting
**What it does:** Before tackling the specific question, the model first identifies the
underlying principle, framework, or class of problem — then applies it to the specific case.  
**Use when:** Complex questions where jumping to specifics misses the governing principle.
Great for strategic advice, technical architecture, and research synthesis.  
**How to invoke:** `Before answering the specific question, first identify: what type of problem
is this? What principles or frameworks apply? Then use those to answer the specific case.`

---

### Debate Prompting
**What it does:** The model argues both sides of a decision before reaching a conclusion.
Forces it to surface counterarguments it would otherwise skip.  
**Use when:** Risk analysis, positioning, go/no-go decisions, pricing, channel strategy.  
**How to invoke:** `First argue the strongest case FOR [X]. Then argue the strongest case
AGAINST [X]. Be specific and concrete in both. Then give your actual recommendation.`

---

### Self-Ask Decomposition
**What it does:** The model breaks a complex question into smaller sub-questions it can
actually answer, answers each, then synthesizes.  
**Use when:** Complex research questions, multi-part analysis, "how should I approach X?"  
**How to invoke:** `Break this question into the 4–6 smaller questions that, if answered, would
let you answer the main question. Answer each. Then synthesize a final response.`

---

### Reflection Prompting
**What it does:** After producing an output, the model audits its own work for weakness,
errors, or missing pieces — and fixes what it finds.  
**Use when:** High-stakes outputs where self-correction adds value. Also as a quality gate
in a prompt chain.  
**How to invoke:** `After drafting, review what you wrote. Identify the 3 weakest parts.
Then rewrite only those parts.`

---

### Confidence-Informed Self-Consistency (CISC)
**What it does:** The model rates its confidence on key claims or steps, then flags where
it's uncertain. Reduces hallucination by surfacing rather than hiding doubt.  
**Use when:** Factual content, technical recommendations, anything where a confident-sounding
wrong answer is worse than an honest "I'm not sure."  
**How to invoke:** `For each key claim, rate your confidence: High / Medium / Low. For any
Medium or Low, explain why and note what would need to be verified.`

---

### Self-Critique Prompting
**What it does:** The model explicitly evaluates its own output against specific criteria
before delivering it.  
**Use when:** Any task with a quality checklist. Especially useful in long-form writing,
analysis, and code review.  
**How to invoke:** `Before delivering your answer, check it against these criteria: [list].
If any criterion is not met, revise before outputting.`

---

### Uncertainty Prompting
**What it does:** Instructs the model to say "I don't know" or flag uncertainty rather than
generate plausible-sounding content.  
**Use when:** Factual accuracy matters. Medical, legal, financial, or technical claims that
could cause harm if wrong.  
**How to invoke:** `If you are not certain about a fact, write [VERIFY] next to it rather
than stating it as fact. Do not fabricate data, statistics, or sources.`

---

## C. Retrieval, Grounding, and Tool Techniques

### RAG (Retrieval-Augmented Generation)
**What it does:** Instead of relying on training knowledge, the model answers based on specific
documents or data you inject. The documents are the source of truth.  
**Use when:** Answers that need to reflect specific, current, private, or changing information.  
**Key instruction:** `Answer only based on the provided documents. If the information isn't
in them, say: "This isn't covered in the provided materials."`

---

### Chain of Evidence (CoE)
**What it does:** Two-pass approach: first the model extracts relevant quotes or facts from
source documents, then it reasons only over those extracted pieces.  
**Use when:** Paired with RAG when accuracy is critical. Prevents the model from mixing
injected documents with training knowledge.  
**How to invoke (two passes):**  
Pass 1: `Extract all quotes from the document that are relevant to [topic]. Present as a
numbered list with page/section reference.`  
Pass 2: `Based only on the extracted quotes above, answer [question].`

---

### ReAct (Reason + Act)
**What it does:** The model alternates between reasoning (what should I do next?) and acting
(calling a tool, running a search, reading a file). Used in agentic loops.  
**Use when:** Building tool-using agents in Claude Code, API function-calling, or any task
where the model needs to gather information before it can answer.  
**Structure:**
```
Thought: [reasoning about what to do]
Action: [tool call or step]
Observation: [result from tool]
Thought: [updated reasoning]
Action: [next step]
... (loop until done)
Final Answer: [synthesis]
```

---

### Tool-Use / Function-Calling Prompting
**What it does:** Tells the model which tools are available, when to use each, and how to
interpret results. The system prompt for agents.  
**Use when:** The model has access to tools (search, code execution, database, APIs) and
needs to decide when and how to use them.  
**Key instruction pattern:** `You have access to the following tools: [list with description
and trigger condition for each]. Call a tool only when the task requires information or
actions you cannot produce from context.`

---

## D. Workflow and Multi-Agent Techniques

### Prompt Chaining
**What it does:** Splits a complex task into sequential prompts. Each prompt gets a focused
job and clean input from the previous stage.  
**Use when:** Quality in one phase depends on another. Research before writing. Plan before
coding. Extract before summarizing.  
**Key rule:** Each stage's output must be clean enough to feed the next without ambiguity.
If it's messy, add a "clean and structure" step between stages.

---

### Multi-Role Collaboration
**What it does:** The model simulates multiple specialist roles — each contributing their
perspective before a synthesis is produced.  
**Use when:** Complex decisions that benefit from multiple lenses: strategist + designer +
researcher + critic.  
**How to invoke:** `Approach this as three specialists. First as a [Role A] — what do you see?
Then as a [Role B] — what do you prioritize differently? Then as a [Role C] — what are the
risks? Finally, synthesize a recommendation that integrates all three perspectives.`

---

### Progressive Disclosure
**What it does:** Context is revealed in stages rather than all at once. The model handles
Phase 1 with limited info, gets more context for Phase 2, and so on.  
**Use when:** The full context would overwhelm or bias early-stage work (e.g., divergent
brainstorming before convergent selection).

---

### Adversarial CoT (Adv-CoT) / Red-Teaming
**What it does:** The model is asked to find the failure modes, edge cases, or weaknesses in
its own output or in a plan.  
**Use when:** High-stakes decisions, code that will go to production, copy that will run as
ads, strategies where a wrong assumption is costly.  
**How to invoke:** `Now act as a critic. Your job is to find everything wrong with the above.
What assumptions are wrong? What's missing? What would make this fail? Be specific.`

---

## Technique Selection by Task Type

| Task Type | Start With | Add If Needed |
|---|---|---|
| Content / brand copy | Role, Negative, Few-shot, Constraint saturation | Style transfer, self-critique |
| Code / architecture | Structured CoT, Debate, Adv-CoT, Output schema | Red-team, guardrails |
| Research / analysis | Step-back, CoE, Reflection, Uncertainty | RAG, Self-consistency |
| Strategy / planning | ToT, Debate, Multi-role, Self-ask | Expansion, Adversarial CoT |
| Agent / tool workflow | ReAct, System/user separation, Tool-use | Prompt chaining |
| Data extraction | Output schema, XML tags, Few-shot, Data-bound | Uncertainty |
| Rewriting / editing | Few-shot before/after, Constraint saturation, Negative | Self-critique |
