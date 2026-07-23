---
name: skill-creator
description: Designs, structures, and writes SKILL.md files for Codex Skills. Use when the user wants to create a new Codex Skill, convert a workflow or service into a reusable Skill, or needs help writing YAML frontmatter, step-by-step instructions, examples, and quality checklists that Codex can auto-discover and load. Also use when the user asks "how do I make a skill?" or "build a skill for X."
metadata:
  author: kenneth-valverde
  version: 1.0
  domain: Codex-skill-authoring
---

## What This Skill Does

Turns any workflow, service, or task description into a properly structured, Anthropic-compliant SKILL.md file that Codex can auto-discover, load, and follow consistently.

The output is always a ready-to-use SKILL.md file, not a theoretical discussion.

---

## When to Use This Skill

Use this skill when the user:
- Wants to create a new Codex Skill from scratch
- Has a workflow or SOP they want to turn into a reusable Skill
- Wants to package a service (CV rewrite, LinkedIn audit, etc.) so Codex always follows the same process
- Asks "how do I make a skill?" or "build a skill for X"
- Wants to refactor an existing big prompt into a proper Skill file
- Asks about skill structure, YAML frontmatter, or what goes in SKILL.md

---

## Inputs Required

Before writing anything, collect:

1. **What the Skill does** — the core task or service (1–3 sentences)
2. **Who uses it** — the end user or client type (e.g., job seekers in Costa Rica, developers, HR managers)
3. **Trigger conditions** — when should Codex load this Skill? What does the user say or upload?
4. **Key outputs** — what does the Skill produce? (PDF, text, report, message, checklist, etc.)
5. **Step-by-step process** (optional) — if the user has a specific workflow, extract it; otherwise infer from the task description

If inputs 1–4 are missing, ask for them before proceeding. Do not write the Skill with gaps.

---

## Step 1 — Define the Skill's Identity

Before writing a single line of SKILL.md, nail down these four things:

**Single responsibility**: What is the ONE job this Skill owns? If the answer is more than one sentence, it needs to be split into multiple Skills.

**Skill name**: Follow these rules exactly:
- Lowercase letters, digits, and hyphens only
- Max 64 characters
- No XML characters (`<` or `>`)
- No reserved words: `anthropic`, `Codex`
- Use gerund or noun-phrase style: `processing-pdfs`, `linkedin-profile-rewriting`, `cv-auditing`

**Description (third person, ≤1024 characters)**: Write it to answer two questions:
- What does this Skill do?
- When should Codex use it?

Example format:
> "Rewrites and optimizes LinkedIn profiles for Spanish-speaking professionals in LATAM. Use when the user shares a LinkedIn URL and asks to improve recruiter visibility, ATS matching, or inbound job offers for a specific target role."

Never use first person ("I can…") or vague scope ("Helps with many tasks…").

**Trigger map**: List 3–5 exact user phrases or scenarios that should activate this Skill. This sharpens the description and helps during testing.

---

## Step 2 — Design the SKILL.md Structure

Every SKILL.md has two layers:

### Layer 1: YAML Frontmatter (always loaded)
```yaml
---
name: your-skill-name
description: Third-person description of capability and usage context.
metadata:
  author: your-name
  version: 1.0
---
```

Optionally add `domain`, `language`, or `tags` to the metadata for your own organization. These are not required by the platform.

### Layer 2: Markdown Body (loaded only when Skill is active)

The body follows progressive disclosure. Keep it lean — ideally under 4,000 tokens. Move anything longer into `references/` files that the Skill can read on demand.

