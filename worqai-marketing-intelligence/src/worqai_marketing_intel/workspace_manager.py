"""Capability-aware workspace routing for WorqAI projects."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import MarketingTask, WorkspaceRecommendation
from .paths import config_path


class WorkspaceManager:
    def __init__(
        self,
        registry: Path | None = None,
        capabilities: Path | None = None,
    ) -> None:
        registry_path = registry or config_path("workspaces.json")
        capabilities_path = capabilities or config_path("workspace-capabilities.json")
        self.data = _read_json(registry_path)
        self.capability_data = _read_json(capabilities_path, fallback={"capabilities": []})
        self._workspaces = {
            str(item["id"]): item for item in self.data.get("workspaces", [])
        }

    def recommend(self, task: MarketingTask) -> WorkspaceRecommendation:
        ranked = self._rank_capabilities(task)
        if ranked:
            capability, score, _priority = ranked[0]
            workspace = self._workspaces[str(capability["workspace_id"])]
            reason = (
                f"{workspace['purpose']} Capability: {capability['id']} "
                f"via {capability['production_adapter']}."
            )
        else:
            workspace, score = self._legacy_recommendation(task)
            reason = str(workspace["purpose"])

        confidence = min(0.97, 0.45 + (score * 0.025))
        return WorkspaceRecommendation(
            workspace_id=str(workspace["id"]),
            path=str(workspace["path"]),
            reason=reason,
            confidence=round(confidence, 2),
        )

    def capability_for(
        self,
        task: MarketingTask,
        workspace_id: str | None = None,
    ) -> dict[str, Any] | None:
        for capability, _score, _priority in self._rank_capabilities(task):
            if workspace_id is None or capability.get("workspace_id") == workspace_id:
                return dict(capability)
        return None

    def capabilities_for_workspace(self, workspace_id: str) -> tuple[dict[str, Any], ...]:
        return tuple(
            dict(item)
            for item in self.capability_data.get("capabilities", [])
            if item.get("workspace_id") == workspace_id
        )

    def _rank_capabilities(
        self,
        task: MarketingTask,
    ) -> list[tuple[dict[str, Any], int, int]]:
        request = task.request.lower()
        asset_type = task.asset_type.value
        ranked: list[tuple[dict[str, Any], int, int]] = []
        for capability in self.capability_data.get("capabilities", []):
            workspace = self._workspaces.get(str(capability.get("workspace_id", "")))
            if workspace is None:
                continue

            capability_hits = _signal_hits(request, capability.get("signals", []))
            if capability.get("requires_any_signal") and capability_hits == 0:
                continue
            score = 0
            if asset_type in capability.get("asset_types", []):
                score += 15
            if asset_type in workspace.get("asset_types", []):
                score += 5
            score += 3 * capability_hits
            score += 2 * _signal_hits(request, workspace.get("signals", []))
            if score == 0:
                continue
            ranked.append((capability, score, int(capability.get("priority", 0))))

        ranked.sort(key=lambda item: (item[1], item[2]), reverse=True)
        return ranked

    def _legacy_recommendation(self, task: MarketingTask) -> tuple[dict[str, Any], int]:
        request = task.request.lower()
        best: tuple[dict[str, Any], int] | None = None
        for workspace in self.data.get("workspaces", []):
            score = 0
            if task.asset_type.value in workspace.get("asset_types", []):
                score += 5
            score += 2 * _signal_hits(request, workspace.get("signals", []))
            if best is None or score > best[1]:
                best = (workspace, score)

        if best is not None:
            return best
        workspaces = self.data.get("workspaces", [])
        if not workspaces:
            raise ValueError("Workspace registry contains no workspaces")
        fallback = self._workspaces.get("worqai-marketing", workspaces[0])
        return fallback, 1


def _signal_hits(request: str, signals: list[object]) -> int:
    return sum(1 for signal in signals if str(signal).lower() in request)


def _read_json(path: Path, *, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if fallback is not None:
            return fallback
        raise
