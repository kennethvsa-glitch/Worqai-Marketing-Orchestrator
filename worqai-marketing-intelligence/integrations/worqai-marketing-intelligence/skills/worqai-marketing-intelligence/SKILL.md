---
name: worqai-marketing-intelligence
description: Create original WorqAI marketing strategy and assets through the local WMI Python context compiler, runtime, and quality loop. Use implicitly for natural-language WorqAI marketing requests involving reels, carousels, motion or video, message and comment replies, pitches, SEO, research, audits, campaigns, performance feedback, or vague strategy prompts.
---

# WorqAI Marketing Intelligence

Ground the task in WMI, then use Codex's judgment to create work that is novel rather than a restatement of runtime output.

## Workflow

1. Preserve the user's request verbatim. Resolve this skill directory and run:

```text
python <skill-dir>/scripts/wmi_bridge.py compile --request "<request>"
```

Add `--live` only for current, source-backed research when network use is appropriate. Treat the returned route, brand context, benchmark patterns, and constraints as grounding, not as finished copy.

2. Perform the creative reasoning yourself. Choose the strongest angle, build the requested asset, and make specific claims only when supported. For vague prompts, use WMI's interpreted intent to make a useful first move; ask a question only when a consequential fact is missing.

3. For research, distinguish WMI's local patterns from current external evidence. Verify time-sensitive facts with primary sources and cite them in the delivered work.

4. Save the draft as UTF-8, then validate it through WMI:

```text
python <skill-dir>/scripts/wmi_bridge.py validate --request "<request>" --draft-file "<draft-path>"
```

Repair substantive `quality.risks` and `script_audit` issues while preserving the best idea. Revalidate after each meaningful repair. Do not pad a concise reply merely to improve a generic length score; record any intentional residual risk in the final answer.

5. Return the useful asset directly. Mention files, evidence gaps, or residual WMI risks only when they matter.

## Approval Boundary

Do not invoke a skill owned by another workspace or write into an external WorqAI workspace until the user explicitly approves the named skill, target workspace, and intended writes. A WMI route or motion handoff recommendation is not approval. After approval, invoke only the approved external skill and keep its writes within the agreed scope.
