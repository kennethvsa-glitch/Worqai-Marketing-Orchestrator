"""Read-only inspection of configured WorqAI workspaces."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from .models import WorkspaceInspection
from .paths import config_path


class WorkspaceInspector:
    def __init__(
        self,
        registry: Path | None = None,
        capabilities: Path | None = None,
    ) -> None:
        path = registry or config_path("workspaces.json")
        self.data = json.loads(path.read_text(encoding="utf-8"))
        capability_path = capabilities or config_path("workspace-capabilities.json")
        try:
            capability_data = json.loads(capability_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            capability_data = {"capabilities": []}
        self._capabilities_by_workspace: dict[str, list[dict[str, Any]]] = {}
        for capability in capability_data.get("capabilities", []):
            workspace_id = str(capability.get("workspace_id", ""))
            self._capabilities_by_workspace.setdefault(workspace_id, []).append(capability)

    def inspect_all(self) -> tuple[WorkspaceInspection, ...]:
        return tuple(self.inspect(workspace) for workspace in self.data["workspaces"])

    def inspect(self, workspace: dict[str, Any]) -> WorkspaceInspection:
        workspace_id = str(workspace["id"])
        raw_path = str(workspace["path"])
        path = Path(raw_path)
        notes: list[str] = []

        try:
            exists = path.exists()
            if not exists:
                return WorkspaceInspection(
                    workspace_id=workspace_id,
                    path=raw_path,
                    exists=False,
                    project_type="missing",
                    is_git_repo=False,
                    notes=("Configured path does not exist from this runtime.",),
                )

            if not path.is_dir():
                return WorkspaceInspection(
                    workspace_id=workspace_id,
                    path=raw_path,
                    exists=True,
                    project_type="file",
                    is_git_repo=False,
                    notes=("Configured path exists but is not a directory.",),
                )

            project_type = _detect_project_type(path, workspace_id)
            capabilities = self._capabilities_by_workspace.get(workspace_id, [])
            commands = _unique(_detect_commands(path) + _capability_commands(capabilities))
            important_files = _unique(
                _important_files(path) + _capability_files(path, capabilities)
            )
            destinations = _unique(
                _asset_destinations(path, workspace_id)
                + _capability_destinations(capabilities)
            )
            git_state = _git_state(path)
            if not commands:
                notes.append("No package/pyproject scripts detected.")
            if not destinations:
                notes.append("No obvious asset destination folders detected yet.")
            for capability in capabilities:
                notes.append(
                    "Capability "
                    f"{capability.get('id')} uses adapter "
                    f"{capability.get('production_adapter')} and produces "
                    f"{capability.get('output_format')}."
                )

            return WorkspaceInspection(
                workspace_id=workspace_id,
                path=str(path),
                exists=True,
                project_type=project_type,
                is_git_repo=git_state["is_git_repo"],
                current_branch=git_state["current_branch"],
                dirty=git_state["dirty"],
                available_commands=tuple(commands),
                asset_destinations=tuple(destinations),
                important_files=tuple(important_files),
                notes=tuple(notes),
                access_error=git_state["access_error"],
            )
        except OSError as error:
            return WorkspaceInspection(
                workspace_id=workspace_id,
                path=raw_path,
                exists=False,
                project_type="inaccessible",
                is_git_repo=False,
                access_error=str(error),
            )


def _detect_project_type(path: Path, workspace_id: str) -> str:
    files = {item.name.lower() for item in _children(path)}
    if "package.json" in files:
        package_type = _package_type(path / "package.json")
        if (path / "next.config.js").exists() or (path / "next.config.mjs").exists():
            return "nextjs"
        if (path / "vite.config.ts").exists() or (path / "vite.config.js").exists():
            return "vite"
        return package_type or "node"
    if "pyproject.toml" in files:
        return "python"
    if workspace_id == "motion-studio" or (path / "scenes").exists():
        return "motion-studio"
    if any((path / name).exists() for name in ("index.html", "app", "src")):
        return "web"
    return "unknown"


def _package_type(package_json: Path) -> str | None:
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    if "next" in deps:
        return "nextjs"
    if "vite" in deps:
        return "vite"
    if "react" in deps:
        return "react"
    return "node"


def _detect_commands(path: Path) -> list[str]:
    commands: list[str] = []
    package_json = path / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            for name in sorted(data.get("scripts", {})):
                commands.append(f"npm run {name}")
        except (OSError, json.JSONDecodeError):
            commands.append("package.json present but scripts could not be parsed")

    pyproject = path / "pyproject.toml"
    if pyproject.exists():
        compile_target = "src" if (path / "src").exists() else "."
        commands.append(f"python -m compileall -q {compile_target}")
        text = _safe_read(pyproject)
        if "[tool.pytest" in text or (path / "tests").exists():
            commands.append("python -m pytest")

    if (path / "Makefile").exists():
        commands.append("make")
    return commands


def _important_files(path: Path) -> list[str]:
    candidates = (
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        "package.json",
        "pyproject.toml",
        "next.config.js",
        "next.config.mjs",
        "next.config.ts",
        "vite.config.ts",
        "vite.config.js",
        ".claude/settings.json",
    )
    return [name for name in candidates if (path / name).exists()]


def _asset_destinations(path: Path, workspace_id: str) -> list[str]:
    candidates = [
        "campaigns",
        "content",
        "carousels",
        "production",
        "export",
        "docs",
        "assets",
        "app",
        "src",
        "scenes",
        "videos",
        "public",
    ]
    existing = [name for name in candidates if (path / name).exists()]
    if existing:
        return existing
    if workspace_id == "worqai-marketing":
        return ["campaigns", "carousels", "content"]
    if workspace_id == "motion-studio":
        return ["Ideation", ".visual-production", "export-video"]
    if workspace_id == "worqai-launch":
        return ["archive", "linkedin-post", "social", "video-scripts"]
    if workspace_id == "cv-tailored":
        return ["plans", "src", "public"]
    return []


def _capability_commands(capabilities: list[dict[str, Any]]) -> list[str]:
    commands: list[str] = []
    for capability in capabilities:
        commands.extend(str(item) for item in capability.get("production_commands", []))
        commands.extend(str(item) for item in capability.get("verification_commands", []))
    return commands


def _capability_files(path: Path, capabilities: list[dict[str, Any]]) -> list[str]:
    files: list[str] = []
    for capability in capabilities:
        workflow = str(capability.get("workflow", ""))
        if workflow and (path / workflow).is_file():
            files.append(workflow)
    return files


def _capability_destinations(capabilities: list[dict[str, Any]]) -> list[str]:
    destinations: list[str] = []
    for capability in capabilities:
        for key in ("source_path_template", "output_path_template"):
            value = str(capability.get(key, ""))
            if value:
                destinations.append(value.replace("\\", "/").split("/", 1)[0])
    return destinations


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _git_state(path: Path) -> dict[str, Any]:
    if not (path / ".git").exists():
        return {
            "is_git_repo": False,
            "current_branch": None,
            "dirty": None,
            "access_error": None,
        }
    branch = _git(path, "rev-parse", "--abbrev-ref", "HEAD")
    status = _git(path, "status", "--short")
    return {
        "is_git_repo": True,
        "current_branch": branch["stdout"] or None,
        "dirty": bool(status["stdout"]),
        "access_error": branch["error"] or status["error"],
    }


def _git(path: Path, *args: str) -> dict[str, str | None]:
    env = os.environ.copy()
    env["GIT_CONFIG_NOGLOBAL"] = "1"
    try:
        result = subprocess.run(
            ["git", "-c", f"safe.directory={path}", "-c", "core.excludesfile=", *args],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"stdout": None, "error": str(error)}
    error = _clean_git_stderr(result.stderr)
    return {"stdout": result.stdout.strip(), "error": error}


def _clean_git_stderr(stderr: str) -> str | None:
    lines = [line for line in stderr.splitlines() if line.strip()]
    actionable = [
        line
        for line in lines
        if "unable to access" not in line or ".config/git/ignore" not in line
    ]
    return "\n".join(actionable) or None


def _children(path: Path) -> tuple[Path, ...]:
    try:
        return tuple(path.iterdir())
    except OSError:
        return ()


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""
