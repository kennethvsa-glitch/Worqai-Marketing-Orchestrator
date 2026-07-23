"""Small Git helpers for execution."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitCommandResult:
    command: str
    returncode: int
    stdout: str
    stderr: str


class GitTools:
    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()

    def is_repo(self) -> bool:
        return (self.workspace / ".git").exists()

    def branch(self) -> str | None:
        result = self.run("rev-parse", "--abbrev-ref", "HEAD")
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None

    def status_short(self) -> str:
        result = self.run("status", "--short")
        return result.stdout.strip()

    def switch_or_create(self, branch: str) -> GitCommandResult:
        current = self.run("rev-parse", "--verify", branch)
        if current.returncode == 0:
            return self.run("switch", branch)
        return self.run("switch", "-c", branch)

    def run(self, *args: str) -> GitCommandResult:
        env = os.environ.copy()
        env["GIT_CONFIG_NOGLOBAL"] = "1"
        command = ["git", "-c", f"safe.directory={self.workspace}", "-c", "core.excludesfile=", *args]
        try:
            result = subprocess.run(
                command,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
                env=env,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            return GitCommandResult(" ".join(command), 1, "", str(error))
        return GitCommandResult(
            " ".join(command),
            result.returncode,
            result.stdout.strip(),
            _clean_stderr(result.stderr),
        )


def _clean_stderr(stderr: str) -> str:
    lines = [line for line in stderr.splitlines() if line.strip()]
    actionable = [
        line
        for line in lines
        if "unable to access" not in line or ".config/git/ignore" not in line
    ]
    return "\n".join(actionable)
