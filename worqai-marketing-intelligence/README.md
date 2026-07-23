# WorqAI Marketing Intelligence

Python-first context, research, validation, learning, and production orchestration for WorqAI marketing.

WMI follows the useful part of the Quantum pattern:

```text
Markdown = editable brand and taste source
JSON     = compact agents, workspaces, and production capabilities
Python   = routing, context compilation, research, validation, memory, and execution
Claude   = novel creative judgment and writing
SQLite   = briefs, examples, plans, and performance evidence
```

Python does not pretend that hard-coded strings are creative intelligence. It prepares a compact generation packet, Claude produces original work, and Python validates, learns, and routes the approved result.

## Natural Prompt Use

The intended user interface is a normal Claude prompt. Open this repository in Claude Code and ask for the work directly; the user does not need to run terminal commands.

Examples:

```text
Create three reel concepts for WorqAI graduates in Costa Rica.
Crea un carrusel de siete slides sobre errores del CV.
Research successful examples, then create the carousel.
Audit this script without replacing its original idea: ...
Reply to this message: Is it free and do I need a card?
Pitch a small WorqAI employability pilot to Universidad Latina.
Make an SEO implementation plan for analizador CV ATS in Colombia.
This carousel got 1,250 impressions, 42 saves, and 8 signups.
This feels weak. Decide what marketing asset should come next.
```

Claude activates WMI through `CLAUDE.md` and `.claude/skills/worqai-marketing-intelligence`. The skill compiles WMI context, lets Claude perform the creative reasoning, validates the draft, repairs substantive risks, and returns the useful asset directly. The older repo-local Codex integration remains optional compatibility code and is not required for Claude use.

## Runtime Flow

```text
plain prompt
  -> multilingual weighted routing
  -> structured request context
  -> brand memory + agent judgments
  -> saved/live benchmark evidence
  -> performance-ranked patterns
  -> original asset generation
  -> taste, fidelity, claim, and format validation
  -> approved workspace capability
  -> real production handoff
  -> performance events feed future pattern ranking
```

Structured context includes the asset, language, market, audience, objective, channel, offer, topic, source text, constraints, research intent, source facts, and requested output count.

## Production Workspaces

- `cv-tailored`: the Next.js WorqAI product and SEO implementation workspace.
- `worqai-marketing`: carousel rendering/export and channel marketing production.
- `worqai-reel-factory`: real-footage Reel production with reviewed captions, explicit storyboards, media QA, and hash-bound human approval.
- `motion-studio`: human-gated motion production and deterministic MP4 export.
- `worqai-launch`: historical launch content and approved launch archives, not website code.

Capabilities are declared in `config/workspace-capabilities.json`. WMI stages an adapter-specific source artifact and records the local workflow, intended final output, and bounded verification commands. External writes and local production skills still require explicit approval.

## Research And Learning

Built-in patterns are fallback knowledge. Saved source-backed examples rank above them, and examples with linked performance events rank highest. Reach metrics carry less weight than outcomes such as signups, meetings, downloads, and conversions.

Live research searches, fetches readable source pages when available, extracts evidence-linked candidate patterns, and reports warnings instead of inventing evidence when the network is unavailable.

Performance notes can be parsed from natural language. The event must be linked to an asset ID before WMI can promote its pattern as a measured winner.

## Developer Setup

WMI uses a standard `src` package layout and has no required runtime dependencies.

```powershell
python -m pip install -e ".[test]"
python -m pytest -q
wmi run "Create a carousel about ATS myths for LatAm graduates"
```

The CLI remains useful for testing and automation, but it is not the intended end-user interface.

## Safety

- Do not copy benchmark wording or visual identity.
- Do not invent user experience, testimonials, metrics, or product behavior.
- Qualify ATS claims and never guarantee interviews, jobs, rankings, or filter passage.
- Preserve source facts during audits and reframes.
- Require approval before writing into another workspace or invoking its production skill.
- Refuse writes outside the configured workspace and skip unsupported verification commands.