Recommended internal structure (use what applies, skip what doesn't):

```
## What This Skill Does        ← 2–4 lines, plain language
## When to Use This Skill      ← bullet list of triggers
## Inputs Required             ← what Codex must collect before starting
## Step-by-Step Workflow       ← numbered steps from start to finish
## Output Formats              ← templates, layouts, or file specs
## Examples                    ← 2–3 before/after samples
## Quality Checklist           ← must-do and must-not-do list
## Rules                       ← hard constraints and edge cases
```

Not every section is needed for every Skill. A simple Skill (like a formatter) might only need workflow + examples. A complex Skill (like a full resume rewriter) needs all sections.

---

## Step 3 — Write the Workflow Section

This is the most important part of SKILL.md. It defines what Codex actually does.

Rules for writing steps:
- Use imperative language: "Do X", "Ask for Y", "Never do Z"
- Number steps in sequence — do not use bullet lists for the main workflow
- Each step should map to one action or decision
- Include branching logic where needed: "If the user has not provided X, ask before proceeding"
- Specify output format per step if the format matters (table, bullets, paragraph, template)

For services like CV rewrites or LinkedIn optimizations, the workflow usually follows this pattern:
1. Gather required inputs (upload, URL, target role)
2. Research: extract keywords, benchmark role, or read the input file
3. Diagnose: identify gaps, red flags, or weak areas
4. Rewrite: produce the optimized output following the format spec
5. Deliver: format the final output, add a report or checklist

Be specific. "Rewrite the resume" is not a step. "Rewrite each experience bullet using Power Verb + Context + Measurable Result, starting every bullet with an action verb, and including at least one metric per bullet" is a step.

---

## Step 4 — Write Examples

Every Skill needs at least 2–3 realistic examples. These are the fastest way to show Codex what "good" looks like.

Format for each example:
```
**Input**: [What the user said or provided]
**Output**: [What Codex should produce]
**Why it works**: [1 sentence explaining the key decision]
```

For rewriting Skills (CV, LinkedIn, outreach), use before/after format:
```
**Before**: [weak original]
**After**: [optimized version]
**Why**: [key change and reason]
```

Examples should reflect real scenarios from your target market. For Costa Rica/LATAM clients, use realistic Spanish-speaking job seeker contexts, real role names (Customer Service Supervisor, Project Coordinator, BPO Team Lead), and accurate market context.

---

## Step 5 — Write the Quality Checklist

The checklist is what Codex checks before delivering the output. It prevents drift and keeps results consistent.

Format:
```
Before delivering, verify:
- [ ] [Must-do item]
- [ ] [Must-do item]
- [ ] [Must-not-do item stated positively]
```

Good checklist items are:
- Specific and binary (pass/fail, not "check quality")
- Anchored to the most common failure modes for this Skill
- Ordered by importance (most critical first)

Example for a CV rewrite Skill:
```
Before delivering, verify:
- [ ] Every experience bullet starts with an action verb
- [ ] At least 80% of bullets contain a quantified metric
- [ ] No tables, columns, text boxes, or images in the document
- [ ] Contact info is in the body, not in a header or footer
- [ ] No experience, roles, or certifications were fabricated
- [ ] The resume fits on exactly 1 page
```

---

## Step 6 — Apply Token Economy Rules

After drafting SKILL.md, run this audit:

| Check | Rule |
|---|---|
| Total body length | Target ≤4,000 tokens. If longer, move content to `references/` |
| Prose vs. lists | Use bullet lists and numbered steps, not long paragraphs |
| Redundancy | Remove anything that repeats the YAML description in the body |
| Long examples | If examples are more than 10 lines each, move 2 of 3 to `references/examples.md` |
| Reference dependencies | If the Skill needs a long style guide, put it in `references/` and add a step: "Load references/style-guide.md before writing" |

The goal: SKILL.md should be a tight, scannable instruction set. Not an essay.

---

## Step 7 — Deliver the Output

Always produce:

1. **The complete SKILL.md file** — ready to copy-paste or save directly.
2. **Recommended folder structure** — show the full folder layout with any scripts, assets, or reference files the Skill will need.
3. **A short testing guide** — list 3–5 exact prompts the user should try to verify the Skill triggers correctly and produces consistent output.

Format the SKILL.md output inside a code block so it can be copied cleanly.

Recommended folder structure example:
```
linkedin-profile-rewriting/
├── SKILL.md
├── references/
│   ├── linkedin-ranking-system.md
│   └── headline-examples.md
└── assets/
    └── report-template.md
```

---

## Output Format

The final deliverable is always:

```markdown
# Skill: [skill-name]

[Brief 1-line summary of what this Skill does]

---

[Complete SKILL.md content, formatted as a code block]

---

## Folder Structure

[Show recommended folder layout]

---

## Testing Guide

[3–5 prompts to test the Skill is triggering and working correctly]
```

---

## Rules

1. Never write a Skill without first confirming the single responsibility, name, and trigger conditions.
2. Never fabricate examples — use realistic scenarios from the user's actual domain and target market.
3. If the user's workflow is complex enough for 2+ Skills, say so and propose a logical split before writing.
4. Always flag if the proposed skill name violates naming rules (reserved words, uppercase, special chars).
5. Always keep SKILL.md under 4,000 tokens. If the draft is longer, propose what to move to `references/`.
6. Write the YAML description in strict third person — no "I", "you", or "we".
7. Never use generic step names like "Do the task" or "Check quality" — every step must be concrete.
8. The final file must be copy-paste ready, not a draft with placeholders.

---

## Reference: Skill vs. Prompt vs. AGENTS.md

| Layer | What it is | When to use |
|---|---|---|
| `AGENTS.md` | Global context, brand voice, house rules — always loaded | Business identity, tone, cross-cutting constraints |
| `SKILL.md` | Modular SOP for a specific task — loaded on demand | Repeatable services: CV rewrite, LinkedIn audit, outreach DMs |
| Prompt | Ephemeral instruction in a single chat | One-off tasks, experiments, quick edits |

Use AGENTS.md for voice and context. Use Skills for each distinct service or workflow. Keep them separate — do not duplicate rules between layers.

