"""Turn marketing briefs into capability-aware workspace action plans."""

from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Any

from .models import MarketingBrief, WorkspaceActionPlan, WorkspaceInspection
from .paths import config_path


class ActionPlanner:
    def __init__(self, capabilities: Path | None = None) -> None:
        path = capabilities or config_path("workspace-capabilities.json")
        try:
            self.capability_data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self.capability_data = {"capabilities": []}

    def plan(
        self,
        brief: MarketingBrief,
        inspections: tuple[WorkspaceInspection, ...],
    ) -> WorkspaceActionPlan:
        inspection = _find_inspection(brief.workspace.workspace_id, inspections)
        capability = self._select_capability(brief)
        values = _template_values(brief)
        source_path = _render_relative_path(
            str(capability["source_path_template"]), values
        )
        output_path = _render_relative_path(
            str(capability.get("output_path_template", source_path)), values
        )
        verification = _verification_commands(capability, inspection, values)
        path_matches = _same_path(brief.workspace.path, inspection.path)
        can_write = (
            inspection.exists
            and not inspection.access_error
            and inspection.project_type != "missing"
            and path_matches
        )
        safety_notes = _safety_notes(
            brief,
            inspection,
            capability,
            source_path,
            output_path,
            path_matches,
        )
        return WorkspaceActionPlan(
            workspace_id=brief.workspace.workspace_id,
            workspace_path=brief.workspace.path,
            asset_type=brief.task.asset_type.value,
            source_request=brief.task.request,
            current_branch=inspection.current_branch,
            dirty=inspection.dirty,
            recommended_branch=_branch_name(brief.task.asset_type.value, brief.task.topic),
            asset_relative_path=source_path,
            write_mode="stage_capability_source",
            can_write=can_write,
            human_approval_required=True,
            verification_commands=verification,
            safety_notes=tuple(safety_notes),
            capability_id=str(capability["id"]),
            adapter=str(capability["production_adapter"]),
            source_format=str(capability["source_format"]),
            output_format=str(capability["output_format"]),
        )

    def _select_capability(self, brief: MarketingBrief) -> dict[str, Any]:
        request = brief.task.request.lower()
        asset_type = brief.task.asset_type.value
        candidates: list[tuple[dict[str, Any], int, int]] = []
        for capability in self.capability_data.get("capabilities", []):
            if capability.get("workspace_id") != brief.workspace.workspace_id:
                continue
            score = 10 if asset_type in capability.get("asset_types", []) else 0
            score += 2 * sum(
                1
                for signal in capability.get("signals", [])
                if str(signal).lower() in request
            )
            candidates.append((capability, score, int(capability.get("priority", 0))))
        if candidates:
            candidates.sort(key=lambda item: (item[1], item[2]), reverse=True)
            return candidates[0][0]
        return _fallback_capability(brief.workspace.workspace_id)


def _find_inspection(
    workspace_id: str,
    inspections: tuple[WorkspaceInspection, ...],
) -> WorkspaceInspection:
    for inspection in inspections:
        if inspection.workspace_id == workspace_id:
            return inspection
    return WorkspaceInspection(
        workspace_id=workspace_id,
        path="",
        exists=False,
        project_type="missing",
        is_git_repo=False,
        notes=("Target workspace was not present in the inspection report.",),
    )


def _fallback_capability(workspace_id: str) -> dict[str, Any]:
    return {
        "id": "legacy-markdown-brief",
        "workspace_id": workspace_id,
        "production_adapter": "markdown",
        "source_format": "markdown",
        "source_path_template": "production/{date}/{asset_type}-{slug}.md",
        "output_format": "markdown",
        "output_path_template": "production/{date}/{asset_type}-{slug}.md",
        "production_commands": [],
        "verification_commands": ["manual_review_generated_markdown"],
    }


def _template_values(brief: MarketingBrief) -> dict[str, str]:
    return {
        "date": date.today().isoformat(),
        "asset_type": _slug(brief.task.asset_type.value),
        "slug": _slug(brief.task.topic),
    }


def _render_relative_path(template: str, values: dict[str, str]) -> str:
    rendered = template.format_map(values).replace("\\", "/")
    path = Path(rendered)
    if path.is_absolute() or ".." in path.parts or not rendered.strip("./"):
        raise ValueError(f"Capability path template is not safely relative: {template}")
    return path.as_posix()


def _branch_name(asset_type: str, topic: str) -> str:
    return f"codex/wmi-{asset_type}-{_slug(topic, limit=36)}"


def _verification_commands(
    capability: dict[str, Any],
    inspection: WorkspaceInspection,
    values: dict[str, str],
) -> tuple[str, ...]:
    command_values = {
        **values,
        "source": _render_relative_path(
            str(capability["source_path_template"]), values
        ),
        "output": _render_relative_path(
            str(capability.get("output_path_template", capability["source_path_template"])),
            values,
        ),
    }
    configured = [
        str(command).format_map(command_values)
        for command in capability.get("verification_commands", [])
    ]
    if configured:
        return tuple(configured)

    preferred = [
        command
        for command in inspection.available_commands
        if command.endswith(" lint")
        or command.endswith(" test")
        or command.endswith(" build")
        or command.startswith("python -m compileall")
        or command == "python -m pytest"
    ]
    if preferred:
        return tuple(preferred[:3])
    return ("manual_review_generated_markdown",)


def _safety_notes(
    brief: MarketingBrief,
    inspection: WorkspaceInspection,
    capability: dict[str, Any],
    source_path: str,
    output_path: str,
    path_matches: bool,
) -> list[str]:
    notes: list[str] = [
        f"Production capability: {capability['id']} via {capability['production_adapter']}.",
        f"Intended source artifact: {source_path} ({capability['source_format']}).",
        f"Final output: {output_path} ({capability['output_format']}).",
        "Human approval is required before writing into a target workspace.",
        "Production workflow commands are handoff metadata and are not run by verification.",
    ]
    workflow = capability.get("workflow")
    if workflow:
        notes.append(f"Production workflow: {workflow}.")
    commands = capability.get("production_commands", [])
    if commands:
        notes.append("Production commands: " + " | ".join(str(item) for item in commands))
    if not inspection.exists:
        notes.append("Target workspace path does not exist or is not reachable.")
    if not path_matches:
        notes.append("Inspection path does not match the configured workspace path; writing is disabled.")
    if inspection.dirty:
        notes.append("Target workspace is dirty; avoid branch switching or promotion until reviewed.")
    if not inspection.is_git_repo:
        notes.append("Target workspace is not detected as a Git repository from this runtime.")
    if inspection.access_error:
        notes.append(f"Inspection reported an access issue: {inspection.access_error}")
    if brief.quality.score < 8:
        notes.append("Brief quality score is below 8; revise before production.")
    return notes


def _same_path(left: str, right: str) -> bool:
    if not left or not right:
        return False
    return os.path.normcase(str(Path(left).resolve())) == os.path.normcase(
        str(Path(right).resolve())
    )


def _slug(text: str, limit: int = 64) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:limit].strip("-") or "asset"
