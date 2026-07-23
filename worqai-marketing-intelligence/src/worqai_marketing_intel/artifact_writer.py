"""Write marketing briefs as portable Markdown artifacts."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from .codec import to_plain
from .models import MarketingBrief
from .paths import project_root


class ArtifactWriter:
    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir or project_root() / "production" / date.today().isoformat()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_brief(self, brief: MarketingBrief, *, record_id: str | None = None) -> Path:
        data = to_plain(brief)
        slug = _slug(brief.task.topic)
        suffix = f"-{record_id}" if record_id else ""
        path = self.output_dir / f"{brief.task.asset_type.value}-{slug}{suffix}.md"
        path.write_text(render_brief(data, record_id=record_id), encoding="utf-8")
        return path


def render_brief(data: dict[str, Any], *, record_id: str | None = None) -> str:
    task = data["task"]
    workspace = data["workspace"]
    quality = data["quality"]
    patterns = "\n".join(
        f"- **{item['name']}**: {item['pattern']}\n  Use when: {item['use_when']}\n  Avoid: {item['avoid']}"
        for item in data["benchmark_patterns"]
    )
    agents = "\n".join(f"- {agent}" for agent in data["active_agents"])
    insights = "\n".join(
        f"- **{item['agent_id']} / {item['focus']}**: {item['recommendation']}"
        + (f" Risk: {item['risk']}" if item.get("risk") else "")
        for item in data.get("agent_insights", [])
    ) or "- No agent insights recorded."
    requirements = "\n".join(
        f"- {item}" for item in data.get("generation_requirements", [])
    ) or "- Complete the requested channel-native asset."
    strengths = "\n".join(f"- {item}" for item in quality["strengths"])
    risks = "\n".join(f"- {item}" for item in quality["risks"])
    notes = "\n".join(f"- {item}" for item in data.get("notes", []))
    concept = json.dumps(data["concept"], indent=2)
    memory_line = f"- Memory ID: `{record_id}`\n" if record_id else ""

    return (
        f"# WorqAI Marketing Brief\n\n"
        f"{memory_line}"
        f"- Request: {task['request']}\n"
        f"- Asset type: `{task['asset_type']}`\n"
        f"- Audience: {task['audience']}\n"
        f"- Workspace: `{workspace['workspace_id']}`\n"
        f"- Workspace path: `{workspace['path']}`\n"
        f"- Route confidence: {workspace['confidence']}\n\n"
        f"## Active Agents\n\n{agents}\n\n"
        f"## Agent Judgments\n\n{insights}\n\n"
        f"## Generation Requirements\n\n{requirements}\n\n"
        f"## Strategic Angle\n\n{data['strategic_angle']}\n\n"
        f"## Benchmark Patterns\n\n{patterns}\n\n"
        f"## Concept\n\n```json\n{concept}\n```\n\n"
        f"## Quality Score\n\n{quality['score']}/{quality['max_score']}\n\n"
        f"### Strengths\n\n{strengths}\n\n"
        f"### Risks\n\n{risks}\n\n"
        f"## Notes\n\n{notes}\n"
    )


def _slug(text: str) -> str:
    lowered = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return slug[:70] or "brief"
