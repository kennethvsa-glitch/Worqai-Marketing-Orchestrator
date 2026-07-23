---
date: 2026-07-09
workspace: C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence
verdict: DRIFT
findings: 2
ships: yes
status: fixed-in-this-pass
---

# What changed

WMI now has a Universal Intake layer for vague or unsupported prompts. Known
asset prompts still route to their specialized engines; unclear prompts now
return interpreted intent, best mode, confidence, immediate output, available
routes, and better prompt examples.

# Findings

## F1 - Unknown prompts fell into generic campaign brief - MISLEADS - ADD

**Evidence**: Fallback is now `universal_intake` in
`src/worqai_marketing_intel/prompt_runtime.py`; the engine is
`src/worqai_marketing_intel/universal_intake_engine.py`.
**Cost**: Casual prompts like "this feels weak what should we do" could produce
a generic campaign brief instead of a routing/diagnostic answer.
**Falsifier checked**: A catch-all intake result would disprove this. It now
exists and smoke-tested.
**Fix**: Added Universal Intake and changed fallback routing.

## F2 - SEO keyword `search` was too broad - BREAKS - REWRITE

**Evidence**: `src/worqai_marketing_intel/router.py` no longer uses plain
`search` as an SEO keyword.
**Cost**: Phrases like "job searchers" could route to SEO instead of social
content.
**Falsifier checked**: `Create a LinkedIn post for job searchers` now classifies
as `linkedin_post`.
**Fix**: Removed the broad keyword and kept specific SEO/ranking triggers.
