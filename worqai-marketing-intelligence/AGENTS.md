# WorqAI Marketing Intelligence Constitution

WMI creates original, professionally restrained WorqAI marketing work from ordinary prompts. It uses Python for compact deterministic intelligence and Claude for creative judgment. `CLAUDE.md` is the primary harness instruction file; this file is compatibility documentation.

## User Interface

Treat natural-language WorqAI marketing prompts as WMI requests. Run the local runtime or Claude skill bridge behind the scenes and return the useful asset, not terminal instructions.

Support English and Spanish/LatAm prompts for reels, carousels, motion, posts, replies, pitches, SEO, campaigns, research, audits, performance feedback, and vague strategic requests.

## Required Loop

1. Preserve the source request and source text.
2. Classify the primary asset with weighted phrase/token routing.
3. Compile language, market, audience, objective, channel, offer, topic, constraints, and research intent.
4. Load relevant brand context, agent judgments, saved examples, and measured patterns.
5. Research current successful examples when requested or when unstable facts matter.
6. Produce original channel-native work. Never treat runtime templates as final creative work.
7. Validate topic fidelity, source preservation, taste, claims, and format requirements.
8. Repair substantive risks and revalidate.
9. Route approved production through the matching workspace capability.
10. Store attributable outcomes so measured patterns can influence later generation.

Research is compositional. A request to research examples and create a carousel must do both; research must not replace the requested asset.

## Agent Roles

`config/agents.json` selects roles. `AgentRegistry.insights_for()` must turn active roles into concrete recommendations, evidence, and risks that reach the generation packet. Do not add decorative agent labels that cannot affect output.

## Brand And Taste

Brand Markdown is editable source material. Python must compile it into the generation packet and validation rules.

- Clear before clever.
- Specific before inspirational.
- Product evidence before broad claims.
- Adapt real experience; never invent it.
- Qualify ATS behavior and never guarantee outcomes.
- In Spanish, sound native to Latin America rather than translated from English SaaS copy.

## Research

Built-in patterns are fallback knowledge. Prefer traceable saved examples and performance-ranked patterns. Separate observed evidence, inference, and pending hypotheses. Current research needs source URLs and readable evidence excerpts.

## Workspaces

- `cv-tailored`: Next.js product and SEO implementation.
- `worqai-marketing`: carousel factory and marketing production.
- `worqai-reel-factory`: human-gated production of captioned Reels from real recordings.
- `motion-studio`: gated motion production.
- `worqai-launch`: launch-content archive.

Read `config/workspace-capabilities.json` before planning production. A recommendation is not approval. Do not write to an external workspace or invoke its skill until the user approves the named target and intended writes.

## Quality Gate

Reject output that:

- could be reused unchanged for a materially different topic or audience;
- replaces the subject of a pasted script or post;
- calls a static plan completed research;
- claims learning without linked performance events;
- copies benchmark wording;
- lacks a visible mechanism, proof requirement, or proportionate next step;
- routes website implementation outside `cv-tailored`;
- bypasses workspace containment, Git state, approval, or verification controls.

## Principle

Markdown explains the taste. JSON declares the system. Python compiles and enforces it. Claude performs the creative judgment.
