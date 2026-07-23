"""Browser launch helpers for Motion Studio tools."""

from __future__ import annotations

import os
from pathlib import Path


def _candidate_chromium_paths() -> list[Path]:
    paths: list[Path] = []

    env_path = os.environ.get("MOTION_CHROMIUM")
    if env_path:
        env_candidate = Path(env_path)
        if env_candidate.exists():
            return [env_candidate]

    home = Path.home()
    hyperframes = home / ".cache" / "hyperframes" / "chrome" / "chrome-headless-shell"
    if hyperframes.exists():
        paths.extend(hyperframes.glob("**/chrome-headless-shell.exe"))

    return sorted([p for p in paths if p.exists()], key=lambda p: str(p))


def launch_chromium(playwright):
    """Launch Playwright Chromium, falling back to cached Hyperframes Chrome.

    Some Codex desktop sessions have Playwright installed without its managed
    browser revision. Hyperframes keeps a compatible headless Chrome cache on
    this machine, so Motion tools can use it without downloading browsers.
    """

    candidates = _candidate_chromium_paths()
    if candidates:
        chosen = candidates[0]
        return playwright.chromium.launch(executable_path=str(chosen))
    return playwright.chromium.launch()
