# Claude: Quantum + Visual Production Workflow

Use this document when working in `C:\Users\kenne\motion-studio` with Claude Code.

## Tool Locations

```powershell
$q = "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\Quantum-Agent-Coding\.venv\Scripts\q.exe"
$vpPython = "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\Visual-Production-Agent\.venv\Scripts\python.exe"
$visualRepo = "C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\Visual-Production-Agent"
```

Claude Code does not automatically load Codex's global skill registry. For visual
reconstruction, read the external skill directly:

```text
C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\Visual-Production-Agent\skills\reconstruct-visual\SKILL.md
```

Video production is local to Motion Studio at
`.claude/skills/produce-motion-video/SKILL.md`.

## Choose The Workflow

### Change code safely with Quantum

Use Quantum for bounded repository changes, refactors, new scripts, or pipeline
features. Start only from a clean Git repository.

```powershell
cd C:\Users\kenne\motion-studio
& $q new "Describe the exact feature and acceptance criteria"
```

Save the returned run ID:

```powershell
& $q status RUN_ID
& $q run RUN_ID
& $q approve RUN_ID
& $q run RUN_ID
```

`q run` means advance one lifecycle stage. It does not always mean write code.
Stop whenever the run requests specification, plan, or human candidate approval.
Never merge or push a Quantum candidate without Kenneth's explicit signoff.

Quantum currently has a known recovery limitation after a long provider timeout.
If a run becomes `failed`, inspect its worktree and evidence before retrying. Do not
delete the worktree or begin a duplicate run blindly.

### Reconstruct an image as editable visual code

Use this for a screenshot, mockup, carousel panel, or web reference that must
become HTML/CSS/SVG.

1. Read `$visualRepo\skills\reconstruct-visual\SKILL.md` completely.
2. Create a persistent job from the target repository:

```powershell
& $vpPython -m visual_production.cli visual-new "C:\path\reference.png" --target carousel
```

Valid targets are `carousel` and `web`. Motion scenes belong to Motion Studio.

3. Present the measured reconstruction specification and stop for approval.
4. Implement editable HTML/CSS/SVG in a bounded branch or worktree.
5. Run the skill scripts in this order:

```powershell
& $vpPython "$visualRepo\skills\reconstruct-visual\scripts\inspect_image.py" REFERENCE --output analysis.json
& $vpPython "$visualRepo\skills\reconstruct-visual\scripts\render_page.py" PAGE OUTPUT.png --width 1080 --height 1920
& $vpPython "$visualRepo\skills\reconstruct-visual\scripts\compare_images.py" REFERENCE OUTPUT.png --diff diff.png --report comparison.json
```

6. Repair the largest structural differences first. A similarity score is evidence,
   not creative approval.
7. Stop for human review with source files, render, diff, comparison report, font or
   asset substitutions, and remaining risks.

### Produce a Motion Studio video

Use this for brief-to-video work. Do not prompt one agent to create everything in
one pass.

1. Read `.claude/skills/produce-motion-video/SKILL.md` completely.
2. Read this repository's `CLAUDE.md`, `.claude/rules/motion-determinism.md`,
   `.claude/rules/output-conventions.md`, and
   `.claude/skills/motion-builder/SKILL.md`.
3. Create and validate the local production packet:

```powershell
cd C:\Users\kenne\motion-studio
py .claude\skills\produce-motion-video\scripts\create_job.py "C:\path\brief.md" --duration 30
py .claude\skills\produce-motion-video\scripts\check_packet.py .visual-production\jobs\JOB_ID\production-packet.json
```

4. Execute distinct roles and preserve their outputs:
   `creative-director` -> `storyboard-editor` -> `copy-editor` +
   `motion-scene-engineer` + `media-engineer` -> `render-controller` ->
   `visual-verifier` + `media-verifier` -> human review.
5. Require approval after the creative specification and storyboard. Changing an
   approved object invalidates downstream approval.
6. Use Motion Studio's existing render scripts. Do not invent a second renderer.
7. Store job evidence under `.visual-production/jobs/JOB_ID/evidence/`.
8. Never replace golden baselines, merge, push, publish, or deliver without explicit
   human signoff.

## Motion Studio Sources Of Truth

Apply instructions in this order:

1. Current human request and approved job objects.
2. `CLAUDE.md` for current architecture and commands.
3. `.claude/rules/` for deterministic and output constraints.
4. `.claude/skills/motion-builder/SKILL.md` for scene implementation details.
5. `.claude/skills/produce-motion-video/SKILL.md` for production orchestration.
6. The external reconstruction skill only for carousel or web reconstruction.
7. `docs/archive/` only as historical evidence.

Do not execute anything under `docs/archive/` merely because it contains imperative
steps.

## Required Human Gates

- Approve creative specification.
- Approve storyboard and copy direction.
- Approve any new dependency, downloaded asset, or licensed media.
- Review draft/contact sheet before final render.
- Sign off the exact candidate before merge or push.
- Approve publication or delivery separately from code merge.
