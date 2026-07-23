---
name: "source-command-upgrade-prompt"
description: "Diagnose and upgrade any weak prompt into 2–4 production-ready variants using the advanced-prompt-upgrader skill."
---

# source-command-upgrade-prompt

Use this skill when the user asks to run the migrated source command `upgrade-prompt`.

## Command Template

Load the `advanced-prompt-upgrader` skill and run the full upgrade workflow on the prompt the user provides.

If the user has not provided a prompt yet, ask for:
1. The raw prompt (required)
2. The target environment — Codex chat, Codex, API, or RAG system (required)
3. Any hard constraints that must be preserved (optional)

Once you have the prompt and environment, proceed directly. Do not ask for more information unless inputs 1–3 from the skill's "Inputs Required" section are genuinely missing.

Output format:
- Start with "What Was Wrong With the Original" (2–4 specific bullets)
- Then deliver the labeled variants in code blocks
- End with "Which Variant to Use" — one or two sentences matching variant to environment

No preamble. Start the response with the diagnosis.
