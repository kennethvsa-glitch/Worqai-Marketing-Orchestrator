"""Run bounded, path-contained verification commands without a shell."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


_MANUAL_CHECKS = {
    "manual_review_generated_markdown",
    "manual_review_launch_archive",
    "manual_review_marketing_content",
    "manual_review_reel_factory_gates",
    "manual_review_produce_carousel_gates",
    "manual_review_produce_motion_video_gates",
}


@dataclass(frozen=True)
class VerificationResult:
    command: str
    returncode: int
    stdout: str
    stderr: str


class VerificationRunner:
    def run(
        self,
        workspace: str | Path,
        commands: tuple[str, ...],
    ) -> tuple[VerificationResult, ...]:
        results: list[VerificationResult] = []
        root = Path(workspace).resolve()
        if not root.is_dir():
            return tuple(
                VerificationResult(
                    command,
                    1,
                    "",
                    "Workspace is not an accessible directory; verification skipped.",
                )
                for command in commands
            )

        for command in commands:
            if command in _MANUAL_CHECKS:
                results.append(VerificationResult(command, 0, "manual review required", ""))
                continue
            args = _command_args(command, root)
            if args is None:
                results.append(
                    VerificationResult(
                        command,
                        1,
                        "",
                        "Unsupported or non-contained verification command; skipped for safety.",
                    )
                )
                continue
            try:
                result = subprocess.run(
                    args,
                    cwd=root,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired) as error:
                results.append(VerificationResult(command, 1, "", str(error)))
                continue
            results.append(
                VerificationResult(
                    command=command,
                    returncode=result.returncode,
                    stdout=result.stdout.strip()[-4000:],
                    stderr=result.stderr.strip()[-4000:],
                )
            )
        return tuple(results)


def _command_args(
    command: str,
    workspace: Path | None = None,
) -> tuple[str, ...] | None:
    parts = command.split()
    if len(parts) == 3 and parts[:2] == ["npm", "run"]:
        script = parts[2]
        if re.fullmatch(r"(?:lint|test|build|typecheck|check)", script):
            return ("npm", "run", script)
        return None
    if parts in (["python", "-m", "pytest"], ["py", "-m", "pytest"]):
        return tuple(parts)
    if len(parts) == 5 and parts[:4] in (
        ["python", "-m", "compileall", "-q"],
        ["py", "-m", "compileall", "-q"],
    ):
        if _safe_path_arg(parts[4], workspace):
            return tuple(parts)
        return None
    if parts == ["make"]:
        return ("make",)
    return _script_command(parts, workspace)


def _script_command(
    parts: list[str],
    workspace: Path | None,
) -> tuple[str, ...] | None:
    if len(parts) < 3 or parts[0] not in {"py", "python"}:
        return None
    script = parts[1].replace("\\", "/")
    if script == "scripts/render_carousel.py":
        if len(parts) == 4 and parts[3] == "--validate-only":
            return tuple(parts) if _all_safe_paths((script, parts[2]), workspace) else None
        return None
    if script in {
        "scripts/preflight.py",
        "scripts/visual_richness_check.py",
        "scripts/motion_preflight.py",
        ".claude/skills/produce-motion-video/scripts/check_packet.py",
    }:
        if len(parts) == 3 and _all_safe_paths((script, parts[2]), workspace):
            return tuple(parts)
    return None


def _all_safe_paths(values: tuple[str, ...], workspace: Path | None) -> bool:
    return all(_safe_path_arg(value, workspace) for value in values)


def _safe_path_arg(value: str, workspace: Path | None) -> bool:
    if not re.fullmatch(r"[A-Za-z0-9_.\\/-]+", value):
        return False
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        return False
    if workspace is None:
        return True
    resolved = (workspace / candidate).resolve()
    try:
        resolved.relative_to(workspace)
    except ValueError:
        return False
    return True
