# WorqAI

Single home for all WorqAI content production. Each subfolder is its own git
repository; this folder is just the shared parent (a workspace root), kept
outside OneDrive so large media, model files, and virtualenvs don't sync.

## Structure

```
worqai/
  worqai-marketing-intelligence/  BRAIN. Routes a plain prompt to the right lane.
  design-core/                    Shared anti-slop engine (all lanes import it).
  worqai-marketing/               Carousels + channel marketing production.
  motion-studio/                  Motion videos / deterministic MP4 export.
  worqai-reel-factory/            Real-footage reels (MOVED IN once Codex is idle).
```

Referenced but intentionally NOT moved here:

- `cv-tailored` — cofounder's Next.js website repo (`TheCsarbeat/cv-tailored`),
  stays at `OneDrive/Documentos/cv-tailored`.
- `worqai-launch` — launch-content archive, stays at
  `OneDrive/Documentos/worqai-launch`.

## How it works

You open `worqai-marketing-intelligence` in Claude Code and ask for the work in
plain language ("crea un carrusel sobre errores del CV", "make a reel from this
footage"). WMI classifies the request and routes it to the matching workspace
(`config/workspaces.json` → `config/workspace-capabilities.json`).

`design-core` is the shared taste layer every lane runs as a build gate:
locked brand tokens, the motion language, the deterministic anti-slop linter
(HTML/CSS for carousels, TSX for reels/motion), the frame audit, and the
six-axis pre-emit critique. One brand contract, enforced everywhere — so a
carousel, a post image, and a reel all pass the same quality bar.

## Git

Every subfolder keeps its own history and remote:

| Repo | Remote |
|---|---|
| worqai-marketing | github.com/kennethvsa-glitch/Worqai-marekting |
| motion-studio | github.com/kennethvsa-glitch/motion-studio |
| design-core | local (new) |
| worqai-marketing-intelligence | github.com/kennethvsa-glitch/Worqai-Marketing-Orchestrator |
| worqai-reel-factory | local (no remote) |
