# Setup — WorqAI Marketing

## Prerequisites

- **VS Code** with Claude Code extension
- **Python 3.11+**
- **Node.js 18+** (for Claude Code CLI)

## 1. Install Python Dependencies

```bash
pip install reportlab python-docx playwright Pillow
playwright install chromium
```

## 2. Make Hooks Executable

```bash
chmod +x .claude/hooks/*.sh
```

## 3. Verify Structure

```bash
ls .claude/agents/          # 6 agent .md files
ls .claude/skills/          # 24 skill folders, each with SKILL.md
ls .claude/commands/        # 10 slash commands
ls scripts/                 # 3 Python scripts
```

## 4. Test Scripts

```bash
python scripts/carousel_exporter.py --help
python scripts/resume_builder.py --help
python scripts/linkedin_report.py --help
```

## 5. First Session

Open in VS Code → Claude Code reads `CLAUDE.md` automatically. Try these routing tests:

| Say this | Should route to |
|---|---|
| "Create an ad brief for WorqAI" | ads-agent |
| "Plan next week's content" | content-agent |
| "Audit this CV" + upload PDF | audit-agent |
| "Write the Pro tier pricing page" | content-agent (landing-page-cro skill) |
| "Build a 90-day marketing roadmap" | strategy-agent |
| "Draft a WhatsApp reply for this prospect" | growth-agent |
| "Deliver the CV for [client-name]" | client-delivery-agent |

## 6. Slash Commands

Once in a session, use `/project:` prefix:

- `/project:ads-carousel` — Full ad carousel pipeline
- `/project:ads-brief` — Meta ad brief
- `/project:weekly-content` — 7-day content calendar
- `/project:monthly-roadmap` — 30/60/90 day plan
- `/project:launch-plan` — Coordinated launch
- `/project:blog-post` — SEO blog post
- `/project:audit` — Free CV/LinkedIn audit
- `/project:client-cv` — Paid CV rewrite
- `/project:client-linkedin` — Paid LinkedIn rewrite
- `/project:reddit-post` — Reddit lead gen post
- `/project:sales-reply` — Sales reply draft

## 7. What the Hooks Do

Registered in `.claude/settings.json`:

- **PostToolUse** (Write/Edit/MultiEdit) → runs `format-check.sh` to warn about AI slop
- **PreToolUse** (Bash) → runs `bash-guard.sh` to block dangerous commands
- **SessionStart** → injects project context so every session starts oriented

## 8. Add Your Brand Assets

Before launching, populate `brand/`:
- Logo files (SVG + PNG)
- Color tokens (see `brand/colors.md`)
- Typography specs (see `brand/typography.md`)
- Tone guide reference (already in `.claude/rules/brand-voice.md`)

## 9. Recommended MCP Connectors

See `roadmap/MCP_RECOMMENDATIONS.md` for which connectors to enable and in what order.

## Troubleshooting

**Hooks not firing?** → Check `chmod +x .claude/hooks/*.sh` was run. Check hook paths in settings.json use `$CLAUDE_PROJECT_DIR`.

**Skills not loading?** → Every SKILL.md must have YAML frontmatter with `name` + `description`. The `description` is how Claude matches user intent.

**Agent not routing?** → Descriptions in agent frontmatter must include trigger phrases. Edit agent `.md` files to add missing keywords.

**Carousel export fails?** → `playwright install chromium` must have completed. Re-run if needed.
