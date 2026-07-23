"""Optional Codex adapter for the harness-neutral WMI bridge."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
runpy.run_path(str(ROOT / "scripts" / "wmi_bridge.py"), run_name="__main__")
